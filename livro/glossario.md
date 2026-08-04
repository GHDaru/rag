# Glossário

> Siglas por extenso e termos com o sentido **que este livro usa**. Quando um termo tem uso ambíguo na indústria, a ambiguidade está registrada — desambiguar é metade do trabalho (cap. 01).
>
> Edição 0.1 · captura em 2026-08. Verbetes novos entram quando o capítulo correspondente é aprofundado.

## A–C

**Alucinação** — afirmação produzida com confiança e sem sustentação. Em sistemas com recuperação, o caso perigoso é a *alucinação fundamentada em ruído*: o modelo usa trechos irrelevantes que foram recuperados por falta de um caminho de abstenção (cap. 09). Métrica associada: *faithfulness* (cap. 15).

**Answer relevance** — métrica que mede se a resposta endereça a pergunta feita. Não diz nada sobre correção (cap. 15).

**BEIR** — *Benchmark for Information Retrieval*: conjunto de avaliação de recuperação zero-shot em domínios variados. Mede o estágio de recuperação isolado do resto do pipeline (cap. 15).

**BM25** — função de pontuação léxica clássica (família *best matching*). É a busca esparsa de referência: acha termos literais, falha em paráfrase (cap. 09).

**Chunk** — a unidade de texto indexada e recuperada. Não equivale a parágrafo; o corte é decisão de engenharia e é irreversível adiante (cap. 09).

**Chunking** — a estratégia de corte. Fixo, estrutural, semântico ou hierárquico; o tamanho ótimo depende do **tipo de pergunta**, não do documento (cap. 09).

**Contexto** — o conteúdo efetivamente montado para uma chamada. Distinto da **janela** (o limite) e do **prompt** (a parte autoral e estável) — cap. 01.

**Context precision** — dos trechos recuperados, quantos eram relevantes. Precisão baixa significa orçamento gasto com ruído (caps. 08, 15).

**Context recall** — dos trechos necessários, quantos foram recuperados. Recall baixo é problema de índice, chunking ou busca (cap. 15).

**Context rot** — degradação de qualidade conforme o contexto cresce. Não é linear com o comprimento: é dirigida pela similaridade entre o alvo e os distratores (cap. 08).

**Contextual retrieval** — prefixar cada chunk, antes de embeddar, com um resumo do seu lugar no documento. Ataca a perda de contexto no corte; custa uma passada de LLM sobre o corpus (cap. 10).

**CoT (*Chain-of-Thought*)** — induzir passos intermediários explícitos antes da resposta. Família *thought generation* (cap. 03).

**CRAG** (*Corrective RAG*) — um avaliador leve classifica o resultado da recuperação e dispara ação corretiva (refinar, ou buscar em outra fonte). O julgamento fica **fora** do modelo, e por isso é auditável (cap. 11).

**Cross-encoder** — modelo que lê consulta e documento **juntos** para pontuar relevância, em vez de comparar vetores calculados separadamente. É a arquitetura típica de reranker: preciso e caro (cap. 09).

## D–L

**Decodificação restrita (*constrained decoding*)** — restringir a amostragem para garantir que a saída obedeça a uma gramática ou schema. Garante forma, não valor (cap. 04).

**DSPy** — framework que trata prompts como parâmetros a serem compilados contra uma métrica, com otimizadores (BootstrapFewShot, COPRO, MIPROv2, GEPA) — cap. 06.

**Embedding** — representação vetorial de texto usada para medir similaridade semântica. Similaridade não é compreensão (cap. 09).

**Faithfulness** — proporção das afirmações da resposta que são inferíveis do contexto fornecido. Uma resposta **correta** pode ter *faithfulness* baixa — e isso é informação, não defeito: o modelo respondeu de memória (cap. 15).

**Few-shot** — incluir exemplos no prompt. Fixa formato e fronteiras de rótulo; custa tokens em toda chamada (cap. 03).

**FLARE** — recupera **durante** a geração, disparado pela incerteza do modelo sobre o que vai escrever a seguir (cap. 11).

**GEPA** — otimizador de prompt que evolui instruções por reflexão em linguagem natural sobre traços de execução, com seleção genético-Pareto (cap. 06).

**GraphRAG** — construir um grafo de entidades e relações, sumarizar regiões densas e recuperar sobre essa estrutura. Muda **do que** se recupera (cap. 10).

**Higiene do corpus** — frescor, procedência, deduplicação e permissão como metadado. É o **teto** da qualidade de recuperação: nenhuma técnica dos caps. 09–11 conserta um corpus podre, porque um documento revogado embedda exatamente igual ao vigente (cap. 09).

**HyDE** (*Hypothetical Document Embeddings*) — gerar uma resposta hipotética e buscar por ela, porque uma resposta se parece mais com o documento do que a pergunta (cap. 10).

**Injeção indireta** — *prompt injection* em que o texto hostil chega por conteúdo que o sistema lê (documento, página, e-mail, memória), e não pela mensagem do usuário. É a forma que sistemas de RAG criam (cap. 16).

