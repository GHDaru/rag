# 17 — Custo, Latência e Cache

> **Estado da arte capturado em 2026-08** · edição 0.1 (esqueleto) · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** A economia do contexto e as alavancas estão fechadas; os números por provedor e o Apêndice A são a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Decompor** o custo de uma requisição nas suas parcelas, e identificar qual domina;
2. **Explicar** o cache por prefixo e por que ele transforma ordem de montagem em decisão financeira;
3. **Escolher** entre as alavancas de redução conhecendo o que cada uma sacrifica;
4. **Instrumentar** qualidade e custo lado a lado, de modo que nenhuma decisão seja tomada com metade da informação.

## O problema

Sistemas de contexto degradam economicamente de forma silenciosa. Cada melhoria acrescenta tokens: mais uma regra no prompt de sistema, um `top_k` maior, mais uma ferramenta no catálogo, memória que cresce com o relacionamento. Nenhuma delas parece cara sozinha. Somadas, multiplicam a fatura por um fator que ninguém decidiu.

E há a assimetria que engana: **contexto é pago em toda requisição, para sempre.** Uma linha acrescentada ao prompt de sistema custa o produto do seu tamanho pelo número de chamadas do sistema, até alguém removê-la. Quase ninguém calcula esse produto antes de acrescentar.

Este é o capítulo que fecha a Parte III porque é o que impõe realidade às decisões dos dezesseis anteriores.

## Fundamentos científicos

