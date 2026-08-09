# 16 — Otimização Automática de Prompts

> **Estado da arte capturado em 2026-08** · edição 0.4 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** O argumento e as três famílias de otimizador estão fechados; as medições comparadas e o Apêndice A são a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Explicar** por que o prompt deixou de ser texto autoral e passou a ser artefato compilado contra uma métrica;
2. **Distinguir** as três famílias de otimizador (busca por exemplos, busca por instrução, reflexão sobre traços);
3. **Montar** o que um otimizador exige antes de rodar: métrica, conjunto de treino e conjunto de validação separados;
4. **Reconhecer** o risco central — otimizar contra uma métrica ruim produz um prompt confiantemente errado.

## O problema

Escrever prompt à mão tem um teto conhecido: você testa as variantes que consegue imaginar, no volume que consegue ler, e para quando parece bom. É artesanato — e artesanato não escala nem se defende quando o modelo muda.

A virada da disciplina foi tratar o prompt como **parâmetro otimizável**: dado um programa (a cadeia de chamadas), uma métrica e alguns exemplos, um algoritmo busca as instruções e os exemplos que maximizam a métrica. O texto que chega ao modelo deixa de ser o que o humano digitou.

Isso muda o trabalho de lugar. A pergunta deixa de ser *"como escrevo isto melhor?"* e passa a ser *"a minha métrica mede o que eu quero?"* — o que joga o peso do capítulo para o 07 e o 15.

## Fundamentos científicos

