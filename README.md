# Engenharia de Prompt e Engenharia de Contexto — O Livro

> Um livro aberto, em português, sobre as **duas disciplinas que decidem o que o modelo vê**: o que se escreve (prompt) e o que se monta em runtime (contexto) — com o RAG no lugar certo, dentro da segunda.

**Edição 0.1 (fundação)** · captura em 2026-08 · [Histórico](livro/HISTORICO.md) · [ROADMAP](ROADMAP.md)

## A pergunta que originou o projeto

> *Engenharia de contexto poderia assumir como substituto do RAG?*

**Não como substituto — como moldura.** As duas coisas não estão no mesmo nível:

|  | Engenharia de contexto | RAG |
|---|---|---|
| Nível | **disciplina** | **técnica** |
| Decide | o que ocupa a janela, em que ordem, e o que sai quando falta espaço | que trechos do corpus respondem à pergunta |
| Concorrentes | prompt, memória, recuperado, resultado de ferramenta, histórico | — |
| Falha típica | *context rot*, instrução afogada, orçamento estourado | recall baixo, chunk cortado, resposta sem fundamento |

RAG é um **subconjunto próprio** da engenharia de contexto — o que resolve "o conhecimento não está nos pesos e não cabe todo na janela". Quem troca o rótulo e mantém o mesmo pipeline só renomeou o problema. O raciocínio completo está na [introdução](livro/00-introducao.md) e no [panorama da comunidade](estudos/2026-08-03-panorama-comunidade.md).

Por isso o livro trata **duas disciplinas em relação**, e dá ao RAG três capítulos dentro da segunda — não o título.

## O livro

### Abertura
| | |
|---|---|
| [00 — Introdução](livro/00-introducao.md) | As duas disciplinas, o lugar do RAG, o método |
| [01 — Fundamentos](livro/01-fundamentos.md) | Vocabulário, o caminho de uma requisição, taxonomia por sintoma |

### Parte I — Engenharia de Prompt (*o que se escreve*)
| | |
|---|---|
| [02 — Anatomia de um Prompt](livro/capitulos/02-anatomia-do-prompt.md) | Seis partes funcionais; separar instrução de dado |
| [03 — Técnicas de Raciocínio](livro/capitulos/03-tecnicas-de-raciocinio.md) | As seis famílias, e quando cada uma ainda paga |
| [04 — Saídas Estruturadas](livro/capitulos/04-saidas-estruturadas.md) | Schema, decodificação restrita, validar e reparar |
| [05 — Prompt de Sistema, Persona e Regras](livro/capitulos/05-persona-e-regras.md) | Camadas por volatilidade; voz ≠ política |
| [06 — Otimização Automática de Prompts](livro/capitulos/06-otimizacao-de-prompts.md) | Do artesanato ao compilador (DSPy, GEPA, TextGrad) |
| [07 — Avaliação de Prompts](livro/capitulos/07-avaliacao-de-prompts.md) | Sem eval, mudar prompt é apostar |

### Parte II — Engenharia de Contexto (*o que se monta em runtime*)
| | |
|---|---|
| [08 — A Janela como Orçamento](livro/capitulos/08-janela-como-orcamento.md) | *Context rot*; contexto longo × recuperação |
| [09 — Recuperação: o Núcleo do RAG](livro/capitulos/09-recuperacao.md) | Chunking, embeddings, busca híbrida, reranking |
| [10 — RAG Avançado](livro/capitulos/10-rag-avancado.md) | Contextual retrieval, late chunking, GraphRAG |
| [11 — RAG Agêntico](livro/capitulos/11-rag-agentico.md) | Quando o agente decide se, quando e como buscar |
| [12 — Memória e Estado](livro/capitulos/12-memoria.md) | Fatos, grafo temporal, paginação — e memória × RAG |
| [13 — Compactação e Isolamento](livro/capitulos/13-compactacao.md) | Caber na janela sem perder o fio |
| [14 — Ferramentas e Contexto Externo](livro/capitulos/14-ferramentas-e-mcp.md) | Resultado de ferramenta também é contexto |

### Parte III — O sistema em produção
| | |
|---|---|
| [15 — Avaliação de Sistemas](livro/capitulos/15-avaliacao-de-sistemas.md) | As quatro métricas e a tabela de diagnóstico |
| [16 — Segurança do Contexto](livro/capitulos/16-seguranca-do-contexto.md) | *Prompt injection* como propriedade da arquitetura |
| [17 — Custo, Latência e Cache](livro/capitulos/17-custo-latencia-cache.md) | A conta do contexto, e o cache de prefixo |

### Fechamento e aparato
| | |
|---|---|
| [18 — Convergências e Tendências](livro/18-convergencias.md) | Consenso, disputa aberta e **seis apostas datadas** |
| [Catálogo de técnicas](livro/apendice-tecnicas.md) | Uma ficha por técnica: o que é, quando usa, o que custa |
| [Apêndice — O ecossistema](livro/apendice-ecossistema.md) | Frameworks e coleções, por problema que resolvem |
| [Glossário](livro/glossario.md) · [Bibliografia](livro/bibliografia.md) | Termos e fontes com status de validação |
| [Guia Editorial](livro/GUIA-EDITORIAL.md) · [Histórico](livro/HISTORICO.md) | Como é escrito; edições e registro de expiração |

