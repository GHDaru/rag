# Catálogo de técnicas

> Uma ficha por técnica: **o que é · quando usa · o que custa · onde está no livro**.
>
> Edição 1.0 · captura em 2026-08.
>
> **Como ler:** esta página é *reference* (Diátaxis) — feita para consulta rápida, não para leitura linear. A explicação de *por que* cada técnica funciona está no capítulo indicado; aqui está só o suficiente para decidir se vale abrir o capítulo.
>
> **Como está organizado:** na ordem das partes do livro — o corpus, a recuperação, a geração, o sistema em produção. Uma técnica que aparece em duas partes traz os dois capítulos.
>
> **Estado:** o catálogo cobre as técnicas que os capítulos mencionam, e desde a edição 1.0 cada uma delas tem **fonte primária conferida** na [bibliografia](bibliografia.md). A expansão — cada ficha com fonte primária e condição experimental, e as 58 técnicas de prompting da taxonomia de referência (*The Prompt Report*) na Parte IV — é a **rodada 5** do [ROADMAP](../ROADMAP.md).

## Parte II — O corpus

### Ingestão e governança (cap. 04)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Leitura humana do extraído** | ler uma amostra do texto que saiu do PDF/HTML | **antes de qualquer otimização** — nenhuma métrica a substitui | uma tarde | 04 |
| **Metadado no chunk** | origem, data, seção, `status`, permissão, hash | **sempre** — é o que permite filtrar antes de buscar | ~0 | 04 |
| **Higiene do corpus** | frescor, procedência, deduplicação, permissão | **antes** de qualquer técnica dos caps. 05–18 | ingestão | 04 |
| **Política de saída** | quem tira do índice, e quando | sempre — times constroem entrada e esquecem remoção | ~0 de código, decisão de produto | 04 |
| **Expiração declarada por tipo** | cada classe de documento tem validade | corpus com vigência (política, preço, doc de release) | reindexação | 04 |
| **Reindexação incremental** | reprocessar só o que mudou, por hash ou webhook | corpus vivo | infraestrutura de mudança | 04 |

### Geração de metadado (cap. 04)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Resumo contextual** | descrever o lugar do trecho no documento | chunk que não se basta — é o *contextual retrieval* visto da ingestão | 1 chamada de LLM por chunk | 04, 09 |
| **Perguntas hipotéticas** | gerar e indexar as perguntas que o trecho responde | pergunta do usuário distante do vocabulário do texto | indexação; **paga uma vez**, contra HyDE (*Hypothetical Document Embeddings*) que paga sempre | 04, 08 |
| **Vigência extraída da prosa** | ler "substitui a de 2023", "válido até" e virar campo | quando o status só existe no texto | 1 chamada por documento | 04 |
| **Classificação por área/tipo** | rotular para habilitar filtro e roteamento | múltiplos domínios ou permissões | 1 chamada por documento | 04, 08 |
| **Confiança junto do valor** | guardar a certeza do gerador ao lado do campo | **sempre que houver metadado gerado** | ~0 | 04 |
| **Gerado impulsiona, não filtra** | filtro duro só com metadado herdado ou derivado | **sempre** — o erro do gerado some o documento sem rastro | ~0 | 04 |

### Chunking e representação (cap. 05)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Chunking fixo com sobreposição** | corte por N tokens | linha de base honesta | ~0 | 05 |
| **Chunking recursivo** | separadores em cascata (parágrafo → frase → token) | o padrão razoável para a maioria dos corpora | ~0 | 05 |
| **Chunking estrutural** | corte pela marcação do documento | documento com hierarquia real | ~0 | 05 |
| **Chunking semântico** | corte por quebra de tópico | prosa longa sem seções | pré-processamento | 05 |
| **Sentence-window** | indexa a frase, entrega a janela em volta | precisão de busca com contexto na entrega | ~0 | 05 |
| **Proposition chunking** | decompõe em afirmações autocontidas | pergunta factual específica | 1 passada de LLM na indexação | 05 |
| **Índice hierárquico** | indexa pequeno, entrega o pai | perguntas de granularidades diferentes | complexidade | 05 |

## Parte III — Recuperação

