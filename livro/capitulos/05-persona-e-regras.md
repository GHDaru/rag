# 05 — Prompt de Sistema, Persona e Regras

> **Estado da arte capturado em 2026-08** · edição 0.1 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** A arquitetura em camadas e a separação voz × política estão fechadas; o tratamento por implementação é a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Ordenar** o prompt de sistema em camadas por volatilidade, e explicar o motivo econômico dessa ordem;
2. **Separar** voz (persona) de política (regras) — e justificar por que misturá-las apodrece o sistema;
3. **Projetar** uma cascata de regras com precedência declarada;
4. **Aplicar** a disciplina de autoria: a regra entra por evidência de falha reincidente, não por antecipação.

## O problema

O prompt de sistema é o único bloco do contexto que está em **toda** chamada. Isso faz dele, simultaneamente, o lugar mais valioso e o mais perigoso do sistema: cada linha ali é paga em todas as requisições, para sempre, e compete com o conteúdo que resolve a tarefa do usuário.

Na prática ele apodrece de forma previsível. Começa enxuto, recebe uma regra a cada incidente, ninguém remove nada, e em seis meses é um documento de 200 linhas onde metade das regras se contradiz e ninguém sabe qual ainda importa. O capítulo é sobre impedir isso por construção.

Sub-problemas: onde vivem as regras e como são descobertas; se o prompt deve variar por modelo; como mudar estado no meio de uma conversa sem destruir o cache.

## Fundamentos científicos

