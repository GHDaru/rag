# 10 — Recuperação Estruturada

> **Estado da arte capturado em 2026-08** · edição 0.3 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** Componentes que aprofunda: **índice** e **retriever**, quando o corpus deixa de ser só texto (cap. 02).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Reconhecer** as duas perguntas que nenhum `top_k` sobre texto responde;
2. **Decidir** se o seu corpus justifica um grafo — e reconhecer quando não justifica;
3. **Comparar** grafo e sumarização hierárquica pelo que cada um custa e resolve;
4. **Combinar** recuperação sobre texto e sobre dado estruturado sem duplicar o sistema.

## O problema

Os capítulos 06 a 09 tratam o corpus como uma coleção de trechos independentes, e a pergunta como algo respondível por alguns deles. Duas classes de pergunta quebram essa suposição:

- **Multi-hop.** *"Quem aprovou a política que o time do João segue?"* Nenhum trecho contém a resposta. Ela existe na **relação** entre trechos, e recuperar os dois melhores não a produz.
- **Global.** *"Quais são os temas recorrentes nestes 800 chamados?"* A resposta é uma propriedade do **conjunto**, não de nenhuma parte dele. Aumentar `top_k` não aproxima — piora.

Há ainda um terceiro caso, comum em empresa e mal atendido: a pergunta cuja resposta está em **dado estruturado** (*"quantos contratos vencem este mês?"*), não em prosa. Buscar texto sobre contratos não responde; contar linhas responde.

Este capítulo trata do que fazer quando **a estrutura do conhecimento importa** — e do custo de reconhecê-la.

## Fundamentos científicos

