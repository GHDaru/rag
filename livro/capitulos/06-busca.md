# 06 — Busca: Esparsa, Densa e Híbrida

> **Estado da arte capturado em 2026-08** · edição 0.2 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
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

- **A tradição** — recuperação por sobreposição de termos, com ponderação por frequência e raridade, é a base de *Information Retrieval* há décadas (a família **BM25**). Sobreviveu a todas as gerações de modelo por resolver uma propriedade do problema: casar o **literal**. `[a validar]`
- **A vez do denso** — a recuperação por similaridade de vetores resolve a paráfrase, que a esparsa nunca resolveu. **BEIR** mede recuperação zero-shot em domínios variados e é a referência para este estágio isolado do resto do pipeline. `[a validar]`
- **A fusão** — combinar rankings de sinais diferentes é técnica clássica de IR, e é o que sustenta a busca híbrida. Na taxonomia de Gao ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)), híbrido é um dos acréscimos que definem o Advanced RAG. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **O consenso mais firme da área** — a leitura publicada é que praticamente todo benchmark recente mostra **BM25 + denso fundidos superando qualquer um sozinho**. É a afirmação com maior convergência independente deste livro.
- **A fusão de fato** — combinar por posição no ranking (em vez de por nota bruta) é a prática dominante, porque dispensa calibrar escalas incomparáveis entre os dois sistemas.
- **O sintoma que denuncia falta de esparsa** — "o RAG não encontra o óbvio". Quase sempre o óbvio é um código, uma sigla ou um nome próprio que o índice denso não representa.

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

## Mão na massa — rag-zero, etapa 5

Na etapa 5 você constrói a busca do `rag-zero` **na mão, antes de qualquer biblioteca**: um BM25 em cerca de 40 linhas sobre o texto deste livro, depois embeddings, depois a fusão por posição — medindo os três com o mesmo conjunto de perguntas. O objetivo pedagógico é ver o ranking acontecer e o ponto cego de cada família aparecer numa pergunta concreta. O exercício de completude: o peso da fusão vem esqueletado; você o calibra e descobre que o ótimo muda com o tipo de pergunta.

## Verificação

1. Usuários buscam por código de produto (`XR-4400-B`) e não encontram, mas encontram por descrição. Qual família está faltando, e por quê?
2. Por que fundir por posição dispensa calibrar as notas dos dois sistemas?
3. Seu sistema filtra por permissão depois de recuperar. Descreva o problema de segurança concreto, além da ineficiência.

---

## Apêndice A — Como cada abordagem busca

**Rodada 1 (edição 0.2)**: os modos de falha complementares e a fusão estão descritos. O tratamento por implementação — variantes de BM25, algoritmos de fusão de ranking, estruturas de índice vetorial e o que BEIR mede — é a **rodada 2** do ROADMAP.

Enfileirado: BM25 e variantes · fusão recíproca de ranking e alternativas · índices vetoriais aproximados e o custo do recall · BEIR · híbrido no Advanced RAG (2312.10997).
