# 0010 — O companion na 1.0: serviço local verificável, deploy pós-1.0

- **Status:** Aceito
- **Data:** 2026-08-09
- **Contexto (feature/spec):** `001-edicao-1-0`

## Contexto

O livro afirmava, em três lugares, que o `chat-companion` **"é o `rag-zero` rodando em
produção — e o exemplo real que o livro disseca"**. A afirmação é falsa em **dois**
níveis, não em um:

1. **Não está no ar.** Publicar exige contas em três serviços de terceiro, credenciais e
   custo recorrente do autor — nada que uma execução autônoma possa ou deva fazer.
2. **Não é o `rag-zero`.** Nenhum módulo do companion importa `rag_zero`. O próprio
   código já dizia a verdade: *"reimplementado aqui porque o companion precisa ser
   deployável sozinho"* (`ragindex.py`). O canônico é `rag_zero/bm25.py`; o companion tem
   uma **cópia**. "É o `rag-zero` rodando" ≠ "reimplementa o desenho do `rag-zero`".

**E essa mesma frase já falhou uma vez.** O `HISTORICO.md` registra que, até a edição 0.4,
o companion pontuava por sobreposição crua de termos *"enquanto seu próprio docstring o
descrevia como o BM25 da etapa 8 do `rag-zero`"*. A frase já correu à frente do código
antes, e foi corrigida **à mão**. Isso é o dado decisivo: **o problema não é redação, é
ausência de portão.** Reescrever sem instalar verificação deixa a mesma armadilha armada.

Dois fatos favoráveis: o site **já degrada corretamente** (sem `companion_backend`
preenchido, o motor não injeta o widget — não há chat quebrado publicado), e o backend
**funciona e tem testes**.

## Decisão

**Manter o código, rebaixar a afirmação ao que é verificável, e tornar a execução local o
produto da 1.0.** O companion deixa de ser "o `rag-zero` em produção" e passa a ser:

> o desenho do `rag-zero` levado a um serviço — as mesmas portas e o mesmo BM25 (*Best
> Matching 25*) Okapi da etapa 5, reimplementados para o backend rodar sozinho — que
> **roda localmente com um comando, sem chave, sem banco e sem custo**. **Não há
> instância pública**; o deploy é pós-1.0.

E — a parte que as opções puramente redacionais não têm — **um portão automático que
amarra a força da afirmação ao estado configurado**:

- `scripts/check-companion.sh`: se `companion_backend` está **vazio**, nenhuma afirmação
  no presente sobre publicação pode existir fora de `adr/` e `HISTORICO.md` (imunes por
  desenho: registro histórico não se reescreve). Se está **preenchido**, exige `/health`
  respondendo. **Publicar sem atualizar o texto quebra tanto quanto afirmar sem
  publicar.**
- Um **teste de paridade**: o top-k do `BookIndex` do companion tem de coincidir, em
  ordem, com o de `rag_zero.bm25` sobre o mesmo corpus. É o que transforma *"o mesmo BM25
  da etapa 5"* de afirmação em **contrato**.

## Alternativas avaliadas

- **A — Publicar agora.** Prós: torna a frase verdadeira no sentido forte. Contras:
  **inexequível** numa execução autônoma (contas, credenciais, custo do autor); amplia a
  superfície de segredo vivo sem política de rotação (Princípio V); e prende a
  acessibilidade a custo zero (Princípio VI) a um *free tier* de terceiro.
- **B — Arquivar o companion.** Prós: elimina a afirmação eliminando o objeto. Contras:
  destrói código funcionando e testado, que é o único artefato "livro em produção" do
  repositório, e regride trabalho de três edições. Custo alto para um problema de
  redação e verificação.
- **C — Serviço local verificável + portão (a escolhida).**
- **D — Manter a frase e datá-la como promessa.** **Rejeitada.** O Princípio IV data o
  que **é**; ele não converte futuro em presente. Afirmação no presente sobre estado
  inexistente é a violação do Princípio I que o ADR 0009 registrou como causa raiz — e
  seria a **reincidência** do episódio já documentado no histórico.

## Justificativa

O defeito não é o companion estar desligado — é **o livro afirmar, no presente, algo que
não pode demonstrar**. O Princípio I não exige que o companion esteja no ar; exige que o
que se afirma sobre ele seja verificável de primeira mão.

E execução local é **melhor evidência que um deploy**: o leitor a reproduz. Um endpoint
público exige que ele confie; um comando na própria máquina, não.

A alternativa C é também a única que trata as **duas** metades do problema. A frase
errada é sintoma; a ausência de portão é a causa — e é ela que fez o mesmo erro acontecer
duas vezes.

## Consequências

- **Positivas:** a afirmação passa a ser reproduzível por qualquer leitor; a paridade com
  o `rag-zero` vira contrato testado em vez de promessa; nenhum segredo novo entra em
  jogo; o `DEPLOY.md` isola o manuseio de credencial.
- **Negativas / custos aceitos:** a promessa "no ar" fica pendente mais uma edição; o
  critério de conclusão da rodada 3 muda de "companion no ar" para "companion
  respondendo em execução local verificável".
- **Reversibilidade:** alta, e **engenheirada**. Quando o autor decidir publicar, ele
  preenche `companion_backend`; o portão **inverte de polaridade** e passa a exigir que a
  frase forte volte, com data. O interruptor já existe no motor de publicação.
