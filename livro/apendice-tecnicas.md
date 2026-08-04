# Catálogo de técnicas

> Uma ficha por técnica: **o que é · quando usa · o que custa · onde está no livro**.
>
> Edição 0.1 · captura em 2026-08.
>
> **Como ler:** esta página é *reference* (Diátaxis) — feita para consulta rápida, não para leitura linear. A explicação de *por que* cada técnica funciona está no capítulo indicado; aqui está só o suficiente para decidir se vale abrir o capítulo.
>
> **Estado:** o catálogo cobre as técnicas que os capítulos da edição 0.1 mencionam. A expansão para as 58 técnicas da taxonomia de referência (*The Prompt Report*), com fonte primária e condição experimental por ficha, é a **rodada 5** do [ROADMAP](https://github.com/GHDaru/rag/blob/main/ROADMAP.md).

## Parte I — Engenharia de Prompt

### Estrutura e contrato

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Delimitação explícita** | material externo dentro de marcadores nomeados | sempre que há texto que você não escreveu | ~0 | 02 |
| **Hierarquia de instruções** | precedência declarada: sistema > dev > usuário > externo | sempre | ~0 | 02, 16 |
| **Regra de fallback** | dizer o que fazer quando não souber | sempre — a ausência dela é alucinação por padrão | ~0 | 02 |
| **Saída estruturada (schema nativo)** | resposta conforme a JSON Schema, garantida pelo provedor | quando o consumidor é código | ~0 | 04 |
| **Decodificação restrita** | gramática/autômato na amostragem | modelo local sem garantia de plataforma | latência | 04 |
| **Validar + reparar** | validar, re-solicitar com o erro anexado, com teto | **sempre**, mesmo com schema nativo | 1 chamada extra quando falha | 04 |
| **Campo de raciocínio** | campo textual antes dos campos de decisão | saída estruturada que exige pensar | tokens de saída | 04 |

### Raciocínio (as seis famílias)

| Família / técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Zero-shot** | instrução direta | primeira tentativa, sempre | 1× | 03 |
| **Few-shot** | exemplos no prompt | formato idiossincrático; fronteira de rótulo sutil | tokens fixos por chamada | 03 |
| **Chain-of-Thought** | passos intermediários explícitos | aritmética, lógica, múltiplas restrições | tokens de saída | 03 |
| **Self-consistency** | N amostras + voto | erro caro; variância é o inimigo | **N×** | 03 |
| **Decomposição** | quebrar em subproblemas | tarefa grande ou composta | + chamadas | 03 |
| **Auto-crítica** | o modelo revisa a própria saída | saída longa, com critério verificável | 2× ou mais | 03 |
| **ReAct** | pensamento → ação → observação | quando a resposta exige ir buscar | latência + superfície de ataque | 03, 11 |

### Camada de sistema

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Camadas por volatilidade** | ordenar do estável ao volátil | sempre | ~0 — e **economiza** | 05, 17 |
| **Separação voz × política** | persona e regras em blocos e donos distintos | quando há mais de um dono do prompt | ~0 | 05 |
| **Cascata de regras** | global → projeto → pasta → pessoal, o mais próximo vence | regras vindas de múltiplas origens | ~0 | 05 |
| **Prompt derivado do tool set** | cada capacidade contribui seu trecho | catálogo de ferramentas que muda | ~0 — e encolhe o prompt | 05, 14 |

### Otimização e avaliação

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Busca por exemplos** (bootstrap) | otimizar quais demonstrações incluir | primeiro recurso de otimização | baixo | 06 |
| **Busca por instrução** (bayesiana/evolutiva) | otimizar o texto da instrução | formato já bom, estratégia ruim | médio-alto | 06 |
| **Reflexão sobre traços** | instruções derivadas da análise das falhas | conjunto heterogêneo; quer entender o ganho | alto | 06 |
| **Asserção determinística** | regra verificável sobre a saída | **todo critério que puder virar assert** | ~0 | 07 |
| **LLM-as-judge** | modelo pontua contra rubrica | só o que não vira assert | médio + viés | 07 |
| **Calibração do juiz** | medir concordância com humano antes de confiar | sempre que usar juiz | amostra revisada | 07 |

## Parte II — Engenharia de Contexto

### Orçamento

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Orçamento declarado por fonte** | alocação escrita: quem recebe quantos tokens | sempre | ~0 | 08 |
| **Política de corte** | quem cede quando estoura, declarado | sempre que há orçamento | ~0 | 08 |
| **Híbrido (recuperar → contexto longo)** | reduzir por busca, raciocinar sobre o resto | o caso geral | indexação | 08 |

### Recuperação

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Chunking fixo com sobreposição** | corte por N tokens | linha de base honesta | ~0 | 09 |
| **Chunking estrutural** | corte pela marcação do documento | documento com hierarquia real | ~0 | 09 |
| **Chunking recursivo** | separadores em cascata (parágrafo → frase → token) | o padrão razoável para a maioria dos corpora | ~0 | 09 |
| **Chunking semântico** | corte por quebra de tópico | prosa longa sem seções | pré-processamento | 09 |
| **Sentence-window** | indexa a frase, entrega a janela em volta | precisão de busca com contexto na entrega | ~0 | 09 |
| **Proposition chunking** | decompõe em afirmações autocontidas | pergunta factual específica | 1 passada de LLM na indexação | 09 |
| **Índice hierárquico** | indexa pequeno, entrega o pai | perguntas de granularidades diferentes | complexidade | 09 |
| **Metadado no chunk** | origem, seção, data, permissão | **sempre** — permite filtrar antes de buscar | ~0 | 09 |
| **BM25 / busca esparsa** | pontuação por termo literal | identificador, código, nome próprio | baixo | 09 |
| **Busca densa** | similaridade de embeddings | paráfrase, sinônimo | indexação + armazenamento | 09 |
| **Busca híbrida (fusão)** | combinar os dois rankings | **quase sempre** — melhor custo/benefício do livro | baixo | 09 |
| **Reranking** | *cross-encoder* sobre os N primeiros | quando os dois anteriores já estão razoáveis | por documento reordenado | 09 |
| **Limiar + abstenção** | não responder quando nada é relevante | sempre | ~0 | 09 |

### RAG avançado

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Contextual Retrieval** | resumo do lugar do chunk, prefixado antes de embeddar | chunk perde contexto; orçamento de indexação folgado | LLM sobre todo o corpus | 10 |
| **Late Chunking** | embeddar o documento, cortar depois do transformer | mesmo problema, orçamento apertado | só o embedder | 10 |
| **Reescrita de consulta** | traduzir a pergunta para o vocabulário do corpus | pergunta ≠ resposta; conversa com referência | 1 chamada por pergunta | 10 |
| **Múltiplas consultas** | decompor a pergunta e buscar cada parte | pergunta composta | N buscas | 10 |
| **HyDE** | gerar resposta hipotética e buscar por ela | pergunta muito distante do texto | 1 chamada + risco de alucinar a hipótese | 10 |
| **Step-back prompting** | generalizar a pergunta antes de buscar | quando falta o princípio geral, não o detalhe | 1 chamada por pergunta | 10 |
| **RAPTOR** | agrupar, resumir, repetir — árvore de resumos recursivos | **pergunta global** (a que nenhum `top_k` responde) | indexação pesada, uma vez | 10 |
| **GraphRAG** | grafo de entidades e relações, com resumo de comunidades | entidades recorrentes; perguntas globais/multi-hop | indexação pesada | 10 |

### Agente, memória e compactação

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Roteamento** | escolher a fonte antes de buscar | múltiplos corpora | 1 classificação | 11 |
| **Recuperação sob demanda** | o modelo decide *se* busca | perguntas que nem sempre precisam de busca | imprevisibilidade | 11 |
| **Laço com reflexão** | criticar o resultado e buscar de novo | busca vazia; resultado parcial; multi-hop | latência variável | 11 |
| **Self-RAG** | o modelo emite marcadores que decidem recuperar e avaliar sustentação | o julgamento cabe no modelo | modelo treinado para isso | 11 |
| **CRAG** | avaliador leve classifica o resultado e dispara correção | quer o julgamento fora do modelo, auditável | 1 avaliador por busca | 11 |
| **FLARE** | recupera **durante** a geração, disparado por incerteza | texto longo que descobre lacunas ao escrever | recuperações imprevisíveis | 11 |
| **Adaptive RAG** | classifica a complexidade e escolhe o grau | perguntas de dificuldade heterogênea | 1 classificação por pergunta | 11 |
| **Teto de iterações + orçamento** | limites duros no laço | **sempre que houver laço** | ~0 | 11 |
| **Memória por fatos extraídos** | destilar afirmações salientes | fatos estáveis | extração por turno | 12 |
| **Memória em grafo temporal** | entidades + relações + validade no tempo | fatos que mudam | manutenção de grafo | 12 |
| **Paginação autogerida** | o modelo move memória para dentro/fora | agentes de execução longa | latência | 12 |
| **Sumarização do histórico** | resumir os turnos antigos | conversa contínua e longa | 1 chamada por compactação | 13 |
| **Estado estruturado fora do texto** | restrições e IDs em estrutura, não em prosa | **sempre** | ~0 | 13 |
| **Isolamento por subagente** | contextos separados por subtarefa | trabalho decomponível | coordenação | 13 |

### Ferramentas e contexto externo

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Teto por ferramenta no adaptador** | truncar do lado do sistema, anunciando | **sempre** | ~0 | 14 |
| **Resumir antes de inserir** | comprimir resultado grande | resultado grande, essencial pequeno | 1 chamada | 14 |
| **Referência em vez de conteúdo** | devolver ID; detalhe sob demanda | resultados grandes e raramente necessários | ida extra quando precisa | 14 |
| **Divulgação progressiva** | anunciar capacidade por nome; detalhe sob uso | catálogo grande de ferramentas | ~0 — **economiza** | 14 |

## Parte III — Sistema

| Técnica | O que é | Quando usa | Custo | Cap. |
|---|---|---|---|:---:|
| **Tabela de diagnóstico** | combinar recall/precision/faithfulness para localizar a falha | antes de escolher qualquer técnica do cap. 11 | rodar o eval | 15 |
| **Taxa de resultado zero** | quantas consultas voltam sem nada acima do limiar | **sempre** — o sinal barato que denuncia por ausência | ~0 | 15 |
| **Taxa de citação** | quantas respostas referenciam o recuperado | *faithfulness* barata, sem juiz, em toda requisição | ~0 | 15 |
| **Higiene do corpus** | frescor, procedência, deduplicação, permissão no metadado | **antes** de qualquer técnica dos caps. 10–12 | ingestão | 09 |
| **Conjunto sintético do corpus** | gerar perguntas dos documentos | cobrir volume barato | superestima o recall | 15 |
| **Casos de falha registrados** | todo incidente vira caso | **sempre** | ~0 | 07, 15 |
| **Marcação de procedência** | declarar no contexto o que veio de fora | sempre que há conteúdo externo | ~0 | 14, 16 |
| **Privilégio mínimo nas ferramentas** | quem lê de fora não age | **sempre** — a única defesa que não depende do modelo | funcionalidade | 16 |
| **Aprovação humana** | confirmar antes do irreversível | ação que não pode ser desfeita | fricção | 16 |
| **Prefixo estável** | nada volátil acima de algo estável | **sempre** — não sacrifica nada | ~0 — **economiza muito** | 05, 17 |
| **Cache semântico** | responder sem chamar o modelo quando a pergunta se parece com uma anterior | muita repetição (base de conhecimento, suporte) | risco de servir a resposta errada; chave precisa incluir permissão | 17 |
| **Serialização determinística** | mesma informação, sempre os mesmos bytes | sempre que há cache | ~0 | 17 |
| **Painel custo + qualidade** | nunca reportar uma sem a outra | sempre | instrumentação | 15, 17 |

---

## As sete que valem começar por aqui

Se você só puder aplicar sete coisas deste livro, e em ordem:

1. **Prefixo estável** (17) — é grátis e economiza mais que qualquer outra.
2. **Regra de fallback** (02) — a ausência dela é alucinação por padrão.
3. **Busca híbrida** (09) — melhor relação benefício/esforço da Parte II.
4. **Asserção determinística** (07) — antes de qualquer juiz.
5. **Orçamento declarado** (08) — uma linha escrita, comportamento previsível.
6. **Privilégio mínimo** (16) — a única defesa que não depende do modelo cooperar.
7. **Tabela de diagnóstico** (15) — para parar de otimizar no lugar errado.