## Por onde começar

Não pelo sumário — pela **tabela de sintomas** do [cap. 01](livro/01-fundamentos.md). Leve o seu problema real:

| Sintoma | Onde ler |
|---|---|
| "Melhorei o prompt" e não sei se melhorou | [cap. 07](livro/capitulos/07-avaliacao-de-prompts.md) |
| O modelo não sabe informação da minha organização | [cap. 09](livro/capitulos/09-recuperacao.md) |
| Recupera errado / não encontra o óbvio | [caps. 09](livro/capitulos/09-recuperacao.md), [10](livro/capitulos/10-rag-avancado.md) |
| Recupera certo mas responde errado | [cap. 15](livro/capitulos/15-avaliacao-de-sistemas.md) |
| Piora quando a conversa fica longa | [caps. 08](livro/capitulos/08-janela-como-orcamento.md), [13](livro/capitulos/13-compactacao.md) |
| Funciona, mas custa demais | [cap. 17](livro/capitulos/17-custo-latencia-cache.md) |

E se você só puder aplicar sete coisas, elas estão listadas, em ordem, no fim do [catálogo de técnicas](livro/apendice-tecnicas.md#as-sete-que-valem-começar-por-aqui).

## Estado desta edição (honestidade obrigatória)

A edição 0.1 é a **fundação**: a moldura completa com profundidade de esqueleto. Isso é uma escolha — moldura completa antes de profundidade parcial.

O que isso significa na prática:

- **Nenhuma referência tem status ✓.** Todas estão marcadas ⏳ na [bibliografia](livro/bibliografia.md) e `[a validar]` nos capítulos. A validação é a [rodada 2](ROADMAP.md#rodada-2--evidência-a-que-tira-os-).
- **Os Apêndices A** (tratamento por implementação) estão enfileirados, não escritos.
- **Nenhum número de terceiro** aparece no corpo sem a marcação e a condição experimental.
- **A trilha prática `contexto-zero`** está descrita capítulo a capítulo, e é implementada na [rodada 3](ROADMAP.md#rodada-3--contexto-zero-a-trilha-prática).

Fora do escopo por decisão: edição em inglês, Radar de atualização automática, benchmark quantitativo de frameworks. Tudo com rodada marcada no [ROADMAP](ROADMAP.md).

## Como o livro é feito

O método está na [constituição](.specify/memory/constitution.md) (8 princípios) e no [Guia Editorial](livro/GUIA-EDITORIAL.md). Os três que mais restringem o dia a dia:

1. **Evidência acima de retórica** — número sem condição experimental ao lado não entra no corpo, nem vindo de fornecedor grande.
2. **A fonte-base é a técnica reprodutível** — paper (o que foi proposto e medido) **+** implementação pública (como vira código). Sem as duas, não entra.
3. **O escopo é o par, não a moda** — todo capítulo responde: "que decisão sobre o que o modelo vê ele ajuda a tomar?".

E o livro é **vivo**: cada capítulo declara sua data de captura, e o [cap. 18](livro/18-convergencias.md) registra **seis apostas datadas** sobre o que vai expirar — com prazo e critério, para serem cobradas. Uma delas prevê que o próprio título expire antes do conteúdo.

## Este repositório

| Diretório | O quê |
|---|---|
| `livro/` | o livro (capítulos, apêndices, glossário, bibliografia, histórico, guia) |
| `publicar/` | o motor de publicação (Markdown → HTML). `npm run build` gera `docs/` |
| `chat-companion/` | o assistente do livro — FastAPI + RAG sobre o próprio texto |
| `estudos/` | notas de pesquisa (panorama da comunidade, parecer editorial) |
| `benchmark/` | metodologia de avaliação de técnicas (avaliações na rodada 4) |
| `adr/` | Architecture Decision Records |
| `.specify/` | spec-kit: constituição, scripts e templates |

### Publicar localmente

```bash
cd publicar
npm ci
npm run build     # gera docs/ e verifica links e template
```

### Rodar o companion

```bash
cd chat-companion/backend
pip install -r requirements.txt
python -m pytest          # 14 smoke tests, sem rede e sem banco
uvicorn app:app --reload  # sem chave -> adapter echo; sem banco -> memória
```

Nenhuma credencial vive no repositório (Princípio V). Use `.env.example` como molde; `.env` é gitignored.

## Contribuir

Toda melhoria passa pelo ciclo spec-driven, em branch própria — ver [`CLAUDE.md`](CLAUDE.md) e o [ROADMAP](ROADMAP.md). A [rodada 2](ROADMAP.md#rodada-2--evidência-a-que-tira-os-) (validar referências) é a mais valiosa e a mais fatiável: cada referência validada é uma contribuição fechada.

## Licença

Texto sob [CC BY 4.0](LICENSE) · código sob [MIT](LICENSE-CODE).

---

**Autor:** [Gilsiley Henrique Darú](livro/autor.md) — edição, direção e orquestração.
**Co-autoria de IA** declarada e registrada por edição no [Histórico](livro/HISTORICO.md).
