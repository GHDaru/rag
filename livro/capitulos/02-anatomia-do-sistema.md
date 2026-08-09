# 02 — Anatomia de um Sistema de RAG

> **Estado da arte capturado em 2026-08** · edição 0.4 · [histórico e registro de expiração](../HISTORICO.md)
>
> **Maturidade: esboço.** O inventário de componentes e os contratos entre eles estão fechados; o tratamento por implementação é a rodada 2 do ROADMAP.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:

1. **Nomear** os componentes de um sistema de RAG e o que cada um decide;
2. **Situar** qualquer técnica do livro no componente que ela aprofunda;
3. **Descrever** o contrato entre dois componentes vizinhos — e por que o contrato importa mais que a implementação;
4. **Diagnosticar** em qual componente mora uma falha observada, antes de escolher a cura.

## O problema

A maior parte do que se escreve sobre RAG é catálogo de técnicas: chunking, embeddings, reranking, HyDE, GraphRAG. Cada uma explicada isoladamente, nenhuma situada.

Isso produz um efeito conhecido de quem já montou um sistema desses: você acumula técnicas sem saber onde elas encaixam, aplica três de uma vez, e quando algo piora não sabe qual desfazer. É a diferença entre conhecer peças e conhecer a máquina.

**Este capítulo é o desenho da máquina.** Ele existe para que todo capítulo seguinte tenha um endereço: quando o cap. 07 falar de reranking, você já sabe que ele aprofunda um componente específico, com entradas, saídas e vizinhos definidos.

E há uma razão mais dura para ele existir: **"engenharia" só se sustenta se houver arquitetura.** Sem componentes nomeados e contratos entre eles, o que se pratica é artesanato com vocabulário técnico.

## Fundamentos científicos

