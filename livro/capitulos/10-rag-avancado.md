# 10 — RAG Avançado

> **Estado da arte capturado em 2026-08** · edição 0.1 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** As quatro frentes e o critério de escolha estão fechados; as medições comparadas e o Apêndice A são a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Diagnosticar** qual das quatro falhas do RAG básico o seu sistema tem, antes de escolher técnica;
2. **Comparar** *contextual retrieval* e *late chunking* pelo que cada uma custa e pelo que resolve;
3. **Explicar** quando reescrever a consulta rende mais do que melhorar o índice;
4. **Decidir** se o seu problema justifica GraphRAG — e reconhecer quando não justifica.

## O problema

O RAG do cap. 09 funciona bem para uma classe de pergunta: fato localizado, expresso com vocabulário próximo do documento, contido em um trecho. Fora dessa classe, ele falha de quatro maneiras distintas — e a cura é diferente para cada uma.

1. **O chunk perdeu o contexto de onde veio.** "A margem caiu 12%" é inútil sem saber de que produto e de que trimestre. O índice não sabe; o chunk não diz.
2. **A pergunta não se parece com a resposta.** O usuário pergunta "por que meu pedido não chegou?" e o documento diz "SLA de entrega em regiões remotas". Nenhum estágio do cap. 09 fecha essa distância.
3. **A resposta exige juntar peças.** "Quem aprovou a política que o time do João segue?" precisa de dois ou três saltos entre documentos.
4. **A pergunta é global.** "Quais são os temas recorrentes nestes 800 chamados?" não tem trecho que a responda — nenhum `top_k` resolve.

Este capítulo é o mapa dessas quatro curas. E abre com o aviso mais importante: **cada uma custa**, e aplicar todas por precaução é a forma mais comum de tornar um RAG caro sem torná-lo bom.

## Fundamentos científicos

