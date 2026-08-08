# Engenharia de RAG — O Livro

> Um livro aberto, em português, sobre **como se constrói um sistema em volta da recuperação da informação**. Do corpus à resposta fundamentada.

**Edição 0.2** · captura em 2026-08 · [Histórico](livro/HISTORICO.md) · [ROADMAP](ROADMAP.md) · **[ler online](https://ghdaru.github.io/rag/)**

## A aposta deste livro

Existe muito material sobre *técnicas* de RAG — chunking, embeddings, reranking, HyDE, GraphRAG — cada uma explicada isoladamente, nenhuma situada. O leitor acumula peças e não recebe a máquina.

Este livro faz a aposta contrária: **RAG é um sistema com componentes, contratos e topologias**, e a decisão que importa quase nunca é "qual técnica", é *onde ela encaixa e o que custa*.

Por isso ele abre com dois capítulos que quase nenhum material tem — a [anatomia do sistema](livro/capitulos/02-anatomia-do-sistema.md) e as [arquiteturas de referência](livro/capitulos/03-arquiteturas-de-referencia.md) — e por isso **cada capítulo de técnica declara qual componente aprofunda**.

O nome é cunhagem nossa, como foi "Engenharia de Harness" no [livro irmão](https://github.com/GHDaru/harness_engineering). Não existe "Engenharia de RAG" consagrada: existe **RAG**, o termo universal, e existe *Information Retrieval*, o campo de 60 anos que o absorveu (há track de RAG no TREC).

## O livro

### Abertura
| | |
|---|---|
| [00 — Introdução](livro/00-introducao.md) | Por que RAG, o que ele **não** resolve, e o que é engenharia aqui |
| [01 — Fundamentos](livro/01-fundamentos.md) | Vocabulário, a herança de IR, a taxonomia por sintoma |

### Parte I — A arquitetura
| | |
|---|---|
| [02 — Anatomia de um Sistema de RAG](livro/capitulos/02-anatomia-do-sistema.md) | Dois caminhos, 16 componentes, e os contratos entre eles |
| [03 — Arquiteturas de Referência](livro/capitulos/03-arquiteturas-de-referencia.md) | Naive → Advanced → Modular → Agêntico, e os padrões de fluxo |

### Parte II — O corpus
| | |
|---|---|
| [04 — Ingestão e Governança](livro/capitulos/04-corpus.md) | O teto de tudo que vem depois |
| [05 — Chunking e Representação](livro/capitulos/05-chunking-e-representacao.md) | As duas decisões mais caras de reverter |

### Parte III — Recuperação
| | |
|---|---|
| [06 — Busca: Esparsa, Densa e Híbrida](livro/capitulos/06-busca.md) | Dois modos de errar, espelhados |
| [07 — Reranking](livro/capitulos/07-reranking.md) | Recuperar barato, reordenar caro — e usar a nota |
| [08 — Entendimento da Consulta](livro/capitulos/08-entendimento-da-consulta.md) | Quando o problema está na pergunta |
| [09 — Recuperação Avançada](livro/capitulos/09-recuperacao-avancada.md) | Contextual retrieval × late chunking: a conta |
| [10 — Recuperação Estruturada](livro/capitulos/10-recuperacao-estruturada.md) | Multi-hop e pergunta global: RAPTOR, grafo, SQL |

### Parte IV — Geração
| | |
|---|---|
| [11 — Anatomia de um Prompt](livro/capitulos/11-anatomia-do-prompt.md) · [12 — Técnicas de Raciocínio](livro/capitulos/12-tecnicas-de-raciocinio.md) · [13 — Saídas Estruturadas](livro/capitulos/13-saidas-estruturadas.md) · [14 — Persona e Regras](livro/capitulos/14-persona-e-regras.md) | Engenharia de prompt, a serviço da geração |
| **[15 — Geração Fundamentada](livro/capitulos/15-geracao-fundamentada.md)** | **O "G" do RAG: grounding, citação verificável, abstenção** |
| [16 — Otimização Automática](livro/capitulos/16-otimizacao-de-prompts.md) · [17 — Avaliação de Prompts](livro/capitulos/17-avaliacao-de-prompts.md) | Do artesanato ao compilador; e como saber se melhorou |

### Parte V — O sistema em produção
| | |
|---|---|
| [18 — RAG Agêntico](livro/capitulos/18-rag-agentico.md) | Quando o modelo decide se, quando e como buscar |
| [19 — RAG Conversacional](livro/capitulos/19-rag-conversacional.md) | Referência, repetição e o que persiste entre sessões |
| [20 — A Janela como Orçamento](livro/capitulos/20-janela-como-orcamento.md) | Quanto do contexto vale gastar com o recuperado |
| [21 — Avaliação e Observabilidade](livro/capitulos/21-avaliacao-e-observabilidade.md) | As quatro métricas e a **tabela de diagnóstico** |
| [22 — Segurança do Corpus](livro/capitulos/22-seguranca-do-corpus.md) | Quem escreve no índice escreve no contexto do modelo |
| [23 — Custo, Latência e Cache](livro/capitulos/23-custo-latencia-cache.md) | A conta do RAG, e onde ela vaza |

### Fechamento e aparato
[24 — Convergências e Tendências](livro/24-convergencias.md) · [Catálogo de técnicas](livro/apendice-tecnicas.md) · [Ecossistema](livro/apendice-ecossistema.md) · [Glossário](livro/glossario.md) · [Bibliografia](livro/bibliografia.md) · [Histórico](livro/HISTORICO.md) · [Guia Editorial](livro/GUIA-EDITORIAL.md)

## Por onde começar

Não pelo sumário — pela **tabela de sintomas** do [cap. 01](livro/01-fundamentos.md), com o seu problema real na mão:

| Sintoma | Onde ler |
|---|---|
| Cita documento revogado | [04](livro/capitulos/04-corpus.md) |
| Não encontra código, sigla, identificador | [06](livro/capitulos/06-busca.md) |
| Traz o trecho certo sem contexto suficiente | [05](livro/capitulos/05-chunking-e-representacao.md), [09](livro/capitulos/09-recuperacao-avancada.md) |
| Traz relevante e irrelevante junto | [07](livro/capitulos/07-reranking.md) |
| Degrada da terceira pergunta em diante | [08](livro/capitulos/08-entendimento-da-consulta.md), [19](livro/capitulos/19-rag-conversacional.md) |
| "Quais os temas de tudo isso?" | [10](livro/capitulos/10-recuperacao-estruturada.md) |
| Recupera certo e responde errado | [15](livro/capitulos/15-geracao-fundamentada.md) |
| Piorou e ninguém sabe quando | [21](livro/capitulos/21-avaliacao-e-observabilidade.md) |
| Funciona e custa demais | [23](livro/capitulos/23-custo-latencia-cache.md) |

## Estado desta edição (honestidade obrigatória)

- **42 das 55 referências com status ✓ (76%)** na [bibliografia](livro/bibliografia.md). A [rodada 2](ROADMAP.md) conferiu **todos os 49 identificadores arXiv** contra o arXiv real (nenhum inventado), leu as fontes, e **corrigiu quatro afirmações do livro** — duas delas na espinha de um capítulo. As 13 restantes são de menor peso estrutural e seguem `[a validar]`.
- **Falta preencher os Apêndices A** dos capítulos (tratamento por implementação). É o item aberto do critério de conclusão da rodada 2.
- **Os Apêndices A** (tratamento por implementação) estão enfileirados, não escritos.
- **Nenhum número de terceiro** entra no corpo sem a condição experimental ao lado.
- **A trilha prática `rag-zero`** está descrita capítulo a capítulo, e é construída na rodada 3.

Fora do escopo por decisão: inglês, Radar de atualização, benchmark quantitativo.

## Como o livro é feito

Método na [constituição](.specify/memory/constitution.md) (8 princípios) e no [Guia Editorial](livro/GUIA-EDITORIAL.md). Os três que mais restringem:

1. **Evidência acima de retórica** — número sem condição experimental não entra, nem de fornecedor grande.
2. **A fonte-base é a técnica reprodutível** — paper **+** implementação pública.
3. **O escopo é o sistema, não a técnica** — todo capítulo declara o componente que aprofunda, e a fronteira com o livro irmão é explícita.

## Este repositório

| Diretório | O quê |
|---|---|
| `livro/` | o livro |
| `publicar/` | motor de publicação (Markdown → HTML). `npm run build` gera `docs/` |
| `chat-companion/` | o assistente do livro — FastAPI + RAG sobre o próprio texto |
| `rag-zero/` | a trilha prática: 17 etapas, uma por capítulo |
| `estudos/` · `benchmark/` · `adr/` | pesquisa, metodologia de avaliação, decisões |

```bash
cd publicar && npm ci && npm run build     # site + verificação
cd chat-companion/backend && python -m pytest   # 14 smoke tests
```

## Licença

Texto sob [CC BY 4.0](LICENSE) · código sob [MIT](LICENSE-CODE).

---

**Autor:** [Gilsiley Henrique Darú](livro/autor.md) — edição, direção e orquestração.
**Co-autoria de IA** declarada e registrada por edição no [Histórico](livro/HISTORICO.md).
