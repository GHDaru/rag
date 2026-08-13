# Histórico e Registro de Expiração

> O livro é vivo (Princípio IV): toda edição é datada, registrada e **atribuída** — inclusive quanto ao modelo de IA usado, porque saídas de LLM não são determinísticas e a rastreabilidade é parte do rigor.
>
> Esta página tem duas metades: o **histórico de edições** (o que mudou, quando, por quem) e o **registro de expiração** (o placar das apostas do cap. 24 — previsões feitas com data, para serem cobradas depois).

## Histórico de edições

### Edição 1.1 — 2026-08-13 · Os portões acionados, e a cadência que faltava

**O que é.** A 1.0 fechou coerente. Uma auditoria comparativa com o livro irmão, em contexto
fresco, mostrou que ela fechou **frágil**: os portões existiam e ninguém os acionava, e o
livro cuja tese central é a cláusula de expiração não tinha política de quando expira.

**Como esta edição foi decidida.** Três decisões foram levadas a um arquiteto em contexto
próprio, e o parecer dele foi **verificado nos três pontos factuais antes de virar ADR** —
inclusive contra o texto da própria spec, que estava errado (dizia "49 URLs em 32 arquivos";
são 30). As decisões viraram [ADR 0013](../adr/0013-cadencia-livro-vivo-rag.md) (cadência),
[0014](../adr/0014-autocontencao-das-etapas.md) (autocontenção das etapas) e
[0015](../adr/0015-links-para-o-proprio-repositorio.md) (links para o repositório).

**O que estava errado, e foi corrigido:**

- **O CI não acionava portão nenhum.** Fazia `build` → `pdf` → deploy. O verificador, as
  duas suítes e o `check-companion.sh` existiam e nunca rodavam — e `rag-zero/**` nem
  disparava o workflow. Um portão que não é acionado não é portão.
- **O ADR 0007 estava "Aceito" e nunca foi implementado**, porque o mecanismo dele é de
  outro domínio: a janela dele executa "re-sync dos 16 forks", corpus que não existe aqui.
- **Os 49 links para o próprio código eram invisíveis ao portão.** O motor já convertia
  caminho relativo em URL do GitHub; as URLs absolutas contornavam esse mecanismo e, por
  serem externas, nenhuma era validada. O livro fazia 49 afirmações sobre onde o próprio
  código está e o build dizia verde para todas.
- **A constituição descrevia um `rag-zero` que não existe.** Ela exigia "etapas
  autocontidas"; a trilha trocou os diretórios-snapshot por um núcleo único com 48 testes,
  e a troca não estava registrada.
- **Treze capítulos falavam do futuro no tempo errado**, remetendo à rodada 2 — concluída em
  2026-08-09, com os 22 Apêndices A preenchidos.
- **A seção "Fontes da indústria" era a que menos citava fonte.** O cap. 22 afirmava que
  *"há registro público de vulnerabilidades"* **sem um identificador**.
- **A "Leitura executiva" tinha virado o capítulo comprimido** — 1.050 a 1.500 caracteres
  num parágrafo único, quando o gênero (*how-to*, no Diátaxis) pede passos executáveis.

**O que a 1.1 acrescenta:**

- **Seis portões no CI**, rodando **antes** do build — publicar e só então descobrir que o
  portão falhou é o mesmo que não ter portão.
- **Cadência declarada** (Guia §7): janela trimestral, **próxima em 2026-11**, e quatro
  gatilhos de domínio. Com uma regra que decide se isso funciona ou apodrece: **recapturar a
  data só onde houve releitura** — datar sem reler passa em qualquer verificador e falsifica
  o livro.
- **Um portão que o tempo consegue quebrar sozinho.** As checagens de cadência ficam
  vermelhas sem ninguém commitar nada, e um workflow agendado abre issue quando a janela
  vence. Foi a mudança de natureza deste ciclo: até aqui, tudo dependia de alguém mexer.
- **A execução isolada de cada etapa virou teste**, não promessa: cada uma roda em diretório
  temporário, ambiente limpo e `socket` derrubado. E a lição do diff volta **gerada**
  (`rag-zero/DIFF.md`), porque o delta é função do que cada etapa importa — e função se
  calcula.
- **Sete fontes da indústria lidas de primeira mão** nos caps. 06, 07, 15 e 22, incluindo a
  *Model Spec* da OpenAI (que escreve a regra do cap. 22 do lado do provedor) e o
  **CVE-2025-32711**. O "registro público" agora tem número.

**O primeiro gatilho extraordinário, no dia em que a política nasceu.** Ao conferir as fontes
do cap. 22, o **G1 disparou**: a página oficial do OWASP virou arquivo histórico e remete a
uma edição publicada em **2026-08-04** — nove dias antes desta captura — que o site novo
**não deixa ler**. A afirmação "*prompt injection* é LLM01 em todas as edições publicadas"
tinha nove dias e já era mais forte que a evidência. O livro passou a dizer **menos**, e o
gatilho ficou registrado como aberto.