- **Chunking avançado, avaliado** — [arXiv 2504.19754](https://arxiv.org/abs/2504.19754) compara estratégias de reconstrução de contexto em vez de assumir a superioridade das mais elaboradas. `[a validar]`
- **Chunking alinhado entre documentos** — [arXiv 2601.05265](https://arxiv.org/abs/2601.05265) trata o corte considerando tópicos que atravessam documentos, atacando diretamente a falha 1. `[a validar]`
- **GraphRAG e a família de grafo** — a linha que constrói um grafo de entidades e relações, sumariza regiões densamente conectadas e recupera sobre essa estrutura, endereçando as falhas 3 e 4. Surveys recentes formalizam o paradigma e propõem estratégias híbridas de fusão entre grafo e texto. `[a validar]`
- **Reescrita de consulta em múltiplos turnos** — trabalho aplicado mostra reescrita de consulta combinada a recuperação híbrida como abordagem para RAG conversacional ([arXiv 2606.28352](https://arxiv.org/abs/2606.28352)), que é a falha 2 no cenário mais difícil (a pergunta depende do turno anterior). `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Contextual Retrieval** (Anthropic, fim de 2024) — antes de embeddar, prefixa-se cada chunk com um resumo curto, gerado por LLM, do seu lugar no documento. Ataca a falha 1 na raiz. Os ganhos publicados são cumulativos com BM25 e com reranking (números no [panorama](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md)); o custo é uma passada de LLM sobre o corpus inteiro na indexação.
- **Late Chunking** (Jina AI, 2024) — inverte a ordem: embeda o documento inteiro, e só **depois** do transformer, antes do *pooling*, aplica o corte. Cada chunk carrega contexto dos vizinhos sem nenhuma chamada de LLM. Resolve a mesma falha 1 por **muito menos dinheiro** — com o limite do comprimento máximo do modelo de embedding.
- **Reescrita e expansão de consulta** — a família que trabalha do lado da pergunta: reescrever para o vocabulário do corpus, gerar múltiplas variantes, ou gerar uma resposta hipotética e buscar por ela (HyDE). Barata em indexação, cara em latência (uma chamada extra antes de buscar).
- **A leitura de praticante de 2026** — o caminho de melhoria com melhor relação custo/benefício é: **embeddings contextuais → reranker → chunking semântico**, nessa ordem. Os dois primeiros são o que a maioria dos sistemas precisa; o terceiro é ajuste fino.

## O estado da arte

### 1. As quatro frentes, e o que cada uma custa

| Falha | Cura | Custo onde | Ordem de grandeza |
|---|---|---|---|
| Chunk sem contexto | **contextual retrieval** | indexação (1 chamada de LLM por chunk) | alto, uma vez |
| Chunk sem contexto | **late chunking** | indexação (só o modelo de embedding) | baixo, uma vez |
| Pergunta ≠ resposta | **reescrita / expansão / HyDE** | consulta (1+ chamada por pergunta) | baixo por vez, sempre |
| Exige juntar peças | **multi-hop / grafo** | consulta e indexação | alto nos dois |
| Pergunta global | **sumarização hierárquica (RAPTOR) / comunidades** | indexação pesada | muito alto, uma vez |

A tabela é a mensagem do capítulo. **Contextual retrieval e late chunking resolvem o mesmo problema com contas muito diferentes** — a primeira paga uma passada de LLM sobre todo o corpus; a segunda usa apenas o modelo de embedding. Para corpus grande e orçamento apertado, essa diferença decide.

E há a assimetria que muda a decisão: custo de **indexação** é pago uma vez e amortizado; custo de **consulta** é pago para sempre. Um sistema com muitas consultas sobre corpus estável deve empurrar o trabalho para a indexação. Um com corpus que muda toda hora e poucas consultas deve fazer o contrário.

### 2. Do lado da pergunta

Melhorar o índice é caro e demorado; melhorar a consulta costuma ser rápido e é frequentemente onde está o ganho:

- **Reescrita** — transformar a pergunta do usuário em uma consulta com o vocabulário do domínio. Em conversas, isso inclui **resolver a referência**: "e no ano passado?" não é uma consulta buscável sem o turno anterior. Esta é a falha 2 na sua forma mais comum e mais ignorada.
- **Múltiplas consultas** (*RAG Fusion*) — decompor uma pergunta composta em várias, buscar cada uma, e fundir os rankings. É a ponte natural para o cap. 11.
- **HyDE** — gerar uma resposta hipotética e usá-la como consulta, porque uma resposta se parece mais com o documento do que a pergunta se parece. Elegante, e vulnerável quando o modelo alucina uma hipótese fora do domínio.
- **Step-back prompting** — generalizar a pergunta antes de buscar ("qual é o princípio por trás disto?"), recuperar o contexto amplo e só então responder o específico. É o inverso da decomposição: sobe um nível em vez de descer.

As quatro atacam a mesma falha por ângulos diferentes, e a escolha é empírica. O que **não** é empírico é a ordem de tentativa: reescrita primeiro, sempre — é a mais barata e a que resolve o caso mais comum.

### 3. Sumarização hierárquica: a resposta para a pergunta global

A falha 4 — "quais são os temas recorrentes nestes 800 chamados?" — não tem trecho que a responda, e por isso nenhum ajuste de recuperação a resolve. A cura conhecida é construir, **na indexação**, camadas de resumo que não existiam no corpus.

A materialização de referência é o **RAPTOR**: agrupar os chunks por similaridade, resumir cada grupo, tratar os resumos como novos nós, e repetir — até uma árvore em que as folhas são o texto original e a raiz é o documento inteiro condensado. A recuperação passa a acontecer **em qualquer nível da árvore**: pergunta factual desce às folhas, pergunta global fica nos nós altos.

O GraphRAG usa a mesma ideia por outro caminho (resumos de comunidades densamente conectadas do grafo). A diferença prática: RAPTOR precisa apenas de embeddings e agrupamento; grafo precisa de extração de entidades, que é um pipeline a mais e uma fonte de erro a mais.

O custo dos dois é de indexação, alto e pago uma vez. Ambos só se justificam quando as perguntas globais são **frequentes** — se aparecem uma vez por mês, um resumo escrito à mão custa menos que a árvore.

### 4. Grafo: quando vale e quando é sobre-engenharia

GraphRAG muda **do que** se recupera: em vez de trechos, um grafo de entidades e relações, com resumos das comunidades densamente conectadas.

**Vale quando** o corpus tem entidades recorrentes com relações reais (pessoas, sistemas, contratos, incidentes) e as perguntas exigem atravessá-las — ou quando são globais ("quais os temas", "quem se conecta a quem"), que nenhum `top_k` responde.

**Não vale quando** o corpus é um conjunto de documentos independentes e as perguntas são factuais e locais. Nesse caso o grafo adiciona um pipeline de extração caro, uma fonte nova de erro (extração errada de entidade) e nenhuma resposta que o cap. 09 não desse.

O erro típico é adotar grafo pela promessa e descobrir que o problema real era chunk sem contexto — que custava uma fração e se resolvia no índice.

### 5. A regra de sequência

Como este capítulo é uma lista de melhorias possíveis, a regra de sequência importa mais que qualquer delas:

1. **Meça primeiro** qual das quatro falhas você tem (cap. 15 dá o instrumento: se a *context recall* está baixa, o problema é achar; se está alta e a *faithfulness* está baixa, o problema não é este capítulo).
2. **Aplique uma técnica por vez**, com medição antes e depois. Duas de uma vez e você não sabe qual pagou.
3. **Recuse o que não pagou.** Complexidade não removida é dívida permanente — e um pipeline com cinco estágios que ninguém entende é pior que um simples que erra de forma conhecida.

### Leitura executiva

O RAG básico falha de **quatro** maneiras — chunk sem contexto, pergunta que não se parece com a resposta, resposta que exige juntar peças, e pergunta global — e cada uma tem cura própria. **O que roubar:** *contextual retrieval* e *late chunking* resolvem a **mesma** falha com contas muito diferentes (uma passada de LLM sobre todo o corpus × só o modelo de embedding) — escolha pela conta, não pela fama. E lembre da assimetria: custo de **indexação** é pago uma vez; custo de **consulta**, para sempre. **O ganho mais rápido e mais ignorado:** trabalhar do lado da **pergunta** — reescrita (sempre a primeira, por ser a mais barata), múltiplas consultas, HyDE e *step-back*; e, em conversa, resolver referência entre turnos ("e no ano passado?" não é consulta buscável). **Para pergunta global** (a falha que nenhum `top_k` resolve), a cura é criar na indexação os resumos que o corpus não tem — **RAPTOR** (agrupar, resumir, repetir até uma árvore) ou comunidades de grafo; RAPTOR sai mais barato, porque dispensa extração de entidades. **Sobre grafo:** vale para entidades recorrentes com relações reais e perguntas globais; é sobre-engenharia para documentos independentes com perguntas locais — e o erro típico é adotá-lo quando o problema era chunk sem contexto. **A regra que vale mais que as técnicas:** meça qual das quatro falhas você tem, aplique **uma por vez**, e remova o que não pagou.

## Mão na massa — contexto-zero, etapa 9

Na etapa 9 você fecha o pipeline do `contexto-zero`: embeddings sobre os chunks da etapa 8, fusão com o BM25 que já existe, reranking dos 20 primeiros, e uma variante de *contextual retrieval* aplicada a um subconjunto do corpus. Cada estágio entra com medição antes e depois, sobre o mesmo conjunto de perguntas — e a tabela resultante é o entregável da etapa, mais do que o código. O exercício de completude: a fusão de rankings vem esqueletada; você implementa o peso entre os dois sinais e descobre que o peso ótimo depende do tipo de pergunta.

## Verificação

1. Você tem 2 milhões de chunks e orçamento apertado de indexação. Entre *contextual retrieval* e *late chunking*, qual escolhe e o que precisa verificar antes?
2. As perguntas do seu domínio quase sempre dependem do turno anterior ("e o segundo caso?"). Qual frente deste capítulo ataca isso, e por que melhorar o índice não resolveria?
3. Um time propõe GraphRAG. Que três perguntas você faz sobre o corpus e as perguntas antes de aprovar?

---

## Apêndice A — Como cada técnica avançada é implementada

> Tratamento por técnica, com fonte primária, condição da medição e implementação — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: as quatro frentes e a economia comparada estão descritas. O tratamento por técnica — com a condição experimental de cada número publicado, que é onde o Princípio I mais aperta neste capítulo — é o trabalho da **rodada 2** do ROADMAP.

Enfileirado: Contextual Retrieval (o número de redução de falha e o corpus em que foi medido) · Late Chunking e o limite do comprimento do modelo de embedding · HyDE e variantes de reescrita · GraphRAG e a família de grafo · sumarização hierárquica para perguntas globais.
