# Guia Editorial

> Como este livro é escrito. A **constituição** ([`.specify/memory/constitution.md`](../.specify/memory/constitution.md)) diz o que é obrigatório; este guia diz **como** cumprir.
>
> Edição 0.1 · captura em 2026-08.

## 1. O método pedagógico (Princípio III)

Quatro tradições combinadas, cada uma resolvendo um problema diferente:

- **Backward Design** (Wiggins & McTighe) — escreve-se de trás para frente: primeiro os **objetivos de aprendizagem** (com verbos de Bloom: explicar, distinguir, projetar, avaliar), depois as **evidências** de que foram atingidos (a seção "Verificação"), e só então o conteúdo. Um capítulo cujo objetivo não tem verificação correspondente está incompleto.
- **4C/ID** (van Merriënboer) — a trilha prática (`rag-zero`) é a espinha: as etapas são *learning tasks* (tarefas inteiras, não fragmentos); os capítulos são *supportive information*; os boxes no código são *just-in-time*; os exercícios curtos são *part-task practice*.
- **Diátaxis** (Procida) — quatro tipos de texto que **nunca se misturam na mesma seção**: capítulos são *explanation*; a construção é *tutorial*; o catálogo de técnicas e o glossário são *reference*; a "Leitura executiva" (o "o que roubar") é *how-to*.
- **Carga Cognitiva** (Sweller) — *worked example* antes do exercício; *completion problem* ("complete", nunca "crie do zero"); *fading* do andaime etapa a etapa; **uma ideia nova por vez**.

## 2. O esqueleto obrigatório de capítulo

Todo capítulo numerado tem, nesta ordem:

```
# NN — Título
> cabeçalho: **linha 1** — data de captura · última revisão · link para o Histórico; **linha 2** — maturidade e o componente que o capítulo aprofunda
>
> A **edição não entra no cabeçalho de capítulo** ([ADR 0016](../adr/0016-datacao-do-capitulo.md)): ela identifica a *obra*, não o capítulo, e vive no Histórico. As duas datas respondem às duas perguntas que o leitor faz — *de quando é esta foto do estado da arte?* e *quando este texto foi mexido pela última vez?* — e a segunda é conferida contra o git, não contra uma constante.

## Objetivos de aprendizagem      ← Backward Design (verbos de Bloom)
## O problema                     ← por que o capítulo existe; a dor concreta
## Fundamentos científicos        ← papers, com status de validação
## Fontes da indústria            ← docs oficiais e prática, com URL
## O estado da arte               ← a síntese: seções numeradas
   ### Leitura executiva          ← o "o que roubar" (how-to), sempre por último
## Mão na massa — rag-zero, etapa N
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
- **Link para arquivo do próprio repositório é sempre relativo** — `../../rag-zero/rag_zero/bm25.py`, nunca a URL completa do GitHub ([ADR 0015](../adr/0015-links-para-o-proprio-repositorio.md)). O motor converte na URL pública, o GitHub resolve nativamente quem lê o `.md`, e — o que decide — **o build confere o alvo contra o disco**. URL absoluta é um link externo: nenhum portão a valida, e a branch fica codificada em cada ocorrência.

## 5. A construção (`rag-zero`)

- **Do zero antes da biblioteca** (restrição 3 da constituição). Toda técnica é implementada na mão primeiro — BM25 em ~40 linhas antes de qualquer vector store. A biblioteca entra depois, nomeada como escolha.
- **Uma etapa por capítulo**, **executável isoladamente** — um comando, sem rede e sem credencial, e sem ter rodado a etapa anterior — sobre o núcleo testado (`rag_zero/`). O **delta** de cada etapa é declarado no cabeçalho do script e gerado em [`DIFF.md`](../rag-zero/DIFF.md); é ele que carrega a lição, no lugar da duplicação de diretório ([ADR 0014](../adr/0014-autocontencao-das-etapas.md)).
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

## 7. Cadência do livro vivo

> Política decidida no [ADR 0013](../adr/0013-cadencia-livro-vivo-rag.md), que substitui o
> [ADR 0007](../adr/0007-cadencia-livro-vivo.md) — herdado do livro irmão, com gatilho de
> outro domínio.

A cláusula de expiração é a tese do livro. Uma tese sem cadência é uma promessa.

**Próxima janela: 2026-11.** Janela **trimestral**, contada da última captura
(2026-08 → 2026-11 → 2027-02 → 2027-05).

O que a janela faz, nesta ordem:

1. **Apêndice A de todos os capítulos** — cada URL de implementação é aberta e conferida; o
   que sumiu ou mudou de contrato é corrigido ou removido. É a espinha empírica do Princípio
   II, e o que apodrece primeiro.
2. **Referências** — papers com versão nova são reconferidos; o status ✓ vale para a versão
   lida.
3. **Recaptura de data — só onde houve releitura.** Mudar "capturado em" sem reler é datar
   uma mentira. Capítulo não relido mantém a data antiga, e a data antiga é informação
   honesta.
4. **Registro de expiração** — toda aposta com prazo dentro da janela recebe veredito
   ✅/❌/🔄. Aposta refutada não se apaga.
5. **Histórico** — edição minor, com o modelo de IA registrado (§6).

**Gatilho extraordinário** — não espera a janela; abre spec própria para o capítulo afetado:

| # | Evento | Por que dispara |
|:--:|---|---|
| G1 | Paper citado é retratado ou corrigido, ou muda o número ou a condição experimental que o livro reproduz | o corpo passa a afirmar um número que a fonte não sustenta (Princípio I) |
| G2 | Implementação citada no Apêndice A é arquivada, ou a função/parâmetro citado deixa de existir | a espinha empírica do Princípio II deixa de ser consultável |
| G3 | A técnica vira funcionalidade nativa de provedor (reranking, embedding contextual, cache de prefixo, janela longa, busca) | invalida o "quando usar" e a conta de custo |
| G4 | Qualquer evento que torne falsa uma **"Leitura executiva"** | é o contrato de frescor com o leitor apressado |

A data "estado da arte capturado em" de cada capítulo é a verdade exposta ao leitor — a
cadência existe para que ela nunca minta por omissão.

## 8. Checklist antes de publicar

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
