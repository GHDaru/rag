# Glossário

> Siglas por extenso e termos com o sentido **que este livro usa**. Quando um termo tem uso ambíguo na indústria, a ambiguidade está registrada — desambiguar é metade do trabalho (cap. 01).
>
> Edição 1.0 · captura em 2026-08. Verbetes novos entram quando o capítulo correspondente é aprofundado.

## A–C

**Abstenção** — o caminho pelo qual o sistema responde "não encontrei" em vez de responder com o que sobrou. Tem duas portas: antes da geração, quando nada passa do limiar (cap. 06), e durante a geração, quando o contexto não sustenta a resposta (cap. 15). A ausência das duas é o que transforma um retriever normal em máquina de alucinação.

**Adaptive RAG** — classificar a complexidade da pergunta e escolher o grau de esforço (sem busca, uma busca, laço). Trata o custo por pergunta como decisão, não como constante (cap. 18).

**Advanced RAG** — o segundo paradigma da taxonomia de Gao: o pipeline linear do *Naive RAG* com otimizações antes e depois da busca — indexação refinada, reescrita de consulta, busca híbrida, reranking. Continua linear (cap. 03).

**Alucinação** — afirmação produzida com confiança e sem sustentação. Em sistemas com recuperação, o caso perigoso é a *alucinação fundamentada em ruído*: o modelo usa trechos irrelevantes que foram recuperados por falta de um caminho de abstenção (cap. 06). Métrica associada: *faithfulness* (cap. 21).

**Answer relevance** — métrica que mede se a resposta endereça a pergunta feita. Não diz nada sobre correção (cap. 21).

**Atribuição por afirmação** — o nível mais alto de citação: cada afirmação da resposta aponta para o trecho que a sustenta, e não só a resposta inteira para uma lista de fontes. É o único nível que permite verificar sem reler tudo — e o único caro (cap. 15).

**BEIR** — *Benchmark for Information Retrieval*: conjunto de avaliação de recuperação zero-shot em domínios variados. Mede o estágio de recuperação isolado do resto do pipeline (cap. 21).

**BM25** — função de pontuação léxica clássica (família *best matching*). É a busca esparsa de referência: acha termos literais, falha em paráfrase (cap. 06).

**Chunk** — a unidade de texto indexada e recuperada. Não equivale a parágrafo; o corte é decisão de engenharia e é irreversível adiante (cap. 05).

**Chunking** — a estratégia de corte. Fixo, recursivo, estrutural, semântico ou hierárquico; o tamanho ótimo depende do **tipo de pergunta**, não do documento (cap. 05).

**Contexto** — o conteúdo efetivamente montado para uma chamada. Distinto da **janela** (o limite) e do **prompt** (a parte autoral e estável) — cap. 01.

**Context precision** — dos trechos recuperados, quantos eram relevantes. Precisão baixa significa orçamento gasto com ruído (caps. 20, 15).

**Context recall** — dos trechos necessários, quantos foram recuperados. Recall baixo é problema de corpus, chunking ou busca (cap. 21).

**Context rot** — degradação de qualidade conforme o contexto cresce. Duas causas somadas, não uma: o **comprimento** degrada sozinho (medido isolando a variável, em tarefas triviais), e **distratores semanticamente próximos** do alvo tornam a queda mais íngreme — um único distrator já reduz o desempenho (cap. 20).

**Contextual retrieval** — prefixar cada chunk, antes de embeddar, com um resumo do seu lugar no documento. Ataca a perda de contexto no corte; custa uma passada de LLM sobre o corpus. Visto do cap. 04, é **geração de metadado** que vai para dentro do texto embeddado em vez de para um campo (cap. 09).

**Contrato** — o que um componente entrega ao seguinte, declarado. Os quatro contratos do cap. 02 têm uma propriedade em comum: todos existem para **carregar procedência adiante**, do documento até a citação na resposta.

**CoT (*Chain-of-Thought*)** — induzir passos intermediários explícitos antes da resposta. Família *thought generation* (cap. 12).

**CRAG** (*Corrective RAG*) — um avaliador leve classifica o resultado da recuperação e dispara ação corretiva (refinar, ou buscar em outra fonte). O julgamento fica **fora** do modelo, e por isso é auditável (cap. 18).

