"""Etapa 7 — o lado da pergunta (cap. 08).

Os capítulos 06 e 07 otimizam **como se busca**. Este otimiza **o que se busca**,
partindo de um fato incômodo: às vezes o índice está bom e a **pergunta** é que
não se parece com a resposta.

Quatro transformações, e a regra econômica que atravessa todas: isto aqui é
**custo de consulta**, pago para sempre — ao contrário do cap. 09, onde se paga
uma vez na indexação.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .portas import LLMPort, normalizar


@dataclass
class Consulta:
    """A pergunta depois de passar pelo entendimento.

    `original` é preservada de propósito. Reescrever cedo demais destrói a
    pergunta do usuário — e quando a reescrita erra, você perde as duas. Guardar
    as duas e buscar com ambas é a mitigação barata (Apêndice A do cap. 08).
    """

    original: str
    variantes: list[str] = field(default_factory=list)
    rota: str = "texto"

    @property
    def todas(self) -> list[str]:
        """Original + variantes, sem duplicata, preservando a ordem."""
        vistas, saida = set(), []
        for q in [self.original, *self.variantes]:
            chave = " ".join(normalizar(q))
            if chave and chave not in vistas:
                vistas.add(chave)
                saida.append(q)
        return saida


# --------------------------------------------------------------------------- #
# Resolução de referência — o maior retorno, e o mais barato
# --------------------------------------------------------------------------- #

_PRONOMES = frozenset("ele ela isso isto aquilo esse essa este esta lá dele dela "
                      "nele nela outro outra mesmo mesma".split())


def precisa_resolver(pergunta: str, historico: list[str]) -> bool:
    """A pergunta depende do turno anterior?

    Heurística deliberadamente simples: pronome/anáfora sem substantivo próprio,
    ou pergunta muito curta. **Barata e falível** — e é assim que a maioria dos
    sistemas de produção faz, porque chamar um modelo a cada turno para descobrir
    se precisa chamar um modelo é o custo que ninguém aceita.

    O ponto do cap. 19 vale aqui: em RAG conversacional, a pergunta isolada
    quase nunca é autocontida, e buscar com ela é buscar a pergunta errada.
    """
    if not historico:
        return False
    termos = normalizar(pergunta)
    tem_pronome = any(p in pergunta.lower().split() for p in _PRONOMES)
    return tem_pronome or len(termos) <= 3


def resolver_referencia(pergunta: str, historico: list[str], llm: LLMPort) -> str:
    """Reescreve a pergunta em forma autocontida, usando o histórico.

    Custa **uma chamada por turno** — e só se `precisa_resolver` disser que sim.
    Esse portão é a diferença entre pagar sempre e pagar quando importa.
    """
    if not precisa_resolver(pergunta, historico):
        return pergunta
    contexto = "\n".join(historico[-4:])
    prompt = (
        "Reescreva a pergunta do usuário de forma autocontida, resolvendo "
        "pronomes e referências com base na conversa. Devolva SÓ a pergunta.\n\n"
        f"<conversa>\n{contexto}\n</conversa>\n\npergunta: {pergunta}"
    )
    reescrita = llm.gerar(prompt, max_tokens=80).strip()
    return reescrita or pergunta


# --------------------------------------------------------------------------- #
# Expansão e decomposição
# --------------------------------------------------------------------------- #

def multiplas_consultas(pergunta: str, llm: LLMPort, *, n: int = 3) -> Consulta:
    """Gera variantes da pergunta para cobrir vocabulários diferentes.

    **A pegadinha do Apêndice A, aqui como código:** N consultas produzem N
    listas, e sem **fusão por posição** (cap. 06) você só multiplicou o custo.
    Por isso esta função devolve uma `Consulta`, e quem chama funde — não há
    caminho em que as listas cheguem separadas ao gerador.
    """
    prompt = (
        f"Gere {n} reformulações da pergunta abaixo, cada uma em uma linha, "
        "usando vocabulários diferentes. Sem numeração.\n\n"
        f"pergunta: {pergunta}"
    )
    linhas = [l.strip(" -•\t") for l in llm.gerar(prompt).splitlines() if l.strip()]
    return Consulta(pergunta, variantes=linhas[:n])


def hyde(pergunta: str, llm: LLMPort) -> Consulta:
    """Gera uma resposta hipotética e busca por **ela** (HyDE).

    A intuição: uma resposta se parece mais com o documento do que a pergunta.

    **A condição experimental muda a recomendação, e está aqui por escrito:** o
    paper ([arXiv 2212.10496](https://arxiv.org/abs/2212.10496)) propõe HyDE para
    o cenário **zero-shot, sem rótulo de relevância**, comparado a um retriever
    denso **não supervisionado**. Contra um híbrido bem ajustado (cap. 06), o
    ganho encolhe — e você paga uma chamada de LLM (*Large Language Model*) por
    pergunta, para sempre.

    O risco próprio da técnica: a hipótese pode ser **alucinada**. O paper conta
    com o gargalo denso do encoder para filtrar o detalhe inventado; num sistema
    híbrido, o lado esparso pode casar justamente com o termo errado que a
    hipótese introduziu.
    """
    prompt = ("Escreva um parágrafo curto que responderia a pergunta abaixo, "
              "como se fosse um trecho de documentação.\n\n"
              f"pergunta: {pergunta}")
    return Consulta(pergunta, variantes=[llm.gerar(prompt, max_tokens=120).strip()])


# --------------------------------------------------------------------------- #
# Roteamento
# --------------------------------------------------------------------------- #

# Sinais de que a pergunta pede agregação — e agregação é trabalho de consulta
# estruturada, não de busca semântica sobre números (cap. 10).
_SINAIS_ESTRUTURADO = frozenset(
    "quantos quantas quanto total soma media média maior menor contagem "
    "percentual ranking listar count".split())

# Sinais de pergunta global: a resposta é propriedade do CONJUNTO (cap. 10).
_SINAIS_GLOBAL = frozenset(
    "temas tema recorrentes principais panorama resumo geral visao visão "
    "assuntos padroes padrões tendencias tendências".split())


def rotear(pergunta: str) -> str:
    """Classifica a pergunta e devolve a rota: `estruturado`, `global` ou `texto`.

    Roteador por **palavra-chave**, não por modelo — e isso é decisão, não
    preguiça: um roteador determinístico é auditável, tem custo zero e falha de
    forma previsível. Um classificador por LLM acerta mais e custa uma chamada
    por pergunta, para sempre. Comece pelo barato e meça se o caro paga.

    A survey de Gao descreve as duas famílias de roteamento — por **metadado**
    (estreita o escopo) e **semântica** — e nota que o híbrido das duas é
    possível. Este é o primeiro tipo.
    """
    termos = set(normalizar(pergunta)) | set(pergunta.lower().split())
    if termos & _SINAIS_ESTRUTURADO:
        return "estruturado"
    if termos & _SINAIS_GLOBAL:
        return "global"
    return "texto"


def entender(pergunta: str, llm: LLMPort, *, historico: list[str] | None = None,
             usar_hyde: bool = False, expandir: bool = False) -> Consulta:
    """O pipeline do lado da pergunta, com cada estágio **opcional**.

    Os padrões são conservadores de propósito: só a resolução de referência
    (barata, condicional, e de maior retorno) vem ligada. HyDE e expansão ficam
    desligados porque cada um custa uma chamada por pergunta **para sempre**, e
    o cap. 09 mostra a alternativa: empurrar o trabalho para a indexação, onde
    se paga uma vez.

    Ligar um deles sem medir contra a linha de base é exatamente o que a regra
    de sequência do cap. 09 proíbe.
    """
    base = resolver_referencia(pergunta, historico or [], llm)
    consulta = Consulta(base, rota=rotear(base))
    if usar_hyde:
        consulta.variantes.extend(hyde(base, llm).variantes)
    if expandir:
        consulta.variantes.extend(multiplas_consultas(base, llm).variantes)
    return consulta
