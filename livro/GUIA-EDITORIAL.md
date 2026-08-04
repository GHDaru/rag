# Guia Editorial

> Como este livro é escrito. A **constituição** ([`.specify/memory/constitution.md`](https://github.com/GHDaru/rag/blob/main/.specify/memory/constitution.md)) diz o que é obrigatório; este guia diz **como** cumprir.
>
> Edição 0.1 · captura em 2026-08.

## 1. O método pedagógico (Princípio III)

Quatro tradições combinadas, cada uma resolvendo um problema diferente:

- **Backward Design** (Wiggins & McTighe) — escreve-se de trás para frente: primeiro os **objetivos de aprendizagem** (com verbos de Bloom: explicar, distinguir, projetar, avaliar), depois as **evidências** de que foram atingidos (a seção "Verificação"), e só então o conteúdo. Um capítulo cujo objetivo não tem verificação correspondente está incompleto.
- **4C/ID** (van Merriënboer) — a trilha prática (`contexto-zero`) é a espinha: as etapas são *learning tasks* (tarefas inteiras, não fragmentos); os capítulos são *supportive information*; os boxes no código são *just-in-time*; os exercícios curtos são *part-task practice*.
- **Diátaxis** (Procida) — quatro tipos de texto que **nunca se misturam na mesma seção**: capítulos são *explanation*; a construção é *tutorial*; o catálogo de técnicas e o glossário são *reference*; a "Leitura executiva" (o "o que roubar") é *how-to*.
- **Carga Cognitiva** (Sweller) — *worked example* antes do exercício; *completion problem* ("complete", nunca "crie do zero"); *fading* do andaime etapa a etapa; **uma ideia nova por vez**.

## 2. O esqueleto obrigatório de capítulo

Todo capítulo numerado tem, nesta ordem:

```
# NN — Título
> cabeçalho: data de captura · edição · maturidade · link para o Histórico

## Objetivos de aprendizagem      ← Backward Design (verbos de Bloom)
## O problema                     ← por que o capítulo existe; a dor concreta
## Fundamentos científicos        ← papers, com status de validação
## Fontes da indústria            ← docs oficiais e prática, com URL
## O estado da arte               ← a síntese: seções numeradas
   ### Leitura executiva          ← o "o que roubar" (how-to), sempre por último
## Mão na massa — contexto-zero, etapa N
## Verificação                    ← as evidências dos objetivos
---
## Apêndice A — Como cada fonte trata X   ← o tratamento por implementação
```

**Regras do esqueleto:**

- **Um `<h1>` por arquivo.** O motor de publicação verifica.
- **O primeiro blockquote é a datação** — o build o transforma no selo de data e o remove do corpo.
- **"Leitura executiva" é o último bloco do estado da arte**, e é o que o leitor apressado lê. Deve conter o *o que roubar*: as decisões acionáveis, não um resumo.
- **O Apêndice A fica depois de `---`.** É complementação online (Princípio II): o corpo recebe a síntese, o apêndice recebe a evidência por implementação.
- **"Verificação" são perguntas, não respostas.** Perguntas que exigem transferência, não recuperação — "diagnostique", "argumente contra", "estime", em vez de "o que é X".

## 3. As regras de evidência (Princípio I)

| Tipo de afirmação | Exige |
|---|---|
| Sobre uma técnica | fonte primária (paper ou doc oficial) com URL |
| Científica | entrada em `bibliografia.md` com status; `[a validar]` no texto enquanto for ⏳ |
| Numérica | **o número + a condição experimental + a fonte da medição**, juntos |
| Sobre uma ferramenta | URL do repositório ou da documentação |
| Sobre o que "a indústria faz" | ou várias fontes independentes, ou a afirmação é enfraquecida |

**A regra que mais importa na prática:** um número sem a condição experimental ao lado não entra no corpo — nem quando vem de fornecedor grande, nem quando confirma o que gostaríamos que fosse verdade. Escreva "reportou X em corpus próprio" e não "melhora X".

E a formulação padrão para medição de terceiro: **"foi medido por N, em C, com M"** — nunca "está provado que".

## 4. Estilo

- **Português**, com termos técnicos consagrados sem tradução: *prompt*, *token*, *chunk*, *embedding*, *retrieval*, *reranking*, *context rot*, *prompt injection*. Traduzir esses termos prejudica o leitor que vai procurar mais.
- **Sigla sempre expandida na primeira ocorrência** do capítulo, e presente no [glossário](glossario.md).
- **Tabela quando a informação é comparativa**; prosa quando é argumentativa. Tabela que poderia ser uma frase é ruído.
- **Sem hype.** Nada é "revolucionário", "poderoso" ou "game changer". Se a coisa é boa, o número e o trade-off dizem.
- **Sem vendor favorito** (Princípio VI). Ferramentas aparecem pelo problema que resolvem, com o custo declarado.
- **Voz ativa e frase curta.** O assunto já é difícil; a prosa não deve somar dificuldade.

## 5. A construção (`contexto-zero`)

- **Do zero antes da biblioteca** (restrição 3 da constituição). Toda técnica é implementada na mão primeiro — BM25 em ~40 linhas antes de qualquer vector store. A biblioteca entra depois, nomeada como escolha.
- **Uma etapa por capítulo**, autocontida e executável.
- **Cada porta nasce da dor do capítulo** (`LLMPort`, `RetrieverPort`, `MemoryPort`, `EvalPort`) — nunca estrutura antecipada.
- **Completion problem, não folha em branco**: a etapa entrega o esqueleto e o leitor implementa a parte que carrega a decisão.
- **Custo zero e sem GPU** (Princípio VI).

## 6. O processo de escrita

### 6.A Revisão em duas camadas (portão de qualidade)

Antes do copyedit de superfície, um passo de **revisão *developmental*** — re-ver estrutura e sentido: o argumento fecha? a ordem serve ao leitor? há redundância ou lacuna? algum objetivo ficou sem verificação? "Escrever é reescrever" (tradição Sommers, Flower & Hayes): nenhum trecho novo é publicado sem esse passo.

### 6.B Spec-driven (Princípio VII)

Toda melhoria — inclusive editorial — passa por `spec → plan → tasks → implement`, em branch própria. O `plan.md` traz o **Constitution Check** como portão.

### 6.C Atribuição e rastreabilidade

Toda edição registra em [`HISTORICO.md`](HISTORICO.md): o que mudou, a data, **o modelo de IA usado** e a sessão. Saídas de LLM não são determinísticas; sem o registro, o resultado não é reproduzível nem auditável.

A co-autoria é declarada, não escondida: **direção, decisão editorial e responsabilidade são humanas; pesquisa, estruturação e redação são assistidas por IA.** Onde a IA errou e foi corrigida, o registro fica no histórico da branch.

## 7. Checklist antes de publicar

- [ ] Objetivos com verbos de Bloom, e **cada um** com verificação correspondente
- [ ] Primeiro blockquote com data de captura e maturidade
- [ ] Um `<h1>`; "Leitura executiva" presente e acionável
- [ ] Toda afirmação técnica com fonte; todo número com condição experimental
- [ ] Referências novas registradas em `bibliografia.md` com status
- [ ] Termos novos no `glossario.md`
- [ ] Diátaxis respeitada (nenhuma seção mistura dois tipos)
- [ ] Revisão developmental feita
- [ ] `cd publicar && npm run build` verde (links internos e template)
- [ ] `HISTORICO.md` atualizado, **com o modelo de IA registrado**
- [ ] Nenhum segredo, nenhuma chave, nenhum identificador interno de modelo (Princípio V)
