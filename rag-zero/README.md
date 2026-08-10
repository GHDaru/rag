# rag-zero — a trilha prática

> O livro executável: um sistema de RAG construído do zero, **uma etapa por capítulo**.
>
> Edição 1.0 · **status: 12 das 17 etapas construídas (0–10 e 14 parcial), 9 delas com script próprio; as 5 restantes, especificadas e declaradas como tal.**
> A implementação é a [rodada 3](../ROADMAP.md) do ROADMAP; o piso da 1.0 está entregue e o restante é pós-1.0.

## Rodar agora

Não precisa instalar nada. **Sem dependências, sem GPU, sem rede, sem credencial** —
só a biblioteca padrão do Python 3.11+.

```bash
cd rag-zero

python3 etapas/etapa00_contador.py     # o instrumento: composição do contexto
python3 etapas/etapa02_naive.py        # a LINHA DE BASE: Naive RAG e os 4 contratos
python3 etapas/etapa03_ingestao.py     # o revogado não é recuperado
python3 etapas/etapa05_busca.py        # esparso × denso × fusão, medidos
python3 etapas/etapa06_reranking.py    # a nota como limiar, e a abstenção
python3 etapas/etapa07_consulta.py     # roteamento, reescrita e a conta de cada estágio
python3 etapas/etapa08_indexacao.py    # contextual × late chunking, medidos
python3 etapas/etapa09_raptor.py       # a árvore de resumos recursivos
python3 etapas/etapa10_geracao.py      # o "G": citação verificável e abstenção

python3 -m pytest tests/ -q            # 39 testes
```

O corpus é **o texto deste livro**. Nenhuma etapa baixa nada.

## O que é

A espinha 4C/ID do livro (Princípio III): cada etapa é uma *learning task* inteira —
não um fragmento — e o capítulo correspondente é a *supportive information* que a
sustenta.

**Stack:** Python puro no núcleo; FastAPI quando chegar o companion.
**Custo zero e sem GPU** (Princípio VI).

## As quatro regras da construção

Da seção "Restrições" da [constituição](../.specify/memory/constitution.md):

1. **Do zero antes da biblioteca.** O [`bm25.py`](rag_zero/bm25.py) tem ~40 linhas e
   implementa IDF, saturação e normalização por comprimento — as três correções que
   separam BM25 de contagem de termos. A biblioteca entra depois, nomeada como
   **escolha**, não como pré-requisito.
2. **Arquitetura hexagonal por refatoração.** Cada porta nasce da dor de um capítulo:
   `LLMPort` na etapa 0, `EmbedderPort` na 4, `RerankerPort` na 6. Nunca antecipada.
3. **Completion problem, não folha em branco** (Carga Cognitiva). O esqueleto vem
   pronto; o que carrega a **decisão** fica com você — o `k_rrf` da fusão, o limiar de
   abstenção, a política de expiração.
4. **Anti-apodrecimento.** Modelo atrás de porta; etapas autocontidas; e **erro
   didático deliberado comentado como tal**.

### O erro didático deliberado, declarado de frente

O `EmbedderHashing` projeta termos em posições por hash. Ele reproduz fielmente a
**mecânica** da busca densa — vetor, cosseno, vizinhança — e **não tem semântica
nenhuma**: não sabe que "carro" e "veículo" são parecidos.

Ou seja: ele tem o ponto cego da busca esparsa com o custo da densa. **O pior dos
dois mundos, de propósito.** A etapa 5 mede isso e mostra o resultado desconfortável:
no corpus deste livro, **fundir BM25 com um embedder ruim piora a precisão** (0,525 →
0,425). Que é exatamente o que o cap. 06 prevê — e a lição é que trocar o adaptador
por um modelo real é uma linha, porque ele está atrás de uma porta.

Há um teste (`test_embedder_hashing_nao_capta_parafrase`) que **fixa esse defeito como
contrato**. Quando alguém plugar um embedder de verdade, ele quebra — e essa quebra é
a lição.

## As 17 etapas

