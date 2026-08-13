# 24 — Convergências e Tendências

> **Estado da arte capturado em 2026-08** · última revisão 2026-08-13 · [histórico e registro de expiração](HISTORICO.md)
>
> **Maturidade: esboço.** As convergências, as disputas e as apostas datadas estão registradas; a revisão do placar é a rodada 6 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Separar** o que já é consenso na disciplina do que ainda é disputa aberta;
2. **Avaliar** uma novidade da área contra o critério "isto resolve um problema ou compensa uma limitação?";
3. **Aplicar** a cláusula de expiração a um texto técnico qualquer desta área — inclusive a este livro.

## O problema

Um livro sobre uma disciplina em movimento tem duas obrigações opostas: ser útil agora e ser honesto sobre o quanto disso vai durar. Este capítulo resolve a tensão da única forma que funciona — **registrando apostas com data**, para que possam ser julgadas depois.

O que segue é dividido em três: o que a comunidade já resolveu, o que ainda disputa, e o que este livro aposta.

## O estado da arte

### 1. As convergências (o que já é consenso)

Cinco pontos em que a prática de 2026 concorda, e que este livro trata como assentados:

1. **O par prompt × contexto é uma disciplina só.** A separação entre "quem escreve prompt" e "quem monta pipeline" desapareceu. O sinal mais claro é editorial: o guia de referência da comunidade cobre prompt, contexto, RAG e agentes no mesmo índice.
2. **Mais contexto não é melhor contexto.** A degradação em contextos longos é fato medido, e curadoria supera volume. Isso encerrou o argumento de que janelas grandes tornariam a disciplina desnecessária.
3. **RAG não morreu, e não é a moldura.** É a técnica central para conhecimento externo, com três níveis de sofisticação, dentro de uma disciplina maior. A leitura híbrida — recuperar para reduzir, raciocinar em contexto longo sobre o que sobrou — é o padrão.
4. **Prompt sem eval é aposta.** A ideia de avaliar sistematicamente saiu do discurso e virou infraestrutura (ferramentas, CI, métricas nomeadas).
5. **Prompt injection é propriedade da arquitetura.** Deixou de ser tratada como bug corrigível. A defesa é de sistema (privilégio, aprovação), não de redação.

### 2. As disputas abertas (o que não está resolvido)

Cinco pontos onde não há consenso, e onde este livro registra a discordância em vez de fingir resposta:

1. **Onde para a janela e começa a recuperação.** O híbrido é consenso; o ponto de corte não é. Varia por modelo, forma do dado e orçamento de latência, e ninguém publicou a regra geral.
2. **Memória × recuperação.** A fronteira entre "isto é memória" e "isto é RAG sobre o histórico" continua decidida caso a caso, e as três arquiteturas dominantes (fatos, grafo temporal, paginação) não convergiram.
3. **Quanto de estrutura o prompt ainda precisa.** Marcação pesada foi prática dominante; há sinal de que modelos recentes precisam de menos. Ninguém mediu isso de forma transferível.
4. **Avaliação de trajetória e de conversa.** Toda a instrumentação madura mede um turno. Sistemas agênticos falham ao longo de trajetórias, e sistemas conversacionais ao longo de sessões. É a maior lacuna de ferramental da área.
5. **Quanto vale otimizar prompt automaticamente.** O ganho é publicado por benchmark e depende fortemente de tarefa. A adoção ainda é minoria, e a legibilidade perdida é um custo real que a literatura subestima.

### 3. As apostas deste livro (com data e veredito futuro)

Registradas para serem cobradas. O placar vive no [registro de expiração](HISTORICO.md).

| # | Aposta (feita em 2026-08) | Como se verifica | Prazo |
|---|---|---|---|
| A1 | **Grande parte do cap. 13 (saída estruturada, metade sintática) vira funcionalidade trivial de plataforma** e deixa de merecer capítulo próprio. | O capítulo encolhe para uma seção do cap. 11. | 2027-08 |
| A2 | **Orçamento explícito de contexto vira prática padrão**, com painel de composição por fonte tão comum quanto painel de latência hoje. | Ferramentas de observabilidade passam a trazê-lo pronto. | 2028-02 |
| A3 | **A otimização automática de prompt não substitui a escrita manual na maioria dos projetos** até 2028 — mas vira padrão em sistemas de alto volume. | Adoção reportada em levantamentos da comunidade. | 2028-08 |
| A4 | **Nenhuma defesa por prompt contra injeção indireta será considerada suficiente**; a defesa continuará sendo de privilégio e aprovação. | Recomendação vigente do OWASP. | 2028-08 |
| A5 | **A avaliação de trajetória/conversa deixa de ser lacuna** e ganha ferramenta madura de uso comum. | Existência de ferramenta adotada com métricas de sessão. | 2027-08 |
| A6 | **O rótulo "engenharia de contexto" perde força como termo de moda** e o conteúdo é absorvido por "engenharia de sistemas de IA" — sem que os problemas mudem. | Uso do termo na literatura e em vagas. | 2028-08 |

A aposta A6 merece nota: se ela se confirmar, o **título** deste livro expira antes do **conteúdo**. Isso é aceitável e até esperado — os problemas de orçamento, separação instrução×dado e medição são propriedades do problema, não do rótulo da vez.

### 4. Como aplicar a cláusula de expiração a qualquer texto da área

O critério que este livro usa, e que o leitor pode usar contra este livro:

- **A técnica compensa uma limitação do modelo?** Se sim, ela expira quando a limitação expirar. A maior parte da engenharia de prompt de 2023 morreu assim.
- **A técnica assume um preço ou um tamanho de janela?** Se sim, expira quando a economia mudar — e ela mudou de ordem de grandeza mais de uma vez.
- **A técnica resolve um problema de informação?** (o que o modelo não sabe, o que não cabe, o que não pode ser confiado) Se sim, provavelmente **não** expira: muda de forma, não de existência.

### Leitura executiva

**Consenso:** o par prompt × contexto é uma disciplina só; mais contexto não é melhor contexto; RAG não morreu e não é a moldura; prompt sem eval é aposta; injeção é propriedade da arquitetura. **Disputa aberta:** o ponto de corte entre janela e recuperação, a fronteira memória × RAG, quanta estrutura o prompt ainda precisa, avaliação de trajetória e de conversa (a maior lacuna de ferramental), e quanto vale otimizar prompt automaticamente. **O que roubar:** o critério de expiração — técnica que **compensa limitação de modelo** morre com a limitação; técnica que **assume um preço ou uma janela** morre com a economia; técnica que resolve **problema de informação** muda de forma, não de existência. Aplique-o a este livro também: as seis apostas da tabela acima estão datadas de propósito, e uma delas prevê que o próprio título expire antes do conteúdo.

## Verificação

1. Escolha uma técnica que você usa hoje e classifique-a com o critério da seção 4. Ela expira?
2. Qual das cinco disputas abertas mais afeta o seu sistema, e que experiência própria você teria para contribuir?
3. Se a aposta A6 se confirmar, o que exatamente deste livro continua válido? Justifique com dois capítulos.
