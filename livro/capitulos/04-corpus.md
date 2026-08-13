# 04 — Ingestão e Governança do Corpus

> **Estado da arte capturado em 2026-08** · edição 1.0 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço novo.** Componentes que aprofunda: **aquisição, extração e enriquecimento** (cap. 02). É o capítulo **menos apoiado em evidência** do livro — a área trata ingestão como pré-processamento e raramente a estuda. A rodada 2 procurou e **não encontrou** medição publicada do impacto isolado de frescor e deduplicação — a lacuna é da área, não do capítulo, e vira experimento próprio na rodada 4.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Explicar** por que a qualidade de recuperação tem um teto definido antes de qualquer decisão dos caps. 06–18;
2. **Descrever** o pipeline de ingestão e onde cada etapa destrói ou preserva informação;
3. **Especificar** o metadado que todo chunk carrega — herdado, derivado e **gerado** — justificando cada campo por uma decisão que ele habilita;
4. **Decidir** o que vale gerar por modelo, e por que metadado gerado errado é pior que metadado ausente;
5. **Projetar** a política de atualização de um índice: o que entra, o que sai, e quando.

## O problema

Os três capítulos seguintes ensinam a buscar melhor. Este capítulo é sobre o fato inconveniente que os precede: **você só pode buscar o que está no índice, e do jeito que foi colocado lá.**

O sintoma é conhecido de quem opera RAG em produção, e a causa quase nunca é procurada onde está:

- O sistema cita com confiança uma política **revogada há oito meses** — porque um documento revogado tem exatamente o mesmo embedding de um vigente. O índice não sabe o que é verdade; sabe o que é parecido.
- A mesma informação aparece em cinco documentos e ocupa **cinco lugares** do `top_k`, deslocando o trecho que faltava.
- Duas versões do mesmo procedimento conflitam, e a resposta depende de qual ranqueou melhor — o que é o mesmo que dizer: depende da sorte.
- Um usuário recebe conteúdo de outro cliente, porque a permissão não era um campo do índice.
- Metade do corpus são PDFs cuja extração produziu texto embaralhado, e ninguém olhou.

Nenhum desses problemas é resolvido por busca híbrida, reranking, *contextual retrieval* ou RAG agêntico. Eles são **anteriores** — e é por isso que este capítulo vem antes.

Há também um argumento de ordem pedagógica: o leitor que aprende a otimizar antes de aprender o que limita a otimização passa meses ajustando `top_k` num corpus que nunca poderia responder bem.

## Fundamentos científicos

Este é o capítulo com a base científica mais fraca do livro, e a honestidade exige dizer por quê: **a literatura acadêmica de RAG concentra-se na recuperação e na geração; a ingestão é tratada como pré-processamento e raramente é o objeto de estudo.** A qualidade de corpus é discutida sobretudo em engenharia de dados, um campo que a literatura de RAG cita pouco.

O que existe, e ancora parcialmente o capítulo:

