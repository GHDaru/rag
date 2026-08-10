# Tarefas 001 — Edição 1.0

> Estado real ao fim do ciclo, com a evidência de cada uma. O que **não** foi
> entregue está marcado como tal — foi o revisor independente que pegou a
> ausência deste arquivo, e reconstruí-lo em silêncio, como se tivesse existido
> desde o início, seria manufaturar rastro.

| # | Tarefa | Lote | Estado | Verificação |
|:---:|---|:---:|:---:|---|
| 1 | `spec.md`, `plan.md` com Constitution Check, `verificar.py` | A | ✅ | `python3 specs/001-edicao-1-0/verificar.py` |
| 2 | `feature.json` deixa de apontar para spec do livro irmão | A | ✅ | aponta para `specs/001-edicao-1-0` |
| 3 | ADR 0009 (escopo), 0010 (companion), 0011 (siglas) | A | ✅ | `adr/README.md` indexa os três |
| 4 | Datação coerente em capítulos, `README`, `CLAUDE.md`, `rag-zero/README` | A | ✅ | R2 verde |
| 5 | `CITATION.cff` e `.zenodo.json` no objeto da constituição 3.0.0 | A | ✅ | R3 verde |
| 6 | Portão do companion + teste de paridade do BM25 | A | ✅ | `bash scripts/check-companion.sh`; `test_bm25_paridade_com_rag_zero` |
| 7 | Remissões corretas (o caso do cap. 21 → 15) | B | ✅ | R4 verde |
| 8 | Política de siglas em quatro classes, com fonte única | B | ✅ | R5 verde; `publicar/siglas.json` lido pelo motor e pelo verificador |
| 9 | Página "Como ler este livro" | B | ❌ **não entregue** | prometida no ADR 0009 item 5; fica como dívida declarada |
| 10 | 22 "Mão na massa" com arquivo, comando e saída esperada | C | ✅ | R6 verde |
| 11 | `rag-zero` no sumário do livro | C | ✅ | R6 verde; 34 páginas no build |
| 12 | Artefato concreto nos caps. 06, 11 e 15 | C | ✅ | R7 verde — o prompt de fundamentação **é exibido** |
| 13 | Etapas 1, 2, 7 e 8 da trilha | D | ✅ | 48 testes; `etapa02_naive.py` roda |
| 14 | Etapa 14 completa (*faithfulness* por juiz) | D | ❌ **rebaixada** | exigida pelo ADR 0009; entregue parcial. Ver ADR 0012 |
| 15 | Etapas não construídas declaradas, nunca no presente | D | ✅ | R8 verde |
| 16 | Zero afirmação do corpo em fonte não-✓ | E | ⚠️ **não verificado** | não existe checagem automática; dívida declarada |
| 17 | Revisão independente em contexto fresco | F | ✅ | reprovou o merge; os bloqueadores viraram este lote de correções |

## O que o revisor independente pegou, e que eu não teria pegado

Registrado porque é o resultado mais valioso do ciclo:

1. **Falsificação de fato histórico.** A regra de datação que escrevi cobrava
   `edição X.Y` em **qualquer** posição do arquivo — e isso reescreveu "capítulo
   criado na edição 0.2" para "criado na edição 1.0". Uma checagem que só passa
   mentindo é pior que checagem nenhuma. Revertido, e a regra passou a olhar só
   a linha de datação do cabeçalho.
2. **A `r4_remissoes` não pegava o caso que dá nome ao requisito** — o regex
   consumia o sujeito errado ("prompt" em vez de "fundamentação").
3. **R7 nunca foi verificado**, e o `HISTORICO` afirmava que estava corrigido.
   Era o defeito fundador reproduzido dentro da correção dele.
4. **"145 falhas"** não era reproduzível: o instrumento mudou no meio do ciclo.
   Número sem condição experimental, num livro que exige condição experimental.
5. **`CLAUDE.md` e `rag-zero/README.md` ficaram em 0.6** — e o segundo virou
   página publicada neste mesmo ciclo.