**O que foi relido, e o que não foi.** Releitura de conteúdo, com fonte conferida: **06, 07,
15, 21 e 22**. Correção pontual, sem releitura: os treze capítulos cuja linha de maturidade
remetia a uma rodada já concluída (02, 03, 04, 11, 12, 13, 14, 16, 17, 18, 20, 21, 23). Os
demais **mantêm a captura de 2026-08** — o que não foi relido não teve a data de captura
mexida, que é a regra do [ADR 0013](../adr/0013-cadencia-livro-vivo-rag.md) aplicada ao
próprio ciclo que a criou. A partir desta edição, o cabeçalho declara **`última revisão`** em
vez de edição, e essa data é conferida contra o git ([ADR 0016](../adr/0016-datacao-do-capitulo.md)).

**A dívida declarada, com contagem:** 45 bullets de "Fontes da indústria" seguem sem URL nem
declaração, e 22 "Leituras executivas" seguem em parágrafo único — nos capítulos fora do lote
deste ciclo. As duas checagens reportam a contagem como aviso: dívida declarada não é dívida
escondida, e o número existe justamente para que o próximo ciclo não possa fingir que ela
diminuiu sem trabalho.

**Atribuição:** direção editorial e decisão de escopo — Gilsiley Henrique Darú. Pareceres,
construção e redação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-13.

---

### Edição 1.0 — 2026-08-09 · A primeira versão

**O que é.** A versão em que o que o livro **afirma** e o que ele **entrega** coincidem — e em que o leitor consegue **construir**, não só decidir.

**Como esta edição foi decidida.** Dois pareceres independentes, em contexto fresco, sem contato entre si. Cada acusação foi **verificada contra o repositório antes de virar plano**. Todas se confirmaram, e os dois chegaram à mesma causa por caminhos diferentes: *o livro não estava bloqueado por falta de conteúdo, e sim por incoerência entre o que afirmava e o que entregava.* As decisões viraram [ADR 0009](../adr/0009-escopo-da-edicao-1-0.md) (escopo), [0010](../adr/0010-companion-na-1-0.md) (companion) e [0011](../adr/0011-politica-de-siglas.md) (siglas).

**O que estava errado, e foi corrigido:**

- **O rastro de processo não existia.** Cinco edições produzidas sem um único `plan.md` — que é **o lugar físico onde o Constitution Check mora**. Sem ele, o ciclo não tinha portão. `specs/` sequer existia, e o contador apontava para uma spec do livro irmão.
- **O estado se contradizia.** O `README.md` anunciava "Edição 0.2" com a vigente em 0.6, e afirmava, a duas linhas de distância, que os Apêndices A estavam preenchidos **e** enfileirados. 29 cabeçalhos de capítulo com a edição errada.
- **O metadado de citação citava o livro anterior.** `CITATION.cff` e `.zenodo.json` descreviam o objeto da constituição 2.0.0, revogada.
- **O livro afirmava algo que não podia demonstrar.** "O companion é o `rag-zero` rodando em produção" era falso em dois sentidos: não estava no ar, e nenhum módulo importava `rag_zero`. **A mesma frase já tinha corrido à frente do código na 0.4** — o que mostrou que o problema não era redação, era **ausência de portão**.
- **O leitor não conseguia construir.** 20 dos 25 capítulos sem um único bloco de código; o cap. 15 prescrevia o prompt de fundamentação e **nunca o mostrava** — os caps. 06, 11 e 15 passaram a exibir o artefato, e a exigência virou checagem (R7); os 25 "Mão na massa" descreviam a trilha em prosa, sem arquivo, sem comando e sem saída esperada; e o `rag-zero` **não estava no sumário** — para quem lia o site, a espinha 4C/ID não existia.
- **Siglas órfãs, inclusive a do título.** *Retrieval-Augmented Generation* nunca era expandida no corpo.

**O que a 1.0 acrescenta:**

- **Um verificador como portão** (`specs/001-edicao-1-0/verificar.py`): cada critério de aceite virou um `pass/fail`. Ele reporta **zero** falhas hoje. O número de partida não entra aqui: o instrumento foi reescrito no meio do ciclo (ADR 0011), e comparar contagens de versões diferentes do verificador é maçã com laranja — exatamente o que o Princípio I proíbe quando exige a condição experimental ao lado. *Prove, não afirme* vale para o próprio relatório.
- **Dois portões permanentes**: `scripts/check-companion.sh`, com invariante **bidirecional** — afirmar sem publicar quebra, e publicar sem atualizar o texto também; e um **teste de paridade** que transforma "o mesmo BM25 da etapa 5" de afirmação em contrato.
- **A escada de execução visível**: os 22 "Mão na massa" com arquivo, comando e saída esperada; o `rag-zero` no sumário; e as cinco etapas não construídas **declaradas como tal**, nunca descritas no presente.
- **A trilha em 12 das 17 etapas construídas** — 9 com script próprio para rodar, as outras 3 como módulo coberto por teste — e **48 testes** — incluindo a **linha de base** (etapa 2, o *Naive RAG*), sem a qual nenhuma tabela de ganho do livro comparava com nada.
- **Política de siglas em quatro classes**, com o motor expandindo a primeira ocorrência de cada página — o que entrega o que a regra editorial queria com **zero palavras a mais no fonte**.

