# 12 — Técnicas de Raciocínio

> **Estado da arte capturado em 2026-08** · edição 0.3 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** As seis famílias e o critério de escolha estão fechados; a ficha por técnica e as medições comparadas são a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Nomear** as seis famílias de técnica de prompting e o problema que cada uma ataca;
2. **Escolher** entre elas por critério de custo/benefício, não por popularidade;
3. **Reconhecer** quando uma técnica de raciocínio deixou de pagar porque o modelo passou a fazer aquilo sozinho;
4. **Conectar** a família *decomposition* + *thought generation* à ponte que leva ao RAG agêntico (cap. 18).

## O problema

Modelos erram tarefas de vários passos não por falta de conhecimento, mas por tentarem produzir a resposta final direto. Uma família inteira de técnicas existe para induzir o modelo a **gastar computação antes de responder** — e cada uma cobra esse gasto em tokens, latência e dinheiro.

O problema real do capítulo não é "quais técnicas existem" (o catálogo é público e grande). É **quando cada uma para de valer a pena**: técnicas nascidas para compensar limitações de modelos de 2022–2023 continuam sendo aplicadas por inércia sobre modelos que já raciocinam por padrão, pagando o custo sem receber o benefício.

## Fundamentos científicos

- **A taxonomia de referência** — *The Prompt Report* ([arXiv 2406.06608](https://arxiv.org/abs/2406.06608)) organiza 58 técnicas textuais em **seis famílias**: *zero-shot*, *few-shot*, *thought generation*, *ensembling*, *self-criticism*, *decomposition*. A estrutura deste capítulo é essa. `[a validar]`
- **Chain-of-Thought** ([arXiv 2201.11903](https://arxiv.org/abs/2201.11903)) — induzir passos intermediários explícitos antes da resposta; a fundação da família *thought generation*. **A condição experimental é a parte que quase todo mundo omite:** o efeito *"emerge naturally in **sufficiently large** language models"* — a demonstração é um modelo de **540B** com **oito** exemplares, no GSM8K. Em modelo pequeno, CoT não reproduz o ganho. ✓
- **Self-Consistency** ([arXiv 2203.11171](https://arxiv.org/abs/2203.11171)) — amostrar caminhos diversos em vez do guloso e escolher por *"marginalizing out the sampled reasoning paths"*; a materialização mais simples e mais cara da família *ensembling*. Ganhos publicados: GSM8K **+17,9%**, SVAMP **+11,0%**, AQuA **+12,2%**. ✓
- **ReAct** ([arXiv 2210.03629](https://arxiv.org/abs/2210.03629)) — gerar raciocínio e ação *"in an interleaved manner"*, com as ações servindo para *"interface with external sources, **such as knowledge bases**"*. Essa última frase é literalmente a ponte deste livro: o paper já previa a base de conhecimento como destino da ação. Nasce como padrão de prompt (Parte IV) e vira arquitetura de recuperação (cap. 18). ✓
- **Avaliação comparada** — há evidência sistemática comparando variantes de CoT em domínios específicos ([exemplo em QA médico](https://www.sciencedirect.com/science/article/pii/S0010482525009655)); o padrão que emerge é que o ganho depende fortemente do domínio e do modelo, o que reforça a regra de medir. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **[Prompt Engineering Guide](https://github.com/dair-ai/prompt-engineering-guide)** (DAIR.AI) — cada técnica com exemplo executável; o caminho mais curto entre ler e testar.
- **Modelos de raciocínio dos provedores** — a mudança estrutural de 2025–2026: raciocínio em passos deixou de ser algo que o prompt induz e passou a ser algo que o modelo faz internamente, com orçamento configurável. Isso **desloca** o capítulo: a pergunta deixa de ser "como induzo CoT?" e passa a ser "quanto raciocínio eu compro para esta tarefa?".
- **Coleções curadas** — [promptslab](https://github.com/promptslab/awesome-prompt-engineering) e [natnew](https://github.com/natnew/Awesome-Prompt-Engineering) reúnem variantes e casos de uso por domínio.

## O estado da arte

### 1. As seis famílias, e o que cada uma compra

| Família | O que faz | Custo típico | Quando ainda paga |
|---|---|---|---|
| **Zero-shot** | instrução direta, sem exemplo | 1× | quase sempre a primeira tentativa — e frequentemente suficiente hoje |
| **Few-shot** | exemplos no prompt fixam formato e estilo | + tokens fixos por chamada | formato idiossincrático; rótulos com fronteira sutil |
| **Thought generation** | força passos intermediários (CoT e variantes) | + tokens de saída | tarefa com aritmética, lógica ou múltiplas restrições |
| **Decomposition** | quebra o problema em subproblemas explícitos | + chamadas | tarefa grande, composta, ou com etapas que exigem ferramenta |
| **Ensembling** | várias amostras + agregação (self-consistency) | N× o custo | quando o erro é caro e a variância é o inimigo |
| **Self-criticism** | o modelo revisa e corrige a própria saída | 2× ou mais | saída longa e estruturada; verificação contra critério explícito |

A leitura que importa: **as três primeiras linhas ficaram mais baratas e menos necessárias; as três últimas ficaram mais relevantes.** À medida que os modelos passaram a raciocinar sozinhos, o valor migrou de *induzir raciocínio* para *estruturar trabalho* — decompor, agregar e verificar são operações de sistema, não de redação.

### 2. O critério de escolha (que não é popularidade)

Três perguntas, nesta ordem, resolvem a escolha na prática:

1. **O erro é de raciocínio ou de conhecimento?** Se o modelo não sabe o fato, nenhuma técnica desta lista ajuda — o problema é da Parte III (recuperação, caps. 04–10). Esta é a confusão mais cara da área: times gastam semanas otimizando prompt para um problema de contexto.
2. **O erro é caro?** Ensembling multiplica o custo por N. Só se justifica quando errar custa mais do que N chamadas.
3. **O ganho sobrevive ao seu eval?** Toda técnica aqui tem evidência publicada em *algum* benchmark. Nenhuma tem garantia no **seu**. O capítulo 17 existe por causa desta pergunta.

### 3. A ponte para a recuperação

*Decomposition* + *thought generation* + uso de ferramenta é literalmente a arquitetura do **ReAct**: pensar sobre o que falta, agir para obter, observar o resultado, repetir. Quando a "ação" é uma busca em corpus, isso deixa de ser técnica de prompt e vira **RAG agêntico** (cap. 18).

Vale marcar a passagem porque ela é a costura entre as duas metades do livro: a mesma ideia — gastar computação antes de responder — muda de natureza quando o que se gasta é uma **ida ao mundo externo** em vez de tokens de pensamento. O custo passa a ser latência e superfície de ataque (cap. 22), não só fatura.

### Leitura executiva

Seis famílias: *zero-shot*, *few-shot*, *thought generation*, *decomposition*, *ensembling*, *self-criticism*. Com modelos que já raciocinam por padrão, o valor **migrou das três primeiras para as três últimas** — de induzir raciocínio para estruturar trabalho. **O que roubar:** antes de escolher técnica, responda se o erro é de raciocínio ou de conhecimento — se for de conhecimento, você está no livro errado (vá ao cap. 06); e trate *ensembling* como decisão financeira (N× o custo), não como upgrade. **A ponte:** *decomposition* + ferramenta = ReAct = a arquitetura do cap. 18. **O que vai expirar:** as receitas de indução de CoT — o raciocínio virou parâmetro de compra, não truque de redação.

## Mão na massa — rag-zero, etapa 10 (o gerador)

Na etapa 10 você implementa duas famílias no `rag-zero` e as compara com números: uma variante *thought generation* e uma variante *self-consistency* (3 amostras + voto), sobre o mesmo conjunto de 20 perguntas. O contador de tokens da etapa 0 mostra o preço; a taxa de acerto mostra o benefício. O exercício de completude: a agregação por voto vem esqueletada — você implementa o desempate, e descobre que o desempate é onde mora a decisão de produto.

## Verificação

1. Seu sistema erra ao responder perguntas sobre a política interna da empresa. Qual das seis famílias resolve? (Cuidado: é pegadinha.)
2. Um time aplica self-consistency com N=5 num classificador que roda 2 milhões de vezes por dia. Que pergunta você faz antes de discutir a técnica?
3. Explique por que ReAct pertence tanto ao cap. 12 quanto ao cap. 18, e o que muda de natureza na passagem.

---

## Apêndice A — Como cada fonte trata as técnicas de raciocínio

> Tratamento por técnica, com fonte primária e implementação — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: a taxonomia está adotada e as fontes primárias identificadas. O tratamento por técnica — ficha com proposta original, condição experimental da medição publicada, e implementação pública consultável — é o trabalho da **rodada 2**, e alimenta o [Catálogo de técnicas](../apendice-tecnicas.md).

Enfileirado para o tratamento: Chain-of-Thought e variantes (zero-shot CoT, least-to-most) · Self-Consistency · ReAct · Tree-of-Thought · Reflexion e a família de auto-crítica · Plan-and-Solve.