**Cross-encoder** — modelo que lê consulta e documento **juntos** para pontuar relevância, em vez de comparar vetores calculados separadamente. É a arquitetura típica de reranker: preciso e caro (cap. 07).

## D–L

**CDTA (*Cross-Document Topic-Aligned*)** — corte que reconstrói o conhecimento **no nível do corpus**: identifica tópicos que atravessam documentos e sintetiza chunks unificados. Ganha em multi-hop e complica a citação verificável, porque o chunk resultante não existe em nenhum documento original (caps. 05, 09, 15).

**Decodificação restrita (*constrained decoding*)** — restringir a amostragem para garantir que a saída obedeça a uma gramática ou schema. Garante forma, não valor (cap. 13).

**DSPy** — framework que trata prompts como parâmetros a serem compilados contra uma métrica, com otimizadores (BootstrapFewShot, COPRO, MIPROv2, GEPA) — cap. 16.

**Embedding** — representação vetorial de texto usada para medir similaridade semântica. Similaridade não é compreensão (cap. 05).

**Faithfulness** — proporção das afirmações da resposta que são inferíveis do contexto fornecido. Uma resposta **correta** pode ter *faithfulness* baixa — e isso é informação, não defeito: o modelo respondeu de memória (cap. 21).

**Few-shot** — incluir exemplos no prompt. Fixa formato e fronteiras de rótulo; custa tokens em toda chamada (cap. 12).

**FLARE** — recupera **durante** a geração, disparado pela incerteza do modelo sobre o que vai escrever a seguir (cap. 18).

**Fundamentação (*grounding*)** — a exigência de que a resposta se sustente no material recuperado, e não no que o modelo sabe. É requisito de prompt antes de ser métrica, e tem três partes: exclusividade da fonte, procedência declarada e regra de ausência (cap. 15).

**Fusão por posição** — combinar dois rankings pela **colocação** de cada documento, e não pela nota bruta. Dispensa calibrar escalas incomparáveis (cosseno × BM25) e é o que torna a busca híbrida prática (cap. 06).

**GEPA** — otimizador de prompt que evolui instruções por reflexão em linguagem natural sobre traços de execução, com seleção genético-Pareto (cap. 16).

**GraphRAG** — construir um grafo de entidades e relações, sumarizar regiões densas e recuperar sobre essa estrutura. Muda **do que** se recupera — enquanto o RAG agêntico muda **como** (cap. 10).

**Higiene do corpus** — frescor, procedência, deduplicação e permissão como metadado. É o **teto** da qualidade de recuperação: nenhuma técnica dos caps. 05–18 conserta um corpus podre, porque um documento revogado embedda exatamente igual ao vigente (cap. 04).

**HyDE** (*Hypothetical Document Embeddings*) — gerar uma resposta hipotética e buscar por ela, porque uma resposta se parece mais com o documento do que a pergunta. Sua versão invertida e movida para a indexação são as **perguntas hipotéticas** do cap. 04 (cap. 08).

**Injeção indireta** — *prompt injection* em que o texto hostil chega por conteúdo que o sistema lê (documento, página, e-mail, memória), e não pela mensagem do usuário. É a forma que sistemas de RAG criam (cap. 22).

**IR (*Information Retrieval*)** — o campo de seis décadas que estuda como encontrar documentos relevantes para uma necessidade de informação. O RAG não nasceu do zero: herdou dele as métricas, os benchmarks e o BM25 — e foi absorvido de volta, com track próprio no TREC (cap. 01).

**Janela de contexto** — o limite físico de tokens de uma chamada. Não é "memória do modelo" (cap. 01).

**Late chunking** — embeddar o documento inteiro e aplicar o corte **depois** do transformer, antes do *pooling*. Resolve a perda de contexto sem chamada de LLM, limitado pelo comprimento máximo do modelo de embedding (cap. 09).

**LLM-as-judge** — usar um modelo para julgar saídas de outro. Padrão de fato e fraqueza metodológica simultaneamente; exige calibração contra julgamento humano (cap. 17).

## M–R

**LLM (*Large Language Model*)** — modelo de linguagem de grande porte. Neste livro ele é sempre o **gerador**, nunca a fonte de verdade: o que ele sabe está nos pesos do dia do treino, e é justamente essa limitação que o RAG existe para contornar (caps. 00, 01).