**O que fica fora, por decisão e não por esquecimento:** medição própria de técnicas · catálogo exaustivo · Radar · edição em inglês · DOI e PDF consolidado · instância pública do companion · etapas 11–13, 15 e 16 da trilha. Tudo no ROADMAP como pós-1.0.

**A dívida declarada:** 13 referências seguem ⏳ (nenhuma sustenta sozinha uma tese de capítulo) e o cap. 04 continua sendo o de base mais fraca — a área trata ingestão como pré-processamento e raramente a estuda.

**Atribuição:** direção editorial e decisão de escopo — Gilsiley Henrique Darú. Pareceres, construção e redação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-09.

### Edição 0.6 — 2026-08-09 · O "G" construído, e a árvore que não condensava

**O que é.** A rodada 3 avança para as duas etapas que faltavam no miolo: o **gerador fundamentado** (etapa 10) e o **RAPTOR** (etapa 9). São 39 testes agora, ainda sem uma única dependência externa.

**A etapa 10 — o "G" do RAG, que até aqui não existia no código.** Um sistema que recupera bem e gera mal erra **com fontes ao lado**, o que é pior porque parece confiável. A etapa constrói o prompt de fundamentação com as três exigências do cap. 15 e — a parte que quase nenhum tutorial faz — **verifica a citação por código**. Três adaptadores encenam os três modos de falha, e o verificador os distingue:

| Modo | O que acontece | Por que importa |
|---|---|---|
| **Citação inválida** | cita `[T7]`, que não estava no contexto | o mais perigoso: a resposta **parece** verificável — tem colchete, tem número, tem cara de fonte |
| **Sem citação** | responde de memória, sem apontar fonte | não prova que inventou; prova que **não dá para conferir** |
| **Abstenção** | responde `NAO_ENCONTRADO` | não é falha — é a resposta certa quando falta base, e por isso conta como fundamentada |

E a primeira porta da abstenção acontece **antes** de qualquer chamada: sem trechos, o modelo não é chamado. Chamar um gerador sem material e torcer para que ele recuse é pagar por uma alucinação provável.

**A etapa 9 — e o defeito que ela revelou.** A primeira versão do RAPTOR usava limiar de agrupamento fixo em `0.35`, como fazem os tutoriais. A árvore **degenerou**: 180 folhas viravam 141 nós, quase todos com um filho só. Um RAPTOR que não condensa não é RAPTOR — é a mesma lista com passos extras.

Medindo a distribuição de similaridade no corpus com o embedder desta trilha: **mediana 0,049, percentil 99 em 0,314**. O limiar fixo agrupava menos de 1% dos pares. A correção não foi chutar outro número — foi **derivar o limiar do corpus** por percentil, que é a mesma regra que o livro já repete para o limiar de reranking (cap. 07) e para o peso da fusão (cap. 06): **similaridade não é comparável entre embedders**. Com o corte derivado, a árvore condensa como deve: **180 → 55 → 24 → 12**.

**As ressalvas declaradas, porque a trilha não finge.** O resumidor é **extrativo**: escolhe as frases mais centrais e nunca produz uma frase que não estava lá. Isso é bom para procedência e ruim para o que dá poder ao RAPTOR — a **síntese**. E o embedder segue sendo o de *hashing*, sem semântica, o que atenua o ganho na pergunta global. Trocar os dois é uma linha cada, porque estão atrás de portas.

**Estado:** etapas 0, 3–6, 9 e 10 ✅ · 14 parcial 🟡 · demais especificadas. Companion em produção segue pendente.

**Atribuição:** direção editorial — Gilsiley Henrique Darú. Construção e redação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-09.

### Edição 0.5 — 2026-08-09 · O livro começa a executar

**O que é.** A rodada 3 começa: o `rag-zero` sai do papel. As **etapas 0 e 3–6** estão construídas, executáveis e testadas — **29 testes, sem rede, sem GPU, sem credencial e sem uma única dependência externa**. O corpus é o texto deste livro.

**O que roda hoje:**

