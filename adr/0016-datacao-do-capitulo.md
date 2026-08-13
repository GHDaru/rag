# 0016 — Datação do capítulo: captura e revisão, sem edição

- **Status:** Aceito
- **Data:** 2026-08-13
- **Contexto (feature/spec):** `002-portoes-e-cadencia`

## Contexto

O ciclo 002 fecha como **edição 1.1**, e isso expôs um defeito no cabeçalho de capítulo.
Hoje ele diz:

```
> **Estado da arte capturado em 2026-08** · edição 1.0 · [histórico e registro de expiração](../HISTORICO.md)
```

E `r2_datacao` exige que **os 25 capítulos** declarem a edição vigente. Bumpar para 1.1
obrigaria a reescrever 25 cabeçalhos — incluindo os **19 capítulos que ninguém releu**.

Isso é a armadilha do ciclo 001 voltando por outra porta. Lá, uma checagem de datação boa
demais forçou reescrever fatos históricos para ficar verde (a lição está no docstring de
`r2_datacao`, e ela fica). Aqui o campo é outro — `edição` em vez de `capturado em` —, mas o
dano é da mesma classe: **atualizar metadado sem trabalho editorial é barato e invisível**.

Três fatos, verificados por comando antes de decidir, mudam o desenho:

| # | Fato | Como foi conferido |
|:---:|---|---|
| 1 | **O campo `edição` nunca chega ao leitor.** O motor substitui o blockquote de datação pelo *hero*, cujos chips são montados por `extrairDatas()` — que lê **só** `capturado em` e `última revisão`. | `grep "edição 1.0" docs/06-busca.html` → vazio |
| 2 | **O motor já sabe renderizar o campo que falta**, e ele está vazio: `última revisão` tem extração e rótulo i18n, e **zero** ocorrências no livro. | `grep -rc "última revisão" livro/` → 0 |
| 3 | **O livro irmão resolveu isto por data, não por edição.** Os 15 capítulos dele têm `última revisão` variando por capítulo sobre uma captura idêntica — e **nenhum** declara edição. | `grep -rc "edição [0-9].[0-9]" .../capitulos/` → 0; `última revisão` → 15/15 |

Ou seja: hoje o **único consumidor** de `edição X.Y` no cabeçalho de capítulo é o próprio
verificador. Um campo que só o portão lê é um campo que existe para satisfazer o portão.

## Decisão

**O cabeçalho de capítulo declara `capturado em` e `última revisão`. A edição sai dele.**

```
> **Estado da arte capturado em 2026-08** · última revisão 2026-08-13 · [histórico e registro de expiração](../HISTORICO.md)
```

A edição continua sendo cobrada — mas dos **artefatos que falam da obra**: `README.md`,
`CLAUDE.md`, `rag-zero/README.md`, `CITATION.cff`, `.zenodo.json` e o `HISTORICO.md`.

E `r2_datacao` deixa de comparar contra uma constante e passa a comparar contra **evidência**:

1. **A edição vigente é derivada do `HISTORICO.md`**, não de uma constante escrita à mão. A
   saída barata para o verde deixa de ser editar um literal e passa a ser **escrever a
   entrada da edição** — que exige prosa sobre o que mudou e a atribuição do modelo.
2. **Edição em cabeçalho de capítulo vira falha**, com mensagem que aponta para cá. A
   checagem não só para de exigir o campo: impede que ele volte.
3. **O git arbitra as datas do capítulo.** `última revisão` não pode ser mais nova que o
   último commit que tocou o arquivo (data sem diff é trabalho que não existe), nem mais
   velha (o arquivo mudou e o cabeçalho não). E a captura só avança com diff no corpo,
   descontada a própria linha de datação — **diff vazio com captura nova é a assinatura
   literal de "datar uma mentira"**.
4. **Sem git, as checagens de evidência viram aviso explícito**, nunca silêncio. Checagem
   que não pôde rodar precisa dizer isso; passar por ausência de fonte é a versão
   automatizada de afirmar sem evidência.

## Alternativas avaliadas

- **A — Bumpar os 25 para 1.1.** Prós: um número só, regex trivial. Contras: produz 19
  afirmações falsas sob a leitura que o leitor faz; **a saída mais barata para o verde é um
  `sed` em 25 arquivos** — a assinatura exata do ciclo 001; e polui o `git log` de 19
  capítulos com um commit que não corresponde a trabalho editorial, destruindo a única
  evidência externa de quem foi mexido.