**Mem0** — sistema de memória que extrai fatos salientes das mensagens e os guarda como memórias compactas (cap. 19).

**MemGPT / Letta** — arquitetura que trata o LLM como sistema operacional gerenciando a própria memória, paginando entre contexto principal, *recall* e *archival* (cap. 19).

**Memória** — estado deliberadamente mantido além do turno atual. Distinta do histórico bruto, e distinta de RAG: memória guarda afirmações que **mudam de valor de verdade** (cap. 19).

**Metadado gerado** — metadado **inferido por modelo** (classificação, entidades, resumo, vigência lida da prosa, perguntas hipotéticas), por oposição ao **herdado** (que a fonte já trazia) e ao **derivado** (computado deterministicamente). É a única das três procedências que pode estar **errada** — daí a regra: o gerado impulsiona, nunca filtra de forma dura (cap. 04).

**MIPROv2** — otimizador que busca instruções e exemplos conjuntamente, via otimização bayesiana e bootstrap (cap. 16).

**Modular RAG** — o terceiro paradigma: o pipeline deixa de ser uma sequência fixa e vira módulos recombináveis, com roteamento e ramificação. O teste verificável de modularidade: **trocar um módulo sem tocar nos vizinhos** (cap. 03).

**MTEB** — *Massive Text Embedding Benchmark*: avaliação ampla de modelos de embedding em múltiplas tarefas (cap. 21).

**Multi-hop** — pergunta cuja resposta não está em nenhum trecho, mas na **relação** entre trechos. Recuperar os dois melhores não a produz (cap. 10).

**MCP (*Model Context Protocol*)** — protocolo que padroniza como um sistema expõe ferramentas e recursos a um modelo. Resolve **integração**, não recuperação: o tratamento é do livro irmão, e aqui ele aparece só como superfície de ataque medida (cap. 22).

**Naive RAG** — o primeiro paradigma: indexar, buscar por similaridade, concatenar, gerar. É a linha de base honesta — e a arquitetura da maioria dos sistemas que se dizem avançados (cap. 03).

**Orçamento de contexto** — a alocação explícita de tokens entre os concorrentes (prompt, memória, recuperado, ferramenta, histórico). Sistemas sem essa alocação declarada degradam de forma inexplicável (cap. 20).

**OWASP LLM Top 10** — a classificação de referência de riscos em aplicações com LLM. *Prompt injection* é LLM01 em todas as edições publicadas (cap. 22).

**Pergunta global** — pergunta cuja resposta é propriedade do **conjunto**, não de nenhuma parte dele ("quais os temas recorrentes nestes 800 chamados?"). Aumentar `top_k` não aproxima: piora (cap. 10).

**Perguntas hipotéticas** — gerar, na indexação, as perguntas que cada trecho responde, e indexá-las junto. O chunk passa a carregar as perguntas, não só as respostas — HyDE invertido, pago uma vez em vez de em toda consulta (cap. 04).

**Procedência** — de onde veio cada coisa, carregada adiante em toda fronteira: do documento ao chunk, do chunk ao candidato, do candidato à citação. É o fio que atravessa os quatro contratos do cap. 02.

**Prompt** — a parte do contexto que é instrução autoral e relativamente estável. Não é o contexto todo (cap. 01).

**Prompt injection** — fazer o modelo obedecer a texto que deveria ser tratado como dado. Propriedade da arquitetura, não bug (cap. 22).

**Proposition chunking** — decompor o documento em afirmações autocontidas e indexar cada uma. Precisão alta para pergunta factual; caro, e perde o encadeamento (cap. 05).

**RAGAS** — framework de avaliação **reference-free** (sem anotação humana) que fixou o vocabulário de fato da área. O paper propõe **três** aspectos — *faithfulness*, *answer relevance* e *context relevance*; o par *context precision* / *context recall* é da **biblioteca**, que desdobrou o terceiro em dois. A distinção importa porque as duas metades diagnosticam falhas diferentes (cap. 21).

**RAG (*Retrieval-Augmented Generation*)** — recuperar trechos de um corpus externo **e** gerar resposta fundamentada neles. Recuperação sozinha não é RAG: as duas metades da sigla têm peso, e é por isso que a geração tem uma parte inteira do livro (caps. 00, 01, 15).