- **Chunking como objeto de estudo** — a linha que avalia estratégias de corte em vez de assumi-las ([arXiv 2504.19754](https://arxiv.org/abs/2504.19754)) e que propõe seleção adaptativa por documento ([arXiv 2603.25333](https://arxiv.org/abs/2603.25333)) é a parte da ingestão que **tem** tratamento formal. O tratamento operacional dela fica no cap. 06, junto da recuperação. `[a validar]`
- **Tópicos que atravessam documentos** — [arXiv 2601.05265](https://arxiv.org/abs/2601.05265) trata o corte considerando o corpus, e não o documento isolado. É o trabalho mais próximo de "a ingestão precisa de visão de conjunto". `[a validar]`
- **Contaminação de base de conhecimento** — a literatura de segurança sobre envenenamento de memória e de corpus ([arXiv 2605.28009](https://arxiv.org/abs/2605.28009)) chega ao mesmo lugar por outro caminho: **o caminho de escrita para o índice é superfície de ataque** (cap. 22). `[a validar]`

**Lacuna declarada:** não localizamos, neste levantamento, trabalho que meça o impacto isolado de *frescor*, *deduplicação* e *procedência* sobre métricas de RAG. Se existir, é a referência mais valiosa que falta ao livro. Se não existir, é uma lacuna real da área — e uma candidata a experimento próprio na rodada 4.

## Fontes da indústria

- **O argumento de governança** — a leitura de fornecedores de catálogo de dados: *"retrieval quality is ultimately bounded by what is in the index"*, com governança como **pré-requisito** e não etapa posterior; ativos certificados, glossário de negócio e linhagem melhorariam a confiabilidade da recuperação. **Fonte interessada** — quem vende catálogo tem motivo para dizer isso — e por isso o livro adota o argumento (que se sustenta por lógica) e **não** os números que o acompanham (ver [panorama §6](../../estudos/2026-08-03-panorama-comunidade.md)).
- **A afirmação que circula sem fonte** — "80% das falhas de RAG remontam à camada de ingestão e chunking" aparece em guias de praticante **sem referência a medição alguma**. É plausível, é citável, e é exatamente o tipo de número que vira consenso sem nunca ter sido medido. Fica registrado aqui como **não utilizável** — e como exemplo do que o Princípio I existe para barrar.
- **A prática convergente** — o que os praticantes descrevem fazer, independentemente do número: pipeline de ingestão versionado, reindexação incremental por mudança, e metadado de permissão aplicado **antes** da busca.

## O estado da arte

### 1. O pipeline de ingestão, e onde cada etapa perde informação

| Etapa | O que faz | O que se perde se malfeita |
|---|---|---|
| **Aquisição** | busca os documentos na fonte | documentos que ninguém sabia que existiam; ou os que não deveriam estar lá |
| **Extração** | PDF/HTML/planilha → texto | tabelas viram sopa de números; ordem de colunas; notas de rodapé grudadas no corpo |
| **Normalização** | limpeza, encoding, cabeçalhos repetidos | ou de menos (ruído em todo chunk) ou de mais (some a estrutura) |
| **Deduplicação** | remove ou funde repetições | orçamento do `top_k` desperdiçado; ou perda de uma variante que importava |
| **Enriquecimento** | metadado: origem, data, seção, permissão, versão | **tudo que o cap. 06 precisa para filtrar antes de buscar** |
| **Chunking** | corte na unidade indexável | contexto da fronteira (tratamento no cap. 06) |
| **Indexação** | embeddings, índice léxico, estruturas | — |

A etapa mais subestimada é a **extração**. Um pipeline com reranking de última geração sobre texto de PDF mal extraído é engenharia cara em cima de lixo — e o defeito é invisível nas métricas do cap. 21, porque o *context recall* mede se o chunk certo veio, não se o chunk certo faz sentido. **Ler uma amostra do texto extraído, com olhos humanos, é a verificação de maior retorno deste capítulo** e leva uma tarde.

### 2. O metadado mínimo

Cada campo se justifica por uma decisão que habilita. Se não habilita decisão nenhuma, não é metadado — é peso morto:

| Campo | Decisão que habilita |
|---|---|
| `origem` (documento, URL, sistema) | citar a fonte na resposta; invalidar em bloco quando a fonte se revela ruim |
| `data` (do conteúdo, não da ingestão) | filtrar por vigência; ordenar versões; expirar |
| `versao` / `status` (vigente, revogado, rascunho) | **não recuperar o revogado** — o problema nº 1 deste capítulo |
| `secao` / caminho hierárquico | reconstruir o contexto do trecho (cap. 06) |
| `permissao` | filtrar **antes** de buscar — requisito de segurança (cap. 22) |
| `hash` do conteúdo | deduplicar; detectar mudança sem reprocessar |

As duas linhas em negrito são as que quase nenhum pipeline tem, e as duas que causam os incidentes mais caros: responder com política revogada, e vazar conteúdo entre clientes.

### 3. Geração de metadado: a camada cara e rendosa

A seção anterior trata do metadado que **já existe**. Esta trata do que precisa ser **criado** — e é aqui que a ingestão deixa de ser encanamento e vira a etapa onde mais se ganha recuperação.

Metadado tem três procedências, e elas não merecem a mesma confiança:

| Procedência | De onde vem | Custo | Confiança |
|---|---|---|---|
| **Herdado** | a fonte já tinha (autor, data, caminho, permissão do sistema de origem) | ~0 | alta — e incompleto |
| **Derivado** | computado deterministicamente do conteúdo (hash, idioma, seção pela marcação, tamanho) | baixo | alta |
| **Gerado** | **inferido por modelo** (entidades, classificação, resumo, vigência lida do texto, perguntas hipotéticas) | alto | **variável — e é o ponto do capítulo** |

O que vale gerar, em ordem de retorno observado na prática:

- **Resumo contextual do trecho.** É exatamente o *contextual retrieval* do cap. 09 — e vale registrar a equivalência: **aquela técnica é geração de metadado**, só que o metadado gerado vai para dentro do texto embeddado em vez de para um campo.
- **Perguntas hipotéticas** que o trecho responde. O chunk passa a carregar as perguntas, não só as respostas — o que casa com a forma como o usuário escreve. É o HyDE (*Hypothetical Document Embeddings*) (cap. 08) invertido e movido para a indexação: paga-se uma vez em vez de em toda consulta.
- **Vigência e status** extraídos do texto ("esta política substitui a de 2023", "válido até"). É o campo que evita o incidente nº 1 do capítulo, e frequentemente ele só existe na prosa.
- **Classificação** por área, tipo e sensibilidade. Habilita filtro por permissão (cap. 06) e roteamento (cap. 08).
- **Entidades e relações.** Caro, e só se justifica se o grafo do cap. 10 estiver no plano — extrair entidades "para o caso de" é a forma mais comum de queimar orçamento de indexação.

### 4. O metadado gerado errado é pior que o ausente

Esta é a razão de a seção existir, e o ponto que quase nenhum material trata.

Metadado **ausente** faz o sistema deixar de filtrar — você recupera demais, e percebe. Metadado **errado** faz o sistema filtrar **errado** — e o documento certo desaparece antes da busca, sem deixar rastro.

O caso concreto: um classificador marca um documento jurídico como "RH". Ele some de toda consulta jurídica filtrada. O sintoma é *context recall* baixo sem explicação — e ninguém vai procurar a causa na ingestão, porque o log da busca mostra uma consulta perfeitamente normal.

Quatro mitigações, em ordem de importância:

1. **Nunca use metadado gerado para filtro duro.** Para excluir candidatos, use só o herdado e o derivado. O gerado serve para **ordenar e impulsionar**, onde o erro degrada em vez de sumir.
2. **Guarde a confiança junto do valor.** Um campo `area: "juridico"` sem a confiança do classificador é uma afirmação sem procedência — exatamente o que o cap. 02 diz para não fazer nas fronteiras.
3. **Revise uma amostra com gente** antes de confiar. Cinquenta itens lidos revelam viés sistemático do gerador que nenhuma métrica agregada mostra.
4. **Versione o extrator.** Quando ele muda, o metadado antigo é de outra versão — e comparar os dois como se fossem o mesmo campo produz conclusões falsas. É o mesmo raciocínio do cap. 21 sobre comparar números de conjuntos diferentes.

E a consequência econômica, que fecha o argumento do capítulo: **enriquecimento é onde a indexação fica cara**, e é para lá que a leitura de 2026 diz que os ganhos migraram. Isso torna a decisão do cap. 09 — empurrar trabalho para a indexação ou para a consulta — uma decisão que começa aqui, e não lá.

### 5. Frescor: o índice como coisa viva

Um índice não é um artefato de build — é um estado que precisa acompanhar a fonte. Três políticas, em ordem crescente de esforço:

- **Reconstrução total periódica.** Simples, cara, e deixa uma janela de desatualização do tamanho do período.
- **Incremental por mudança.** Reindexa o que mudou, via hash ou webhook da fonte. É o padrão razoável.
- **Expiração declarada por tipo.** Cada classe de documento tem validade (política: 1 ano; preço: 1 dia; documentação: por release). Passou do prazo sem revalidação, sai do índice ou entra marcado como potencialmente vencido.

O ponto que a maioria dos sistemas erra não é a política de **entrada** — é a de **saída**. Times constroem ingestão e esquecem a remoção; o índice acumula, e conteúdo revogado nunca sai porque ninguém definiu quem o tira. **Todo pipeline de ingestão precisa de um caminho de deleção, e ele precisa ser testado** — inclusive porque é requisito legal quando o corpus tem dado pessoal (cap. 19).

### 6. O corpus como superfície de ataque

Quem pode escrever no seu índice pode escrever no contexto do seu modelo. Isso faz da ingestão o mesmo tipo de fronteira que o cap. 22 descreve para memória e ferramentas:

- **Ingestão automática de fonte aberta** (web, e-mail, upload de usuário) é o caminho mais curto para *prompt injection* indireta — e o agravante do RAG é que o conteúdo malicioso pode ser **escrito para ranquear bem** nas consultas que interessam ao atacante.
- **Procedência por chunk** permite invalidar em bloco quando uma fonte se revela comprometida. Sem ela, a resposta a um incidente é reindexar tudo.
- **Aprovação para fontes novas** é barata e evita a classe inteira: um documento entra no índice de produção quando alguém decidiu que ele entra.

### 7. O que quase ninguém mede

O corpus é a única parte do pipeline que costuma não ter painel algum. Quatro números baratos:

- **Idade mediana do conteúdo** indexado — sobe sozinha, e ninguém percebe.
- **Taxa de duplicação** (chunks com hash repetido ou similaridade acima de um limiar).
- **Cobertura por fonte** — quantos documentos de cada sistema entraram, comparado ao que existe lá. Revela o que a aquisição está perdendo em silêncio.
- **Chunks nunca recuperados** — os que jamais apareceram em nenhum `top_k`. Ou são irrelevantes (e custam armazenamento e ruído), ou são invisíveis por um defeito de indexação. As duas respostas são acionáveis.

### Leitura executiva

Os capítulos seguintes ensinam a buscar melhor; este é sobre o **teto** que os precede — você só recupera o que está no índice, do jeito que foi colocado lá. Um documento **revogado embedda exatamente igual ao vigente**: o índice não sabe o que é verdade, sabe o que é parecido. **O que roubar, em ordem:** (1) leia uma amostra do **texto extraído** com olhos humanos — é a verificação de maior retorno do capítulo e leva uma tarde, e nenhuma métrica do cap. 21 a substitui; (2) exija dois campos de metadado que quase ninguém tem — **`versao`/`status`** (para não recuperar o revogado) e **`permissao`** (para filtrar antes de buscar); (3) escreva a política de **saída**, não só a de entrada — times constroem ingestão e esquecem a remoção, e o índice apodrece por acúmulo. **A fronteira de segurança:** quem escreve no índice escreve no contexto do modelo — ingestão automática de fonte aberta é o caminho mais curto para injeção indireta, e o conteúdo hostil pode ser escrito para ranquear bem (cap. 22). **A camada cara e rendosa é o enriquecimento:** metadado tem três procedências — herdado (da fonte), derivado (determinístico) e **gerado por modelo** — e só a terceira pode estar errada. Vale gerar, em ordem: resumo contextual (que é o *contextual retrieval* do cap. 09 sob outro nome), **perguntas hipotéticas** que o trecho responde (HyDE invertido, pago uma vez em vez de em toda consulta), vigência extraída da prosa, e classificação. **A regra que evita o incidente silencioso:** metadado gerado **nunca** filtra de forma dura — ele ordena e impulsiona. Metadado ausente faz recuperar demais, e você percebe; metadado errado faz o documento certo **sumir antes da busca**, e o log mostra uma consulta normal. Guarde a confiança junto do valor, revise uma amostra com gente, e versione o extrator. **Meça o que ninguém mede:** idade mediana do conteúdo, taxa de duplicação, cobertura por fonte, e chunks nunca recuperados.

## Mão na massa — `rag-zero`, etapa 3

Na etapa 3 você constrói o ingestor do `rag-zero` antes de qualquer busca: varre o `livro/`, extrai, normaliza, deduplica por hash e enriquece cada chunk com origem, seção, data e status. O teste que fecha a etapa é o que dá nome ao capítulo: um documento marcado como `revogado` **não** aparece em nenhuma recuperação, mesmo sendo o mais similar à consulta. Depois você acrescenta uma camada de **geração**: um classificador simples de área por capítulo e a extração de perguntas hipotéticas para um subconjunto — guardando a confiança junto do valor, e usando o resultado só para impulsionar, nunca para excluir. O exercício de completude: a política de expiração por tipo vem esqueletada — você define as validades e descobre que essa é uma decisão de produto, não de engenharia.

**Rode agora** — sem instalar nada, sem chave e sem GPU:

```bash
cd rag-zero
python3 etapas/etapa03_ingestao.py
```

Código: [`rag_zero/ingestao.py`](../../rag-zero/rag_zero/ingestao.py). O que você deve ver: o documento `revogado` ranqueando **melhor** sem governança, e sumindo com ela.
## Verificação

1. Seu RAG cita uma política revogada. Liste os pontos do pipeline onde isso poderia ter sido evitado, do mais barato ao mais caro.
2. Por que *context recall* alto (cap. 21) não prova que a sua extração de PDF está boa? O que provaria?
3. Sua taxa de "chunks nunca recuperados" é de 40%. Dê duas interpretações opostas e o experimento que as separa.
4. Um classificador marcou 3% dos documentos com a área errada, e você usa esse campo para filtrar. Descreva o sintoma que o time vai observar — e por que ele não vai procurar a causa aqui.

---

## Apêndice A — Como cada abordagem trata a ingestão

> Tratamento por implementação, com URL. **Este é o apêndice mais magro do livro, e a razão é honesta:** a área trata ingestão como encanamento e publica pouco sobre ela.

| Etapa | Implementação de referência | O que reter |
|---|---|---|
| **Extração** | bibliotecas de parsing de documento (por formato), com ou sem modelo de layout | **Pegadinha, e é a do capítulo:** nenhuma delas falha ruidosamente. PDF mal extraído produz texto plausível e embaralhado, e o pipeline segue. **Leia uma amostra com olhos humanos.** |
| **Geração de metadado** | uma chamada de LLM por documento, com schema (cap. 13) | resumo contextual, perguntas hipotéticas, vigência, classificação. **Pegadinha:** guarde a **confiança** junto do valor, e nunca filtre de forma dura com o gerado. |
| **Resumo contextual** | é o *contextual retrieval* do [cap. 09](09-recuperacao-avancada.md) visto daqui | a survey de Gao lista *"incorporation of metadata"* entre os refinamentos de indexação do Advanced RAG — o argumento deste capítulo tem âncora na survey de referência. |
| **Deduplicação** | hash exato para idênticos; similaridade para quase-idênticos | **Pegadinha:** o quase-idêntico costuma ser **versão diferente**, não duplicata. Deduplicar sem olhar `versao`/`status` apaga a atualização e mantém a revogada. |
| **Papel funcional na escrita** | a lição do [MemGuard](https://arxiv.org/abs/2605.28009), trazida da memória | atribuir a cada item um papel explícito **no momento em que entra** impede que coisas de naturezas diferentes sejam usadas como evidência intercambiável. Vale para memória e vale para corpus. |

**A lacuna declarada, que a rodada 2 confirmou existir:** não localizamos trabalho publicado que meça o impacto **isolado** de frescor, deduplicação e procedência sobre métricas de RAG. Duas buscas independentes, nada. Se não existir, é lacuna real da área — e vira **experimento próprio na rodada 4**.
