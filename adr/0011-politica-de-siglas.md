# 0011 — Política de siglas: quatro classes, uma regra cada

- **Status:** Aceito
- **Data:** 2026-08-09
- **Contexto (feature/spec):** `001-edicao-1-0`

## Contexto

O guia editorial exigia: *"sigla sempre expandida na primeira ocorrência do capítulo"*.
Um verificador automático encontrou **43 violações** — inclusive a sigla do título:
*Retrieval-Augmented Generation* nunca era expandida no corpo dos caps. 00 e 01.

Mas aplicar a regra ao pé da letra significaria **25 capítulos abrindo com
"RAG (*Retrieval-Augmented Generation*)"** — cerca de 300 palavras de ruído concentradas
justamente nos parágrafos de abertura, que é o ponto de **maior carga cognitiva**. A regra
combateria o empilhamento produzindo empilhamento.

Três achados do parecer mudaram o desenho da decisão:

1. **O motor de publicação já resolve metade.** `build.mjs` tem `abrirSiglas`, que envolve
   toda ocorrência em `<abbr title="…">`, com `pre/code/a/h1-h6` protegidos — e o `pdf.mjs`
   reaproveita o mesmo HTML e o mesmo CSS.
2. **O dicionário desse motor é herança do livro irmão.** Lista `ACP, A2A, MRTR, LSP, MAST`
   — e **não** lista `IR, TREC, SIGIR, RRF, BEIR, MTEB, RAGAS, OWASP`. Havia **duas fontes
   de verdade divergentes**: a do motor e a do verificador.
3. **O verificador tinha dois falsos positivos próprios:** cobrava `BM25 → "Best Matching
   25"`, forma que **não existe** em lugar nenhum do texto, e `DoD`, que é sigla do livro
   irmão.

E um detalhe técnico decisivo: **o build remove o blockquote de datação** das páginas de
capítulo. O cap. 01 introduzia `SIGIR`/`TREC` exatamente ali — no site, essa ocorrência
não existe, e qualquer expansão colocada lá é invisível.

## Decisão

**Expande-se no texto quando a expansão *ensina*; delega-se ao motor quando ela só
*decodifica*.** Quatro classes, uma regra cada:

| Classe | Exemplos | Regra no texto |
|---|---|---|
| **Núcleo** | `RAG`, `LLM`, `IR` | **Não se expande por capítulo.** A expansão canônica fica em **duas portas**: cap. 00 e cap. 01 — as duas entradas que o livro declara. Nos demais, quem expande é o motor. |
| **Franca** | `API`, `JSON`, `URL`, `PDF`, `GPU` | **Nunca expandida no texto.** Vive no dicionário e no glossário. |
| **Técnica** | `RRF`, `NDCG`, `ANN` | **Expandida na primeira ocorrência do arquivo**, com a expansão **primeiro**: "fusão recíproca de ranking (RRF)". Se aparece **uma única vez**, não use sigla — escreva o termo. |
| **Nome próprio** | `BM25`, `BEIR`, `MTEB`, `RAGAS`, `TREC`, `HyDE`, `RAPTOR` | **Não se expande por letras** — "BM25 = Best Matching 25" não ensina nada. A primeira ocorrência traz **glosa funcional + fonte com URL**. |

Mais três consequências operacionais:

- **`publicar/siglas.json` vira fonte única**, lida pelo motor **e** pelo verificador. As
  duas listas divergentes deixam de existir.
- **O motor passa a marcar a primeira ocorrência por página** (`data-primeira` + CSS), o
  que entrega exatamente o que a regra original queria — expansão uma vez por unidade de
  leitura — com **zero palavras no fonte** e sem risco de divergência. Vale também no PDF.
- **Nunca introduzir sigla no blockquote de datação**, porque o build o apaga.

## Alternativas avaliadas

- **A — Literal (expandir em todo capítulo).** Prós: regra simples, verificação trivial.
  Contras: ~300 palavras de ruído nas aberturas; ensina zero na 25ª repetição; e força
  expansão de nome próprio, que é informação falsa disfarçada de rigor.
- **B — Delegar tudo ao motor.** Prós: zero custo de leitura no site. Contras: perde nos
  **artefatos Markdown que o próprio build gera** (`docs/md/*.md` e o consolidado "bom
  para LLMs") e na leitura pelo GitHub; tooltip não funciona em toque e é fraco no
  teclado; e **decodificar não é ensinar** — saber as letras de BEIR não diz o que ele
  mede.
- **C — Escalonada por classe (a escolhida).** ~8–12 expansões no livro inteiro, cada uma
  onde carrega conteúdo.

## Justificativa

A regra antiga tratava como iguais três coisas diferentes: a sigla **do título**, um
**conceito** que o leitor pode não ter, e um **nome próprio**. A política nova separa os
três, e cada regra passa a ter uma razão que se sustenta sozinha.

A alternativa B foi rejeitada por um motivo concreto e verificável: o build gera Markdown
cru, sem `<abbr>`. Um livro que só funciona renderizado não é o livro que este projeto
publica.

## Consequências

- **Positivas:** aberturas limpas; expansão no ponto em que ensina; **uma** fonte de
  verdade em vez de duas divergentes; a checagem passa a pegar também o **excesso**
  (expansão redundante de sigla de núcleo) e a **sigla não catalogada**, que era o buraco.
- **Negativas / custos aceitos:** exige uma passada de classificação (~40 siglas) e torna
  a política dependente do motor entregar a expansão por página. O `.md` avulso de um
  capítulo intermediário terá `RAG` sem expansão no corpo — mitigado pelo glossário, que
  vai junto no consolidado.
- **Reversibilidade:** alta. O dicionário é dado, não código; mudar de classe é editar uma
  chave.
