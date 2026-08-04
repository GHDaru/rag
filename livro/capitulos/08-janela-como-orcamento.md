# 08 — A Janela como Orçamento

> **Estado da arte capturado em 2026-08** · edição 0.1 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** A tese do orçamento e a leitura híbrida estão fechadas; as medições por regime e o Apêndice A são a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Explicar** por que "mandar tudo" é anti-padrão com base empírica, e não por economia;
2. **Descrever** *context rot* e por que a degradação não é linear com o comprimento;
3. **Decidir** entre contexto longo e recuperação para um caso concreto, com critérios;
4. **Declarar** um orçamento de contexto explícito para um sistema real — quem recebe quantos tokens, e quem cede quando falta.

## O problema

A janela cresceu de milhares para milhões de tokens, e a conclusão intuitiva — "então acabou o problema" — é falsa por dois motivos independentes.

O primeiro é de **qualidade**: a capacidade de usar o que está na janela não acompanha o tamanho dela. Colocar mais texto pode piorar a resposta, e piora de forma que não é proporcional ao que se acrescentou.

O segundo é de **conta**: contexto é cobrado por token e a latência cresce com ele. Um sistema que enche a janela por preguiça de decidir paga essa preguiça em toda requisição, para sempre.

Este capítulo abre a Parte II porque é o capítulo que transforma "colocar informação no prompt" em **decisão de alocação**.

## Fundamentos científicos

