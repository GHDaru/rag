# 06 — Busca: Esparsa, Densa e Híbrida

> **Estado da arte capturado em 2026-08** · edição 1.0 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** Componentes que aprofunda: **índice** e **retriever** (cap. 02).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Explicar** por que busca densa e esparsa erram em direções opostas;
2. **Implementar** busca híbrida com fusão de ranking, e justificar o peso escolhido;
3. **Aplicar** filtro por metadado **antes** da busca, e dizer por que depois não serve;
4. **Instalar** o caminho de "não encontrei": limiar, abstenção e o sinal que os monitora.

## O problema

O corpus está governado (cap. 04) e representado (cap. 05). Agora a pergunta precisa virar **candidatos**.

Este é o estágio que quase todo mundo implementa primeiro e ajusta por último, e o erro dominante é adotar **uma** família de busca e brigar com os defeitos dela. A escolha "densa ou esparsa" é falsa: as duas erram, em direções complementares, e a fusão custa pouco.

Há também o problema que ninguém vê até virar incidente: o sistema **sempre devolve `top_k` resultados**. Mesmo quando o corpus não tem a resposta. Sem limiar e sem caminho de abstenção, a alucinação fundamentada em ruído é o comportamento padrão.

## Fundamentos científicos

- **A tradição** — recuperação por sobreposição de termos, com ponderação por frequência e raridade, é a base de *Information Retrieval* há décadas (a família **BM25**). Sobreviveu a todas as gerações de modelo por resolver uma propriedade do problema: casar o **literal** — e o BEIR o mede com todas as letras: ***"BM25 is a robust baseline"***. Se o seu sistema não bate BM25, ele não está pronto. ✓
- **A vez do denso** — a recuperação por similaridade de vetores resolve a paráfrase, que a esparsa nunca resolveu. **BEIR** ([arXiv 2104.08663](https://arxiv.org/abs/2104.08663)) mede recuperação zero-shot em 18 datasets sobre 10 sistemas — e o resultado desmonta a expectativa de que denso substitui esparso: *"dense and sparse-retrieval models are computationally more efficient but **often underperform** other approaches"*. ✓
- **A fusão, e a razão dela** — a survey de Gao ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)) enuncia a tese central deste capítulo com todas as letras: *"Sparse and dense embedding approaches **capture different relevance features** and can **benefit from each other by leveraging complementary relevance information**"*. Não é que uma seja melhor — é que os sinais são **complementares**, e por isso a fusão ganha. Híbrido está entre as estratégias de **pré-recuperação** que definem o Advanced RAG. ✓

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **A fusão por posição é a prática de fato** — os motores de busca comerciais implementam a fusão recíproca de ranking (RRF, *Reciprocal Rank Fusion*) como o modo padrão de combinar listas. A documentação do Elasticsearch a define como *"a method for combining multiple result sets with different relevance indicators into a single result set"*, e a fórmula publicada opera sobre `rank(result(q), d)` — a **posição** do documento em cada lista, não a nota original ([Elastic, *Reciprocal rank fusion*](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion), consultado em 2026-08-13). É exatamente o argumento da seção anterior, e é o que dispensa calibrar escalas incomparáveis.
- **O consenso, e o tamanho dele** — a leitura publicada é que benchmarks recentes mostram BM25 e denso **fundidos** superando qualquer um sozinho. As duas metades têm âncora científica neste livro: a robustez do BM25 pelo BEIR, e a complementaridade dos sinais pela survey de Gao (ambas ✓ na [bibliografia](../bibliografia.md)). **O que não temos é medição própria** — e por isso o consenso entra como consenso, não como número.
- **O sintoma que denuncia falta de esparsa** — "o RAG não encontra o óbvio". Quase sempre o óbvio é um código, uma sigla ou um nome próprio que o índice denso não representa. É observação de campo dos autores deste livro, não resultado publicado; está aqui porque é acionável, e declarada como o que é.

## O estado da arte

### 1. Dois modos de errar, espelhados

| | Busca esparsa (BM25) | Busca densa |
|---|---|---|
| Casa | termos literais | proximidade semântica |
| Acha | `ERR_4021`, `XR-4400-B`, nomes próprios, siglas | "veículo" quando se perguntou "carro" |
| **Erra em** | paráfrase, sinônimo, vocabulário diferente do documento | identificador, código, número, jargão fora do treino |
| Custo | baixo; índice invertido | embeddings + armazenamento vetorial |
| Explicabilidade | alta — dá para ver o termo que casou | baixa — a similaridade não se explica |

