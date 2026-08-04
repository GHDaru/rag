# 05 — Chunking e Representação

> **Estado da arte capturado em 2026-08** · edição 0.2 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** Componentes que aprofunda: **chunking** e **embedding** (cap. 02).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Escolher** uma estratégia de corte a partir do tipo de pergunta, não do formato do documento;
2. **Aplicar** o padrão que separa a unidade de busca da unidade de entrega;
3. **Avaliar** um modelo de embedding pelo que ele erra no seu domínio, não pelo lugar no ranking;
4. **Reconhecer** quando o problema atribuído à busca é, na verdade, de representação.

## O problema

O corpus já está limpo e governado (cap. 04). Agora ele precisa virar **unidades indexáveis** e **vetores** — e as duas conversões destroem informação de formas diferentes.

O corte destrói **contexto**: o parágrafo que começa com "isso implica que…" perde o antecedente ao virar chunk isolado. A vetorização destrói **precisão**: dois textos com sentidos distintos podem ficar próximos, e um identificador raro pode não ter representação nenhuma.

O que torna este capítulo caro de errar é que **as duas decisões são anteriores a tudo** — mudar o chunking ou o modelo de embedding significa reindexar o corpus inteiro. É a decisão mais difícil de reverter do sistema.

## Fundamentos científicos