### Busca (cap. 06)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **BM25 / busca esparsa** | pontuação por termo literal | identificador, código, nome próprio | baixo | 06 |
| **Busca densa** | similaridade de embeddings | paráfrase, sinônimo | indexação + armazenamento | 06 |
| **Busca híbrida (fusão por posição)** | combinar os dois rankings pela colocação, não pela nota | **quase sempre** — melhor custo/benefício do livro | baixo | 06 |
| **Filtro por metadado na consulta** | restringir no índice, nunca sobre o resultado | sempre que houver permissão ou vigência | ~0 | 06, 22 |
| **Limiar + abstenção** | não responder quando nada é relevante | sempre | ~0 | 06, 15 |

### Reordenar (cap. 07)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Reranking (*cross-encoder*)** | modelo lê consulta e documento juntos e pontua | quando corpus e busca já estão razoáveis | por documento reordenado | 07 |
| **Usar a nota, não só a ordem** | a pontuação do reranker vira limiar de corte | sempre que houver reranker | ~0 | 07, 06 |

### Do lado da pergunta (cap. 08)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Reescrita de consulta** | traduzir a pergunta para o vocabulário do corpus | pergunta ≠ resposta; conversa com referência | 1 chamada por pergunta | 08 |
| **Múltiplas consultas** | decompor a pergunta e buscar cada parte | pergunta composta | N buscas | 08 |
| **HyDE** | gerar resposta hipotética e buscar por ela | pergunta muito distante do texto | 1 chamada + risco de alucinar a hipótese | 08 |
| **Step-back prompting** | generalizar a pergunta antes de buscar | quando falta o princípio geral, não o detalhe | 1 chamada por pergunta | 08 |
| **Roteamento** | classificar a pergunta e escolher o retriever | múltiplos corpora; texto + dado estruturado | 1 classificação | 08, 10 |

### Indexação avançada (cap. 09)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Contextual Retrieval** | resumo do lugar do chunk, prefixado antes de embeddar | chunk perde contexto; orçamento de indexação folgado | LLM sobre todo o corpus | 09, 04 |
| **Late Chunking** | embeddar o documento, cortar depois do transformer | mesmo problema, orçamento apertado | só o embedder | 09 |
| **Uma técnica por vez, e remover o que não pagou** | medir antes e depois de cada mudança | **sempre** — é a regra que vale mais que as técnicas | disciplina | 09, 21 |

### Recuperação estruturada (cap. 10)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **RAPTOR** | agrupar, resumir, repetir — árvore de resumos recursivos | **pergunta global** (a que nenhum `top_k` responde) | indexação pesada, uma vez | 10 |
| **GraphRAG** | grafo de entidades e relações, com resumo de comunidades | multi-hop sobre entidades recorrentes e nomeáveis | indexação pesada + **extração de entidades** | 10 |
| **Texto + consulta gerada** | rotear entre retriever de prosa e consulta a banco | parte do conhecimento está em tabela | 1 classificação + risco de segurança | 10, 22 |

## Parte IV — Geração

### Estrutura e contrato (cap. 11)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Delimitação explícita** | material externo dentro de marcadores nomeados | sempre que há texto que você não escreveu | ~0 | 11 |
| **Hierarquia de instruções** | precedência declarada: sistema > dev > usuário > externo | sempre | ~0 | 11, 22 |
| **Regra de fallback** | dizer o que fazer quando não souber | sempre — a ausência dela é alucinação por padrão | ~0 | 11, 15 |

### Raciocínio, as seis famílias (cap. 12)

| Família / técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Zero-shot** | instrução direta | primeira tentativa, sempre | 1× | 12 |
| **Few-shot** | exemplos no prompt | formato idiossincrático; fronteira de rótulo sutil | tokens fixos por chamada | 12 |
| **Chain-of-Thought** | passos intermediários explícitos | aritmética, lógica, múltiplas restrições | tokens de saída | 12 |
| **Self-consistency** | N amostras + voto | erro caro; variância é o inimigo | **N×** | 12 |
| **Decomposição** | quebrar em subproblemas | tarefa grande ou composta | + chamadas | 12 |
| **Auto-crítica** | o modelo revisa a própria saída | saída longa, com critério verificável | 2× ou mais | 12 |
| **ReAct** | pensamento → ação → observação | quando a resposta exige ir buscar | latência + superfície de ataque | 12, 18 |

