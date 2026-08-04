# 15 — Ferramentas e Contexto Externo

> **Estado da arte capturado em 2026-08** · edição 0.1 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** O argumento (resultado de ferramenta é contexto) está fechado; o tratamento por protocolo e implementação é a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Tratar** resultado de ferramenta como item de orçamento de contexto, e não como efeito colateral;
2. **Projetar** a descrição e o schema de uma ferramenta pensando no custo que ela impõe à janela;
3. **Explicar** o que MCP padroniza e o que ele não resolve;
4. **Aplicar** as três defesas mínimas para conteúdo que entra no contexto vindo de fora.

## O problema

Um agente com ferramentas tem uma porta pela qual entra conteúdo que ninguém revisou, em volume que ninguém previu. Uma consulta a um banco pode devolver 40 mil tokens. Uma página web pode devolver instruções disfarçadas de conteúdo. Uma listagem de arquivos pode encher a janela com ruído irrelevante.

O erro conceitual que causa quase todos os problemas deste capítulo: tratar a chamada de ferramenta como **ação** e esquecer que o resultado é **contexto**. Ele ocupa orçamento (cap. 08), pode conter instrução (cap. 17), e permanece no histórico consumindo espaço em todos os turnos seguintes até alguém compactá-lo (cap. 14).

Há ainda um custo que precede a chamada: **as definições das ferramentas também ocupam contexto**, em toda requisição. Vinte ferramentas com descrições generosas são um bloco fixo caro, pago mesmo quando nenhuma é usada.

## Fundamentos científicos

