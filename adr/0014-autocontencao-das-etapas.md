# 0014 — Autocontenção das etapas: núcleo único testado, delta como artefato derivado

- **Status:** Aceito
- **Data:** 2026-08-13
- **Contexto (feature/spec):** `002-portoes-e-cadencia`
- **Emenda:** constituição 3.0.0 → 3.1.0 (restrição 4 da construção)

## Contexto

A restrição 4 da constituição exige "etapas **autocontidas** e executáveis". A palavra veio
do livro irmão, onde significa uma coisa concreta: o `harness-zero` tem 13 diretórios, cada
um com um `app.py` completo, e a tese declarada no README daquele projeto é que *"você pode
abrir qualquer uma e rodá-la sem as anteriores — e o diff entre etapas consecutivas é a
lição do capítulo"*.

O `rag-zero` fez outra escolha, sem registrá-la: um **núcleo compartilhado** (`rag_zero/`,
12 módulos) com 9 scripts em `etapas/` que o importam, e **48 testes** que o harness-zero
não tem. Cada script roda sozinho — sem rede, sem credencial, sem dependência externa, sem
ter executado a etapa anterior. Mas `git diff etapa05 etapa06` deixou de ser uma lição:
mostra a *chamada nova*, não a *evolução do sistema*.

Traduzindo o desacordo: a palavra "autocontida" esconde **duas propriedades diferentes**.

- **Executabilidade isolada** — o leitor roda a etapa N sem ter feito a N-1. *Preservada, e
  testável.*
- **Legibilidade do delta** — o leitor **vê** o que a etapa N acrescentou. *Perdida.*

A troca é defensável. O problema é que ela não está escrita em lugar nenhum, e a
constituição vigente diz o contrário do que o código faz.

## Decisão

**Manter o núcleo único testado e recuperar a lição do diff como artefato derivado.** Três
peças:

### 1. A constituição passa a distinguir as duas propriedades

Nova redação da restrição 4 (bump para **3.1.0** — muda restrição da construção, não
princípio):

> **Anti-apodrecimento** — modelo atrás de `LLMPort`; **cada etapa é executável
> isoladamente** — um comando, sem rede, sem credencial, sem dependência externa e **sem
> depender da execução das etapas anteriores** — sobre um **núcleo único e testado**
> (`rag_zero/`), e não sobre cópias por etapa: cópia divergente é a forma mais comum de
> apodrecimento, e o teste é o que impede o núcleo de apodrecer. **A lição do diff entre
> etapas consecutivas é preservada por artefato derivado** — o delta de módulos e símbolos
> que cada etapa acrescenta, gerado e publicado —, nunca por duplicação de diretório. Erros
> didáticos deliberados são comentados como tais.

### 2. O delta volta, gerado

- **Bloco "O que esta etapa acrescenta"** no cabeçalho de cada `etapaNN_*.py`, em formato
  fixo: etapa anterior, símbolos novos usados, decisão que a etapa introduz. É a prosa do
  *fading* (4C/ID) que hoje só existe no README.
- **`rag-zero/DIFF.md` gerado** por `ferramentas/diff_etapas.py`: a partir dos imports de
  cada script, a tabela `etapa N-1 → N: módulos novos · símbolos novos · testes que passam a
  valer`. O diff vira **saída verificável**, não convenção de diretório.
- **Testes atribuídos a etapas**, para que "a prova da etapa 5" deixe de ser prosa e vire
  consulta. *(Ver a nota de correção ao final: a implementação atribui por **seção** do
  arquivo de testes, não por nome de função — e a mudança é deliberada.)*

### 3. Guia §5 e `rag-zero/README.md` acompanham a redação nova

## Alternativas avaliadas

- **A — Reverter para 13 diretórios snapshot.** Prós: paridade com o livro irmão; diff
  literal; o leitor baixa um diretório. Contras: 12 módulos × ~12 etapas de duplicação;
  contradiz a **restrição 2** (a porta nasce por refatoração — com 13 cópias ela nasceria
  13 vezes e divergiria); os 48 testes viram uma suíte sobre a última cópia (as anteriores
  apodrecem sem ninguém ver) ou 13 suítes duplicadas.
