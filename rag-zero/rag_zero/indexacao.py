"""Etapa 8 — indexação refinada: as duas curas para o chunk sem contexto (cap. 09).

A falha específica: **o chunk perdeu o contexto de onde veio.** *"A margem caiu
12%"* é inútil sem saber de que produto e de que trimestre. O documento sabia; o
chunk não. E o índice trata o chunk como se ele se bastasse.

Duas curas, com contas de ordem de grandeza diferente:

- **Contextual Retrieval** — prefixa cada chunk com um resumo do seu lugar no
  documento, **antes** de embeddar e de indexar no BM25 (*Best Matching 25*).
  Custo: uma chamada de LLM (*Large Language Model*) por chunk.
- **Late Chunking** — embeda o documento inteiro e corta **depois** do
  transformer, antes do *pooling*. Custo: só o modelo de embedding.

E a correção que a rodada 2 trouxe, que este módulo materializa: **a escolha não
é só de preço**. A comparação publicada ([arXiv 2504.19754](https://arxiv.org/abs/2504.19754))
mede que o *contextual retrieval* preserva mais coerência semântica e custa mais,
enquanto o *late chunking* é mais eficiente e **sacrifica relevância e
completude**. Dois eixos, não um.

---

**As duas aproximações desta etapa, declaradas de frente.** Nenhuma das duas é a
técnica original, porque as duas exigem o que a trilha não tem (um LLM e um
embedder de contexto longo). O que elas preservam é o **mecanismo** e a
**assimetria de custo**, que é o que o capítulo ensina:

1. `contexto_estrutural` prefixa com o **caminho hierárquico** (arquivo › seção)
   em vez de um resumo gerado. É a versão de custo **zero** da mesma ideia — e
   vale saber que ela sozinha já resolve boa parte dos casos, porque a maior
   parte do contexto perdido no corte é justamente *de que seção isto veio*.
2. `vetor_com_vizinhanca` mistura ao vetor do chunk uma fração do vetor do
   documento. É o análogo pobre do *pooling* tardio: o chunk passa a carregar
   contexto dos vizinhos sem nenhuma chamada de LLM.
"""

from __future__ import annotations

from dataclasses import dataclass

from .portas import EmbedderPort


@dataclass
class ChunkIndexado:
    """O que vai para o índice — separado do que vai para o gerador.

    `texto_indexado` pode conter o prefixo de contexto; `texto_entrega` nunca.
    Misturar os dois é o erro que faz a citação do cap. 15 devolver ao leitor um
    texto que não existe no documento original.
    """

    texto_indexado: str
    texto_entrega: str
    origem: str
    secao: str


def contexto_estrutural(texto: str, origem: str, secao: str) -> ChunkIndexado:
    """*Contextual retrieval* de custo zero: prefixa o caminho hierárquico.

    O prefixo entra **no texto indexado** — portanto vale tanto para o embedding
    quanto para o índice esparso, que é exatamente o que a receita original faz
    (ela alimenta os dois lados, não só o vetorial).

    O que se perde em relação à versão com LLM: um resumo gerado sabe dizer *"a
    margem citada é do produto X no 3º trimestre"*; o caminho hierárquico só sabe
    dizer *"isto veio da seção Resultados"*. Para corpus bem estruturado, a
    diferença é menor do que a conta sugere — e este é o tipo de coisa que só se
    descobre medindo.
    """
    caminho = f"{origem.rsplit('/', 1)[-1]} › {secao}".strip(" ›")
    return ChunkIndexado(
        texto_indexado=f"[{caminho}] {texto}",
        texto_entrega=texto,
        origem=origem,
        secao=secao,
    )


def vetor_com_vizinhanca(vetor_chunk: list[float], vetor_documento: list[float],
                         *, peso: float = 0.3) -> list[float]:
    """*Late chunking* aproximado: o chunk carrega uma fração do documento.

    No método original, o contexto dos vizinhos entra **antes** do *pooling*,
    dentro do transformer. Aqui ele entra como mistura linear depois — o que é
    mais pobre, e preserva a propriedade que interessa: **nenhuma chamada de
    LLM**, só o embedder.

    `peso` é o *completion problem* desta etapa. Alto demais e todos os chunks de
    um documento ficam parecidos entre si (a busca perde precisão — que é
    exatamente o *"sacrifice relevance"* que a comparação publicada mede). Baixo
    demais e a técnica não faz nada.
    """
    misturado = [(1 - peso) * c + peso * d
                 for c, d in zip(vetor_chunk, vetor_documento)]
    norma = sum(v * v for v in misturado) ** 0.5
    return [v / norma for v in misturado] if norma else misturado


class IndiceDenso:
    """Índice denso com a estratégia de indexação como **parâmetro**.

    Ter as três estratégias atrás da mesma interface é o que permite a tabela da
    etapa 8: mesma pergunta, mesmo corpus, mesmo `k` — só a indexação muda.
    Sem isso, comparar é comparar sistemas diferentes.
    """

    def __init__(self, chunks: list[ChunkIndexado], embedder: EmbedderPort, *,
                 estrategia: str = "simples", peso_vizinhanca: float = 0.3) -> None:
        self.chunks = chunks
        self.embedder = embedder
        self.estrategia = estrategia

        if estrategia == "late":
            # Um vetor por documento, calculado uma vez — é o que torna a técnica
            # barata. Concatenar o documento inteiro por chunk seria o oposto.
            por_documento: dict[str, list[float]] = {}
            for c in chunks:
                if c.origem not in por_documento:
                    inteiro = " ".join(x.texto_entrega for x in chunks
                                       if x.origem == c.origem)
                    por_documento[c.origem] = embedder.embutir(inteiro)
            self.vetores = [
                vetor_com_vizinhanca(embedder.embutir(c.texto_entrega),
                                     por_documento[c.origem], peso=peso_vizinhanca)
                for c in chunks
            ]
        else:
            # "simples" usa o texto puro; "contextual" usa o texto já prefixado.
            campo = "texto_entrega" if estrategia == "simples" else "texto_indexado"
            self.vetores = [embedder.embutir(getattr(c, campo)) for c in chunks]

    def buscar(self, consulta: str, k: int = 5) -> list[int]:
        from .portas import cosseno
        v = self.embedder.embutir(consulta)
        notas = [(i, cosseno(v, vd)) for i, vd in enumerate(self.vetores)]
        notas = [(i, s) for i, s in notas if s > 0]
        notas.sort(key=lambda kv: (-kv[1], kv[0]))
        return [i for i, _ in notas[:k]]


def custo_estimado(n_chunks: int, n_documentos: int, estrategia: str) -> dict:
    """A conta do capítulo, explícita — porque ela é metade da decisão.

    Os números de chamada são **estruturais** (quantas vezes cada técnica precisa
    do modelo), não medições de tempo. O preço em dólar depende do provedor; o
    que não depende é a **ordem de grandeza**, e é ela que decide em corpus
    grande.
    """
    tabela = {
        "simples":    {"chamadas_llm": 0, "embeddings": n_chunks},
        "contextual": {"chamadas_llm": n_chunks, "embeddings": n_chunks},
        "late":       {"chamadas_llm": 0, "embeddings": n_chunks + n_documentos},
    }
    base = dict(tabela[estrategia])
    base["estrategia"] = estrategia
    # A referência publicada: US$ 1,02 por milhão de tokens de documento, com
    # cache de prompt. Aqui fica só a contagem de chamadas, que é o que não
    # expira com a tabela de preços.
    return base
