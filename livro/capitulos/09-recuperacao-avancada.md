# 09 — Recuperação Avançada

> **Estado da arte capturado em 2026-08** · edição 0.2 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** Componentes que aprofunda: **chunking** e **embedding**, do lado da indexação (cap. 02).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Explicar** a falha que as técnicas deste capítulo curam: o chunk que perdeu de onde veio;
2. **Comparar** *contextual retrieval* e *late chunking* pela conta, não pela fama;
3. **Decidir** entre empurrar trabalho para a indexação ou para a consulta;
4. **Aplicar** a regra de sequência: medir, uma técnica por vez, remover o que não pagou.

## O problema

Os capítulos 06 e 07 otimizam **como se busca**. Este otimiza **o que está no índice** — sem mexer no corpus (cap. 04), que já está governado, e sem mexer na pergunta (cap. 08).

A falha específica: **o chunk perdeu o contexto de onde veio.** "A margem caiu 12%" é um trecho inútil sem saber de que produto e de que trimestre. O documento sabia; o chunk não. E o índice trata o chunk como se ele se bastasse.

O sintoma é característico: a busca traz trechos que são *sobre* o assunto certo, e a resposta sai errada ou vaga porque nenhum deles diz **de quê** está falando.

E o aviso que abre o capítulo, porque é o erro mais caro daqui: **cada técnica custa**, e aplicar todas por precaução é a forma mais comum de tornar um RAG caro sem torná-lo bom.

## Fundamentos científicos

- **Chunking avaliado** — [arXiv 2504.19754](https://arxiv.org/abs/2504.19754) compara estratégias avançadas de reconstrução de contexto em vez de assumir sua superioridade. `[a validar]`
- **Corte alinhado entre documentos** — [arXiv 2601.05265](https://arxiv.org/abs/2601.05265) trata o corte considerando tópicos que atravessam documentos, atacando a falha na raiz. `[a validar]`
- **O lugar no paradigma** — na taxonomia de Gao ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)), estas são técnicas de **indexação refinada** do Advanced RAG. O movimento de 2026 é justamente o deslocamento do esforço de otimização para a etapa de indexação. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Contextual Retrieval** (Anthropic, fim de 2024) — antes de embeddar, prefixa-se cada chunk com um resumo curto, gerado por LLM, do seu lugar no documento. Ataca a falha na raiz; custa uma passada de LLM sobre o **corpus inteiro**. Os ganhos publicados são cumulativos com busca esparsa e com reranking — e a curva importa mais que os números (ver a ressalva abaixo).
- **Late Chunking** (Jina AI, 2024) — inverte a ordem: embeda o documento inteiro e só **depois** do transformer, antes do *pooling*, aplica o corte. Cada chunk carrega contexto dos vizinhos **sem nenhuma chamada de LLM**. Resolve a mesma falha por muito menos dinheiro, limitado pelo comprimento máximo do modelo de embedding (cap. 05).
- **A ressalva do Princípio I** — os números de *contextual retrieval* são o caso de deriva documentado no [panorama §6.2](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md): a redução de ~67% é resultado dos **três estágios cumulativos** e reaparece, em fontes secundárias, como mérito da técnica sozinha. Este livro cita a curva, não o número solto.

## O estado da arte

### 1. Duas curas, contas muito diferentes

| Técnica | O que faz | Custo de indexação | Limite |
|---|---|---|---|
| **Contextual Retrieval** | prefixa cada chunk com um resumo do seu lugar no documento, antes de embeddar | **1 chamada de LLM por chunk** | preço, em corpus grande |
| **Late Chunking** | embeda o documento inteiro, corta depois do transformer | só o modelo de embedding | comprimento máximo do embedder |

Esta tabela é a mensagem do capítulo. As duas resolvem **a mesma falha**, e a diferença de conta é de ordem de grandeza. Para corpus de milhões de chunks com orçamento apertado, a decisão é aritmética, não estética.

O que decide entre elas:

- **Tamanho do corpus** — quantas chamadas de LLM você está disposto a pagar uma vez.
- **Tamanho dos documentos** — se eles excedem o comprimento máximo do embedder, *late chunking* não se aplica inteiro.
- **Volatilidade** — corpus que muda toda hora reprocessa sempre, e aí o custo "uma vez" vira recorrente.