- **Raciocínio integrado a ferramentas** — o survey [arXiv 2507.13334](https://arxiv.org/abs/2507.13334) trata *tool-integrated reasoning* como uma das quatro implementações da engenharia de contexto, ao lado de RAG, memória e multiagente. Ferramenta não é anexo: é fonte de contexto de primeira classe. `[a validar]`
- **ReAct** — o padrão que formaliza a intercalação de raciocínio e ação, e portanto a entrada de observação externa no contexto. `[a validar]`
- **Injeção via ferramenta** — há trabalho específico sobre ferramentas de desenvolvimento assistido por IA e sua exposição a *prompt injection* ([arXiv 2603.21642](https://arxiv.org/abs/2603.21642)); a superfície nasce aqui e é tratada no cap. 17. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **MCP (Model Context Protocol)** — o protocolo que padronizou como um sistema expõe ferramentas, recursos e prompts a um modelo, com transporte e descoberta definidos. O ganho é real e é de **integração**: uma ferramenta escrita uma vez serve a qualquer cliente compatível. O que ele explicitamente **não** resolve: quanto contexto aquela ferramenta vai consumir, e se o que ela devolve é confiável.
- **Descrição de ferramenta como prompt** — a descrição e o schema são lidos pelo modelo em toda requisição. São, na prática, parte do prompt de sistema — e devem obedecer às regras do cap. 05 (enxuto, cresce por evidência de falha).
- **Divulgação progressiva** — a prática de anunciar capacidades por nome e descrição curta, carregando o detalhe só quando usado. Nasceu da pressão de orçamento e virou padrão de projeto.

## O estado da arte

### 1. Resultado de ferramenta é o pior concorrente do orçamento

Das cinco fontes que disputam a janela (cap. 08), esta é a única com três propriedades ruins ao mesmo tempo:

- **Tamanho imprevisível** no momento de pedir;
- **Conteúdo não revisado**, vindo de fora do sistema;
- **Persistência**, porque fica no histórico depois de usado.

As mitigações, em ordem de importância:

- **Teto por ferramenta, aplicado no lado do sistema.** Não peça ao modelo que "não traga muito"; trunque no adaptador, e diga explicitamente que truncou.
- **Resumir antes de inserir** quando o resultado é grande e o que importa é pouco. Uma chamada de resumo é mais barata que 30 mil tokens carregados por dez turnos.
- **Referência em vez de conteúdo.** Devolver um identificador e permitir que o modelo peça o detalhe se precisar — o just-in-time do cap. 12 aplicado a ferramentas.
- **Expirar do histórico.** Resultado de ferramenta antigo é o primeiro candidato à compactação (cap. 14), e raramente precisa sobreviver literal.

### 2. O custo fixo das definições

Antes de qualquer chamada, o catálogo de ferramentas já é pago:

- **Menos ferramentas, mais bem descritas** vence mais ferramentas mal descritas — em custo e em taxa de escolha correta.
- **Ferramentas por contexto de uso.** Expor só o que faz sentido no momento reduz o bloco fixo e a confusão do modelo.
- **Descrição orientada a decisão.** O que o modelo precisa saber é *quando* usar, não como a API funciona internamente. Descrição que ensina a distinguir de uma ferramenta parecida vale mais que descrição completa.
- **Snippet acoplado à definição.** Quando a orientação de uso vive junto da ferramenta, desligar a ferramenta remove a orientação — e prompt e capacidade nunca dessincronizam.

### 3. O que MCP padroniza — e o que não

**Padroniza:** o transporte, o formato de descoberta, o schema das ferramentas, a exposição de recursos e prompts, e o modelo de autorização. Isso resolve o problema de integração N×M, que era real e caro.

**Não padroniza, e continua sendo trabalho seu:**

- Quanto do orçamento aquele servidor vai consumir;
- Se o conteúdo devolvido é confiável — um servidor MCP externo é **fonte não confiável** por definição;
- O que acontece quando ele demora, falha ou devolve algo gigante;
- Quais ferramentas fazem sentido expor **juntas**.

A conclusão prática: adotar MCP resolve encanamento e não resolve engenharia de contexto. Um agente com trinta servidores MCP conectados tem um problema de orçamento e um problema de segurança, ambos novos.

### 4. As três defesas mínimas

Para todo conteúdo que entra pela porta das ferramentas (tratamento completo no cap. 17):

1. **Marcar a procedência.** O contexto deve deixar explícito que aquele bloco veio de fora e é dado, não instrução.
2. **Privilégio mínimo.** Uma ferramenta que só lê não deve poder escrever. A combinação perigosa é ler de fonte não confiável **e** ter ferramenta de efeito colateral no mesmo laço.
3. **Aprovação humana para o que é irreversível.** Nenhuma marcação de procedência é garantia; o que não pode ser desfeito precisa de confirmação.

### Leitura executiva

O erro que causa quase tudo neste capítulo é tratar a chamada de ferramenta como **ação** e esquecer que o resultado é **contexto** — que ocupa orçamento, pode conter instrução, e fica no histórico consumindo espaço em todos os turnos seguintes. É o pior concorrente da janela: tamanho imprevisível, conteúdo não revisado e persistente. **O que roubar:** teto por ferramenta aplicado **no adaptador** (não peça ao modelo que se contenha), resumir antes de inserir, devolver **referência em vez de conteúdo**, e expirar resultado antigo do histórico. **O custo que se esquece:** as *definições* das ferramentas são pagas em toda requisição — menos ferramentas bem descritas vencem muitas mal descritas, e a descrição deve ensinar **quando** usar, não como a API funciona. **Sobre MCP:** resolve o encanamento (integração N×M) e **não** resolve engenharia de contexto — um agente com trinta servidores conectados ganhou um problema de orçamento e um de segurança. **Mínimo inegociável:** marcar procedência, privilégio mínimo, e aprovação humana para o irreversível.

## Mão na massa — contexto-zero, etapa 14

Na etapa 14 o `contexto-zero` ganha ferramentas de verdade, com o adaptador fazendo o trabalho que o modelo não deve fazer: teto de tokens por ferramenta, truncamento anunciado, marcação de procedência no bloco de resultado, e contabilização do custo fixo do catálogo. O teste da etapa injeta uma ferramenta que devolve 50 mil tokens e prova que o orçamento da etapa 7 sobrevive. O exercício de completude: a política de expiração de resultados antigos vem esqueletada — você decide quando um resultado deixa de valer o espaço que ocupa.

## Verificação

1. Uma ferramenta de consulta devolve entre 200 e 40.000 tokens, imprevisivelmente. Descreva três mitigações e diga qual você aplica primeiro.
2. Por que adotar MCP não reduz, por si só, o custo de contexto do seu agente? O que exatamente ele resolve?
3. Qual combinação de ferramentas em um mesmo laço é perigosa, e por quê? (Dica: uma lê de fora.)

---

## Apêndice A — Como cada protocolo e implementação trata o contexto externo

> Tratamento por protocolo e implementação, com URL — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: o argumento (resultado é contexto) e o recorte do que MCP resolve estão descritos. O tratamento por implementação — como cada cliente aplica teto, o que faz com resultado grande, e como marca procedência — é o trabalho da **rodada 2** do ROADMAP.

Enfileirado: a especificação MCP (o que padroniza e o que deixa aberto) · padrões de divulgação progressiva de capacidades · práticas de truncamento e resumo de resultado · a superfície de injeção via ferramenta.