### Saída como contrato (cap. 13)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Saída estruturada (schema nativo)** | resposta conforme a JSON Schema, garantida pelo provedor | quando o consumidor é código | ~0 | 13 |
| **Decodificação restrita** | gramática/autômato na amostragem | modelo local sem garantia de plataforma | latência | 13 |
| **Validar + reparar** | validar, re-solicitar com o erro anexado, com teto | **sempre**, mesmo com schema nativo | 1 chamada extra quando falha | 13 |
| **Campo de raciocínio** | campo textual antes dos campos de decisão | saída estruturada que exige pensar | tokens de saída | 13 |
| **Campo explícito de incerteza** | um lugar para dizer "não encontrei" | **sempre** — sem ele o modelo preenche | ~0 | 13, 15 |

### Camada de sistema (cap. 14)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Camadas por volatilidade** | ordenar do estável ao volátil | sempre | ~0 — e **economiza** | 14, 23 |
| **Separação voz × política** | persona e regras em blocos e donos distintos | quando há mais de um dono do prompt | ~0 | 14 |
| **Cascata de regras** | global → projeto → pasta → pessoal, o mais próximo vence | regras vindas de múltiplas origens | ~0 | 14 |

### Fundamentação (cap. 15)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Exclusividade da fonte** | responder **só** com o material fornecido | todo sistema de RAG | ~0 | 15 |
| **Procedência no contexto** | cada trecho entra rotulado com sua origem | sempre — é o que torna a citação possível | ~0 | 15, 02 |
| **Regra de ausência** | dizer o que fazer quando o contexto não sustenta | **sempre** — é a metade esquecida do prompt de RAG | ~0 | 15 |
| **Citação por identificador** | apontar a fonte de forma resolvível, não por menção | quando alguém precisa conferir | ~0 | 15 |
| **Atribuição por afirmação** | cada frase da resposta aponta seu trecho de apoio | domínio auditado (jurídico, saúde, financeiro) | tokens + complexidade de prompt | 15 |
| **Abstenção na geração** | não responder quando o recuperado não basta | sempre | ~0 — custa produto, não computação | 15, 06 |

### Otimização e avaliação de prompt (caps. 16–17)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Busca por exemplos** (bootstrap) | otimizar quais demonstrações incluir | primeiro recurso de otimização | baixo | 16 |
| **Busca por instrução** (bayesiana/evolutiva) | otimizar o texto da instrução | formato já bom, estratégia ruim | médio-alto | 16 |
| **Reflexão sobre traços** | instruções derivadas da análise das falhas | conjunto heterogêneo; quer entender o ganho | alto | 16 |
| **Asserção determinística** | regra verificável sobre a saída | **todo critério que puder virar assert** | ~0 | 17 |
| **LLM-as-judge** | modelo pontua contra rubrica | só o que não vira assert | médio + viés | 17 |
| **Calibração do juiz** | medir concordância com humano antes de confiar | sempre que usar juiz | amostra revisada | 17 |
| **Casos de falha registrados** | todo incidente vira caso | **sempre** | ~0 | 17, 21 |

## Parte V — O sistema em produção

### Quando o modelo decide (cap. 18)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Recuperação sob demanda** | o modelo decide *se* busca | perguntas que nem sempre precisam de busca | imprevisibilidade | 18 |
| **Laço com reflexão** | criticar o resultado e buscar de novo | busca vazia; resultado parcial; multi-hop | latência variável | 18 |
| **Self-RAG** | o modelo emite marcadores que decidem recuperar e avaliar sustentação | o julgamento cabe no modelo | modelo treinado para isso | 18 |
| **CRAG** | avaliador leve classifica o resultado e dispara correção | quer o julgamento fora do modelo, auditável | 1 avaliador por busca | 18 |
| **FLARE** | recupera **durante** a geração, disparado por incerteza | texto longo que descobre lacunas ao escrever | recuperações imprevisíveis | 18 |
| **Adaptive RAG** | classifica a complexidade e escolhe o grau | perguntas de dificuldade heterogênea | 1 classificação por pergunta | 18 |
| **Teto de iterações + orçamento** | limites duros no laço | **sempre que houver laço** | ~0 | 18, 03 |