- **Etapa 0** — o contador de tokens por bloco, que é o instrumento do livro. Imprime a composição do contexto e delimita o bloco externo como dado, nunca instrução.
- **Etapa 3** — a ingestão, com o teste que dá nome ao cap. 04: um documento `revogado` **não** é recuperado, mesmo ranqueando melhor que o vigente. E o teste da outra metade: um extrator que **erra** não custa nada, porque metadado gerado não filtra de forma dura.
- **Etapa 5** — BM25 Okapi em ~40 linhas (IDF, saturação, normalização por comprimento), busca densa, fusão por posição, e a tabela de ganho por estágio.
- **Etapa 6** — reranking usando a **nota** como limiar, e o caminho de abstenção: a pergunta fora do corpus abstém, e a taxa de resultado zero deixa de ser zero.

**O achado desconfortável que a etapa 5 imprime — e que fica.** No corpus deste livro, **fundir BM25 com o embedder de *hashing* piora a precisão** (0,525 → 0,425). É exatamente o que o cap. 06 prevê quando o embedder não carrega semântica, e a trilha o mantém visível em vez de esconder: o adaptador barato tem o ponto cego da busca esparsa **com o custo da densa**. Trocar por um modelo real é uma linha, porque ele está atrás de uma porta — e há um teste que fixa o defeito como contrato, para quebrar quando alguém fizer a troca.

**A correção que a construção revelou.** Escrever o BM25 de verdade expôs que o **chat companion** vinha pontuando por **sobreposição crua de termos** — sem IDF, sem normalização por comprimento — **enquanto seu próprio docstring o descrevia como "o BM25 da etapa 8 do rag-zero"**. Não era. O livro afirma que o companion *é* o `rag-zero` rodando; a afirmação só passou a ser verdadeira agora. O ranking melhorou de forma visível: consultas que antes caíam em blocos longos e genéricos agora caem no capítulo certo.

**Uma armadilha de medição, corrigida e transformada em lição.** A primeira versão da tabela da etapa 5 reportava `context_recall` contra um gabarito que marcava **todos** os blocos do capítulo-alvo como relevantes. Com `k=5` e dezenas de relevantes, o teto matemático é ~0,12 — o número parecia péssimo **por construção**, não por defeito da busca. A métrica certa para a pergunta ("o pipeline acha o lugar certo do livro?") é **taxa de acerto**. O erro virou uma função documentada e um teste (`test_recall_tem_teto_quando_o_gabarito_e_grande`), porque é o tipo de engano fácil de cometer e difícil de perceber.

**Estado:** etapas 0 e 3–6 ✅ · 14 parcial 🟡 · demais especificadas. O companion em produção segue pendente.

**Atribuição:** direção editorial — Gilsiley Henrique Darú. Construção e redação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-09.

### Edição 0.4 — 2026-08-09 · Os 22 Apêndices A, e a rodada 2 fechada

**O que é.** O item que faltava para concluir a rodada 2: o **tratamento por implementação**. O Princípio II exige que a fonte-base seja a técnica reprodutível — *paper* **mais** implementação pública — e o corpo dos capítulos recebia só a primeira metade. Os apêndices eram um "enfileirado: X · Y · Z".

**O que mudou:** os **22 Apêndices A** passaram de fila a conteúdo. Cada um é uma tabela com a implementação de referência, URL, e — a parte que dá valor — **a pegadinha**: o que a documentação não diz e o livro aprendeu a perguntar. Alguns exemplos do que só aparece aí:

- **Self-RAG exige treino.** O método treina o modelo a emitir *reflection tokens*; se você não vai treinar nem usar um modelo já treinado assim, o padrão simplesmente não está disponível — enquanto o CRAG é *"plug-and-play"*. É a diferença que decide qual dos dois você consegue adotar, e ela não está no corpo do capítulo.
- **O cache semântico precisa da permissão na chave.** Sem isso ele serve a resposta de um usuário a outro — o incidente do cap. 04 entrando por outra porta.
- **O índice vetorial aproximado troca recall por latência.** Recall que cai sem explicação costuma ser parâmetro de busca do índice, não o modelo de embedding.
- **O *late chunking* degrada em silêncio** quando o documento excede o embedder de contexto longo.
- **Um dicionário de três colunas** (cap. 02) mostrando que LangChain, LlamaIndex e Haystack convergem na mesma anatomia e divergem só no vocabulário — o argumento de aprender componentes em vez de framework, demonstrado em tabela.

**Verificação dos links.** Os 32 repositórios citados foram conferidos **um a um** contra o repositório real, com o README lido para confirmar que é o projeto certo. O acesso direto ao GitHub está bloqueado nesta sessão para repositórios fora do escopo; a conferência foi feita por `raw.githubusercontent`, que resolve. Uma correção veio daí: `anthropics/anthropic-cookbook` foi renomeado para *Claude Cookbooks*.