- **Eficiência como problema aberto** — os surveys da área listam **eficiência** entre os desafios não resolvidos, ao lado de avaliação, coordenação e governança. Não é um detalhe de implantação: é uma restrição de projeto reconhecida. `[a validar]`
- **Servir agentes de horizonte longo** — há trabalho recente sobre atendimento eficiente de agentes de longa duração, com engenharia de contexto antecipatória ([arXiv 2607.00151](https://arxiv.org/abs/2607.00151)), sinalizando que a otimização de custo/latência está virando disciplina própria. `[a validar]`
- **A justificativa técnica do cache** — a inferência processa um prefixo e, para prefixos idênticos já vistos, o estado intermediário pode ser reutilizado. É o que torna o cache por prefixo possível, e o que torna a **ordem** de montagem economicamente relevante. `[a validar]`

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **Cache por prefixo** — oferecido pelos grandes provedores com desconto substancial sobre os tokens de entrada que repetem um prefixo já visto, e com ganho de latência. As regras variam (tamanho mínimo, tempo de vida, como se marca o ponto de corte), mas o princípio é universal: **o desconto vale até o primeiro token que muda.**
- **Cache hit rate como métrica de primeira classe** — a prática relatada por quem opera assistentes em produção é tratar a taxa de acerto do cache como indicador operacional, monitorado como qualquer outro, e não como otimização eventual.
- **Os invalidadores clássicos** — timestamp no topo do prompt, identificador aleatório na lista de ferramentas, reserialização não determinística do histórico (um mapa de chaves que muda de ordem). São bugs de custo que não aparecem em nenhum teste funcional.

## O estado da arte

### 1. A decomposição do custo

| Parcela | Cresce com | Cacheável? | Quem esquece |
|---|---|---|---|
| Prompt de sistema e ferramentas | releases, incidentes | **sim**, se estável | quase todos |
| Memória recuperada | tempo de relacionamento | parcialmente | quase todos |
| Trechos recuperados | `top_k` × tamanho do chunk | raramente | ninguém — é o que se otimiza |
| Histórico | turnos | por prefixo, se não reescrito | quase todos |
| Resultado de ferramenta | imprevisível | não | todos |
| Tokens de saída | verbosidade, raciocínio | não | quem compra raciocínio sem medir |

O padrão da coluna "quem esquece" é a mensagem: a atenção vai para a parcela que é fácil de ver (`top_k`) e não para as que dominam a conta em sistemas de conversa longa — o prompt fixo pago em toda chamada e o histórico que cresce.

### 2. Cache por prefixo: a ordem é dinheiro

O cache vale do início do contexto até o primeiro token que difere. Isso converte a arquitetura de camadas do cap. 05 em decisão financeira direta:

```
estável   → identidade, política, ferramentas    ─┐ cacheável
semi      → regras do projeto                     │
volátil   → estado, memória, tarefa do turno     ─┘ recalculado
```

Três consequências práticas:

- **Nada volátil acima de algo estável.** O timestamp no topo é o erro mais caro e mais comum da área — invalida o prompt inteiro, em toda requisição.
- **Serialização determinística.** Se a mesma informação pode ser serializada de duas formas (ordem de chaves, espaçamento), o cache quebra sem que nada tenha mudado de fato.
- **Acrescentar, não reescrever.** Histórico que cresce por acréscimo mantém o prefixo; histórico reserializado a cada turno perde tudo.

### 3. As alavancas, e o que cada uma sacrifica

| Alavanca | Reduz | Sacrifica |
|---|---|---|
| Estabilizar o prefixo | custo de entrada, latência | nada — é a primeira, sempre |
| `top_k` menor + reranking | tokens de recuperado | recall, se o reranking não compensar |
| Resumir resultado de ferramenta | tokens e persistência | detalhe literal |
| Compactar mais cedo | custo do histórico | detalhe da conversa (cap. 13) |
| Modelo menor por etapa | custo por token | qualidade, de forma desigual por etapa |
| Cache de resposta | tudo, quando repete | frescor |

A primeira linha é gratuita: estabilizar o prefixo não sacrifica nada. É por isso que ela vem antes de qualquer discussão sobre trocar de modelo — e é por isso que "reordenar o prompt" é a otimização de maior retorno e menor risco deste livro.

A penúltima merece um alerta: usar modelo menor por etapa (classificar, reescrever consulta, resumir) funciona bem em algumas etapas e mal em outras, e a diferença **não é intuitiva**. Exige medição por etapa (cap. 15), não por sistema.

### 4. Instrumentar custo e qualidade juntos

A regra que fecha o livro: **nenhuma métrica de qualidade deve ser reportada sem o custo ao lado.**

Um painel mínimo:

- Custo médio por requisição, **decomposto por parcela**;
- Taxa de acerto do cache;
- Latência p50 e p95 (a p95 é onde os laços do cap. 11 aparecem);
- Qualidade (cap. 15) na mesma tela.

Sem isso, toda decisão de arquitetura é tomada com metade da informação — e a metade que falta é a que aparece na fatura três meses depois, quando ninguém lembra qual mudança a causou.

### Leitura executiva

Contexto é pago **em toda requisição, para sempre**: uma linha acrescentada ao prompt de sistema custa o seu tamanho vezes o número de chamadas, até alguém removê-la — e quase ninguém calcula esse produto antes de acrescentar. **O que roubar, e é grátis:** **estabilizar o prefixo**. O cache vale do início até o primeiro token que difere, então nada volátil acima de algo estável (o timestamp no topo é o erro mais caro e mais comum da área), serialização determinística, e histórico que **cresce por acréscimo** em vez de ser reserializado. É a única alavanca que não sacrifica nada — vem antes de qualquer conversa sobre trocar de modelo. **Onde a atenção erra:** vai para o `top_k`, que é fácil de ver, e não para o prompt fixo e o histórico, que dominam a conta em conversas longas. **A regra que fecha o livro:** nenhuma métrica de qualidade deve ser reportada sem o **custo ao lado** — decomposto por parcela, com taxa de acerto do cache e latência p95 na mesma tela.

## Mão na massa — contexto-zero, etapa 16

Na etapa 16 você fecha a construção: o contador da etapa 0 vira painel. Custo por parcela, taxa de acerto do cache antes e depois de reordenar as camadas, latência p50/p95 com e sem o laço agêntico da etapa 10 — e as métricas de qualidade da etapa 14 na mesma tela. O entregável é a tela, não o código. O exercício de completude: a detecção de invalidação de cache vem esqueletada — você implementa o alerta que dispara quando a taxa cai, e descobre, ao rodar, que o seu próprio sistema tinha um invalidador escondido.

## Verificação

1. Seu prompt de sistema tem 3.000 tokens e o sistema faz 500 mil chamadas por mês. Estime a ordem de grandeza do custo dessa decisão e diga o que a mudaria de graça.
2. Uma equipe adiciona um identificador único de requisição no início do contexto "para rastreabilidade". Qual é o custo escondido, e onde o identificador deveria ficar?
3. Por que reportar ganho de qualidade sem custo ao lado é uma decisão pela metade? Dê um exemplo em que a decisão se inverteria.

---

## Apêndice A — Como cada provedor e sistema trata o custo do contexto

> Tratamento por provedor e implementação, com regra de cache e medição — complementação online, expandida a cada rodada.

**Rodada 1 (edição 0.1)**: a economia do contexto e as alavancas estão descritas. O tratamento por provedor — regras exatas de cache (mínimo, tempo de vida, marcação), descontos vigentes e como cada um mede — é o trabalho da **rodada 2** do ROADMAP, com a ressalva do Princípio IV: esta é a seção do livro com maior taxa de expiração.

Enfileirado: regras de cache por prefixo dos provedores · práticas de monitoramento de taxa de acerto · roteamento por modelo e por etapa · a economia comparada entre indexar e encher a janela (cap. 08).
