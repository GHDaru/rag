"""As portas do rag-zero — e os adaptadores que não custam nada.

Regra 2 da construção (constituição, "Restrições"): **arquitetura hexagonal por
refatoração**. Cada porta nasce da dor de um capítulo, nunca antecipada:

- `LLMPort`      — etapa 0 (cap. 01): o modelo atrás de uma interface, para que
                   nenhuma etapa dependa de credencial para rodar.
- `EmbedderPort` — etapa 4 (cap. 05): a representação é decisão trocável, e
                   trocá-la obriga a reindexar. A porta torna isso explícito.
- `RerankerPort` — etapa 6 (cap. 07): o reranker é caro, e o adaptador é o lugar
                   onde o teto de custo mora.

Os adaptadores daqui são **falsos de propósito**. Eles existem para que a trilha
inteira rode com `python3 etapas/etapaNN_*.py`, sem chave de API e sem GPU
(Princípio VI). O adaptador de verdade entra atrás da mesma porta — e o ponto
pedagógico é justamente que o resto do código não muda.
"""

from __future__ import annotations

import hashlib
import math
import re
import unicodedata
from typing import Protocol


# --------------------------------------------------------------------------- #
# Normalização — compartilhada por todo o pipeline.
#
# Fica aqui, e não em cada módulo, porque **indexação e consulta precisam usar a
# mesma função**. Quando elas divergem, o sintoma é recall baixo sem causa
# aparente — e ninguém procura o defeito aqui.
# --------------------------------------------------------------------------- #

_STOP = frozenset(
    "de da do das dos a o e que em para com sem por no na nos nas um uma os as se "
    "ao à é são como mais ou seu sua ser tem foi mas já não the of to and in is an".split()
)


def normalizar(texto: str) -> list[str]:
    """Minúsculas, sem acento, só alfanumérico, sem stopwords, mínimo 3 letras."""
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return [t for t in re.findall(r"[a-z0-9]+", texto) if len(t) > 2 and t not in _STOP]


# --------------------------------------------------------------------------- #
# LLMPort
# --------------------------------------------------------------------------- #

class LLMPort(Protocol):
    """O modelo, atrás de uma interface. Etapa 0."""

    def gerar(self, prompt: str, *, max_tokens: int = 512) -> str: ...


class LLMEco:
    """Adaptador que não chama modelo nenhum.

    Devolve uma resposta determinística construída a partir do próprio prompt.
    Serve para dois propósitos didáticos:

    1. provar que o pipeline roda ponta a ponta sem credencial;
    2. deixar **visível** o que foi realmente enviado ao modelo — o que, na
       prática, é o instrumento que falta na maioria dos sistemas (cap. 20).
    """

    def __init__(self) -> None:
        self.chamadas: list[str] = []

    def gerar(self, prompt: str, *, max_tokens: int = 512) -> str:
        self.chamadas.append(prompt)
        marca = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:8]
        return f"[eco {marca}] recebi {len(prompt)} caracteres de prompt"


# --------------------------------------------------------------------------- #
# EmbedderPort
# --------------------------------------------------------------------------- #

class EmbedderPort(Protocol):
    """A representação vetorial, atrás de uma interface. Etapa 4."""

    dimensao: int

    def embutir(self, texto: str) -> list[float]: ...


class EmbedderHashing:
    """Embedder de *hashing* — o mecanismo sem a semântica.

    **Leia isto antes de tirar conclusão de qualquer número que ele produza.**

    Ele projeta os termos em `dimensao` posições por hash e normaliza o vetor.
    Isso reproduz fielmente a **mecânica** da busca densa — vetor, cosseno,
    vizinhança — e serve para você ver o ranking acontecer sem baixar 400 MB de
    modelo nem depender de rede.

    O que ele **não** faz é o que mais importa: ele não sabe que "carro" e
    "veículo" são parecidos. Termos diferentes caem em posições diferentes, e
    pronto. Ou seja: ele tem exatamente o **ponto cego da busca esparsa**, com o
    custo da densa — o pior dos dois mundos, de propósito.

    Isso é um **erro didático deliberado** (regra 4 da construção). A etapa 5 o
    usa para demonstrar, com uma pergunta concreta, que a busca densa só paga
    quando o embedder carrega semântica de verdade. Trocar este adaptador por um
    modelo real é uma linha — e é esse o ponto da porta.
    """

    def __init__(self, dimensao: int = 256) -> None:
        self.dimensao = dimensao

    def embutir(self, texto: str) -> list[float]:
        vetor = [0.0] * self.dimensao
        for termo in normalizar(texto):
            h = int(hashlib.md5(termo.encode("utf-8")).hexdigest(), 16)
            # sinal por hash: evita que todos os termos empurrem na mesma direção
            vetor[h % self.dimensao] += 1.0 if (h >> 8) % 2 else -1.0
        norma = math.sqrt(sum(v * v for v in vetor))
        return [v / norma for v in vetor] if norma else vetor