- **Degradação posicional** — *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)): a informação no meio de contextos longos é sistematicamente pior aproveitada que a das bordas. É a base empírica da regra "o que importa vai para as pontas". `[a validar]`
- **Avaliação unificada dos dois regimes** — *U-NIAH: Unified RAG and LLM Evaluation for Long Context Needle-In-A-Haystack* ([arXiv 2503.00353](https://arxiv.org/abs/2503.00353)) coloca contexto longo e RAG no mesmo teste, em vez de compará-los por anedota. O achado que interessa: RAG com top-k supera o modelo sozinho em cenários de contexto longo. `[a validar]`
- **Gestão de contexto como componente formal** — o survey [arXiv 2507.13334](https://arxiv.org/abs/2507.13334) trata compressão, hierarquia de memória e otimização de contexto como um dos três componentes da disciplina — o que dá nome acadêmico ao que este capítulo chama de orçamento. `[a validar]`
- **A natureza da degradação** — a leitura consolidada de 2026 é que a queda **não é linear com o comprimento**: ela é dirigida pela **similaridade semântica entre o alvo e os distratores**. Alvo semanticamente distinto do ruído é encontrado mesmo em contexto muito longo; distratores parecidos derrubam a acurácia, e o efeito piora com o comprimento. `[a validar — esta é a afirmação do capítulo que mais precisa de citação primária]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Context rot** — o termo que a indústria adotou para a degradação de qualidade em contextos longos e conversas longas. A consequência de projeto que os praticantes descrevem é sempre a mesma: **curadoria agressiva supera janela cheia**.
- **O consenso híbrido de 2026** — a leitura de praticante convergiu para: recuperar um conjunto focado (dezenas a poucas centenas de milhares de tokens) e **raciocinar em contexto longo sobre esse conjunto**. Nem RAG puro (que perde raciocínio sobre documento inteiro), nem contexto longo puro (que apodrece). O ponto de corte exato varia por modelo — e é exatamente o tipo de número que este livro se recusa a fixar sem medição própria.
- **Orçamento como prática** — sistemas maduros declaram limites por fonte (tantos tokens para regras, tantos para recuperado, tantos para histórico) e uma política de corte quando estoura. A maioria dos sistemas não declara — e degrada silenciosamente.

## O estado da arte

### 1. A janela é um orçamento, e os concorrentes são conhecidos

Cinco fontes disputam o mesmo espaço em toda requisição:

| Fonte | Cresce com | Quem costuma cortar |
|---|---|---|
| Prompt de sistema e regras | releases e incidentes | ninguém (cap. 05) |
| Histórico da conversa | número de turnos | compactação (cap. 14) |
| Recuperado | `top_k` e tamanho do chunk | quase sempre o primeiro a ser cortado |
| Memória de longo prazo | tempo de relacionamento | raramente instrumentado (cap. 13) |
| Resultado de ferramenta | imprevisível, e é o pior | quase ninguém (cap. 15) |

A linha crítica é a última: resultado de ferramenta é a única fonte cujo tamanho **você não controla** no momento de pedir. Uma consulta que devolve 40 mil tokens não avisa antes. Sistemas sem teto por ferramenta descobrem isso em produção.

**O exercício que este capítulo cobra:** escrever a alocação em uma linha. `sistema 2k | memória 1k | recuperado 8k | ferramenta ≤4k | histórico o resto, compactando`. Um sistema com essa linha escrita se comporta de forma previsível quando o orçamento aperta; um sem ela se comporta de forma que ninguém consegue explicar depois.

### 2. Contexto longo × recuperação: os critérios

A pergunta "RAG morreu com janelas de 1M?" tem resposta operacional, não filosófica. Quatro critérios decidem:

1. **Tamanho do corpus.** Se o conhecimento total cabe confortavelmente com folga, contexto longo é mais simples e evita uma classe inteira de falhas de recuperação. Se não cabe, a pergunta nem se coloca.
2. **Frescor.** Dado que muda entre requisições exige busca. Não há janela grande o suficiente para conteúdo que mudou há um minuto.
3. **Forma do raciocínio.** Pergunta que exige entender um documento **inteiro** (resumir, comparar seções distantes) sofre com chunking. Pergunta que exige achar um fato específico entre milhares de documentos é recuperação.
4. **Orçamento de latência e custo.** Encher a janela custa em toda requisição; indexar custa uma vez. Volume alto de requisições sobre corpus estável favorece recuperação por pura aritmética.

O padrão híbrido é a resposta na maioria dos casos reais: **recupere para reduzir, depois raciocine em contexto longo sobre o que sobrou.**

### 3. O que medir

Orçamento sem instrumentação é intenção. Quatro números que um sistema maduro conhece:

- **Composição do contexto por fonte** (tokens por bloco, por requisição). É o painel básico e quase ninguém tem.
- **Taxa de estouro** — com que frequência o orçamento aperta, e quem foi cortado quando apertou.
- **Utilidade do recuperado** — quantos dos trechos enviados foram efetivamente citados na resposta. Um `top_k` de 20 com 2 usados é 18 blocos de ruído pagos (a métrica formal disso é *context precision*, cap. 16).
- **Qualidade × comprimento** — a mesma pergunta com contextos de tamanhos diferentes. É o teste que mostra se o seu sistema está em regime de *context rot* ou não, e nenhuma referência externa substitui rodá-lo no seu dado.

### Leitura executiva

Janela maior não resolveu nada: a degradação **não é linear com o comprimento** — ela é dirigida pela similaridade entre o alvo e os distratores, e por isso encher a janela pode piorar a resposta **e** a fatura. **O que roubar:** escreva a alocação do seu contexto em **uma linha** (`sistema 2k | memória 1k | recuperado 8k | ferramenta ≤4k | histórico o resto`) e defina quem cede quando aperta — sistemas sem essa linha degradam de um jeito que ninguém consegue explicar depois. **O concorrente esquecido:** resultado de ferramenta é a única fonte cujo tamanho você não controla ao pedir; sem teto por ferramenta, você descobre em produção. **Contexto longo × RAG:** decida por corpus, frescor, forma do raciocínio e aritmética de custo — e prefira o híbrido (recupere para reduzir, raciocine sobre o que sobrou). **Meça:** composição por fonte, taxa de estouro, utilidade do recuperado, e qualidade × comprimento no **seu** dado.

## Mão na massa — contexto-zero, etapa 7

Na etapa 7 você transforma o contador de tokens da etapa 0 em **orçamento com política**: limites por fonte, ordem de corte declarada, e um log por requisição com a composição do contexto. O teste da etapa força o estouro (um resultado de ferramenta gigante) e prova que o sistema corta segundo a política escrita, e não segundo o acaso da ordem de concatenação. O exercício de completude: a política de corte vem esqueletada — você decide quem cede primeiro e defende a decisão por escrito.

## Verificação

1. Seu sistema responde bem com 5 documentos recuperados e pior com 20. Dê duas explicações compatíveis com o que este capítulo apresentou, e um experimento que as distingue.
2. Em que situação contexto longo **puro** é a escolha certa, e o que precisa ser verdade sobre o seu corpus para isso?
3. Você mede que 2 dos 15 trechos recuperados aparecem citados na resposta. Isso é um problema de recuperação, de orçamento, ou dos dois? Justifique.

---

## Apêndice A — Como cada fonte trata o orçamento de contexto

> Tratamento por sistema e por medição, com URL — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: a tese do orçamento e a leitura híbrida estão descritas. O tratamento por medição — os regimes onde cada abordagem domina, com o benchmark e os modelos usados em cada afirmação — é o trabalho da **rodada 2**, e é o capítulo onde este livro mais precisa desconfiar de números de terceiros.

Enfileirado: U-NIAH e a avaliação unificada dos dois regimes · estudos de *needle-in-a-haystack* com distratores semânticos · práticas publicadas de orçamento explícito em agentes de produção · a economia comparada (indexar uma vez × encher a janela sempre).