- **A base tripartite** — a survey de referência de RAG ([arXiv 2312.10997](https://arxiv.org/abs/2312.10997), Gao et al.) escrutina *"the tripartite foundation of RAG frameworks, which includes the **retrieval**, the **generation** and the **augmentation** techniques"*. A distinção que mais rende é a do meio: *aumento* é o que acontece **entre** buscar e responder — filtrar, reordenar, comprimir, ordenar, montar — e é justamente a parte que quase nenhum tutorial trata como etapa própria. ✓
- **O sistema como módulos reconfiguráveis** — *Modular RAG* ([arXiv 2407.21059](https://arxiv.org/html/2407.21059v1)) propõe *"decomposing complex RAG systems into independent **modules** and specialized **operators**"*, em vez de um pipeline fixo. É a formalização mais próxima de "arquitetura" que a área tem. ✓
- **A camada de raciocínio** — [arXiv 2506.10408](https://arxiv.org/abs/2506.10408) separa os sistemas entre ***predefined reasoning***, que *"follows fixed modular pipelines"*, e ***agentic reasoning***, em que *"the model **autonomously orchestrates** tool interaction during inference"*. É o orquestrador virando objeto de estudo — e o componente que decide *se* e *como* os demais são acionados. ✓

(Bibliografia completa: [`bibliografia.md`](../bibliografia.md).)

## Fontes da indústria

- **A convergência de fato** — as arquiteturas publicadas por fornecedores e praticantes divergem em nomes e concordam em estrutura: um caminho de **indexação** (offline) e um caminho de **consulta** (online), ligados por um índice, com uma camada de avaliação e uma de observabilidade em volta.
- **O erro de desenho mais comum** — tratar a indexação como script de setup, e não como componente de primeira classe com versão, teste e reprocessamento. É o que o cap. 04 chama de teto do corpus.
- **O componente que a maioria não desenha** — a **camada de aumento**. Entre "o índice devolveu 20 trechos" e "o modelo recebeu o contexto" há decisões (quantos entram, em que ordem, comprimidos ou não, com que metadado) que costumam viver espalhadas no código, sem dono.

## O estado da arte

### 1. Os dois caminhos

Todo sistema de RAG tem dois caminhos com ritmos, custos e donos diferentes — e confundi-los é a origem de metade dos problemas de arquitetura:

```
CAMINHO DE INDEXAÇÃO  (offline · lote · caro uma vez)
  fontes → aquisição → extração → normalização → dedup
         → enriquecimento (metadado) → chunking → embedding → ÍNDICE

CAMINHO DE CONSULTA   (online · por requisição · caro sempre)
  pergunta → entendimento da consulta → recuperação → aumento
           → montagem do contexto → geração → resposta (+ citações)

EM VOLTA DOS DOIS
  orquestração · avaliação · observabilidade · guardrails · cache
```

A assimetria entre eles é a decisão econômica que atravessa o livro: **o que se paga uma vez** (indexação) **e o que se paga para sempre** (consulta). Empurrar trabalho para a indexação é quase sempre o movimento certo em sistemas com muitas consultas — e o errado em corpus que muda toda hora.

### 2. O inventário de componentes

| # | Componente | Decide | Falha típica | Onde no livro |
|---|---|---|---|:---:|
| 1 | **Aquisição** | o que entra no sistema | fonte esquecida; conteúdo que não deveria estar lá | 04 |
| 2 | **Extração** | texto a partir do formato | tabela virando sopa; PDF embaralhado | 04 |
| 3 | **Enriquecimento** | metadado por unidade | sem `status`, sem `permissao` — os dois incidentes caros | 04 |
| 4 | **Chunking** | a unidade indexável | corte que destrói o antecedente | 05 |
| 5 | **Embedding** | a representação vetorial | modelo fora do domínio; comprimento máximo | 05 |
| 6 | **Índice** | como se armazena e se busca | filtro aplicado depois da busca | 06 |
| 7 | **Retriever** | os candidatos | não acha o literal; não acha a paráfrase | 06 |
| 8 | **Reranker** | a ordem final | ausente — e o `top_k` vira ruído pago | 07 |
| 9 | **Entendimento da consulta** | o que se busca, afinal | pergunta ≠ resposta; referência entre turnos | 08 |
| 10 | **Aumento** | o que dos candidatos vira contexto | tudo entra, sem orçamento nem ordem | 20 |
| 11 | **Gerador** | a resposta | responde de memória em vez do recuperado | 15 |
| 12 | **Orquestrador** | se, quando e quantas vezes buscar | laço sem teto; custo imprevisível | 18 |
| 13 | **Avaliador** | se está bom | mede a resposta e não a recuperação | 21 |
| 14 | **Observabilidade** | o que está mudando | nenhum sinal até o usuário reclamar | 21 |
| 15 | **Guardrails** | o que não pode passar | conteúdo recuperado tratado como instrução | 22 |
| 16 | **Cache** | o que não precisa ser refeito | chave sem permissão — vazamento | 23 |

Dezesseis componentes é mais do que a maioria dos sistemas tem **explicitamente** — e essa é a observação do capítulo. Eles existem em qualquer RAG que funcione; a diferença entre um sistema mantível e um emaranhado é se cada um tem **nome, dono e contrato**, ou se está diluído em funções que fazem três coisas.

### 3. Os contratos importam mais que as implementações

A parte de engenharia deste capítulo não é a lista — é o que atravessa as setas. Quatro contratos que decidem a saúde do sistema:

- **Chunk → índice.** O que viaja junto do texto: id, origem, seção, data, `status`, permissão, hash. Um chunk sem esse envelope condena o sistema a filtrar depois de buscar (cap. 06) e a não conseguir invalidar por fonte (cap. 22).
- **Retriever → aumento.** O que volta não é texto: é **texto + nota + procedência**. Sistemas que devolvem só as strings perdem a nota, e sem nota não há limiar, não há abstenção e não há taxa de resultado zero (cap. 21).
- **Aumento → gerador.** O contexto montado precisa dizer, no próprio texto, **o que é dado e de onde veio** — é o que torna citação possível (cap. 15) e injeção mais difícil (cap. 22).
- **Gerador → resposta.** A saída não é prosa: é resposta **+ referências + sinal de confiança**. Quem devolve só a prosa não consegue medir *faithfulness* nem oferecer "não sei".

Repare no padrão: **os quatro contratos são sobre carregar procedência adiante.** Um sistema que perde a proveniência em qualquer uma dessas fronteiras não consegue citar, auditar nem se defender — e recuperá-la depois é caro ou impossível.

### 4. Como usar este mapa

O uso prático é diagnóstico. Diante de uma falha, o mapa faz a pergunta certa antes da cura:

| O que se observa | Componente suspeito |
|---|---|
| Não encontra o que existe | 6, 7 — e antes deles, 4 e 5 |
| Encontra e traz lixo junto | 8, 10 |
| Cita documento revogado | 3 — não adianta mexer em 6–8 |
| Responde bem, mas inventa a fonte | 11, 15 |
| Custa/demora demais | 10, 12, 16 |
| Piorou e ninguém sabe quando | 14 — a ausência dele é a falha |

E o uso editorial: **cada capítulo de técnica deste livro declara, no cabeçalho, qual componente aprofunda.** É o que impede o livro de virar o catálogo que ele critica.

### Leitura executiva

RAG não é uma técnica, é um **sistema com dois caminhos**: indexação (offline, caro uma vez) e consulta (online, caro sempre) — e a assimetria entre eles é a decisão econômica que atravessa o livro. Sobre eles, **16 componentes** que existem em qualquer RAG funcional; o que separa sistema mantível de emaranhado é cada um ter **nome, dono e contrato**. **O que roubar:** o componente que quase ninguém desenha é o **aumento** — o que acontece *entre* buscar e responder (quantos trechos entram, em que ordem, comprimidos ou não). Ele costuma viver espalhado no código, sem dono, e é onde o orçamento vaza. **A regra que vale mais que o inventário:** os quatro contratos entre componentes são todos sobre **carregar procedência adiante** — chunk com envelope, resultado com nota e origem, contexto que declara o que é dado, resposta com referências. Perdeu a proveniência em qualquer fronteira, o sistema não consegue citar, auditar nem se defender — e recuperá-la depois é caro ou impossível. **Use como diagnóstico:** cita documento revogado é componente 3, e nenhum ajuste em busca ou reranking resolve.

## Mão na massa — rag-zero, etapa 1

Na etapa 1 você não escreve técnica nenhuma: desenha o esqueleto do `rag-zero` com os dezesseis componentes como interfaces vazias, e um teste que verifica os **contratos** — um chunk sem `status` não entra no índice; um resultado sem nota não passa para o aumento. Só depois as etapas seguintes preenchem cada caixa. O exercício de completude: o envelope do chunk vem esqueletado, e você decide quais campos são obrigatórios — descobrindo que essa é a decisão mais consequente da etapa.

## Verificação

1. Seu sistema responde citando uma política revogada. Percorra a tabela de diagnóstico: quais componentes você **não** deve tocar, e por quê?
2. Dê um exemplo concreto de informação que se perde na fronteira retriever → aumento quando o contrato devolve apenas strings.
3. Por que empurrar trabalho para o caminho de indexação é a decisão certa em um sistema com muitas consultas — e errada em um corpus volátil?

---

## Apêndice A — Como cada framework nomeia os componentes

> Tratamento por implementação, com URL. O valor deste apêndice é o **dicionário**: o mesmo componente tem três nomes.

| Componente (cap. 02) | [LangChain](https://github.com/langchain-ai/langchain) | [LlamaIndex](https://github.com/run-llama/llama_index) | [Haystack](https://github.com/deepset-ai/haystack) |
|---|---|---|---|
| corte | *text splitter* | *node parser* | *splitter* |
| unidade indexada | *document* | *node* | *document* |
| busca | *retriever* | *retriever* | *retriever* |
| pós-recuperação | *document compressor* | *node postprocessor* | *ranker* / *joiner* |
| montagem do contexto | *prompt template* | *response synthesizer* | *prompt builder* |
| fluxo | *chain* / *graph* | *query engine* / *workflow* | *pipeline* |

**O que a tabela revela, e é o ponto do capítulo:** os três convergem na mesma anatomia. As divergências são de vocabulário, não de desenho — e é por isso que vale aprender os **componentes**, não um framework.

**A pegadinha comum aos três:** nenhum deles carrega procedência de ponta a ponta por padrão. O identificador que chega ao gerador costuma ser o que **você** colocou no metadado (cap. 04) — se não colocou, a citação do cap. 15 não tem em que se apoiar.