def cosseno(a: list[float], b: list[float]) -> float:
    """Similaridade de cosseno. Assume vetores já normalizados."""
    return sum(x * y for x, y in zip(a, b))


# --------------------------------------------------------------------------- #
# RerankerPort
# --------------------------------------------------------------------------- #

class RerankerPort(Protocol):
    """A reordenação cara, atrás de uma interface. Etapa 6."""

    def pontuar(self, consulta: str, documento: str) -> float: ...


class RerankerLexical:
    """*Stand-in* de cross-encoder, em Python puro.

    Um cross-encoder de verdade lê consulta e documento **juntos** e devolve uma
    nota de relevância da relação. Este adaptador aproxima isso com cobertura de
    termos da consulta pelo documento — o que captura a **forma** da nota (0 a 1,
    comparável dentro de uma consulta) sem capturar a compreensão.

    Serve para a etapa 6 exercitar o que o capítulo diz que importa: usar a
    **nota** como limiar de corte, e não só a ordem. A pegadinha registrada no
    Apêndice A do cap. 07 vale igual aqui: a nota é comparável dentro de uma
    consulta, **não** entre consultas nem entre versões do modelo.
    """

    def pontuar(self, consulta: str, documento: str) -> float:
        termos = set(normalizar(consulta))
        if not termos:
            return 0.0
        no_doc = set(normalizar(documento))
        return len(termos & no_doc) / len(termos)


# --------------------------------------------------------------------------- #
# Adaptadores de LLM que encenam modos de falha — etapa 10
#
# A etapa 10 precisa demonstrar que a verificação de citação FUNCIONA, e para
# isso precisa de respostas ruins de propósito. Estes adaptadores produzem cada
# modo de falha do cap. 15 de forma determinística, sem gastar um token.
#
# Não são simulação de modelo: são **casos de teste executáveis** do verificador.
# --------------------------------------------------------------------------- #

class LLMFundamentado:
    """Obedece às três exigências: usa só o material, cita, e abstém quando falta.

    Extrai a primeira sentença de cada trecho e a cita. É burro de propósito —
    o que ele demonstra não é qualidade de redação, é **conformidade ao
    contrato**.
    """

    def gerar(self, prompt: str, *, max_tokens: int = 512) -> str:
        # Casa cada bloco <trecho>…</trecho> isoladamente. A âncora de abertura
        # é obrigatória: sem ela o `.*?` atravessa blocos e mistura os trechos.
        trechos = re.findall(r"<trecho[^>]*>\s*\[(T\d+)\]\s*(.*?)\s*</trecho>",
                             prompt, re.S)
        if not trechos:
            return "NAO_ENCONTRADO"
        partes = []
        for ident, corpo in trechos[:3]:
            frase = corpo.strip().split(".")[0].strip()
            if frase:
                partes.append(f"{frase} [{ident}].")
        return " ".join(partes) if partes else "NAO_ENCONTRADO"


class LLMAlucinado:
    """Cita um identificador que **não existe** no contexto enviado.

    É o modo de falha mais perigoso do cap. 15, porque a resposta *parece*
    verificável — tem colchetes, tem número, tem cara de fonte. Só que a fonte
    não existe. É exatamente isto que `geracao.verificar()` pega.
    """

    def gerar(self, prompt: str, *, max_tokens: int = 512) -> str:
        return ("O prazo é de 30 dias corridos [T1]. "
                "A contagem começa na data da nota fiscal [T7].")


class LLMDeMemoria:
    """Responde de memória: ignora a regra de ausência e não cita nada.

    Não inventa fonte — apenas responde. É o comportamento **padrão** de um
    modelo sem regra de ausência no prompt, e por isso o mais comum. A resposta
    pode até estar certa; o problema é que **não dá para conferir**.
    """

    def gerar(self, prompt: str, *, max_tokens: int = 512) -> str:
        return ("De acordo com a prática usual do setor, o prazo costuma ser "
                "de trinta dias. Vale confirmar com o suporte.")