A linha em negrito é o conteúdo do capítulo: **os erros são complementares, não sobrepostos.** Não é que uma seja melhor; é que cada uma tem um ponto cego que a outra cobre.

Daí a conclusão prática: **busca híbrida é o upgrade de melhor relação benefício/esforço deste livro**, e é a primeira coisa a tentar quando um RAG "não encontra o óbvio".


**O núcleo do BM25, para você ver que cabe mesmo.** É o laço de pontuação de
[`rag_zero/bm25.py`](../../rag-zero/rag_zero/bm25.py):

```python
for termo in normalizar(consulta):
    postings = self.invertido.get(termo)
    if not postings:
        continue
    idf = self.idf[termo]                       # termo raro vale mais
    for i, freq in postings.items():
        norma = 1 - self.b + self.b * (self.tamanhos[i] / self.tamanho_medio)
        notas[i] = notas.get(i, 0.0) + idf * (freq * (self.k1 + 1)) / (
            freq + self.k1 * norma)             # satura e normaliza por tamanho
```

As três correções que separam isto de contagem crua de termos estão nessas
linhas: **IDF** (termo raro pesa mais), **saturação** pelo `k1` (a décima
ocorrência vale menos que a segunda) e **normalização por comprimento** pelo `b`
(documento longo não ganha só por ser longo). Tire as três e você tem o
ranqueador ingênuo que favorece bloco comprido — que foi, por três edições, o que
o companion deste livro de fato usava enquanto se descrevia como BM25.

### 2. Fusão: como combinar dois rankings

O problema é que as duas listas trazem **notas incomparáveis** — a similaridade de cosseno e a pontuação BM25 vivem em escalas diferentes, e normalizá-las é frágil.

A saída consolidada é fundir **por posição**: um documento bem colocado nas duas listas sobe mais do que um documento excelente em uma só e ausente na outra. Isso dispensa calibração e é robusto a mudanças de escala.

Duas decisões ficam com você:

- **O peso entre os sinais.** Não existe valor universal. Corpus com muito identificador pede mais esparsa; corpus de prosa pede mais densa. E o peso ótimo **depende do tipo de pergunta**, o que sugere pesos por rota quando há roteamento (cap. 08).
- **Quantos candidatos de cada.** Fundir os 50 primeiros de cada lista não é o mesmo que fundir os 100 de uma. O número alimenta o reranking (cap. 07), e é lá que se mede se aumentar compensa.

### 3. Filtrar antes, nunca depois

Se a busca pode ser restrita por metadado — permissão, data, tipo, `status` (cap. 04) — o filtro tem que acontecer **na consulta ao índice**, não sobre os resultados.

Recuperar tudo e filtrar depois tem três defeitos, e o terceiro é grave:

1. **Desperdiça** o `top_k`: você pediu 20, sobraram 3 depois do filtro.
2. **Falseia** as métricas: o recall medido não é o recall que o usuário recebe.
3. **Vaza.** Dependendo da implementação — logs, cache, telemetria, mensagens de erro — o conteúdo filtrado já passou por lugares onde não deveria. Isso é requisito de segurança (cap. 22), não de eficiência.

### 4. O caminho de "não encontrei"

Um retriever que sempre devolve K resultados sempre devolve **algo**. Se o corpus não tem a resposta, esse algo é ruído — e o gerador, sem instrução contrária, vai usá-lo (cap. 15).

O mínimo:

- **Limiar de relevância**, abaixo do qual o resultado não entra no contexto. Calibrado no seu corpus, não copiado.
- **Caminho de abstenção** quando nada passa: o sistema responde que não encontrou, e o gerador nem é chamado.
- **Taxa de resultado zero** monitorada (cap. 21). Se subir, algo mudou; se estiver **sempre em zero**, provavelmente não existe limiar — e é essa a leitura mais útil do indicador.

### Leitura executiva

