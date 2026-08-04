# 17 — Avaliação de Prompts

> **Estado da arte capturado em 2026-08** · edição 0.2 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** O argumento e a escada de métodos estão fechados; o tratamento por ferramenta é a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Construir** um conjunto de avaliação mínimo a partir de falhas reais, e não de casos imaginados;
2. **Escolher** o método de julgamento adequado ao tipo de saída (determinístico, por referência, por juiz);
3. **Reconhecer** e mitigar os vieses conhecidos do LLM-as-judge;
4. **Integrar** a avaliação ao ciclo de mudança, de modo que alterar prompt deixe de ser aposta.

## O problema

Quase todo time que trabalha com LLM tem a mesma história: alguém "melhorou o prompt", o time achou que ficou melhor, e ninguém consegue provar. Semanas depois, uma regressão em um caso que funcionava aparece em produção — e não há como saber quando quebrou.

A causa é que a saída é texto e texto não tem `assert` óbvio. A consequência é que a disciplina de engenharia inteira — versionar, testar, revisar, reverter — deixa de operar exatamente onde o comportamento do produto é decidido.

Este capítulo é o portão da Parte IV. Sem ele, o cap. 16 é perigoso e o cap. 12 é folclore.

## Fundamentos científicos

- **A escolha de técnica depende do domínio.** Estudos comparativos de variantes de CoT em domínios específicos mostram que o ranking das técnicas **muda com o domínio e o modelo** ([exemplo em QA médico](https://www.sciencedirect.com/science/article/pii/S0010482525009655)). É a evidência de que resultado publicado não transfere sem medição local. `[a validar]`
- **Juiz automático como método** — a prática de usar um modelo para julgar saídas de outro consolidou-se como padrão de fato nas ferramentas de avaliação (cap. 21), com um conjunto conhecido de vieses documentados: preferência por respostas longas, por respostas do próprio modelo, e sensibilidade à ordem de apresentação. `[a validar]`
- **Assimetria compreensão × geração** — [arXiv 2507.13334](https://arxiv.org/abs/2507.13334): a lacuna entre entender e produzir é onde as falhas aparecem, e por isso avaliar só a entrada (o prompt) sem avaliar a saída sob condições realistas subestima o problema. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Ferramentas de eval** — o ecossistema convergiu para um formato comum: casos + métricas + execução em CI. As mesmas ferramentas cobrem prompt e sistema de RAG (cap. 21), o que na prática significa que montar a infraestrutura uma vez serve às duas metades do livro.
- **Red teaming de prompt** — ferramentas de teste adversarial (por exemplo, [promptfoo](https://www.promptfoo.dev/docs/red-team/owasp-llm-top-10/)) tratam avaliação e segurança no mesmo pipeline, mapeando casos contra o OWASP LLM Top 10. A conexão com o cap. 22 é operacional, não temática.
- **A prática que separa os times** — não é a ferramenta: é a origem dos casos. Conjuntos construídos a partir de **falhas reais registradas** superam conjuntos escritos em mesa, porque contêm as ambiguidades que ninguém imaginaria.

## O estado da arte

### 1. A escada de métodos

Do mais barato e confiável ao mais caro e frágil — e a regra é subir só o necessário:

| Método | Como julga | Custo | Confiabilidade |
|---|---|---|---|
| **Asserção determinística** | regra sobre a saída (schema válido, campo presente, valor em enum, ausência de termo proibido) | ~0 | alta |
| **Comparação com referência** | contra uma resposta esperada (exato, ou por similaridade) | baixo | alta onde há resposta única |
| **Rubrica com juiz** | um modelo pontua contra critérios escritos | médio | média — enviesada |
| **Julgamento humano** | amostra revisada por pessoa | alto | alta, mas não escala |

O erro dominante é começar pelo terceiro degrau. Boa parte do que os times avaliam com juiz — "a resposta está em JSON?", "citou a fonte?", "respeitou o limite de frases?" — é asserção determinística disfarçada, mais barata e mais confiável.

**A regra prática:** todo critério que puder virar `assert` deve virar `assert`. O juiz é para o que sobrar.

### 2. Os vieses do juiz, e o que fazer com eles

Quando o juiz é necessário, os vieses conhecidos exigem mitigação explícita:

- **Preferência por comprimento** → normalizar ou penalizar comprimento na rubrica.
- **Preferência pelo próprio modelo** → usar como juiz um modelo de família diferente da que gerou.
- **Sensibilidade à ordem** (em comparação A/B) → alternar a ordem e agregar.
- **Rubrica vaga** → critérios binários e verificáveis ("cita ao menos uma fonte do contexto fornecido?") em vez de escalas subjetivas ("qualidade de 1 a 5").
- **Ausência de calibração** → medir a **concordância do juiz com humano** numa amostra, antes de confiar nele. Um juiz não calibrado é um número inventado com aparência de rigor.

Este último item é o que separa avaliação de teatro de avaliação.

### 3. O ciclo que torna a mudança segura

O que a avaliação precisa entregar não é um número: é a capacidade de **mudar sem medo**.

```
falha em produção ──► vira caso no conjunto ──► roda em CI a cada mudança
                                                  │
        mudança de prompt/modelo ──► compara ─────┘──► regressão bloqueia
```

Três propriedades que fazem esse ciclo funcionar:

- **Todo incidente vira caso.** É o mecanismo que faz o conjunto crescer com valor real, e o mesmo princípio da autoria de regras do cap. 14 ("cresce por evidência de falha").
- **Versionar prompt, modelo e conjunto juntos.** Um resultado só é interpretável se você sabe as três coisas. Comparar números de conjuntos diferentes é a forma mais comum de se enganar.
- **Rodar em CI, não sob demanda.** Avaliação que depende de alguém lembrar não existe.

### 4. O que ainda não está resolvido

- **Custo.** Avaliar em CI a cada mudança tem fatura. Estratégias de amostragem e níveis (rápido a cada commit, completo antes de release) são o padrão emergente, sem consenso sobre o corte.
- **Casos gerados sinteticamente.** Aumentam cobertura barato e trazem o risco de avaliar o modelo com o viés do modelo que gerou os casos.
- **Métricas de conversa, não de turno.** Quase toda a instrumentação existente mede uma resposta isolada; sistemas reais falham ao longo de muitos turnos (cap. 19). É a lacuna mais visível da área.

### Leitura executiva

Sem eval, mudar prompt é apostar — e este capítulo é o portão da Parte IV: sem ele o cap. 16 é perigoso e o cap. 12 é folclore. Suba a escada só o necessário: **todo critério que puder virar `assert` deve virar `assert`**; o juiz é para o que sobrar. **O que roubar:** monte o conjunto a partir de **falhas reais registradas** (não de casos imaginados), faça todo incidente virar caso, e versione prompt + modelo + conjunto **juntos** — número comparado entre conjuntos diferentes é auto-engano. **Se usar juiz:** modelo de outra família, critérios binários, ordem alternada, e **meça a concordância com humano** antes de confiar — juiz não calibrado é número inventado com aparência de rigor. **A lacuna aberta:** quase toda métrica mede um turno; os sistemas falham ao longo da conversa.

## Mão na massa — rag-zero, etapa 10 (o gerador)

Na etapa 10 você monta o conjunto de avaliação do `rag-zero` com 20 casos vindos das falhas que as etapas anteriores produziram, três asserções determinísticas, uma rubrica com juiz — e o passo que quase ninguém faz: **calibrar o juiz** contra 10 julgamentos seus e reportar a concordância. Se a concordância for baixa, a rubrica é reescrita antes de o número ser usado. O exercício de completude: o runner vem esqueletado; você implementa a comparação entre duas versões e o bloqueio por regressão.

## Verificação

1. Liste três critérios que seu time hoje avalia com juiz e que poderiam virar asserção determinística.
2. Um relatório mostra que o prompt B ganha do A por 6 pontos, com juiz da mesma família do modelo avaliado. Que dois ajustes você exige antes de aceitar o resultado?
3. Por que comparar dois números obtidos em conjuntos de avaliação diferentes é pior do que não medir?

---

## Apêndice A — Como cada ferramenta trata a avaliação de prompt

> Tratamento por ferramenta, com URL e método — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: a escada de métodos e os vieses do juiz estão descritos. O tratamento por ferramenta — o que cada uma mede, como executa em CI, e como lida com calibração — é o trabalho da **rodada 2**, e converge com o Apêndice A do cap. 21 (as ferramentas são, em grande parte, as mesmas).

Enfileirado: frameworks de eval com integração de CI · ferramentas de red teaming mapeadas ao OWASP LLM Top 10 · práticas de calibração de juiz · estratégias de amostragem para controlar custo.