**Rodada 2 concluída.** Os três critérios: ≥60% em ✓ (**76%**), nenhum número sem condição experimental, e **22 de 22 Apêndices A preenchidos**. O que sobrou — 13 referências de menor peso e a evidência do cap. 04 — migra para a rodada 4, onde vira **medição própria** em vez de busca bibliográfica.

**Atribuição:** direção editorial — Gilsiley Henrique Darú. Redação e verificação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-09.

### Edição 0.3 — 2026-08-04 · Rodada 2: o livro passa a ser citável

**O que é.** A rodada de **evidência**. Até aqui o livro tinha um mapa de fontes e nenhuma delas conferida — 55 referências ⏳, zero ✓. Esta edição leva **42 delas (76%) a ✓**, acima do critério de 60% da rodada.

**O que foi feito:**

- **Os 49 identificadores arXiv do repositório foram resolvidos contra o arXiv real**, com um ID falso de controle para provar que o teste discrimina. **Nenhum inventado, nenhum título divergente.** A citação alucinada — a falha mais corrosiva possível num livro assim — está descartada como classe.
- **42 referências passaram a ✓**: texto lido, afirmação do livro conferida contra o original.
- **As ~20 técnicas nomeadas que estavam sem URL ganharam fonte primária.** RAPTOR, Self-RAG, CRAG, FLARE, Adaptive RAG, HyDE, step-back, late chunking, proposição e GraphRAG entraram no livro pela porta dos guias de praticante, e a rodada 2 confirmou que **todas chegam ao paper que as propôs**. O que se revelou distorcido foi um número, não uma técnica.
- **Condição experimental ao lado de cada número validado** — o modelo de 540B do Chain-of-Thought, o GPT-4 acoplado ao RAPTOR, o cenário zero-shot sem rótulo do HyDE, o custo por milhão de tokens do *contextual retrieval*.

**As quatro correções — o resultado mais valioso da rodada:**

1. **✗ *Lost in the Middle* não sustentava a afirmação do cap. 20.** O livro dizia que a degradação em contexto longo "não é linear com o comprimento, é dirigida pela similaridade entre alvo e distratores", e citava aquele paper. Ele estabelece degradação **posicional** e não trata de distratores. Pior: a fonte que **de fato** mede distratores (relatório *Context Rot*, 18 modelos) contradiz a outra metade — isolando a variável, **o comprimento degrada sozinho**, mesmo em tarefa trivial. O certo é "é o comprimento, e distratores próximos tornam a queda mais íngreme". Era a afirmação que o próprio livro marcava como a mais frágil; estava frágil pelos dois lados.
2. **✗ As quatro métricas não são todas do paper do RAGAS.** O original propõe **três** — *faithfulness*, *answer relevance*, *context relevance*. O par *context precision* / *context recall* é da **biblioteca**, que desdobrou o terceiro. O livro construiu um capítulo inteiro sobre o quarteto atribuindo-o à fonte errada.
3. **⚠ O `67%` do *contextual retrieval* ganhou a curva inteira**: taxa de falha no top-20 caindo de 5,7% para 3,7% (técnica sozinha), 2,9% (com BM25) e 1,9% (com reranker). O número que circula é o da pilha completa.

**Nota de método que vale registrar.** A primeira consulta automática ao PDF do RAGAS devolveu uma citação **inventada** — "We propose four metrics" — que teria confirmado o erro do livro em vez de revelá-lo. Só apareceu porque o texto foi extraído e lido diretamente. **Resumo automático de fonte não é validação.** É exatamente para isso que o status ✓ existe.

**O que a validação também **acrescentou** ao livro, além de corrigir:** cinco **métricas intrínsecas de chunking** que permitem avaliar o corte sem pipeline inteiro (cap. 05); a *heterogeneous memory contamination* e a cura por papel funcional na escrita (caps. 19, 22); o corpus sintético ficcional do U-NIAH como método para separar recuperação de memorização (cap. 20); e a precisão de que *zero-shot* e *few-shot* são irmãos sob **In-Context Learning**, não pares dos outros quatro ramos (cap. 12).

**Estado da evidência:** **42 ✓ · 13 ⏳ · 3 ✗**. As 13 restantes são de menor peso estrutural — nenhuma sustenta sozinha uma tese de capítulo. **Fica aberto** o preenchimento dos Apêndices A, que é o item restante do critério de conclusão da rodada.

**Atribuição:** direção editorial — Gilsiley Henrique Darú. Validação, correções e redação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-04.

### Adendo 0.2.1 — 2026-08-04 · Geração de metadado, e a dívida da renumeração

**A pergunta do editor:** *"na ingestão, acredito que teremos coisas do tipo geração de metadados, etc, ou não é isto?"* — e estava certo: o cap. 04 listava "enriquecimento" numa linha de tabela e depois só tratava do metadado **que já existe** (origem, data, permissão). A camada onde o metadado é **criado** é justamente a parte cara e mais rendosa da ingestão, e faltava.

