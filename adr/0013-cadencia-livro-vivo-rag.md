# 0013 — Cadência do livro vivo (RAG): janela trimestral e quatro gatilhos de domínio

- **Status:** Aceito
- **Data:** 2026-08-13
- **Contexto (feature/spec):** `002-portoes-e-cadencia`
- **Substitui:** [ADR 0007](0007-cadencia-livro-vivo.md)

## Contexto

O [ADR 0007](0007-cadencia-livro-vivo.md) foi herdado do livro irmão, está marcado
**Aceito** desde 2026-07-29 — e **nunca foi implementado aqui**. Ele manda o Guia Editorial
ganhar a seção "Cadência do livro vivo"; ela existe no harness e não existe neste
repositório (`grep -c "Cadência" livro/GUIA-EDITORIAL.md` → **0**).

Pior que a omissão: o **mecanismo** do 0007 é de outro domínio. A janela dele executa
"re-sync dos 16 forks (`scripts/sync-forks.ps1`)" — script e corpus que não existem neste
projeto. Uma política cuja ação principal é impossível não é uma política.

O resultado é a contradição mais séria do repositório: os 25 capítulos declaram "estado da
arte capturado em 2026-08" e **não há política de quando isso será recapturado**, num livro
cuja tese central é a cláusula de expiração. A tese está no corpo; a engrenagem que a
sustenta, não.

## Decisão

Um ADR **novo** que substitui o 0007, com janela periódica e gatilho extraordinário
adaptados ao que **este** livro cita.

### 1. Janela trimestral, ancorada na última captura

Captura vigente `2026-08` → **próxima janela: 2026-11**; depois 2027-02, 2027-05.

Trimestral e não anual porque a meia-vida da área é curta — o placar de expiração ficaria
vermelho o ano inteiro. Trimestral e não contínua porque o custo recai sobre um autor.

O **escopo da janela é fechado**, senão vira "revisar tudo" e não acontece:

1. reconferir as URLs do **Apêndice A** de todos os capítulos — é a espinha empírica do
   Princípio II, e o que apodrece primeiro;
2. reconferir o status ✓ das referências cujo paper ganhou versão nova;
3. **recapturar a data apenas dos capítulos efetivamente relidos**;
4. julgar toda aposta do registro de expiração cujo prazo caiu dentro da janela;
5. edição *minor* no `HISTORICO.md`, com o modelo de IA registrado (Guia §6.C).

O item 3 é a regra que impede o desfecho pior. Um verificador que cobra data fresca sem
cobrar releitura **força a datar uma mentira** — foi exatamente o que aconteceu no ciclo
001, quando uma checagem de datação boa demais fez reescrever fatos históricos para ficar
verde. Data antiga é informação honesta; data nova sem releitura, não.

### 2. Gatilho extraordinário — quatro eventos observáveis

O 0007 usava "harness do corpus arquivado/renomeado". O análogo funcional aqui é *o que
este livro efetivamente referencia*:

| # | Evento | Por que dispara |
|:--:|---|---|
| **G1** | Paper citado no corpo é retratado ou corrigido, ou ganha versão nova que altera o número ou a condição experimental reproduzida no livro | o Princípio I exige o número **com a condição ao lado**; se a condição mudou, o corpo mente |
| **G2** | Implementação pública citada no Apêndice A é arquivada, ou a função/parâmetro citado deixa de existir | a espinha empírica do Princípio II deixa de ser consultável |
| **G3** | A técnica vira funcionalidade nativa de provedor (reranking, embedding contextual, cache de prefixo, janela longa, busca) | invalida o "quando usar" e a conta de custo, que são o núcleo da Leitura executiva |
| **G4** | Qualquer evento que torne **falsa uma "Leitura executiva"** | cláusula guarda-chuva herdada do 0007 — é o contrato de frescor com o leitor apressado |

Qualquer G dispara revisão pontual do capítulo afetado, fora da janela, com spec própria
(Princípio VII).

### 3. Onde a política vive

Seção **§7 do `livro/GUIA-EDITORIAL.md`** (o checklist passa a §8), com a próxima janela
datada em linha de formato fixo, para ser lida por máquina.

## Alternativas avaliadas

- **A — Complementar o 0007 com um ADR que o estende.** Prós: barato, não mexe em status.
  Contras: deixa **duas instruções contraditórias vivas** — quem lê o 0007 encontra um
  `sync-forks.ps1` que não existe e não sabe qual manda.
- **B — Reescrever o 0007 no lugar.** Prós: zero arquivo novo. Contras: proibido pela
  convenção do próprio `adr/README.md` — "reescrever um ADR apaga a decisão que ele
  registra".
- **C — Substituir (a escolhida).** O vocabulário de status já prevê `Substituído por NNNN`;
  o texto do 0007 fica intacto e o registro histórico é preservado.
- **D — Não ter cadência e revisar por demanda.** Prós: custo zero. Contras: é o estado
  atual, e é o que o achado A2 da spec 002 acusa.

## Justificativa

A **decisão** do 0007 continua correta e é reafirmada: janela periódica **mais** gatilho
observável, com a Leitura executiva como critério — a revisão acontece quando a síntese
deixaria de ser verdadeira, não quando um calendário manda. O que muda é o mecanismo, que
precisava passar de "os forks que aquele livro lê" para "os papers e implementações que
este livro cita".

Os quatro gatilhos foram escolhidos por serem **observáveis sem julgamento**: cada um é um
fato verificável sobre um artefato externo, não uma impressão sobre relevância.

## Consequências

- **Positivas:** o livro passa a poder **ficar vermelho pelo tempo**, e não só por commit —
  é uma mudança de natureza no portão. A tese da expiração ganha engrenagem.
- **Custos aceitos:** o ADR 0007 muda de status no arquivo e no índice; o Guia renumera o
  checklist de §7 para §8 (nenhum documento do repositório remete a §7, verificado).
- **Sobre a verificação:** a passagem do tempo não gera pull request. Sem um job
  **agendado**, o portão de cadência nunca dispara — a verificação abaixo depende disso, e
  é por isso que este ADR é o último dos três a ser implementado, depois do CI acionado
  (R1 da spec 002).
- **Reversibilidade:** alta. Janela e gatilhos são dados no Guia; mudar a janela é uma
  linha, e mudar a política é um ADR que substitui este.

## Como verificar

Checagens novas em `specs/001-edicao-1-0/verificar.py` (padrão `rN_*`) mais um job
`schedule` mensal:

1. **Janela declarada e parseável** — o Guia contém exatamente uma linha
   `**Próxima janela: AAAA-MM**`. Ausente ou duplicada → falha.
2. **Janela cumprida** — se `hoje > janela + 30 dias` sem edição correspondente no
   `HISTORICO.md`: **aviso**; `+ 60 dias`: **falha**. A gradação evita vermelho por atraso
   de dias.
3. **Nenhum capítulo com captura mais velha que duas janelas** (6 meses).
4. **Placar honesto** — toda aposta do registro de expiração com prazo vencido tem veredito
   ≠ ⏳.