**Janela de contexto** — o limite físico de tokens de uma chamada. Não é "memória do modelo" (cap. 01).

**Late chunking** — embeddar o documento inteiro e aplicar o corte **depois** do transformer, antes do *pooling*. Resolve a perda de contexto sem chamada de LLM, limitado pelo comprimento máximo do modelo de embedding (cap. 10).

**LLM-as-judge** — usar um modelo para julgar saídas de outro. Padrão de fato e fraqueza metodológica simultaneamente; exige calibração contra julgamento humano (cap. 07).

## M–R

**MCP (*Model Context Protocol*)** — protocolo que padroniza como um sistema expõe ferramentas, recursos e prompts a um modelo. Resolve integração; **não** resolve orçamento nem confiança (cap. 14).

**Mem0** — sistema de memória que extrai fatos salientes das mensagens e os guarda como memórias compactas (cap. 12).

**MemGPT / Letta** — arquitetura que trata o LLM como sistema operacional gerenciando a própria memória, paginando entre contexto principal, *recall* e *archival* (cap. 12).

**Memória** — estado deliberadamente mantido além do turno atual. Distinta do histórico bruto, e distinta de RAG: memória guarda afirmações que **mudam de valor de verdade** (cap. 12).

**MIPROv2** — otimizador que busca instruções e exemplos conjuntamente, via otimização bayesiana e bootstrap (cap. 06).

**MTEB** — *Massive Text Embedding Benchmark*: avaliação ampla de modelos de embedding em múltiplas tarefas (cap. 15).

**Orçamento de contexto** — a alocação explícita de tokens entre os concorrentes (prompt, memória, recuperado, ferramenta, histórico). Sistemas sem essa alocação declarada degradam de forma inexplicável (cap. 08).

**OWASP LLM Top 10** — a classificação de referência de riscos em aplicações com LLM. *Prompt injection* é LLM01 em todas as edições publicadas (cap. 16).

**Prompt** — a parte do contexto que é instrução autoral e relativamente estável. Não é o contexto todo (cap. 01).

**Prompt injection** — fazer o modelo obedecer a texto que deveria ser tratado como dado. Propriedade da arquitetura, não bug (cap. 16).

**Proposition chunking** — decompor o documento em afirmações autocontidas e indexar cada uma. Precisão alta para pergunta factual; caro, e perde o encadeamento (cap. 09).

**RAGAS** — framework de avaliação que fixou o vocabulário de fato: *faithfulness*, *answer relevance*, *context precision*, *context recall* (cap. 15).

**RAG (*Retrieval-Augmented Generation*)** — recuperar trechos de um corpus externo **e** gerar resposta fundamentada neles. Recuperação sozinha não é RAG. Neste livro, é a técnica central da engenharia de contexto — não a moldura (caps. 00, 09).

**RAPTOR** — construir uma árvore de resumos recursivos (agrupar chunks por similaridade, resumir cada grupo, repetir). A recuperação acontece em qualquer nível: folhas para pergunta factual, nós altos para **pergunta global**. É a materialização de referência da sumarização hierárquica (cap. 10).

**ReAct** — ciclo pensamento → ação → observação. Nasce como técnica de prompt (cap. 03) e vira arquitetura de recuperação (cap. 11).

**Reranking** — reordenar os primeiros candidatos com um modelo mais caro e mais preciso. Terceiro estágio do pipeline; o de maior retorno marginal (cap. 09).

## S–Z

**Saída estruturada** — restringir a resposta a um schema. Garante forma, nunca valor; a validação semântica continua sendo sua (cap. 04).

**Self-consistency** — amostrar vários caminhos de raciocínio e agregar por voto. Multiplica o custo por N; é decisão financeira (cap. 03).

**Self-RAG** — o modelo emite marcadores de reflexão que decidem se recupera e se o trecho sustenta a resposta. O julgamento fica **dentro** do modelo (cap. 11).

**Sentence-window** — indexar a frase e entregar a janela de texto em volta dela. Caso particular do padrão **desacoplar a unidade de busca da unidade de entrega** (cap. 09).

**Step-back prompting** — generalizar a pergunta antes de recuperar, para trazer o princípio e não só o detalhe. É o inverso da decomposição (cap. 10).

**Taxa de resultado zero** — proporção de consultas que voltam sem nada acima do limiar. O sinal operacional mais barato da recuperação — e que denuncia por ausência: se está sempre em zero, provavelmente não há limiar nem caminho de abstenção (caps. 09, 15).

**Token** — a unidade que o modelo processa e que a fatura cobra. Não é palavra (cap. 01).

**Trajetória** — a sequência de decisões (buscas, chamadas, reflexões) que levou a uma resposta em um sistema agêntico. Duas trajetórias podem dar a mesma resposta com custos muito diferentes — e a instrumentação madura ainda não a mede (caps. 11, 15).

**Zep** — sistema de memória que adiciona grafo de conhecimento **temporal** sobre recuperação densa, para raciocinar sobre fatos que mudam com o tempo (cap. 12).