**O que mudou:**

- **Cap. 04 ganha duas seções.** *Geração de metadado* — as três procedências (**herdado**, **derivado**, **gerado**), e o que vale gerar em ordem de retorno: resumo contextual (que é o *contextual retrieval* do cap. 09 sob outro nome), **perguntas hipotéticas** (HyDE invertido e movido para a indexação, pago uma vez em vez de em toda consulta), vigência extraída da prosa, classificação, entidades. E *o metadado gerado errado é pior que o ausente* — a falha silenciosa em que o documento certo some **antes** da busca, com o log mostrando uma consulta normal; daí a regra de que metadado gerado **impulsiona, nunca filtra de forma dura**.
- **A dívida da renumeração 0.2, paga.** A reestruturação renumerou os capítulos mas não alcançou o **aparato**: o catálogo de técnicas inteiro ainda apontava para a numeração original (busca em "09", RAPTOR em "10"), o glossário tinha o cluster de recuperação errado, e cinco capítulos citavam partes do sumário antigo ("a Parte II adiciona superfície de ataque"). Corrigido em 16 referências de capítulo e nas três páginas de aparato.
- **Catálogo reorganizado** na ordem das partes atuais, com as técnicas dos dois capítulos removidos retiradas e as da geração fundamentada (cap. 15) acrescentadas. As "sete que valem começar por aqui" viram **oito**, e agora começam pelo corpus — não pelo prompt.
- **Glossário** com os verbetes que a edição 0.2 passou a exigir: os quatro paradigmas, contrato, procedência, fusão por posição, metadado gerado, abstenção, fundamentação, atribuição por afirmação, multi-hop, pergunta global.

**Atribuição:** crítica editorial — Gilsiley Henrique Darú. Redação e correção — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-04.

### Edição 0.2 — 2026-08-04 · O livro vira *Engenharia de RAG*

**A crítica que originou a rodada**, do editor: o livro anterior (*Engenharia de Prompt e Engenharia de Contexto*) **duplicava o livro irmão**. Quatro capítulos — memória, compactação, ferramentas/MCP, segurança de contexto — eram território do *Engenharia de Harness*, e o que era genuinamente deste livro (corpus, recuperação, RAG avançado, agêntico) estava espremido no meio. A crítica estava certa.

**O que mudou:**

- **Nome e objeto.** O livro passa a ser **Engenharia de RAG** — *como se constrói um sistema em volta da recuperação da informação*. Cunhagem nossa, como "Engenharia de Harness"; a pesquisa confirmou que não existe termo consagrado (existe **RAG**, universal, e *Information Retrieval*, o campo que o absorveu — há track de RAG no TREC).
- **Constituição 3.0.0.** Princípio VIII reescrito: o objeto é o **sistema**, todo capítulo declara o **componente da arquitetura** que aprofunda, e a **fronteira com o livro irmão** é explícita — gestão de contexto de agente é de lá; aqui entra só o que decide a recuperação ou a fundamentação.
- **Três capítulos novos**, que fechavam a lacuna real: **02 — Anatomia de um Sistema de RAG** (dois caminhos, 16 componentes, os contratos), **03 — Arquiteturas de Referência** (Naive → Advanced → Modular → Agêntico, e os quatro padrões de fluxo) e **15 — Geração Fundamentada** (o "G" que faltava: grounding, citação verificável, abstenção).
- **A Parte III desdobrada** em cinco capítulos (busca, reranking, consulta, avançada, estruturada), onde antes havia dois.
- **A Parte IV mantida inteira** — os seis capítulos de engenharia de prompt ficam, agora a serviço da geração. Decisão do editor, contra a proposta inicial de condensá-los.
- **Dois capítulos removidos** (compactação; ferramentas e MCP) e devolvidos ao livro irmão; o que era de RAG neles foi absorvido pelos caps. 19 e 18.
- `contexto-zero` → **`rag-zero`**, com 17 etapas realinhadas.

**A correção de evidência que esta edição registra:** a survey de Gao et al. ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997)) — **a referência mais citada de RAG** — não constava do levantamento da edição 0.1. Falha do panorama, que trouxe a revisão sistemática e a de RAG agêntico e passou batido pela fundacional. Ela agora ancora os caps. 01–03, junto de *Modular RAG* (2407.21059). Registrar a omissão é mais útil que corrigi-la em silêncio.

**Estado da evidência:** segue **nenhuma referência com status ✓**. A validação é a rodada 2.

**Atribuição:** crítica editorial, decisão de nome e de escopo — Gilsiley Henrique Darú. Pesquisa de terminologia, reestruturação e redação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-04.

