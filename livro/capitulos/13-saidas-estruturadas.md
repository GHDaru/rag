# 13 — Saídas Estruturadas

> **Estado da arte capturado em 2026-08** · edição 0.2 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** O argumento está fechado; o comparativo entre modos de garantia (schema nativo × gramática × validação externa) é a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Distinguir** os três níveis de garantia de formato: pedir, restringir a decodificação, validar depois;
2. **Projetar** um schema que serve ao modelo, não só ao seu código;
3. **Implementar** o ciclo validar → reparar → repetir com limite, sem laço infinito;
4. **Avaliar** quando estruturar a saída degrada a qualidade do conteúdo — e o que fazer a respeito.

## O problema

Um sistema real não consome prosa: consome campos. E o ponto onde a maioria dos pipelines quebra em produção não é o raciocínio do modelo — é o `json.loads` que falha porque veio uma vírgula sobrando, uma cerca de markdown em volta, ou um campo com o nome quase certo.

O problema tem duas metades que costumam ser confundidas:

- **Sintática** — a saída é parseável e respeita o schema? Esta metade está essencialmente **resolvida** por funcionalidade de plataforma, e é onde este capítulo mais vai expirar.
- **Semântica** — os campos estão *corretos*? Um JSON perfeitamente válido com o valor errado passa em toda validação de formato e falha em produção. Esta metade não tem solução de plataforma: é eval (cap. 17) e fundamentação (cap. 21).

## Fundamentos científicos