**RAG agêntico** — o quarto paradigma: o modelo decide **se**, **o que** e **onde** buscar, e se o que voltou basta. A recuperação deixa de ser etapa e vira ferramenta; o fluxo deixa de ser previsível e passa a exigir teto de iterações (caps. 03, 18).

**RAPTOR** — construir uma árvore de resumos recursivos (agrupar chunks por similaridade, resumir cada grupo, repetir). A recuperação acontece em qualquer nível: folhas para pergunta factual, nós altos para **pergunta global**. É a resposta mais barata que grafo, porque não exige extrair entidades (cap. 10).

**ReAct** — ciclo pensamento → ação → observação. Nasce como técnica de prompt (cap. 12) e vira arquitetura de recuperação (cap. 18).

**Reranking** — reordenar os primeiros candidatos com um modelo mais caro e mais preciso. É o estágio de maior retorno marginal do pipeline — e o único que entrega uma **nota** utilizável como limiar (cap. 07).

**Roteamento** — classificar a pergunta antes de buscar e mandá-la ao retriever certo (texto, dado estruturado, corpus específico). É o que torna o pipeline ramificado sem torná-lo imprevisível (cap. 08).

## S–Z

**RRF (*Reciprocal Rank Fusion*)** — fusão recíproca de ranking: combina listas pela **posição** de cada documento, não pela nota. É o que torna a busca híbrida prática, porque dispensa calibrar escalas incomparáveis (cap. 06).

**`recall@k`** — dos trechos necessários, quantos apareceram entre os `k` primeiros. Tem uma armadilha que o `rag-zero` documenta em teste: se o gabarito marca dezenas de trechos como relevantes e você mede em `k=5`, o teto matemático é `5/40` — o número parece péssimo **por construção**, não por defeito da busca (cap. 21).

**Saída estruturada** — restringir a resposta a um schema. Garante forma, nunca valor; a validação semântica continua sendo sua (cap. 13).

**Self-consistency** — amostrar vários caminhos de raciocínio e agregar por voto. Multiplica o custo por N; é decisão financeira (cap. 12).

**Self-RAG** — o modelo emite marcadores de reflexão que decidem se recupera e se o trecho sustenta a resposta. O julgamento fica **dentro** do modelo (cap. 18).

**Sentence-window** — indexar a frase e entregar a janela de texto em volta dela. Caso particular do padrão **desacoplar a unidade de busca da unidade de entrega** (cap. 05).

**Step-back prompting** — generalizar a pergunta antes de recuperar, para trazer o princípio e não só o detalhe. É o inverso da decomposição (cap. 08).

**SIGIR** — a conferência de referência de *Information Retrieval*, e uma das evidências de que o RAG não nasceu do zero: as métricas, os benchmarks e a reordenação em estágios vêm de lá (cap. 01).

**Taxa de resultado zero** — proporção de consultas que voltam sem nada acima do limiar. O sinal operacional mais barato da recuperação — e que denuncia por ausência: se está sempre em zero, provavelmente não há limiar nem caminho de abstenção (caps. 06, 21).

**Token** — a unidade que o modelo processa e que a fatura cobra. Não é palavra (cap. 01).

**Trajetória** — a sequência de decisões (buscas, chamadas, reflexões) que levou a uma resposta em um sistema agêntico. Duas trajetórias podem dar a mesma resposta com custos muito diferentes — e a instrumentação madura ainda não a mede (caps. 18, 21).

**TREC (*Text REtrieval Conference*)** — o programa de avaliação que estrutura a pesquisa em recuperação há décadas. Tem **track dedicado a RAG** — o sinal mais claro de que a área absorveu o tema em vez de tratá-lo como estranho (cap. 01).

**`top_k`** — quantos candidatos o retriever devolve por consulta. É o botão mais mexido e o menos medido do livro: aumentar melhora *recall* e piora *precision*, e o custo é **linear no orçamento de contexto** (cap. 20). O valor certo não se escolhe — se mede, com a tabela de diagnóstico do cap. 21 (caps. 06, 07).

**Zep** — sistema de memória que adiciona grafo de conhecimento **temporal** sobre recuperação densa, para raciocinar sobre fatos que mudam com o tempo (cap. 19).
