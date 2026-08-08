# 00 — Introdução

> **Estado da arte capturado em 2026-08** · edição 0.3 · [histórico e registro de expiração](HISTORICO.md)
>
> **Maturidade: fundação.** A moldura do livro está fechada. O aprofundamento por capítulo é o trabalho das rodadas seguintes — ver [ROADMAP](https://github.com/GHDaru/rag/blob/main/ROADMAP.md).

## Objetivos de aprendizagem

Ao final desta introdução, você deve ser capaz de:

1. **Definir** o problema que o RAG resolve — e os dois que ele não resolve;
2. **Explicar** por que RAG é um **sistema**, não uma técnica, e o que essa distinção muda na prática;
3. **Situar** este livro em relação ao debate "RAG morreu" e à engenharia de contexto;
4. **Navegar** as seis partes e escolher por onde entrar.

## O problema

Um modelo de linguagem sabe o que estava nos seus pesos no dia em que foi treinado. Não sabe o preço de hoje, a política que sua empresa revisou semana passada, nem o histórico daquele cliente.

A saída óbvia — "coloque tudo na pergunta" — esbarra em três limites duros: o corpus não cabe, o que cabe custa caro em toda chamada, e o que cabe demais o modelo aproveita mal.

**RAG é a resposta a esse impasse**: buscar, em um corpus externo, os pedaços relevantes para *esta* pergunta, e gerar uma resposta fundamentada neles. Recuperação e geração — as duas metades da sigla, e a segunda costuma ser esquecida.

O que RAG **não** resolve, e vale dizer logo:

- **Não ensina o modelo a raciocinar melhor.** Se o erro é de raciocínio, recuperar mais não ajuda.
- **Não conserta corpus ruim.** Um documento revogado embedda exatamente igual a um vigente. O índice não sabe o que é verdade; sabe o que é parecido.

## Por que "Engenharia" de RAG

Existe muito material sobre *técnicas* de RAG: chunking, embeddings, reranking, HyDE, GraphRAG. Cada uma explicada isoladamente, nenhuma situada. O leitor acumula peças e não recebe a máquina.

Este livro faz a aposta contrária: **RAG é um sistema com componentes, contratos e topologias** — e a decisão que importa quase nunca é "qual técnica", é "onde ela encaixa e o que ela custa".

Por isso o livro abre com dois capítulos que quase nenhum material tem:

- **[02 — Anatomia de um sistema de RAG](capitulos/02-anatomia-do-sistema.md)**: os dezesseis componentes, o que cada um decide, e os contratos entre eles.
- **[03 — Arquiteturas de referência](capitulos/03-arquiteturas-de-referencia.md)**: os quatro paradigmas (Naive → Advanced → Modular → Agêntico) e os padrões de fluxo.

E por isso **cada capítulo de técnica declara qual componente aprofunda.** É o que impede este livro de virar o catálogo que ele critica.

O nome é cunhagem nossa, como foi "Engenharia de Harness" no [livro irmão](https://github.com/GHDaru/harness_engineering). Não existe "Engenharia de RAG" consagrada na literatura — existe RAG, que é o termo universal, e existe *Information Retrieval*, o campo de 60 anos que o absorveu (há um track de RAG no TREC). O que este livro propõe é tratar a composição desses dois mundos como disciplina.

## "RAG morreu" e a engenharia de contexto

Você vai encontrar as duas afirmações, e as duas merecem resposta curta.

**"RAG morreu porque as janelas cresceram."** Não. Janela grande resolve o caso em que o corpus inteiro cabe — e mesmo aí a qualidade não acompanha o tamanho, além de você pagar por todos os tokens em toda requisição. A leitura de 2026 é híbrida: **recuperar para reduzir, raciocinar em contexto longo sobre o que sobrou.** O cap. 20 trata do ponto de corte.

**"RAG virou engenharia de contexto."** A engenharia de contexto é a camada **acima**: ela decide o que ocupa a janela entre todos os candidatos — instrução, memória, histórico, resultado de ferramenta e trechos recuperados. É uma disciplina maior e legítima, e é o assunto do livro irmão sobre harness de agentes.

Este livro fica no andar de baixo, deliberadamente: **como se constrói o sistema que produz o melhor trecho recuperado, e a melhor resposta fundamentada nele.** Quando um capítulo esbarra no andar de cima — orçamento de janela, memória entre sessões — ele trata só a parte que é de RAG e aponta para lá.

## Como o livro é organizado

| Parte | O que responde |
|---|---|
| **Abertura** (00–01) | o problema, o vocabulário, a herança de IR |
| **I — A arquitetura** (02–03) | quais são os componentes e as topologias |
| **II — O corpus** (04–05) | o que entra no índice e como vira unidade buscável |
| **III — Recuperação** (06–10) | como se acha: busca, reranking, a pergunta, indexação refinada, estrutura |
| **IV — Geração** (11–17) | como se responde: o prompt, o raciocínio, o contrato, e a **fundamentação** |
| **V — Produção** (18–23) | agente, conversa, orçamento, avaliação, segurança, custo |
| **Fechamento** (24) | consenso, disputa aberta, e o que vai expirar |

A **Parte IV** merece nota: ela é engenharia de prompt inteira, a serviço da geração. Um livro de RAG que trata o "G" como detalhe está tratando metade da sigla como detalhe — e o [cap. 15](capitulos/15-geracao-fundamentada.md) é o elo que costura as duas metades.

Fora da linha narrativa, dois apoios de consulta: o **[Catálogo de técnicas](apendice-tecnicas.md)** e o **[Apêndice do ecossistema](apendice-ecossistema.md)**.

## O método

O livro é **vivo** e **empírico**, e assume as consequências das duas coisas.

**Vivo**: todo capítulo declara sua data de captura, e revisar é uma nova rodada registrada no [Histórico](HISTORICO.md) — nunca uma sobrescrita silenciosa. O [cap. 24](24-convergencias.md) registra apostas datadas sobre o que vai deixar de valer.

**Empírico**: uma técnica só entra no corpo com **fonte primária** (o paper ou a documentação que propôs e mediu) **e** **implementação pública**. Número sem condição experimental ao lado não entra — nem de fornecedor grande, nem quando confirma o que gostaríamos.

E um aviso que vale para o livro inteiro: **toda medição citada aqui foi feita por alguém, em algum corpus, com algum modelo.** Reproduza no seu. É o que o [benchmark](https://github.com/GHDaru/rag/blob/main/benchmark/README.md) existe para fazer, a partir da rodada 4.

### Leitura executiva

RAG resolve um impasse concreto — o conhecimento não está nos pesos, não cabe na janela e o que cabe custa caro — e **não** resolve dois outros: raciocínio ruim e corpus ruim. **A aposta deste livro:** RAG é um **sistema com componentes, contratos e topologias**, não um catálogo de técnicas; a decisão que importa quase nunca é "qual técnica" e sim "onde ela encaixa e o que custa". Por isso os caps. 02 e 03 vêm antes de qualquer técnica, e cada capítulo declara o componente que aprofunda. **Sobre os dois debates:** janela grande não matou o RAG (a leitura é híbrida — recuperar para reduzir, raciocinar sobre o que sobrou), e engenharia de contexto é a camada **acima**, assunto do livro irmão. Este fica no andar de baixo, de propósito. **Por onde começar:** pela tabela de sintomas do [cap. 01](01-fundamentos.md), com o seu problema real na mão — não pelo sumário.

## Verificação

1. Um time diz que vai "resolver o RAG" trocando por um modelo de janela de 2M. Cite uma razão de qualidade e uma de custo para duvidar.
2. Qual é a diferença prática entre conhecer as técnicas de RAG e conhecer a arquitetura? Dê um exemplo de decisão que só a segunda permite.
3. Por que este livro exige *paper* **e** *implementação pública*? Que erro cada exigência previne sozinha?