- **Estruturar tem custo cognitivo para o modelo.** A literatura registra que impor formato rígido pode competir com a qualidade do conteúdo, especialmente quando a estrutura é pedida junto com raciocínio. A mitigação conhecida — deixar o raciocínio acontecer em campo próprio, antes dos campos de resposta — é prática convergente entre provedores. `[a validar]`
- **A assimetria compreensão × geração.** O survey de engenharia de contexto ([arXiv 2507.13334](https://arxiv.org/abs/2507.13334)) identifica como lacuna central da área o descompasso entre a capacidade dos modelos de **compreender** contexto complexo e a de **produzir** saída igualmente complexa. Saída estruturada longa é exatamente onde essa assimetria dói. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Saída estruturada nativa** — os três grandes provedores oferecem hoje conformidade a JSON Schema como garantia de plataforma (nomes variam: *structured outputs*, *response format*, *controlled generation*). É a mudança que aposentou uma geração inteira de prompts do tipo "responda APENAS com JSON, sem explicação".
- **Tool calling / function calling** — a mesma tecnologia, com outro nome e outro propósito: o schema da ferramenta é um contrato de saída estruturada. Quem entende os dois como a mesma coisa para de manter duas soluções.
- **Bibliotecas de decodificação restrita** — a linhagem de *constrained decoding* (gramáticas, autômatos sobre o vocabulário) que garante o formato **na amostragem**, e não depois. É a opção quando o modelo é aberto/local e não há garantia de plataforma.
- **Validação e reparo** — a prática dominante em produção continua sendo validar contra o schema e re-solicitar com a mensagem de erro anexada, porque nenhuma garantia cobre a metade semântica.

## O estado da arte

### 1. Três níveis de garantia — e eles não são alternativas

| Nível | Mecanismo | Garante | Não garante |
|---|---|---|---|
| **Pedir** | instrução + exemplo de formato no prompt | nada | nada |
| **Restringir** | schema nativo do provedor ou gramática na decodificação | sintaxe e forma | valores corretos |
| **Validar** | parse + validação de tipo/regra no seu código | o que você escreveu como regra | o que você não pensou em escrever |

O erro comum é tratá-los como escada onde o degrau de cima dispensa os de baixo. **Não dispensa**: mesmo com garantia nativa de schema, a validação semântica no seu lado continua obrigatória — o modelo pode preencher `"data_vencimento": "2019-02-30"` respeitando perfeitamente o tipo `string`.

A escada correta é: restrinja quando puder, valide sempre, e trate o "pedir" como documentação para o modelo — não como mecanismo.

### 2. Projetar o schema para o modelo, não só para o seu banco

Um schema que serve ao código pode ser péssimo para o modelo. Os padrões que a prática consolidou:

- **Campo de raciocínio primeiro.** Um campo textual livre (`analise`, `justificativa`) **antes** dos campos de decisão dá ao modelo o espaço de pensar que o cap. 12 discutiu, dentro do contrato. Ordem importa: os campos são gerados na ordem em que aparecem.
- **Enum em vez de string livre** para qualquer campo com domínio fechado. Elimina uma classe inteira de erro semântico sem custo.
- **Nomes que carregam a instrução.** `resumo_em_ate_3_frases` ensina mais que `resumo` com uma descrição que o modelo pode não priorizar.
- **Campo explícito de incerteza.** Sem um lugar para dizer "não encontrei", o modelo preenche. Este é o mesmo argumento da restrição de fallback do cap. 11, agora como estrutura.
- **Achatar o aninhamento.** Estrutura profunda é onde a assimetria compreensão × geração cobra caro. Duas chamadas com schemas rasos costumam superar uma com schema profundo.

### 3. O ciclo de reparo, e seu limite

O padrão de produção é: gerar → validar → se falhar, re-solicitar anexando o erro de validação → repetir até um teto pequeno (2 ou 3).

Duas regras que separam quem já apanhou disso de quem ainda vai apanhar:

- **Teto obrigatório e falha explícita.** Sem teto, um schema impossível de satisfazer vira laço infinito com fatura aberta. A falha após o teto deve ser um erro tratado, não um valor vazio silencioso.
- **Contar as tentativas como métrica.** A taxa de reparo é um indicador de saúde do schema. Se subiu, alguma coisa mudou — modelo, prompt ou dado de entrada. Este número pertence ao painel do cap. 21, não ao log.

### Leitura executiva

Duas metades: a **sintática** está resolvida por plataforma (schema nativo, decodificação restrita) e é onde este capítulo vai expirar; a **semântica** — o campo válido com o valor errado — não tem solução de plataforma e é eval (cap. 17) e fundamentação (cap. 21). **O que roubar:** restrinja quando puder, **valide sempre** (garantia de forma não é garantia de valor); ponha um campo de raciocínio antes dos campos de decisão, use enum em domínio fechado, e dê ao modelo um lugar explícito para dizer "não sei". **O sinal operacional:** monitore a **taxa de reparo** — ela é o termômetro do schema, e mudanças nela avisam antes de o usuário reclamar.

## Mão na massa — rag-zero, etapa 10 (o gerador)

Na etapa 10 você troca a resposta em texto livre do `rag-zero` por um contrato: schema com campo de raciocínio, enum de intenção e campo de incerteza; validação no lado do servidor; ciclo de reparo com teto 2 e falha explícita. O exercício de completude: o repórter de erro vem esqueletado — você faz a mensagem de validação virar uma instrução útil para a re-solicitação, e mede quanto isso muda a taxa de reparo.

## Verificação

1. Você ativou saída estruturada nativa com schema garantido pelo provedor. Que classe de erro **continua** possível, e onde ela deve ser pega?
2. Um schema com 4 níveis de aninhamento tem taxa de reparo de 18%. Cite duas mudanças de design de schema antes de considerar trocar de modelo.
3. Por que o campo de raciocínio precisa vir **antes** dos campos de decisão, e não depois?

---

## Apêndice A — Como cada fonte trata a saída estruturada

> Tratamento por mecanismo e por implementação, com URL — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: os três níveis de garantia estão mapeados e os mecanismos identificados. O tratamento comparado — o que cada provedor garante exatamente, o que a decodificação restrita custa em latência, e como as bibliotecas de validação se encaixam — é o trabalho da **rodada 2** do ROADMAP.

Enfileirado: modos de saída estruturada dos três grandes provedores (o que é garantia e o que é *best effort*) · bibliotecas de *constrained decoding* para modelos locais · frameworks de validação e reparo · a equivalência entre schema de ferramenta e schema de resposta.