- **GraphRAG** ([arXiv 2404.16130](https://arxiv.org/abs/2404.16130)) — o paper nomeia a falha exatamente como este capítulo: *"RAG **fails on global questions** directed at an entire text corpus, such as **'What are the main themes in the dataset?'**"*, porque isso é sumarização orientada a consulta, não recuperação. O mecanismo tem duas etapas: derivar um **grafo de entidades** e **pré-gerar resumos de comunidade** para grupos de entidades relacionadas. Cada resumo gera uma resposta parcial, e as parciais são resumidas na final. A distinção que a literatura marca: **GraphRAG muda *do que* se recupera; RAG agêntico muda *como*** (cap. 18). ✓
- **RAPTOR** ([arXiv 2401.18059](https://arxiv.org/abs/2401.18059)) — *"recursively embedding, clustering, and summarizing chunks of text, constructing a tree with differing levels of summarization from the bottom up"*, com recuperação *"at different levels of abstraction"*. **Número com a condição ao lado:** +20% de acurácia absoluta no QuALITY sobre o melhor anterior — **acoplado ao GPT-4**, não isolado. ✓
- **Grafo + agente** — a convergência das duas linhas, com o agente navegando a estrutura em vez de receber trechos ([arXiv 2509.22009](https://arxiv.org/abs/2509.22009)). `[a validar]`
- **Surveys de RAG agêntico sobre grafo** — a área tem revisão própria, sinal de que deixou de ser experimento. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **A promessa e a conta** — grafo é a técnica mais vendida e a que mais decepciona quando adotada pelo motivo errado. Ela adiciona um pipeline de extração de entidades — caro, e uma fonte nova de erro que não existia antes.
- **O erro típico**, relatado repetidamente: adotar grafo e descobrir que o problema real era chunk sem contexto (cap. 09) — que custava uma fração e se resolvia no índice.
- **Texto + estruturado** — a prática consolidada em empresa é rotear entre um retriever de texto e uma consulta a banco, e não tentar representar tudo como texto. Transformar tabela em prosa para embeddar é o anti-padrão desta seção.

## O estado da arte

### 1. As duas curas, e suas contas

| Cura | Como funciona | Resolve | Custo |
|---|---|---|---|
| **Sumarização hierárquica (RAPTOR)** | agrupa, resume, repete → árvore | pergunta global; visão por nível | indexação: embeddings + resumos |
| **Grafo (GraphRAG)** | entidades + relações + resumo de comunidades | multi-hop e global | indexação: **extração de entidades** + grafo |

A diferença prática que decide: **RAPTOR precisa apenas de embeddings e agrupamento; grafo precisa extrair entidades e relações.** Essa extração é um modelo a mais, um erro a mais e um custo a mais — e é ela que faz a maior parte da diferença de preço entre as duas. Vale notar que os dois papers **descrevem o próprio mecanismo assim**: o RAPTOR fala em *embedding, clustering and summarizing*; o GraphRAG, em *derive an entity knowledge graph* como primeira das duas etapas. A conta não é interpretação do livro — está nas fontes.

A recomendação que decorre: **se a pergunta é global, tente RAPTOR antes de grafo.** Se a pergunta é multi-hop sobre entidades reais e recorrentes, grafo é o caminho.

### 2. Quando o grafo paga

**Paga quando** o corpus tem entidades recorrentes com relações que importam — pessoas, sistemas, contratos, incidentes, componentes — **e** as perguntas atravessam essas relações. Um corpus de incidentes em que se pergunta "que serviços foram afetados pelos incidentes causados pelo deploy X?" é o caso exemplar.

**Não paga quando** o corpus é um conjunto de documentos independentes e as perguntas são factuais e locais. Aí o grafo adiciona extração cara, erro novo, e nenhuma resposta que os caps. 06–09 não dessem.

As três perguntas que decidem, antes de aprovar:

1. As entidades do meu domínio são **recorrentes e nomeáveis**, ou cada documento fala de coisas diferentes?
2. As perguntas reais atravessam **mais de um documento por relação**, ou se resolvem em um trecho?
3. Eu já **medi** que a falha é de multi-hop, e não de chunk sem contexto ou de recall?

Um "não" em qualquer uma delas é motivo suficiente para adiar.

### 3. Texto e dado estruturado no mesmo sistema

O caso mais comum em empresa, e o menos tratado nos livros de RAG: parte do conhecimento está em prosa, parte em tabela.

O anti-padrão é **transformar tabela em texto para embeddar**. Perde-se agregação, ordenação e contagem — exatamente o que a tabela fazia bem — em troca de uma busca semântica sobre números, que é o pior uso possível de embedding.

O padrão que funciona é **roteamento** (cap. 08): classificar a pergunta e mandar para o retriever certo — texto para prosa, consulta gerada para dado estruturado — e, quando a resposta exige os dois, buscar em paralelo e fundir. É um padrão ramificado (cap. 03), com um retriever a mais, não um sistema a mais.

A ressalva de segurança, que vale registrar aqui: consulta gerada por modelo contra banco de produção é superfície de ataque e de acidente. Vale somente-leitura, escopo restrito e teto de resultado (cap. 22).

### 4. O que ainda não está resolvido

- **Manutenção do grafo.** Documentos mudam; entidades se fundem e se renomeiam. Reconstruir o grafo inteiro é caro, e atualizá-lo incrementalmente é problema aberto.
- **Avaliação.** As quatro métricas do cap. 21 supõem trechos recuperados. Como medir *context recall* quando o recuperado é um subgrafo, ou um resumo de comunidade, não tem resposta consolidada.
- **Quando parar de subir na árvore.** Em RAPTOR, escolher o nível certo por pergunta é decisão em aberto, hoje resolvida por heurística.

### Leitura executiva

Duas perguntas quebram a suposição dos capítulos anteriores: **multi-hop** (a resposta está na *relação* entre trechos) e **global** (a resposta é propriedade do *conjunto* — aumentar `top_k` piora). **O que roubar:** a diferença de conta entre as duas curas — **RAPTOR precisa só de embeddings e agrupamento; grafo precisa extrair entidades**, o que é um modelo a mais, um erro a mais e um custo a mais. Daí a regra: **se a pergunta é global, tente RAPTOR antes de grafo**; grafo é para multi-hop sobre entidades recorrentes e reais. **Antes de aprovar grafo, três perguntas** — as entidades são recorrentes e nomeáveis? as perguntas atravessam documentos por relação? você já **mediu** que a falha é de multi-hop, e não de chunk sem contexto? Um "não" basta para adiar, e o erro típico da área é adotar grafo para curar um problema que custava uma fração. **Sobre texto + tabela:** o anti-padrão é transformar tabela em prosa para embeddar (perde agregação e contagem em troca de busca semântica sobre números); o padrão é **rotear** entre retrievers e fundir — com a consulta gerada em somente-leitura, escopo restrito e teto.

## Mão na massa — rag-zero, etapa 9

Na etapa 9 você monta a versão mínima honesta das duas curas sobre o texto deste livro: uma árvore de resumos por agrupamento (RAPTOR reduzido a ~80 linhas) e um roteador que manda perguntas globais para os nós altos e factuais para as folhas. Grafo fica **de fora**, deliberadamente — e a etapa explica por quê: o corpus do livro não tem entidades recorrentes o suficiente para justificá-lo, e fingir que tem seria ensinar o erro que o capítulo denuncia. O exercício de completude: o critério de escolha de nível vem esqueletado.

## Verificação

1. *"Quais os assuntos mais frequentes nos nossos 5.000 chamados?"* Por que aumentar `top_k` piora essa resposta?
2. Um time propõe GraphRAG. Faça as três perguntas de aprovação e diga o que faria se a resposta à terceira for "ainda não medimos".
3. Por que transformar uma tabela de contratos em texto para embeddar é um anti-padrão? O que se perde exatamente?

---

## Apêndice A — Como cada abordagem estrutura a recuperação

**Rodada 1 (edição 0.2)**: as duas curas e a fronteira texto/estruturado estão descritas. O tratamento por implementação — construção e manutenção de grafo, variantes de RAPTOR, e o problema aberto de avaliar recuperação estruturada — é a **rodada 2** do ROADMAP.

Enfileirado: GraphRAG e a família de grafo · RAPTOR · grafo + agente (2509.22009) · roteamento texto/SQL e seus riscos de segurança.