### Edição 0.1 — 2026-08-04 · Fundação: o esqueleto das duas disciplinas

**O que é.** A primeira versão pública do livro. Estabelece a moldura (prompt × contexto, com RAG dentro da segunda), o sumário completo em três partes, os 19 capítulos com esqueleto e explicação de abertura, o catálogo de técnicas, o mapa do ecossistema e o glossário.

**O que foi feito:**
- **Constituição 2.0.0** — derivada da 1.2.0 do livro *Engenharia de Harness* (mesmo método pedagógico e editorial, domínio novo). Princípio II reescrito: a fonte-base deixa de ser "o código de harnesses" e passa a ser **paper + implementação pública**. Princípio VIII criado: fixa a moldura do par e o lugar do RAG.
- **Levantamento da comunidade** — [panorama](../estudos/2026-08-03-panorama-comunidade.md) cruzando academia (surveys estruturantes), repositórios públicos, frameworks e técnicas, e respondendo à pergunta que originou o projeto ("engenharia de contexto substitui RAG?" — não como substituto, como moldura).
- **Sumário em três partes** — Parte I (Engenharia de Prompt, caps. 11–17), Parte II (Engenharia de Contexto, caps. 20–14, com RAG em três capítulos), Parte III (o sistema em produção, caps. 21–23), mais abertura (00–01) e fechamento (18).
- **Aparato** — catálogo de técnicas, apêndice do ecossistema, glossário, bibliografia com status de validação, grafo do livro.
- **Motor de publicação** adaptado: PT-only, sem Radar, com o grafo remapeado para o novo domínio.

**Fora do escopo, por decisão explícita:** edição em inglês, Radar de atualização automática, benchmark quantitativo de frameworks, e a trilha prática `rag-zero` (descrita nos capítulos, implementada na rodada 3). Ver [ROADMAP](../ROADMAP.md).

**Estado da evidência (honestidade obrigatória, Princípio I):** **nenhuma referência tem status ✓ nesta edição.** Todas estão marcadas ⏳ na [bibliografia](bibliografia.md) e `[a validar]` nos capítulos. Os capítulos declaram maturidade "esboço" ou "fundação" no cabeçalho. A validação é a rodada 2.

**Atribuição:** direção editorial e decisões — Gilsiley Henrique Darú. Pesquisa, estruturação e redação assistidas por **Claude (Anthropic)**, modelo Opus 5, em sessão de 2026-08-03/04. Levantamento por busca aberta na web, sem acesso a bases pagas.

### Adendo 0.1.1 — 2026-08-04 · Técnicas nomeadas e o teto do corpus

