# 00 — Introdução

> **Estado da arte capturado em 2026-08** · edição 0.1 (esqueleto) · [histórico e registro de expiração](HISTORICO.md)
>
> **Maturidade: fundação.** O argumento e a moldura do livro estão fechados. O aprofundamento por capítulo é o trabalho das rodadas seguintes — ver [ROADMAP](https://github.com/GHDaru/rag/blob/main/ROADMAP.md).

## Objetivos de aprendizagem

Ao final desta introdução, você deve ser capaz de:

1. **Distinguir** engenharia de prompt de engenharia de contexto pelo que cada uma decide;
2. **Situar** o RAG como técnica dentro da engenharia de contexto, e explicar por que a troca de rótulo sozinha não muda nada;
3. **Reconhecer** o problema comum às duas disciplinas — a janela é finita e o que entra nela é uma decisão de engenharia;
4. **Navegar** o livro: as três partes, o catálogo de referência e a trilha prática.

## O problema

Um modelo de linguagem não sabe nada sobre a sua tarefa além do que aparece na chamada. Nem o seu banco de dados, nem a conversa de ontem, nem a regra que "todo mundo sabe" na sua empresa. O que ele vê é uma sequência de tokens que **alguém montou** — e essa montagem tem orçamento, ordem, custo e consequência.

Duas disciplinas cresceram em volta dessa montagem, e a confusão entre elas custa caro:

- **Engenharia de prompt** decide **o que se escreve**: a instrução, os exemplos, o formato pedido, a estratégia de raciocínio induzida. É trabalho de *design de linguagem* — em grande parte estático, versionável, testável como código.
- **Engenharia de contexto** decide **o que se monta em runtime**: quais trechos recuperar, o que lembrar da sessão passada, qual resultado de ferramenta cabe, o que descartar quando o orçamento acabar. É trabalho de *arquitetura de sistema* — dinâmico, por requisição, com custo mensurável em tokens e latência.

A primeira pergunta que a maioria dos projetos faz é "como escrevo um prompt melhor?". A pergunta que resolve o problema, quase sempre, é a segunda: **"o que deveria estar na janela agora, e o que não deveria?"**

## RAG não é o tema — é a técnica central da segunda disciplina

Vale gastar um parágrafo nisto porque foi a pergunta que originou este livro: *engenharia de contexto substitui RAG?*

**Não como substituto — como moldura.** RAG (*Retrieval-Augmented Generation*) resolve um problema específico e bem definido: o conhecimento necessário não está nos pesos do modelo e não cabe inteiro na janela, então buscamos os pedaços relevantes em um corpus externo e os colocamos no contexto. Isso é **uma** forma de preencher **parte** da janela.

Engenharia de contexto é a disciplina que decide o conjunto todo — instrução, exemplos, histórico, memória de longo prazo, resultado de ferramenta, estado do ambiente **e** trechos recuperados — e como esses concorrentes dividem um orçamento finito.

|  | Engenharia de contexto | RAG |
|---|---|---|
| Nível | disciplina | técnica |
| Decide | o que ocupa a janela, em que ordem, e o que sai | que trechos do corpus respondem à pergunta |
| Falha típica | *context rot*, instrução afogada, orçamento estourado | recall baixo, chunk cortado, resposta sem fundamento |

A consequência prática é que quem adota a moldura passa a fazer perguntas que o RAG isolado não faz: *quanto* do orçamento vale gastar com recuperação; se aquele trecho compete com a memória; se recuperar agora ou deixar o agente decidir depois (cap. 11). Quem só troca o rótulo continua com o mesmo pipeline e o mesmo problema.

Este livro trata, portanto, **duas disciplinas em relação** — e dá ao RAG três capítulos (09, 10 e 11), que é o peso que ele merece dentro da segunda.

## Como o livro é organizado

**Parte I — Engenharia de Prompt** (caps. 02–07). O que se escreve. Começa na anatomia (separar instrução de dado), passa pelas famílias de técnica de raciocínio, pelo contrato de saída estruturada, pela camada de sistema/persona, e termina onde a disciplina virou engenharia de verdade: **otimização automática** (o prompt compilado contra uma métrica) e **avaliação** (sem a qual mudar prompt é apostar).

**Parte II — Engenharia de Contexto** (caps. 08–14). O que se monta em runtime. Abre com a janela como orçamento e a tensão contexto longo × recuperação; desce ao RAG em três níveis (recuperação, avançado, agêntico); e sobe de volta para memória, compactação e o contexto que vem de ferramentas.

**Parte III — O sistema em produção** (caps. 15–17). O que atravessa as duas: avaliar, proteger e pagar a conta. Estes três morreriam diluídos se ficassem espalhados nos capítulos anteriores.

**Fechamento** (cap. 18). O que já é consenso, o que ainda é disputa aberta e o que este livro aposta que vai expirar — com data.

Fora da linha narrativa, dois apoios de consulta (Diátaxis: *reference* nunca se mistura com *explanation*): o **[Catálogo de técnicas](apendice-tecnicas.md)**, com uma ficha por técnica, e o **[Apêndice do ecossistema](apendice-ecossistema.md)**, com frameworks e bibliotecas organizados por problema que resolvem.

## O método

O livro é **vivo** e **empírico**, e assume as consequências das duas coisas.

**Vivo** significa que todo capítulo declara sua data de captura, e que a revisão é uma nova rodada registrada no [Histórico](HISTORICO.md) — nunca uma sobrescrita silenciosa. A área muda rápido demais para fingir permanência; a honestidade é datar.

**Empírico** significa que uma técnica só entra no corpo do livro com duas coisas: a **fonte primária** (o paper ou a documentação oficial que propôs e mediu) e a **implementação pública** (o código consultável que mostra como aquilo vira sistema). Número sem condição experimental ao lado não entra — nem quando vem de fornecedor grande, nem quando confirma o que gostaríamos que fosse verdade.

E há uma regra que vale como aviso ao leitor: **toda medição citada aqui foi feita por alguém, em algum corpus, com algum modelo**. Reproduza no seu.

### Leitura executiva

O modelo só sabe o que você mostra. Engenharia de **prompt** decide o que se escreve; engenharia de **contexto** decide o que se monta em runtime — e **RAG é a técnica central da segunda, não a moldura de nada**. As duas resolvem o mesmo problema por ângulos diferentes: a janela é finita, e o que ocupa cada token é uma decisão de engenharia com custo e consequência. **Por onde começar:** se você já escreve prompts e o resultado é inconsistente, vá para o cap. 07 (avaliação) antes de escrever o próximo. Se o seu problema é "o modelo não sabe da minha empresa", comece no cap. 08 — e resista ao impulso de ir direto para o 09.

## Verificação

1. Uma equipe diz que "migrou de RAG para engenharia de contexto" e descreve o mesmo pipeline de antes. O que exatamente não mudou?
2. Dê um exemplo de decisão que a engenharia de contexto toma e que nenhuma escolha de prompt consegue tomar.
3. Por que este livro exige *paper* **e** *implementação pública* antes de colocar uma técnica no corpo? Que erro cada uma das duas exigências previne sozinha?
