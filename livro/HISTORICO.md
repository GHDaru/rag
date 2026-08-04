# Histórico e Registro de Expiração

> O livro é vivo (Princípio IV): toda edição é datada, registrada e **atribuída** — inclusive quanto ao modelo de IA usado, porque saídas de LLM não são determinísticas e a rastreabilidade é parte do rigor.
>
> Esta página tem duas metades: o **histórico de edições** (o que mudou, quando, por quem) e o **registro de expiração** (o placar das apostas do cap. 18 — previsões feitas com data, para serem cobradas depois).

## Histórico de edições

### Edição 0.1 — 2026-08-04 · Fundação: o esqueleto das duas disciplinas

**O que é.** A primeira versão pública do livro. Estabelece a moldura (prompt × contexto, com RAG dentro da segunda), o sumário completo em três partes, os 19 capítulos com esqueleto e explicação de abertura, o catálogo de técnicas, o mapa do ecossistema e o glossário.

**O que foi feito:**
- **Constituição 2.0.0** — derivada da 1.2.0 do livro *Engenharia de Harness* (mesmo método pedagógico e editorial, domínio novo). Princípio II reescrito: a fonte-base deixa de ser "o código de harnesses" e passa a ser **paper + implementação pública**. Princípio VIII criado: fixa a moldura do par e o lugar do RAG.
- **Levantamento da comunidade** — [panorama](https://github.com/GHDaru/rag/blob/main/estudos/2026-08-03-panorama-comunidade.md) cruzando academia (surveys estruturantes), repositórios públicos, frameworks e técnicas, e respondendo à pergunta que originou o projeto ("engenharia de contexto substitui RAG?" — não como substituto, como moldura).
- **Sumário em três partes** — Parte I (Engenharia de Prompt, caps. 02–07), Parte II (Engenharia de Contexto, caps. 08–14, com RAG em três capítulos), Parte III (o sistema em produção, caps. 15–17), mais abertura (00–01) e fechamento (18).
- **Aparato** — catálogo de técnicas, apêndice do ecossistema, glossário, bibliografia com status de validação, grafo do livro.
- **Motor de publicação** adaptado: PT-only, sem Radar, com o grafo remapeado para o novo domínio.

**Fora do escopo, por decisão explícita:** edição em inglês, Radar de atualização automática, benchmark quantitativo de frameworks, e a trilha prática `contexto-zero` (descrita nos capítulos, implementada na rodada 3). Ver [ROADMAP](https://github.com/GHDaru/rag/blob/main/ROADMAP.md).

**Estado da evidência (honestidade obrigatória, Princípio I):** **nenhuma referência tem status ✓ nesta edição.** Todas estão marcadas ⏳ na [bibliografia](bibliografia.md) e `[a validar]` nos capítulos. Os capítulos declaram maturidade "esboço" ou "fundação" no cabeçalho. A validação é a rodada 2.

**Atribuição:** direção editorial e decisões — Gilsiley Henrique Darú. Pesquisa, estruturação e redação assistidas por **Claude (Anthropic)**, modelo Opus 5, em sessão de 2026-08-03/04. Levantamento por busca aberta na web, sem acesso a bases pagas.

---

## Registro de expiração

O placar das apostas registradas no [cap. 18](18-convergencias.md). Uma aposta só vale se puder ser julgada — por isso cada uma tem critério de verificação e prazo.

| # | Aposta | Feita em | Prazo | Critério | Veredito |
|---|---|:---:|:---:|---|:---:|
| A1 | A metade sintática da saída estruturada (cap. 04) vira funcionalidade trivial e o capítulo encolhe para uma seção do cap. 02 | 2026-08 | 2027-08 | o capítulo é fundido | ⏳ aberta |
| A2 | Orçamento explícito de contexto vira prática padrão, com painel de composição por fonte | 2026-08 | 2028-02 | ferramentas de observabilidade trazem pronto | ⏳ aberta |
| A3 | Otimização automática de prompt **não** substitui a escrita manual na maioria dos projetos, mas vira padrão em alto volume | 2026-08 | 2028-08 | adoção reportada em levantamentos | ⏳ aberta |
| A4 | Nenhuma defesa por prompt contra injeção indireta será considerada suficiente | 2026-08 | 2028-08 | recomendação vigente do OWASP | ⏳ aberta |
| A5 | Avaliação de trajetória/conversa deixa de ser lacuna e ganha ferramenta madura | 2026-08 | 2027-08 | ferramenta adotada com métricas de sessão | ⏳ aberta |
| A6 | O rótulo "engenharia de contexto" perde força e o conteúdo é absorvido por "engenharia de sistemas de IA" | 2026-08 | 2028-08 | uso do termo na literatura e em vagas | ⏳ aberta |

**Como o placar é fechado:** na revisão de cada prazo (rodada 6 e seguintes), cada aposta recebe ✅ (confirmada), ❌ (refutada) ou 🔄 (ainda indefinida, com novo prazo). **Aposta refutada não é apagada** — é o registro mais valioso desta página, porque mostra onde o livro errou e por quê.

## Três datas, sempre distintas

O livro distingue rigorosamente (Princípio IV):

- **Data do evento** — quando a coisa descrita aconteceu (o paper foi publicado, a funcionalidade foi lançada).
- **Data de captura** — quando este livro olhou para aquilo. É a data no cabeçalho de cada capítulo.
- **Data da rodada** — quando a revisão sistemática aconteceu. É a data desta página.

Confundir as três é o erro que faz um livro técnico parecer atual quando não é.
