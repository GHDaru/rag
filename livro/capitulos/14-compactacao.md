# 14 — Compactação e Isolamento

> **Estado da arte capturado em 2026-08** · edição 0.1 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** As estratégias e o argumento do isolamento estão fechados; o tratamento por implementação é a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Comparar** as estratégias de redução do histórico pelo que cada uma preserva e destrói;
2. **Identificar** o que nunca deve ser compactado, e por quê;
3. **Explicar** o isolamento de contexto (subagentes) como alternativa arquitetural à compactação;
4. **Detectar** o sintoma de compactação malfeita: o sistema que "esquece" o que foi combinado.

## O problema

Toda conversa longa chega ao limite. Quando chega, alguma coisa tem de sair — e a escolha de o que sai é feita por alguém: por você, deliberadamente, ou pelo acaso da implementação.

O sintoma de que foi o acaso é reconhecível: o assistente que, depois de vinte turnos, esquece a decisão do turno três, refaz uma pergunta já respondida, ou volta a violar uma restrição que o usuário estabeleceu no começo. Isso não é limitação de modelo. É perda de informação num ponto do sistema que ninguém projetou.

E há um segundo problema, mais sutil: compactar tem **custo de qualidade que não aparece na métrica de turno**. Uma resposta ruim porque o resumo perdeu uma restrição é indistinguível, no eval do cap. 07, de uma resposta ruim por qualquer outra razão. Esta é a lacuna que o cap. 07 já registrou: quase toda a instrumentação mede um turno, e este capítulo trata do que falha ao longo de muitos.

## Fundamentos científicos

