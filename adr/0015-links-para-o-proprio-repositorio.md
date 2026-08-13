# 0015 — Links para o próprio repositório: caminho relativo, base única, tag da edição

- **Status:** Aceito
- **Data:** 2026-08-13
- **Contexto (feature/spec):** `002-portoes-e-cadencia`

## Contexto

O livro aponta para o próprio código **49 vezes, em 30 arquivos**, com URL absoluta e a
branch `main` codificada:

```
https://github.com/GHDaru/rag/blob/main/rag-zero/rag_zero/bm25.py
```

Três problemas, e um fato que muda o desenho da solução.

- O **link-check do build não valida nenhuma delas** — ele confere `href` `.html` e ignora
  todo link externo. As 49 passam mudas: se o arquivo for movido, o livro aponta para o
  vazio e o portão continua verde.
- **Renomear a branch quebra 49 links em silêncio.**
- O leitor do site é **ejetado para o GitHub** no meio do capítulo.

O fato: **o motor já resolve link relativo → GitHub**. `publicar/build.mjs:58` define
`GITHUB_BASE` e a regra `link_open` (linhas 218–232) reescreve qualquer link relativo não
publicado para essa base. A "variável única" que faltaria já existe — **as 49 URLs
absolutas contornam um mecanismo pronto**. O livro irmão usa a forma relativa; este herdou
o motor e não herdou a convenção, que não está escrita nem no Guia nem em ADR.

Achado colateral, verificado: `build.mjs:78` — o rodapé da edição **em inglês** aponta para
`https://github.com/GHDaru/harness_engineering`. Resíduo do fork, e um bug real.

## Decisão

**No fonte, sempre caminho relativo. No motor, uma base única, apontando para a tag da
edição quando ela existir e para `main` como fallback.**

1. **Convenção editorial** (Guia §4, Estilo): link para arquivo do próprio repositório é
   sempre relativo — `../rag-zero/rag_zero/bm25.py`. O motor o converte na URL pública; o
   GitHub o resolve nativamente ao ler o `.md`. **URL absoluta para o próprio repositório é
   proibida.**
2. **Fonte única de configuração**: `publicar/sumario.json` ganha
   `"repo": { "base": "https://github.com/GHDaru/rag", "ref": "v1.0" }`, e `GITHUB_BASE` é
   montado a partir dela. Se a tag não existir, cai para `main` **com aviso visível no log**
   — hoje não há nenhuma tag no repositório, então o fallback é o caminho vigente, e ele
   precisa ser barulhento para não virar silêncio permanente.
3. **Mesma fonte nos outros pontos** onde a URL do repositório está codificada, incluindo o
   rodapé EN de `build.mjs:78` (o bug).
4. **Mitigação obrigatória no download `.md`**: hoje o Markdown bruto é copiado literalmente
   para `docs/md/*.md`; com links relativos, eles resolveriam a partir de `docs/md/` e
   quebrariam. Ao gravar, aplicar a mesma normalização relativa → base pública. É a única
   consequência não óbvia desta decisão, e custa poucas linhas no mesmo bloco.

## Alternativas avaliadas

- **A — Manter absolutas e validar o path extraído da URL.** Prós: zero mudança de conteúdo.
  Contras: `main` segue codificada em 49 pontos; o leitor segue ejetado; ignora um
  mecanismo que já existe.
- **B — Caminho relativo (a escolhida, com E).** Prós: uma fonte de verdade; funciona nas
  duas superfícies; o link-check passa a poder validar **contra o disco**. Contras: migrar
  49 ocorrências (mecânico) e a mitigação do `docs/md/`.
- **C — Placeholder `{{repo}}`.** Prós: intenção explícita. Contras: quebra a leitura do
  `.md` no GitHub e no editor; **o link relativo já é esse placeholder** — e um que todas as
  superfícies entendem.
- **D — Publicar os alvos como páginas do site** (código transcluído no capítulo). Prós:
  acaba com a ejeção do leitor. Contras: escopo de rodada inteira; nem todo alvo deve virar
  página. Fica como direção pós-1.0.
- **E — Base na tag da edição em vez de `main` (adotada junto de B).** Prós: o trecho citado
  não muda debaixo do leitor — Princípios I e IV aplicados ao próprio repositório. Contras:
  exige que a tag exista; daí o fallback.

## Justificativa

O critério que decide é o Princípio I aplicado ao repositório: **afirmação sem verificação é
retórica**. Hoje o livro faz 49 afirmações sobre onde o próprio código está e nenhuma delas
é conferida por portão nenhum. A forma relativa não é uma preferência de estilo — é a única
que torna a afirmação **verificável contra o disco**, porque só ela é um caminho que existe
no sistema de arquivos no momento do build.

A tag (E) resolve um problema mais sutil e do mesmo tipo: com `main`, o leitor da edição 1.0
clica e vê o código de amanhã. Um livro que data a captura no cabeçalho de cada capítulo não
pode apontar para um alvo móvel no corpo.

## Consequências

- **Positivas:** renomear branch, publicar tag ou mover o repositório passa a ser **uma
  linha** de configuração. O link-check deixa de ter ponto cego: **100% dos links do livro**
  — internos e de repositório — passam a ser validados pelo build. Três dos 49 apontam para
  governança (constituição, ADRs) e passam a ser navegáveis também no editor.
- **Custos aceitos:** 49 ocorrências migradas em 30 arquivos; o bloco de gravação do `.md`
  ganha a normalização.
- **Efeito imediato:** o bug do rodapé EM (`harness_engineering`) sai junto — é o mesmo
  hardcode, no mesmo arquivo.
- **Reversibilidade:** alta e mecânica nas duas direções.

## Como verificar

1. **No motor, no ponto da reescrita** (a correção de raiz): ao montar `repoRel`, checar
   `existsSync`; acumular as falhas e sair com erro no fim, no mesmo padrão do array
   `quebrados` que o link-check já usa.
2. **Proibição de regressão** (`verificar.py`): `grep` por `github.com/GHDaru/rag/` em
   `livro/**.md` retorna **zero**, com a mensagem "use caminho relativo; o motor resolve".
3. **Fonte única**: `blob/` aparece no máximo uma vez em `publicar/*.mjs` (a definição), e
   nenhuma URL de `harness_engineering` aparece em `publicar/`.
4. **Sanidade da referência**: se `ref` for uma tag, o build confere que ela existe; se não
   existir, cai para `main` com aviso no log — nunca em silêncio.

## Nota de correção na spec 002

A spec 002 registrou "49 URLs absolutas em **32** arquivos". A contagem real, conferida ao
escrever este ADR, é **49 ocorrências em 30 arquivos**. O número de ocorrências estava
certo; o de arquivos, não. Corrigido na spec — a regra de evidência vale para o texto do
próprio processo, não só para o do livro.