- **GEPA** ([arXiv 2507.19457](https://arxiv.org/abs/2507.19457)) — amostra trajetórias (*"reasoning, tool calls, and tool outputs"*) e reflete sobre elas em linguagem natural para *"diagnose problems, propose and test prompt updates"*, combinando lições pela **fronteira de Pareto** das próprias tentativas. O argumento do paper é o do capítulo: linguagem é meio de aprendizado mais rico que **recompensa escalar esparsa** — daí o contraste com RL/GRPO, que *"often require thousands of rollouts"*. ✓
- **MIPROv2** ([arXiv 2406.11695](https://arxiv.org/abs/2406.11695)) — otimizar instruções **e** demonstrações de cada módulo *"without access to module-level labels or gradients"*, com avaliação estocástica em mini-lotes para aprender um modelo surrogate do objetivo. O problema que ele nomeia é o que torna sistema composto difícil: **atribuição de crédito entre módulos**. ✓
- **TextGrad** — trata o prompt como variável textual otimizável e propaga "gradiente" em linguagem natural, mantendo os pesos do modelo fixos. Mais simples de montar; funciona melhor quando a dificuldade das amostras é uniforme. `[a validar]`
- **Promptomatix** ([arXiv 2507.14241](https://arxiv.org/abs/2507.14241)) — framework de otimização automática que reduz o setup manual exigido do usuário. `[a validar]`
- **Evidência de contexto** — estudos empíricos aplicados (por exemplo, otimização automática de prompt para construção de grafo de conhecimento, [arXiv 2506.19773](https://arxiv.org/abs/2506.19773)) sugerem que o ganho é real mas **dependente de tarefa** — o que é a moral do capítulo. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **DSPy** — o framework que popularizou a ideia de *compilar* prompts. O modelo mental que ele impôs à área: você declara **assinaturas** (entrada → saída) e módulos; os otimizadores (BootstrapFewShot, COPRO, MIPROv2, GEPA) escrevem o texto. É a referência prática deste capítulo.
- **[gepa-ai/gepa](https://github.com/gepa-ai/gepa)** — a implementação de referência do otimizador reflexivo, utilizável fora do DSPy.
- **Comparativos de praticante** — a leitura convergente de 2026 é que a escolha do otimizador depende da **heterogeneidade do conjunto de avaliação**: tarefas com dificuldade uniforme favorecem o caminho mais simples; conjuntos com tipos de problema variados favorecem os otimizadores que produzem estratégias especializadas.

## O estado da arte

### 1. As três famílias

| Família | O que busca | Custo | Quando escolher |
|---|---|---|---|
| **Busca por exemplos** (bootstrap) | quais demonstrações colocar no prompt | baixo | primeiro recurso; ganho rápido em tarefas de formato |
| **Busca por instrução** (bayesiana, evolutiva) | o texto da instrução, e às vezes exemplos junto | médio-alto | quando o formato já está bom e o problema é a estratégia |
| **Reflexão sobre traços** | instruções derivadas da análise do que deu errado na execução | alto | conjuntos heterogêneos; quando você quer entender *por que* melhorou |

A terceira família tem uma propriedade que as outras não têm e que é subestimada: ela produz **explicação junto com o artefato**. A reflexão em linguagem natural sobre traços de falha é legível — o que a torna útil mesmo quando você decide não usar o prompt otimizado.

### 2. O que o otimizador exige antes de rodar

Otimizador não é ferramenta que se aponta para um problema. Ele exige, na ordem:

1. **Uma métrica que valha a pena maximizar.** Este é o item que decide tudo. Otimizar contra uma métrica frouxa produz um prompt que é ótimo naquela métrica frouxa — e pior no que você realmente queria, porque o otimizador vai encontrar exatamente as brechas que a métrica deixou.
2. **Conjuntos separados de treino e validação.** Sem separação, o otimizador memoriza. O sintoma é o clássico: números excelentes no relatório e nenhum ganho em produção.
3. **Um orçamento.** Cada iteração são chamadas pagas. O custo de otimizar é real e deve ser comparado ao custo de continuar no artesanato.

O item 1 é o motivo de este capítulo vir **depois** do 07 na ordem de leitura recomendada, embora venha antes na numeração: quem não sabe medir não deveria otimizar.

### 3. O que muda no processo de engenharia

Adotar otimização automática reorganiza o trabalho:

- **O prompt vira artefato de build**, não arquivo editado à mão. Ele é gerado, versionado com o hash do conjunto de avaliação que o produziu, e regenerado quando o modelo ou o dado muda.
- **A revisão humana muda de objeto.** Você para de revisar o texto e passa a revisar a **métrica** e os **casos de avaliação** — que é onde a intenção do produto realmente mora.
- **A troca de modelo deixa de ser reescrita.** Recompila-se. Este é, na prática, o maior argumento econômico da abordagem.

### 4. A fronteira honesta

Três ressalvas que o entusiasmo costuma pular:

- **Nem toda tarefa ganha.** O ganho publicado é por benchmark; a evidência aplicada mostra dependência forte de tarefa. Meça no seu.
- **O prompt otimizado é frequentemente ilegível** — e a legibilidade tem valor operacional (auditoria, debug, confiança do time). Perdê-la é um custo, não um detalhe.
- **A métrica vira a especificação do produto.** É uma responsabilidade que a maioria das equipes assume sem perceber que assumiu.

### Leitura executiva

O prompt deixou de ser texto autoral e virou **artefato compilado** contra uma métrica: você declara entrada→saída e um otimizador escreve o texto. Três famílias — busca por **exemplos** (barata, comece aqui), busca por **instrução** (bayesiana/evolutiva) e **reflexão sobre traços** (cara, mas devolve explicação legível junto). **O que roubar:** trate o prompt como artefato de build, versionado com o hash do conjunto que o produziu — e a troca de modelo vira recompilação, não reescrita. **O risco central:** o otimizador encontra exatamente as brechas da sua métrica — **otimizar contra métrica ruim produz um prompt confiantemente errado**. Por isso: não otimize antes de saber medir (cap. 17), e nunca sem separar treino de validação.

## Mão na massa — rag-zero, etapa 10 (o gerador)

Na etapa 10 você constrói um otimizador mínimo, na mão, antes de qualquer framework: 20 casos rotulados, uma métrica, um laço que propõe K variantes de instrução, avalia e mantém a melhor — com validação separada. São ~60 linhas e ensinam o que nenhum tutorial de biblioteca ensina: o overfitting aparece na sua frente. Só depois a etapa mostra o mesmo problema com um framework, e a comparação é o conteúdo.

## Verificação

1. Seu otimizador reporta ganho de 12 pontos e produção não muda. Cite as duas causas mais prováveis, em ordem.
2. Por que a família "reflexão sobre traços" pode valer a pena mesmo quando você decide **não** usar o prompt que ela gerou?
3. Argumente contra a otimização automática num caso concreto: qual propriedade se perde, e para que tipo de sistema essa perda é inaceitável?

---

## Apêndice A — Como cada otimizador funciona

> Tratamento por implementação, com URL.

| Família | Implementação de referência | O que reter |
|---|---|---|
| **Busca por exemplos** | `BootstrapFewShot` do [DSPy](https://github.com/stanfordnlp/dspy) | o mais barato e o primeiro recurso. **Pegadinha:** o ganho vem dos exemplos, então ele evapora se a distribuição de produção diverge do conjunto. |
| **Busca por instrução** | `MIPROv2` ([arXiv 2406.11695](https://arxiv.org/abs/2406.11695)), no DSPy | otimiza instruções **e** exemplos sem rótulo por módulo, com surrogate sobre mini-lotes. O problema que ele nomeia — **atribuição de crédito entre módulos** — é o que torna sistema composto difícil. |
| **Reflexão sobre traços** | [gepa-ai/gepa](https://github.com/gepa-ai/gepa) | reflete em linguagem natural sobre trajetórias e combina lições pela fronteira de Pareto. **Devolve explicação legível** junto do artefato, o que os outros não fazem. |
| **Gradiente textual** | [zou-group/textgrad](https://github.com/zou-group/textgrad) | mais simples de montar. Funciona melhor quando a dificuldade das amostras é uniforme. |

**O alerta do Princípio I, que este apêndice não resolve:** todos os números comparativos entre otimizadores vêm de avaliações dos **próprios proponentes**. Nenhum entra no corpo do livro sem modelo e orçamento declarados — e a medição independente é a rodada 4.

**E a dependência que decide tudo:** otimizador precisa de **métrica**. Sem o cap. 17 de pé, otimizar prompt é acelerar na direção errada.