- **Chunking avaliado, não assumido** — [arXiv 2504.19754](https://arxiv.org/abs/2504.19754) compara estratégias avançadas de reconstrução de contexto em vez de presumir que as mais elaboradas vencem. `[a validar]`
- **Seleção adaptativa** — [arXiv 2603.25333](https://arxiv.org/abs/2603.25333) propõe escolher o método de corte **por documento**, reconhecendo formalmente que "um tamanho serve para tudo" é a hipótese errada. `[a validar]`
- **Tópicos que atravessam documentos** — [arXiv 2601.05265](https://arxiv.org/abs/2601.05265) trata o corte considerando o corpus como conjunto, e não o documento isolado. `[a validar]`
- **Avaliação de representação** — **MTEB** mede modelos de embedding em múltiplas tarefas e é a referência para escolher sem confundir com o resto do pipeline. A ressalva vale mais que o ranking: posição em benchmark geral **não transfere** para domínio específico (cap. 21). `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **O caminho de melhoria de melhor relação custo/benefício** relatado pelos praticantes começa em embeddings contextuais e chunking semântico — mas ambos vêm **depois** de acertar a granularidade, que é decisão deste capítulo.
- **O limite que decide o desenho** — todo modelo de embedding tem comprimento máximo. Ele restringe o tamanho do chunk e, portanto, a estratégia inteira (é o que limita *late chunking*, cap. 09).
- **A prática que quase ninguém faz** — inspecionar visualmente os chunks gerados. Uma amostra de trinta lidos por gente revela problemas de corte que nenhuma métrica agregada mostra.

## O estado da arte

### 1. As estratégias de corte

| Estratégia | Como corta | Boa para | Falha em |
|---|---|---|---|
| **Nenhuma** | o documento é a unidade | FAQ, tickets, descrições curtas | documento longo |
| **Tamanho fixo** | N tokens, com sobreposição | linha de base honesta | corta no meio do raciocínio |
| **Recursiva** | separadores em cascata (parágrafo → frase → token) | o padrão razoável da maioria dos corpora | ainda é corte cego, só que educado |
| **Estrutural** | pela marcação do documento | documentos com hierarquia real | documento sem estrutura confiável |
| **Semântica** | por quebra de tópico detectada | prosa longa sem seções | pré-processamento; fronteiras instáveis |
| **Sentence-window** | indexa a frase, entrega a janela em volta | precisão na busca com contexto na entrega | janela fixa nem sempre serve |
| **Proposition** | decompõe em afirmações autocontidas | pergunta factual específica | caro; perde o encadeamento |
| **Hierárquica** | indexa pequeno, entrega o pai | perguntas de granularidades diferentes | complexidade de índice |

### 2. O padrão que vale mais que a escolha

As três últimas compartilham uma ideia, e ela é o conteúdo deste capítulo: **desacoplar a unidade de busca da unidade de entrega.**

O que se indexa deve ser pequeno e preciso — é o que faz o ranking funcionar. O que se envia ao modelo deve ser grande o bastante para responder — é o que faz a geração funcionar. Fixar as duas coisas no mesmo chunk é aceitar um compromisso que não precisava existir.

Quase todo sistema que sofre com "o trecho certo veio, mas sem contexto suficiente" está preso nesse compromisso — e a saída não é aumentar o chunk (o que degrada o ranking), é separar as duas unidades.

### 3. Três regras que sobrevivem à escolha da estratégia

- **Sobreposição não é opcional** em corte cego. É o remendo mais barato para a fronteira mal colocada.
- **O tamanho ótimo depende da pergunta, não do documento.** Perguntas factuais favorecem chunks pequenos; perguntas que exigem contexto favorecem grandes. Corpus com os dois tipos pede índice com mais de uma granularidade.
- **Metadado viaja junto** (o contrato do cap. 02). Sem ele, não há filtro antes da busca — e filtro antes da busca costuma render mais que qualquer ajuste de similaridade.

### 4. Representação: o que o embedding não vê

Escolher modelo de embedding por posição em ranking geral é o erro previsível. O que decide no seu caso:

- **O domínio.** Vocabulário técnico, siglas internas e nomes de produto podem estar fora do treino do modelo — e aí a busca densa não os representa, por melhor que ele seja no benchmark.
- **O idioma.** Modelo multilíngue ou específico muda o resultado em português mais do que a diferença entre os primeiros colocados do ranking.
- **O comprimento máximo.** Define o teto do chunk e restringe estratégias inteiras.
- **O custo de reindexação.** Trocar de modelo é reprocessar tudo. Isso torna a escolha mais permanente do que ela parece na hora de fazer.

E a consequência que este capítulo empurra para o próximo: **o que o embedding não representa, a busca densa não acha** — e é exatamente por isso que a busca esparsa continua indispensável (cap. 06). Muita falha atribuída ao retriever é, na verdade, de representação.

### Leitura executiva

Chunking e embedding são as duas decisões **mais caras de reverter** do sistema — mudar qualquer uma significa reindexar tudo. **O que roubar:** o padrão que vale mais que a escolha da estratégia — **desacople a unidade de busca da unidade de entrega**. O que se indexa deve ser pequeno e preciso; o que se envia, grande o bastante para responder. Quem sofre com "veio o trecho certo, sem contexto suficiente" está preso a esse compromisso, e a saída **não** é aumentar o chunk (isso degrada o ranking) — é separar as unidades (sentence-window, hierárquico, proposition). **Sobre tamanho:** o ótimo depende da **pergunta**, não do documento; corpus com perguntas de tipos diferentes pede mais de uma granularidade. **Sobre embedding:** escolha pelo que ele erra no **seu** domínio (vocabulário interno, siglas, idioma, comprimento máximo), não por posição em ranking geral — benchmark geral não transfere. **A ponte para o próximo capítulo:** o que o embedding não representa, a busca densa não acha — e é por isso que a esparsa continua indispensável.

## Mão na massa — rag-zero, etapa 4

Na etapa 4 você implementa três estratégias de corte sobre o texto deste livro e as compara com o mesmo conjunto de perguntas: fixa com sobreposição, estrutural por seção, e sentence-window. A etapa entrega a tabela, não o vencedor — e o achado pedagógico é que o vencedor muda com o tipo de pergunta. O exercício de completude: a janela do sentence-window vem esqueletada; você decide o tamanho e descobre que ele é uma decisão de produto disfarçada de parâmetro.

## Verificação

1. Seu sistema recupera o trecho certo, mas a resposta sai incompleta por falta de contexto em volta. Qual é a solução **errada** e qual é a certa?
2. Um identificador interno (`XR-4400-B`) não é encontrado pela busca densa. Isso é falha de representação ou de busca? O que muda na sua ação?
3. Por que trocar o modelo de embedding é uma decisão mais permanente do que parece?

---

## Apêndice A — Como cada abordagem trata corte e representação

**Rodada 1 (edição 0.2)**: as estratégias e o padrão de desacoplamento estão descritos. O tratamento por implementação — bibliotecas de chunking, famílias de modelo de embedding e o que MTEB mede exatamente — é a **rodada 2** do ROADMAP.

Enfileirado: chunking avaliado (2504.19754) · seleção adaptativa (2603.25333) · corte alinhado entre documentos (2601.05265) · MTEB e os limites da transferência de benchmark.
