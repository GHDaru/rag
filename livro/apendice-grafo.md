# Apêndice — Grafo do livro

> O mapa de conexões do livro, extraído **deterministicamente** do próprio texto a cada build — sem LLM, sem curadoria manual. Um nó é um capítulo, uma ferramenta do ecossistema, um conceito do glossário ou uma etapa do `contexto-zero`; uma aresta é uma menção real, e o peso é o número de ocorrências.
>
> Edição 0.1 · captura em 2026-08.

Como o grafo nasce do texto, ele é sempre honesto: se um capítulo não cita uma técnica, não há aresta. Nós sem nenhuma conexão são podados — o que torna o grafo um instrumento de revisão editorial, e não só uma ilustração. Um conceito que ninguém menciona é um conceito que o livro promete e não entrega.

<div data-viz="grafo-livro"></div>

## Como ler

- **Capítulos** (âmbar) — os 19 textos numerados.
- **Ferramentas e frameworks** (azul) — o ecossistema mapeado no [apêndice do ecossistema](apendice-ecossistema.md).
- **Conceitos** (verde) — os verbetes do [glossário](glossario.md).
- **contexto-zero** (roxo) — as 16 etapas da trilha prática.

Arestas mais grossas são menções mais frequentes. Capítulo→capítulo aparece quando um texto cita outro por número ("cap. 09").

## O que o grafo revela nesta edição

Na edição 0.1 o grafo é esparso por construção — os capítulos estão no nível de esqueleto, e a densidade de menções cresce com o aprofundamento. Os pisos de qualidade do build (nós e arestas mínimos) foram calibrados para esta edição e **sobem a cada rodada** de aprofundamento, registrado no [ROADMAP](https://github.com/GHDaru/rag/blob/main/ROADMAP.md).

O uso editorial do grafo, a partir da rodada 2: procurar **nós isolados** (conceito prometido no glossário e não usado em nenhum capítulo) e **pontes ausentes** (capítulos que deveriam conversar e não se citam — por exemplo, 12 e 16, que tratam do mesmo risco por ângulos diferentes).