- **Posição e volume degradam** — *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)) sustenta que um prompt de sistema crescente não é neutro: ele empurra conteúdo relevante para a zona de pior aproveitamento. Crescer o bloco de regras tem custo de qualidade, além do custo de token. `[a validar]`
- **Gestão de contexto como componente** — o survey [arXiv 2507.13334](https://arxiv.org/abs/2507.13334) trata organização e compressão do contexto como componente de primeira classe, e não como higiene. A camada de sistema é o caso mais simples e mais ignorado desse componente. `[a validar]`
- **Deriva de persona** — há linha de pesquisa recente sobre detecção de *persona drift* em agentes de produção (a identidade declarada erodindo ao longo de conversas longas), o que dá suporte empírico à separação entre voz e política. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Cache por prefixo** — a mecânica que decide a ordem das camadas: provedores cobram menos (e respondem mais rápido) por tokens que repetem um **prefixo já visto**. Qualquer conteúdo volátil no topo invalida tudo abaixo dele. O tratamento completo é o cap. 17; aqui entra como restrição de arquitetura.
- **[AGENTS.md](https://agents.md/)** — o "README para agentes" convergiu como formato portável de regras de projeto, com governança neutra e adoção ampla. A lição transferível para qualquer sistema: regras versionadas, próximas do que descrevem, em formato aberto.
- **Hierarquia de instruções** — os provedores treinam precedência entre camadas (sistema > desenvolvedor > usuário > conteúdo externo). A montagem deve refletir essa hierarquia; contrariá-la é pedir comportamento indefinido.

## O estado da arte

### 1. Camadas por volatilidade

O prompt de sistema maduro é montado em camadas ordenadas do mais estável para o mais volátil:

```
[1] identidade e política     ← muda em release        ─┐
[2] capacidades e ferramentas ← muda em release         │ prefixo cacheável
[3] regras do domínio/projeto ← muda em dias             ┘
[4] estado do ambiente        ← muda por sessão
[5] tarefa atual              ← muda por turno
```

A ordem não é organizacional, é **econômica**: tudo abaixo do primeiro token que muda deixa de ser cacheável. Um timestamp no topo — o erro clássico — custa o cache do prompt inteiro, em toda requisição. A regra prática cabe em uma linha: **nada volátil acima de algo estável**.

### 2. Voz não é política

A distinção que mais rende a médio prazo:

| | Persona (voz) | Regras (política) |
|---|---|---|
| Responde | *como* falar | *o que* pode e não pode |
| Quem edita | produto, marca | engenharia, jurídico, segurança |
| Como falha | soa errado | faz errado |
| Testável por | julgamento, amostra | asserção, caso de teste |

Misturadas no mesmo bloco, as duas se degradam: a política vira sugestão de tom ("seja cuidadoso com dados sensíveis") em vez de restrição verificável, e a voz vira lista de proibições que deixa o assistente ríspido. Separadas — arquivos distintos, blocos distintos, donos distintos — cada uma pode ser testada pelo método que lhe cabe.

E há um argumento de segurança: **política que não é verificável não é política** (cap. 16). Se a regra existe só como frase no prompt e não tem contraparte no que as ferramentas permitem, ela é uma preferência.

### 3. Cascata com precedência declarada

Regras vêm de lugares diferentes — o produto, o projeto, a pasta, o usuário. O padrão consolidado é a **cascata**: global → projeto → subpasta → pessoal, com o mais próximo vencendo, a precedência escrita e o nível pessoal fora do versionamento.

O que a prática ensinou sobre autoria, e que vale como regra editorial do próprio arquivo:

- **Comece pequeno.** Dezenas de linhas, não centenas.
- **Comandos exatos antes de prosa.** O que é executável vale mais que o que é explicado.
- **Cresça por evidência de falha reincidente.** A regra entra quando o sistema errou a mesma coisa duas vezes — não quando alguém imaginou que poderia errar. É a diferença entre um arquivo de regras e um documento morto.
- **E encolha.** Nenhuma equipe tem processo para *remover* regra. Sem isso, a cascata vira sedimento.

### 4. As fronteiras novas

- **Prompt por família de modelo.** Manter variantes por modelo melhora resultado e multiplica manutenção. A fronteira é a mesma de sempre: quanto de duplicação vale quanto de ganho — e ninguém tem a resposta geral.
- **Prompt derivado do que está ativo.** Em vez de um bloco fixo, cada capacidade contribui seu trecho; desligar a capacidade encolhe o prompt. Impede a dessincronia entre o que o prompt promete e o que o sistema faz.
- **Mudança de estado sem quebrar o prefixo.** Informar ao modelo que algo mudou no meio de uma conversa longa, sem reescrever o topo — resolvido com fronteiras de turno seguras e mensagens de sistema tardias, em vez de reserialização.

### Leitura executiva

O prompt de sistema está em **toda** chamada — é o bloco mais caro do sistema e o que mais apodrece. Monte-o em **camadas por volatilidade** (identidade → capacidades → regras → ambiente → tarefa), porque tudo abaixo do primeiro token que muda deixa de ser cacheável: **nada volátil acima de algo estável**. **O que roubar:** separe **voz** de **política** em blocos e donos distintos — a primeira se testa por julgamento, a segunda por asserção; e adote a cascata com precedência declarada. **A disciplina que salva o arquivo:** a regra entra por **evidência de falha reincidente** e sai quando não se justifica mais — sem processo de remoção, toda cascata vira sedimento. **A regra de segurança:** política sem contraparte no que as ferramentas permitem é preferência, não política.

## Mão na massa — contexto-zero, etapa 4

Na etapa 4 você separa o prompt do `contexto-zero` em cinco camadas ordenadas, com `SOUL`/persona e `REGRAS`/política em arquivos distintos, e implementa a descoberta em cascata. O teste que fecha a etapa prova **estabilidade de prefixo**: dois turnos consecutivos produzem exatamente os mesmos bytes até a última mensagem. O exercício de completude: a função de precedência vem esqueletada — você decide e implementa quem vence, e escreve a regra por extenso no arquivo.

## Verificação

1. Seu prompt de sistema começa com a data de hoje, "para o modelo se situar". Estime o que isso custa e proponha onde a data deveria ficar.
2. Um sistema tem a regra "nunca revele dados de outro cliente" apenas no prompt. Por que isso não é uma política, segundo este capítulo? O que faltaria?
3. O arquivo de regras do seu projeto tem 180 linhas. Descreva um critério objetivo para decidir o que remover.

---

## Apêndice A — Como cada fonte trata a camada de sistema

> Tratamento por implementação e por formato, com URL — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: a arquitetura em camadas e a cascata estão descritas a partir da prática convergente. O tratamento por implementação — como cada sistema real ordena as camadas, onde coloca a fronteira de cache, e como resolve precedência — é o trabalho da **rodada 2** do ROADMAP.

Enfileirado: o formato AGENTS.md e a governança do padrão · documentação de cache por prefixo dos provedores · a separação persona × regras em agentes pessoais de código aberto · estratégias de atualização de estado mid-conversation.
