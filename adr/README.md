# ADR — Architecture Decision Records

Registros de decisões arquiteturais e editoriais do projeto. Cada decisão relevante (que tem alternativas e consequências) vira um ADR: **contexto → decisão → alternativas avaliadas → justificativa → consequências**. Assim o *porquê* fica rastreável, não só o *o quê* (que já está nos specs e no HISTORICO).

Convenção: arquivos `NNNN-titulo-curto.md`, numerados em sequência. Status: `Proposto` · `Aceito` · `Substituído por NNNN` · `Descontinuado`.

> **Herança (edição 0.1).** Os ADRs 0001–0007 foram **herdados do livro irmão *Engenharia de Harness***, que compartilha com este projeto o método editorial, o motor de publicação e o modelo de governança. Eles são mantidos **como escritos** — reescrever um ADR apaga a decisão que ele registra — e por isso citam exemplos daquele domínio (harnesses, `harness-zero`). A **decisão** que cada um documenta continua valendo aqui; só os exemplos são de outro livro. ADRs a partir do 0009 são deste projeto — e o 0009 é o primeiro, escrito na abertura do ciclo da edição 1.0.
>
> Uma remoção: o **0008** (Radar diário automatizado) saiu do índice — o Radar está fora do escopo da v1 e volta na rodada 6 do ROADMAP, quando ganha ADR próprio.

## Índice
- [0001 — Modelo de publicação (main=live, branch por spec, release p/ DOI)](0001-modelo-de-publicacao.md) · Aceito
- [0002 — Licenciamento duplo (CC BY 4.0 + MIT)](0002-licenciamento-duplo.md) · Aceito
- [0003 — Reescrita do cap. 01 com história + método](0003-fundamentos-rigor.md) · Aceito
- [0004 — Cross-link de citações (MVP) e Apêndice "O estudo"](0004-citacoes-e-apendice.md) · Aceito
- [0005 — Template dos capítulos: um spec de motor, verificação por capítulo](0005-template-capitulos-um-spec.md) · Aceito
- [0006 — Design system: entregáveis como componentes de tela](0006-design-system-componentes.md) · Aceito
- [0007 — Cadência de revisão do livro vivo](0007-cadencia-livro-vivo.md) · **Substituído por 0013**
- [0009 — Escopo da edição 1.0](0009-escopo-da-edicao-1-0.md) · Aceito
- [0010 — O companion na 1.0: serviço local verificável, deploy pós-1.0](0010-companion-na-1-0.md) · Aceito
- [0011 — Política de siglas: quatro classes, uma regra cada](0011-politica-de-siglas.md) · Aceito
- [0012 — A etapa 14 entra parcial na 1.0](0012-etapa-14-parcial.md) · Aceito
- [0013 — Cadência do livro vivo (RAG): janela trimestral e quatro gatilhos de domínio](0013-cadencia-livro-vivo-rag.md) · Aceito · *substitui o 0007*
- [0014 — Autocontenção das etapas: núcleo único testado, delta como artefato derivado](0014-autocontencao-das-etapas.md) · Aceito · *emenda a constituição para 3.1.0*
- [0015 — Links para o próprio repositório: caminho relativo, base única, tag da edição](0015-links-para-o-proprio-repositorio.md) · Aceito
- [template](template.md)