- **B — Bumpar só os tocados.** Prós: honesto. Contras: o campo passa a significar coisas
  diferentes em capítulos diferentes, e **um campo com duas semânticas é pior que dois
  campos**. Pior: a saída mais barata para o verde passa a ser **declarar que releu**.
- **C — Captura + revisão, sem edição (a escolhida).**
- **D — "revisto na edição X.Y" ao lado da revisão.** Duas expressões da mesma coisa (a
  edição é derivável da data via Histórico), com risco de divergirem — o defeito que o ADR
  0011 e o `adr15_fonte_unica` já combateram aqui.
- **E — "edição vigente: ver Histórico", sem número.** Nunca mente e nunca informa. Remove o
  dano sem entregar o ganho.

## Justificativa

O Princípio IV manda distinguir **três datas** — evento, captura, rodada — e atribui o
cabeçalho do capítulo à **captura**. A edição é o identificador da **rodada**, e a rodada tem
página própria. Pôr um dentro do outro mistura dois dos três eixos que o princípio manda
separar.

E o critério que decide entre as opções é o **custo relativo da mentira**. Sob A e B, ficar
verde mentindo custa um `sed`. Sob C, o campo que resta é confrontável com o git: mentir
passa a exigir **produzir um diff** — que é exatamente o que releitura de verdade produz, e
o que a revisão humana consegue ver.

Há também o que o leitor ganha, que hoje ele não tem: a **idade do texto**, distinta da idade
da foto. Um capítulo que levou um conserto de link não precisa mais fingir releitura, e um
capítulo não relido não precisa parecer abandonado.

## Consequências

- **Positivas:** cada campo com uma semântica só; o chip novo aparece **sem uma linha de
  código no motor** (fato 2); paridade com o livro irmão, verificada; e o convite mensal a
  25 edições mecânicas deixa de existir.
- **Custos aceitos:** migração única nos 25 cabeçalhos — com as datas **lidas do git**, não
  digitadas. Uma migração que digitasse 25 datas à mão cometeria o pecado que este ADR
  resolve. Perde-se saber "de que edição é este `.md`" olhando só o fonte; o link para o
  Histórico, na mesma linha, devolve.
- **Custo de partida, declarado:** a migração toca os 25 arquivos, então **todos saem com
  `última revisão 2026-08-13`** — inclusive os que só tiveram o cabeçalho alterado. É
  literalmente verdade (o texto mudou hoje) e é pouco informativo: **o campo só começa a
  discriminar a partir do próximo ciclo**, quando apenas os capítulos efetivamente tocados
  mudarem de data. Registrar isso é preferível a fingir uma distribuição de datas que a
  migração destruiu.
- **Risco conhecido:** rebase ou cherry-pick reescrevem datas de commit e podem deixar a
  checagem 3 vermelha sem que nada esteja errado no texto. A mensagem de falha manda
  **diagnosticar antes de corrigir o cabeçalho**.
- **Efeito no Guia:** a §2 descreve o cabeçalho como `data de captura · edição · maturidade ·
  link`, e passa a `data de captura · última revisão · link` **mais** a linha de maturidade,
  que é separada.

## Uma correção ao parecer que originou este ADR

O parecer afirmou que *"maturidade não existe em nenhum dos 25 cabeçalhos reais
(verificado)"*. **É falso:** `grep -rc "Maturidade" livro/capitulos/*.md` retorna **22
arquivos**. O que é verdade — e é o que importava para o argumento — é que a maturidade não
está na **linha de datação**, e sim numa linha própria do mesmo bloco.

Fica registrado porque o Princípio I vale para o parecer que embasa a decisão, e não só para
o texto do livro. A recomendação não dependia dessa afirmação; as três que a sustentam foram
conferidas uma a uma e se confirmaram.

## Como verificar

```bash
python3 specs/001-edicao-1-0/verificar.py     # r2_datacao_e_edicao: as quatro checagens
grep -rc "· edição" livro/capitulos/          # → 0
grep -rLc "última revisão" livro/capitulos/   # → vazio (todos declaram)
```