### 2. A assimetria que decide muita coisa

Custo de **indexação** é pago uma vez e amortizado por todas as consultas. Custo de **consulta** (cap. 08) é pago para sempre.

| O seu caso | Empurre o trabalho para |
|---|---|
| Muitas consultas, corpus estável | **indexação** — amortiza |
| Poucas consultas, corpus volátil | **consulta** — não reprocessa nada |
| Muitas consultas, corpus volátil | o caso difícil: reindexação incremental (cap. 04) |

O terceiro caso é onde a maioria dos sistemas de empresa vive, e é o que torna a política de reindexação do cap. 04 uma decisão de arquitetura, não de manutenção.

### 3. A regra de sequência

Como este capítulo é uma lista de melhorias possíveis, a regra de **como** aplicá-las vale mais que qualquer uma delas:

1. **Meça primeiro** qual falha você tem (cap. 21). Se *context recall* está baixo, o problema é achar — e pode estar no corpus (04), na representação (05) ou na busca (06), não aqui. Se está alto e *faithfulness* está baixa, o problema é a geração (15).
2. **Aplique uma técnica por vez**, com medição antes e depois. Duas de uma vez e você não sabe qual pagou.
3. **Remova o que não pagou.** Complexidade não removida é dívida permanente — e um pipeline de cinco estágios que ninguém entende é pior que um simples que erra de forma conhecida.

O passo 3 é o que quase ninguém faz, e é o que separa um sistema que evolui de um que só acumula.

### Leitura executiva

A falha deste capítulo é uma só: **o chunk perdeu o contexto de onde veio** — "a margem caiu 12%" é inútil sem saber de que produto e trimestre. **O que roubar:** *contextual retrieval* e *late chunking* curam a **mesma** falha com contas de ordem de grandeza diferente — a primeira paga **uma chamada de LLM por chunk** sobre o corpus inteiro; a segunda usa **só o modelo de embedding**, limitada pelo comprimento máximo dele. Para corpus grande, a decisão é aritmética, não estética. **A assimetria que decide muita coisa:** indexação é paga uma vez e amortizada; consulta é paga para sempre — muitas consultas sobre corpus estável pedem indexação, corpus volátil pede o lado da pergunta, e "muitas consultas + corpus volátil" é o caso difícil que transforma reindexação incremental em decisão de arquitetura. **A regra que vale mais que as técnicas:** meça qual falha você tem antes de escolher, aplique **uma por vez** com medição dos dois lados, e **remova o que não pagou** — este último passo quase ninguém faz, e é o que separa um sistema que evolui de um que só acumula. **Sobre os números publicados:** o ~67% do *contextual retrieval* é resultado de três estágios cumulativos e circula como mérito de um só; cite a curva, não o número.

## Mão na massa — rag-zero, etapa 8

Na etapa 8 você aplica *contextual retrieval* a um subconjunto do corpus do `rag-zero` e mede: ganho de recall, custo de indexação em chamadas, e tempo. Depois faz o mesmo com uma aproximação de *late chunking*, e coloca as duas contas lado a lado. A etapa entrega a tabela comparativa — e o achado é que a escolha depende de números do seu corpus, não da reputação da técnica. O exercício de completude: o prompt que gera o contexto do chunk vem esqueletado; você descobre que a qualidade dele decide o ganho inteiro.

## Verificação

1. Você tem 2 milhões de chunks e orçamento apertado de indexação. Entre as duas técnicas, qual escolhe e o que precisa verificar antes?
2. Seu corpus muda várias vezes por dia e recebe milhares de consultas. Por que esse é o caso difícil, e o que ele exige do cap. 04?
3. Você aplicou três técnicas de uma vez e o recall subiu 8 pontos. Qual é o problema com essa informação?

---

## Apêndice A — Como cada técnica avançada é implementada

**Rodada 1 (edição 0.2)**: as duas curas e a economia comparada estão descritas. O tratamento por técnica — com a condição experimental de cada número publicado, que é onde o Princípio I mais aperta neste capítulo — é o trabalho da **rodada 2** do ROADMAP.

Enfileirado: Contextual Retrieval (o corpus em que foi medido) · Late Chunking e o limite do embedder · chunking avaliado (2504.19754) · corte alinhado entre documentos (2601.05265) · indexação refinada no Advanced RAG (2312.10997).