- **Compressão como componente formal** — o survey [arXiv 2507.13334](https://arxiv.org/abs/2507.13334) coloca compressão de contexto e hierarquias de memória entre os componentes de gestão de contexto, ao lado da otimização. Compactar não é gambiarra: é parte da disciplina. `[a validar]`
- **A degradação que justifica compactar** — *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)) e a literatura de *context rot* (cap. 08) sustentam o argumento contraintuitivo: às vezes compactar **melhora** a resposta, mesmo quando havia espaço. Menos ruído vale mais que mais informação. `[a validar]`
- **Segmentação por evento** — a linha de trabalho sobre segmentar diálogos longos por evento em vez de por janela deslizante ([arXiv 2601.07582](https://arxiv.org/abs/2601.07582)) aponta que **onde** se corta importa tanto quanto quanto se corta. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Compactação por sumarização** — a prática dominante em assistentes de execução longa: ao aproximar-se do limite, resumir os turnos antigos em um bloco e continuar. A engenharia está nos detalhes: quando disparar, o que preservar literalmente, e como sinalizar ao usuário que aconteceu.
- **Isolamento por subagente** — a alternativa arquitetural: em vez de compactar um contexto que cresce, distribuir o trabalho entre contextos que não se misturam. Cada subagente recebe uma tarefa fechada e devolve um resultado curto; o contexto principal nunca vê o meio do caminho. Troca compressão por delegação.
- **Descarregar para fora da janela** — manter o estado em arquivo ou estrutura externa e recuperar sob demanda, em vez de carregar no histórico. É o encontro deste capítulo com o cap. 10: o histórico vira corpus.

## O estado da arte

### 1. As estratégias, e o que cada uma destrói

| Estratégia | Como reduz | Preserva | Destrói |
|---|---|---|---|
| **Janela deslizante** | descarta os turnos mais antigos | o recente, literal | tudo que foi combinado no início |
| **Sumarização** | resume o antigo em um bloco | o sentido geral | detalhe literal, número, nome exato |
| **Sumarização por camadas** | resume resumos, progressivamente | mais horizonte | precisão, cumulativamente |
| **Seleção por relevância** | mantém os turnos relevantes ao momento | o pertinente | o contexto de por que algo foi decidido |
| **Descarregamento** | move para fora e recupera sob demanda | tudo, potencialmente | nada — mas depende da recuperação funcionar |

Não há estratégia sem perda. A pergunta de projeto não é "qual perde menos", é **"qual perde o que eu posso perder"** — e isso depende do produto. Um assistente de suporte pode perder o histórico de conversa fiada; não pode perder o número do pedido.

### 2. O que nunca se compacta

Uma lista curta e inegociável:

- **Restrições estabelecidas pelo usuário.** "Nunca me mande e-mail" precisa sobreviver a toda compactação. Restrição vira estado estruturado, não texto no histórico.
- **Decisões e seus identificadores.** Números de pedido, IDs, valores acordados, nomes de arquivo. São exatamente o que a sumarização apaga primeiro, porque parecem detalhe.
- **A memória de trabalho.** O plano da tarefa em andamento (cap. 13): se estava implícito no histórico, a compactação o destrói.
- **O que a política exige registrar.** Consentimento, aviso dado, confirmação recebida.

A implicação de arquitetura é o ponto do capítulo: **essas coisas não deveriam estar no histórico em primeiro lugar.** Elas pertencem a estado estruturado, fora do texto compactável. Compactação segura começa antes de compactar — na decisão de que informação crítica não mora em prosa.

### 3. Isolamento como alternativa

Compactação assume um contexto único que cresce. Isolamento questiona a premissa.

Quando uma tarefa grande é decomposta em subtarefas fechadas, cada uma pode ter seu próprio contexto — com seu próprio orçamento — e devolver ao principal apenas o resultado. O contexto principal nunca vê os cinquenta passos intermediários que a subtarefa consumiu.

| | Compactação | Isolamento |
|---|---|---|
| Premissa | um contexto que cresce | vários contextos pequenos |
| Perda | informação resumida | contexto compartilhado entre as partes |
| Custo | uma chamada de resumo | coordenação, e chamadas paralelas |
| Falha | esquecer o combinado | subtarefa que precisava do que não recebeu |

Isolamento é frequentemente a resposta certa para trabalho **decomponível** (analisar 30 documentos, executar 10 verificações). Compactação é a resposta para conversa **contínua**, que não decompõe. Muito sistema aplica a segunda quando precisava da primeira.

### 4. Quando compactar, e como avisar

- **Não espere o limite.** Compactar sob pressão, no meio de uma tarefa, é o pior momento. O gatilho deve ser um percentual do orçamento (cap. 08), não o erro de estouro.
- **Compacte em fronteira segura** — entre tarefas, não no meio de um raciocínio ou de um ciclo de ferramenta.
- **Sinalize.** O usuário deve saber que o histórico foi comprimido. Um sistema que esquece silenciosamente parece quebrado; um que avisa parece honesto — e o custo de implementar é uma linha.
- **Meça o antes e o depois.** Guardar o histórico original permite auditar o que a compactação destruiu. É a única forma de melhorar o resumo, e quase ninguém faz.

### Leitura executiva

Toda conversa longa chega ao limite, e a escolha do que sai é feita por alguém — por você, ou pelo acaso da implementação. Nenhuma estratégia é sem perda; a pergunta não é "qual perde menos" e sim **"qual perde o que eu posso perder"**. **O que roubar:** a lista do que **nunca** se compacta (restrições do usuário, identificadores e decisões, memória de trabalho, registros exigidos por política) — e a implicação de arquitetura que ela carrega: **essas coisas não deveriam estar no histórico em primeiro lugar**, e sim em estado estruturado fora do texto compactável. **A alternativa que se esquece:** **isolamento** (subagentes com contextos próprios) resolve trabalho *decomponível* melhor que qualquer resumo; compactação é para conversa *contínua* — e muito sistema aplica a segunda quando precisava da primeira. **Operacional:** dispare por percentual do orçamento (não pelo erro de estouro), corte em fronteira segura, **avise o usuário**, e guarde o original para auditar o que o resumo destruiu.

## Mão na massa — contexto-zero, etapa 13

Na etapa 13 o `contexto-zero` ganha compactação: gatilho em 70% do orçamento da etapa 7, sumarização em fronteira de turno, e um bloco de **estado estruturado** que nunca é compactado (restrições, identificadores, plano). O teste que fecha a etapa é o que importa: uma restrição estabelecida no turno 2 continua sendo respeitada no turno 40, depois de duas compactações. O exercício de completude: o extrator de estado vem esqueletado — você decide o que promove de prosa para estrutura.

## Verificação

1. Seu assistente esquece, depois de vinte turnos, o formato de resposta que o usuário pediu no começo. Onde está o erro de arquitetura — e por que "melhorar o prompt do resumo" é a resposta errada?
2. Dê um caso em que compactar **melhora** a qualidade da resposta mesmo havendo espaço na janela. Qual capítulo sustenta isso?
3. Você precisa analisar 40 relatórios e produzir uma síntese. Compactação ou isolamento? Justifique pela natureza da tarefa.

---

## Apêndice A — Como cada sistema trata a compactação

> Tratamento por implementação, com estratégia e gatilho — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: as estratégias e a fronteira compactação × isolamento estão descritas. O tratamento por implementação — gatilhos reais, o que cada sistema preserva literalmente, como sinaliza ao usuário e como (ou se) audita a perda — é o trabalho da **rodada 2** do ROADMAP.

Enfileirado: estratégias de compactação em assistentes de execução longa · segmentação por evento × janela deslizante · padrões de isolamento por subagente · descarregamento de estado para fora da janela.