- **B — Manter e só emendar a constituição.** Prós: barato e honesto. Contras: perde a lição
  do diff, que o livro irmão demonstra ter valor pedagógico real.
- **C — Núcleo único + delta derivado (a escolhida).**
- **D — Gerar os snapshots por etapa a partir do pacote.** Prós: diff literal sem
  duplicação mantida à mão. Contras: o gerador teria de saber qual subconjunto de cada
  módulo existia na etapa N — frágil —, e cria uma segunda árvore de código que o leitor
  confunde com a fonte. Fica **reabrível pós-1.0** se o delta gerado se mostrar insuficiente.

## Justificativa

A propriedade que a restrição 4 quer proteger — o nome dela é *anti-apodrecimento* — é a
**executabilidade isolada**, e ela está preservada e é testável. A duplicação por diretório
não protege contra apodrecimento: ela é um **vetor** de apodrecimento, porque a cópia 3
diverge da 11 e nenhum teste percebe. O livro irmão paga esse preço conscientemente por não
ter suíte; aqui há 48 testes, e jogá-los fora para ganhar um diff seria trocar a garantia
pela ilustração.

E o diff não precisa da duplicação: ele é uma **função** do que cada etapa importa. Gerar é
mais barato que manter, e o gerado pode ser verificado contra a fonte — a cópia manual, não.

## Consequências

- **Positivas:** a constituição volta a descrever o que o código faz (Princípio I aplicado
  ao próprio repositório); o delta vira verificável; `pytest -k eNN` fecha a promessa da
  coluna "Prova" do README.
- **Custos aceitos:** o leitor não pode mais baixar *um diretório* e ter a etapa — precisa
  do repositório (que já é o caso, e continua sem dependência externa). O diff perde a
  literalidade do `git diff`.
- **Emenda registrada:** constituição 3.1.0, com nota no `HISTORICO.md` (Princípio VII
  permite emenda direta, exige registro).
- **Reversibilidade:** média. Voltar para snapshots é possível a qualquer momento; o que
  este ADR impede é fazê-lo **sem** decidir.

## Nota de correção — 2026-08-13, após a revisão independente

A redação original deste ADR prometia **testes renomeados por etapa**, para que
`pytest -k e05` selecionasse a prova da etapa 5. O revisor independente rodou o comando:
`48 deselected`. A promessa estava "Aceita" e o repositório não a entregava — que é
exatamente o defeito que este ciclo existe para consertar, cometido pelo próprio ciclo.

**A implementação divergiu de propósito, e a divergência é a escolha melhor.** O mapeamento
teste ↔ etapa vem da **seção** do arquivo de testes (`# Etapa N — ...`), não do nome da
função, porque mapear por nome convidaria a **renomear teste para o portão ficar verde** —
a forma mais barata de mentir para um verificador. As seções já estavam lá, escritas por
quem escreveu os testes: são registro, não adaptação ao instrumento.

O que se corrige aqui é o **texto**, não a decisão: a decisão sempre foi "a prova de cada
etapa tem de ser consultável". `pytest -k` era um meio, e um meio pior. O texto acima foi
ajustado; esta nota fica para que a correção não apague o erro.

## Como verificar

`rag-zero/ferramentas/verificar_etapas.py`, acionado no CI junto do R1 da spec 002:

1. **Executabilidade isolada** — cada `etapas/etapa*.py` roda em diretório temporário, com
   ambiente limpo e `socket` bloqueado, e sai com 0. Prova "sem rede, sem credencial".
2. **Independência entre etapas** — AST de cada script: nenhum import de outra etapa; só
   stdlib e `rag_zero.*`. Prova "sem depender das anteriores" e "zero dependências" de uma
   vez.
3. **Delta declarado** — todo script tem o bloco de cabeçalho no formato fixo.
4. **`DIFF.md` em dia** — regenerar e comparar. Diff velho nunca finge ser atual.
5. **Etapa ✅ tem teste** — cada linha ✅ do README referencia ao menos um teste, e o
   contador de `def test_` bate com o número publicado (fecha também o achado A4 da spec).