Rodada curta, disparada por três guias de praticante indicados pelo editor ([análise no panorama §6](../estudos/2026-08-03-panorama-comunidade.md#6-adendo-2026-08-04--guias-de-praticante-sobre-rag-em-produção)). Um quarto guia devolveu HTTP 403 e fica como pendência declarada.

**O que entrou:**
- **Seis técnicas nomeadas** que o esqueleto tratava de forma genérica: RAPTOR (cap. 09), Self-RAG / CRAG / FLARE / Adaptive RAG (cap. 18), step-back prompting (cap. 09), sentence-window e proposition chunking (cap. 06). Todas ⏳, na fila da rodada 2.
- **Dois padrões que a organização revelou** e que não estavam escritos: *desacoplar a unidade de busca da unidade de entrega* (cap. 06) e *as materializações de RAG agêntico diferem por onde mora o julgamento* (cap. 18).
- **Sinais de produção** (cap. 21): taxa de resultado zero, distribuição de nota do reranker, taxa de citação, p99 por camada. E o **cache semântico** com seu modo de falha (cap. 23).
- **Seção nova "O teto que ninguém mede: o corpus"** (cap. 06) — frescor, procedência, deduplicação. Declarada como a seção mais fraca da edição.

**O que NÃO entrou, e é o registro que importa:** nenhum número das três fontes. São secundárias (praticante citando proponente), e o panorama §6.2 documenta o caso de **deriva numérica** do *contextual retrieval* — o 67% da Anthropic, que é resultado de três estágios cumulativos, aparece em fonte secundária como mérito de um só. Também ficou registrado como não utilizável o "80% das falhas de RAG vêm da ingestão", que circula **sem fonte alguma**.

**Pergunta editorial aberta para o editor:** governança/ingestão do corpus merece **capítulo próprio** na Parte II, ou continua como seção do cap. 06? É hoje a única parte do pipeline que nenhuma das três partes do livro cobre.

**Atribuição:** direção editorial — Gilsiley Henrique Darú (indicação das fontes). Análise, verificação e redação — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-04.

### Adendo 0.1.2 — 2026-08-04 · O corpus vira capítulo

Decisão editorial do autor sobre a pergunta deixada em aberto no adendo 0.1.1: **governança e ingestão do corpus merecem capítulo próprio.**

- **Novo [cap. 04 — Ingestão e Governança do Corpus](capitulos/04-corpus.md)**, inserido **antes** da recuperação. A ordem é o argumento: o corpus é o teto de tudo que os caps. 06–18 otimizam, e quem aprende a otimizar antes de conhecer o teto passa meses ajustando `top_k` num corpus que nunca poderia responder bem.
- **Renumeração**: os antigos caps. 04–23 passam a 10–19. O `rag-zero` ganha a etapa 8 (ingestão) e passa a 18 etapas.
- **O capítulo declara a própria fragilidade**: é o de base científica mais fraca do livro, porque a literatura de RAG trata ingestão como pré-processamento e raramente a estuda. Fica registrada a pergunta que a rodada 2 deve responder — *existe medição publicada do impacto isolado de frescor e deduplicação sobre métricas de RAG?* Se não existir, vira experimento próprio na rodada 4.

**Atribuição:** decisão editorial — Gilsiley Henrique Darú. Redação e renumeração — **Claude (Anthropic)**, modelo Opus 5, sessão de 2026-08-04.

---

## Gatilhos extraordinários abertos

Eventos que dispararam um gatilho do [Guia §7](GUIA-EDITORIAL.md) fora da janela, e o que
o livro fez com eles. **Gatilho aberto é dívida declarada** — o livro diz menos, não mais.

| # | Data | Gatilho | Evento | O que o livro fez |
|:---:|:---:|:---:|---|---|
| G-01 | 2026-08-13 | **G1** | A página oficial do *OWASP Top 10 for LLM Applications* virou **arquivo histórico** e remete à **OWASP GenAI LLM Top 10 2026**, publicada em **2026-08-04** — nove dias antes desta captura. O site do projeto novo **recusa leitura automatizada**, e não conseguimos conferir o conteúdo dela. | O cap. 22 e o apêndice de ecossistema passaram de *"prompt injection é LLM01 em todas as edições publicadas"* para **"nas edições que conferimos"**, com a edição 2026 declarada como não lida. O livro **não afirma** o que ela traz. Fica aberto até alguém ler a fonte. |

Este é o primeiro gatilho registrado, e ele apareceu **durante a verificação que criou a
política** — o que é a melhor evidência possível de que a política era necessária: a
afirmação "em todas as edições publicadas" tinha nove dias de idade e já era mais forte que
a evidência que a sustentava.

---

## Registro de expiração

O placar das apostas registradas no [cap. 24](24-convergencias.md). Uma aposta só vale se puder ser julgada — por isso cada uma tem critério de verificação e prazo.

| # | Aposta | Feita em | Prazo | Critério | Veredito |
|---|---|:---:|:---:|---|:---:|
| A1 | A metade sintática da saída estruturada (cap. 13) vira funcionalidade trivial e o capítulo encolhe para uma seção do cap. 11 | 2026-08 | 2027-08 | o capítulo é fundido | ⏳ aberta |
| A2 | Orçamento explícito de contexto vira prática padrão, com painel de composição por fonte | 2026-08 | 2028-02 | ferramentas de observabilidade trazem pronto | ⏳ aberta |
| A3 | Otimização automática de prompt **não** substitui a escrita manual na maioria dos projetos, mas vira padrão em alto volume | 2026-08 | 2028-08 | adoção reportada em levantamentos | ⏳ aberta |
| A4 | Nenhuma defesa por prompt contra injeção indireta será considerada suficiente | 2026-08 | 2028-08 | recomendação vigente do OWASP | ⏳ aberta |
| A5 | Avaliação de trajetória/conversa deixa de ser lacuna e ganha ferramenta madura | 2026-08 | 2027-08 | ferramenta adotada com métricas de sessão | ⏳ aberta |
| A6 | O rótulo "engenharia de contexto" perde força e o conteúdo é absorvido por "engenharia de sistemas de IA" | 2026-08 | 2028-08 | uso do termo na literatura e em vagas | ⏳ aberta |

**Como o placar é fechado:** na revisão de cada prazo (rodada 6 e seguintes), cada aposta recebe ✅ (confirmada), ❌ (refutada) ou 🔄 (ainda indefinida, com novo prazo). **Aposta refutada não é apagada** — é o registro mais valioso desta página, porque mostra onde o livro errou e por quê.

## Três datas, sempre distintas

O livro distingue rigorosamente (Princípio IV):

- **Data do evento** — quando a coisa descrita aconteceu (o paper foi publicado, a funcionalidade foi lançada).
- **Data de captura** — quando este livro olhou para aquilo. É a data no cabeçalho de cada capítulo.
- **Data da rodada** — quando a revisão sistemática aconteceu. É a data desta página.

Confundir as três é o erro que faz um livro técnico parecer atual quando não é.