| Etapa | Cap. | Constrói | Prova (o teste que fecha) | Estado |
|:---:|:---:|---|---|:---:|
| 0 | 01 | `LLMPort` + **contador de tokens por bloco** | a composição do contexto sai impressa; bloco externo é delimitado | ✅ |
| 1 | 02 | os dois caminhos + os quatro contratos | **a procedência atravessa documento → chunk → índice → candidato → citação** | ✅ |
| 2 | 03 | o Naive RAG inteiro, ponta a ponta | **a linha de base** — sem ela nenhuma tabela de ganho compara com nada | ✅ |
| 3 | 04 | **ingestão**: extração, dedup, metadado, status | **documento `revogado` não é recuperado, mesmo sendo o mais similar** | ✅ |
| 4 | 05 | chunking estrutural + *sentence-window* | a unidade de busca difere da de entrega | ✅ |
| 5 | 06 | **BM25 na mão** + denso + fusão por posição | tabela de ganho por estágio, mesmas perguntas | ✅ |
| 6 | 07 | reranking com a **nota** como limiar | pergunta fora do corpus **abstém**; taxa de zero deixa de ser zero | ✅ |
| 7 | 08 | reescrita, HyDE e roteamento | o portão de reescrita e a conta: 2 chamadas por pergunta com tudo ligado, 0 com os padrões | ✅ |
| 8 | 09 | contextual retrieval × late chunking | as três indexações medidas com as mesmas perguntas, e as chamadas de LLM de cada uma | ✅ |
| 9 | 10 | RAPTOR reduzido (~80 linhas) + busca por nível | a árvore condensa a cada nível (180 → 55 → 24 → 12) | ✅ |
| 10 | 11–17 | **o gerador**: blocos, fundamentação, citação verificável | **citação para um trecho que não existe é pega por código** | ✅ |
| 11 | 18 | recuperação como ferramenta + reflexão + teto | custo médio por pergunta, antes e depois da autonomia | 🔜 |
| 12 | 19 | referência entre turnos + memória com procedência | fato externo não vira fato do usuário; exclusão apaga | 🔜 |
| 13 | 20 | orçamento com política de corte declarada | resultado gigante estoura e o corte segue a política escrita | 🔜 |
| 14 | 21 | as quatro métricas + tabela de diagnóstico | eval da etapa 5 × etapa 8: o ganho esperado aparece? | 🟡 parcial |
| 15 | 22 | **atacar o próprio sistema** | quanto cada camada bloqueia — e o que continua passando | 🔜 |
| 16 | 23 | painel custo + cache + latência + qualidade | acerto de cache antes e depois de reordenar as camadas | 🔜 |

A etapa 14 está **parcial** por decisão: as métricas de recuperação
([`avaliacao.py`](rag_zero/avaliacao.py)) foram antecipadas porque o cap. 09 exige
medir antes de otimizar, e não dava para escrever a etapa 5 sem elas. *Faithfulness* e
*answer relevance* exigem LLM-as-judge e ficam para a etapa completa.

## O mapa dos módulos

| Módulo | Cap. | O que resolve |
|---|:---:|---|
| [`portas.py`](rag_zero/portas.py) | 01, 05, 07 | as três portas e os adaptadores que não custam nada |
| [`contexto.py`](rag_zero/contexto.py) | 01, 20 | o contador por bloco, a montagem determinística, o orçamento |
| [`ingestao.py`](rag_zero/ingestao.py) | 04 | pipeline de ingestão, metadado com procedência, o filtro duro |
| [`chunking.py`](rag_zero/chunking.py) | 05 | desacoplar a unidade de busca da unidade de entrega |
| [`bm25.py`](rag_zero/bm25.py) | 06 | BM25 Okapi em ~40 linhas, com índice invertido |
| [`recuperacao.py`](rag_zero/recuperacao.py) | 06, 07 | denso, fusão RRF, reranking e **abstenção** |
| [`raptor.py`](rag_zero/raptor.py) | 10 | a árvore recursiva, com o limiar derivado do corpus |
| [`geracao.py`](rag_zero/geracao.py) | 11, 15 | fundamentação, citação verificável, abstenção |
| [`pipeline.py`](rag_zero/pipeline.py) | 02, 03 | os dois caminhos, os quatro contratos, o Naive RAG |
| [`consulta.py`](rag_zero/consulta.py) | 08 | resolução de referência, HyDE, expansão, roteamento |
| [`indexacao.py`](rag_zero/indexacao.py) | 09 | contextual retrieval × late chunking, com a conta |
| [`avaliacao.py`](rag_zero/avaliacao.py) | 21 | recall, precisão, taxa de resultado zero, taxa de acerto |

## A tese pedagógica das etapas

Quatro delas carregam o argumento do livro inteiro, e valem mesmo isoladas:

- **Etapa 0 — o contador.** O instrumento que você olha em todas as outras. A maior
  parte dos sistemas em produção não tem nada equivalente, e é por isso que degradam de
  forma inexplicável (cap. 20).
- **Etapa 3 — a ingestão antes da busca.** Provar que um documento revogado não é
  recuperado, mesmo sendo o mais similar, é o que separa um índice de uma pilha de
  texto (cap. 04). E o teste `test_metadado_gerado_nao_filtra_de_forma_dura` prova a
  outra metade: um extrator que **erra** não custa nada, porque o gerado não filtra.
- **Etapa 5 — o ganho por estágio.** Não se adota híbrido porque está na moda: adota-se
  porque a tabela mostra o ganho no **seu** corpus. Aqui ela mostra que, com embedder
  ruim, não há ganho — e isso é informação.
- **Etapa 6 — a abstenção.** A pergunta fora do corpus é a única que revela se o
  sistema sabe dizer "não encontrei" (caps. 06, 15).
- **Etapa 10 — a citação verificável.** Três geradores encenam os três modos de
  falha do cap. 15, e o verificador distingue os três: **citar fonte inexistente**
  (o mais perigoso, porque *parece* verificável), **responder sem citar** (pode
  estar certo, mas não dá para conferir) e **abster** (que é a resposta certa
  quando falta base, e por isso conta como fundamentada).

## Uma nota de honestidade sobre os números

Os números que a etapa 5 imprime vêm de um conjunto **sintético derivado do próprio
corpus** — perguntas escritas a partir dos documentos que as respondem. Isso
**superestima o recall** (cap. 21) e serve para comparar estágios entre si, que é o uso
aqui. Não serve para reportar qualidade absoluta, e o livro não o faz.

A medição com condição experimental publicada é a **rodada 4** do ROADMAP.