A escolha "densa ou esparsa" é falsa: **as duas erram em direções complementares** — a densa perde identificador, código e nome próprio; a esparsa perde paráfrase e sinônimo. **O que roubar:** busca **híbrida com fusão por posição** é o upgrade de melhor relação benefício/esforço do livro, e a primeira coisa a tentar quando o RAG "não encontra o óbvio" — porque quase sempre o óbvio é um literal que o índice denso não representa. Funda **por posição no ranking**, não por nota: as escalas de cosseno e BM25 são incomparáveis, e normalizá-las é frágil. **O peso entre os sinais não tem valor universal** e depende do tipo de pergunta — o que sugere pesos por rota quando há roteamento. **Inegociável:** filtre por metadado **na consulta ao índice**, nunca sobre os resultados — filtrar depois desperdiça `top_k`, falseia a métrica e, dependendo de logs e cache, **vaza**; é requisito de segurança, não de eficiência. **E instale o "não encontrei":** limiar calibrado no seu corpus, abstenção quando nada passa, e a taxa de resultado zero monitorada — se ela vive em zero, provavelmente não há limiar nenhum.

## Mão na massa — `rag-zero`, etapa 5

Na etapa 5 você constrói a busca do `rag-zero` **na mão, antes de qualquer biblioteca**: um BM25 em cerca de 40 linhas sobre o texto deste livro, depois embeddings, depois a fusão por posição — medindo os três com o mesmo conjunto de perguntas. O objetivo pedagógico é ver o ranking acontecer e o ponto cego de cada família aparecer numa pergunta concreta. O exercício de completude: o peso da fusão vem esqueletado; você o calibra e descobre que o ótimo muda com o tipo de pergunta.

**Rode agora** — sem instalar nada, sem chave e sem GPU:

```bash
cd rag-zero
python3 etapas/etapa05_busca.py
```

Código: [`rag_zero/bm25.py`](../../rag-zero/rag_zero/bm25.py). O que você deve ver: a tabela de ganho por estágio, e o BM25 achando `arXiv 2401.18059` onde o denso erra.
## Verificação

1. Usuários buscam por código de produto (`XR-4400-B`) e não encontram, mas encontram por descrição. Qual família está faltando, e por quê?
2. Por que fundir por posição dispensa calibrar as notas dos dois sistemas?
3. Seu sistema filtra por permissão depois de recuperar. Descreva o problema de segurança concreto, além da ineficiência.

---

## Apêndice A — Como cada abordagem busca

> Tratamento por implementação, com URL. Cada linha traz **a pegadinha** — o que a documentação não diz e o livro aprendeu a perguntar.

| O quê | Implementação de referência | O que reter |
|---|---|---|
| **BM25 puro, sem serviço** | [`rank_bm25`](https://github.com/dorianbrown/rank_bm25) | "A two line search engine". É a linha de base honesta em ~40 linhas, e é o que o `rag-zero` usa. **Pegadinha:** não tem índice invertido persistido — memória e reindexação são por sua conta acima de alguns milhares de documentos. |
| **BM25 em produção** | motores de busca (Elasticsearch, OpenSearch, Vespa, Tantivy) | trazem índice invertido, filtro por campo **na consulta** (§3) e análise linguística. **Pegadinha:** o analisador (stemming, stopwords, tokenização) muda o resultado tanto quanto o `k1`/`b` — e quase ninguém o audita. |
| **Fusão por posição** | `EnsembleRetriever` do [LangChain](https://github.com/langchain-ai/langchain); `QueryFusionRetriever` do [LlamaIndex](https://github.com/run-llama/llama_index); `JoinDocuments` do [Haystack](https://github.com/deepset-ai/haystack) | é a fusão recíproca de ranking, a implementação dominante do que a §2 descreve. **Pegadinha:** o parâmetro de amortecimento (o `k` da fusão recíproca de ranking, tipicamente 60) decide quanto peso a cauda recebe, e o padrão raramente é discutido. |
| **Índice denso** | bancos vetoriais ([Chroma](https://github.com/chroma-core/chroma) e congêneres); `faiss` para o caso embutido | **Pegadinha, e é a que mais dói:** o índice aproximado troca **recall** por latência. Um recall@k que cai sem explicação costuma ser o parâmetro de busca do índice, não o modelo de embedding. |
| **A régua** | [BEIR](https://github.com/beir-cellar/beir) | 18 datasets, protocolo zero-shot. Serve para **comparar contra BM25**, que é o que o paper mostra ser difícil de bater. |

**O que fica para a rodada 4:** medir a fusão no corpus deste livro — hoje o livro afirma que híbrido vence com base em Gao (complementaridade dos sinais) e no consenso publicado, mas **sem número próprio**.