### Conversa e memória (cap. 19)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Resolução de referência antes de buscar** | reescrever "e o outro?" na pergunta autocontida | todo RAG conversacional | 1 chamada por turno | 19, 08 |
| **Memória por fatos extraídos** | destilar afirmações salientes | fatos estáveis sobre o usuário | extração por turno | 19 |
| **Memória em grafo temporal** | entidades + relações + validade no tempo | fatos que mudam de valor de verdade | manutenção de grafo | 19 |
| **Paginação autogerida** | o modelo move memória para dentro/fora | sessões muito longas | latência | 19 |

### Orçamento (cap. 20)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Orçamento declarado por fonte** | alocação escrita: quem recebe quantos tokens | sempre | ~0 | 20 |
| **Política de corte** | quem cede quando estoura, declarado | sempre que há orçamento | ~0 | 20 |
| **Híbrido (recuperar → contexto longo)** | reduzir por busca, raciocinar sobre o resto | o caso geral | indexação | 20 |

### Medir (cap. 21)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Tabela de diagnóstico** | combinar recall/precision/faithfulness para localizar a falha | **antes** de escolher qualquer técnica das Partes II–III | rodar o eval | 21 |
| **Taxa de resultado zero** | quantas consultas voltam sem nada acima do limiar | **sempre** — o sinal barato que denuncia por ausência | ~0 | 21, 06 |
| **Taxa de citação** | quantas respostas referenciam o recuperado | *faithfulness* barata, sem juiz, em toda requisição | ~0 | 21, 15 |
| **Conjunto sintético do corpus** | gerar perguntas dos documentos | cobrir volume barato | superestima o recall | 21 |
| **Chunks nunca recuperados** | os que jamais apareceram em nenhum `top_k` | painel de corpus | ~0 | 21, 04 |

### Proteger (cap. 22)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Marcação de procedência** | declarar no contexto o que veio de fora | sempre que há conteúdo recuperado | ~0 | 22, 15 |
| **Privilégio mínimo nas ferramentas** | quem lê de fora não age | **sempre** — a única defesa que não depende do modelo | funcionalidade | 22 |
| **Aprovação para fonte nova** | um documento entra no índice quando alguém decidiu | ingestão automática de fonte aberta | fricção barata | 22, 04 |
| **Aprovação humana** | confirmar antes do irreversível | ação que não pode ser desfeita | fricção | 22 |

### Pagar (cap. 23)

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Prefixo estável** | nada volátil acima de algo estável | **sempre** — não sacrifica nada | ~0 — **economiza muito** | 23, 14 |
| **Cache semântico** | responder sem chamar o modelo quando a pergunta se parece com uma anterior | muita repetição (base de conhecimento, suporte) | risco de servir a resposta errada; a chave precisa incluir permissão | 23 |
| **Serialização determinística** | mesma informação, sempre os mesmos bytes | sempre que há cache | ~0 | 23 |
| **Painel custo + qualidade** | nunca reportar uma sem a outra | sempre | instrumentação | 23, 21 |

---

## As oito que valem começar por aqui

Se você só puder aplicar oito coisas deste livro, e nesta ordem — porque cada uma depende de a anterior estar de pé:

1. **Ler uma amostra do texto extraído** (04) — leva uma tarde, e nenhuma métrica substitui.
2. **`status` e `permissao` como metadado do chunk** (04) — evita os dois incidentes mais caros: responder com o revogado, e vazar entre clientes.
3. **Busca híbrida com fusão por posição** (06) — melhor relação benefício/esforço do livro.
4. **Limiar + abstenção** (06) — sem eles, um corpus sem a resposta produz alucinação por padrão.
5. **Regra de ausência no prompt de geração** (15) — a metade esquecida do prompt de RAG.
6. **Reranking** (07) — o maior retorno marginal, depois que os quatro acima estão de pé.
7. **Tabela de diagnóstico** (21) — para parar de otimizar no lugar errado.
8. **Prefixo estável** (23) — é grátis e economiza mais que qualquer outra.
