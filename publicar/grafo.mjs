// Knowledge Graph do livro — extração DETERMINÍSTICA, sem LLM.
// Nós: capítulos, ferramentas/frameworks do ecossistema, conceitos-chave,
// etapas do contexto-zero. Arestas: menções reais no texto (peso = nº de
// ocorrências) — evidência verificável.
// Chamado pelo build.mjs a cada build ⇒ o grafo acompanha toda mudança do livro.

import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

// O ecossistema mapeado no panorama da comunidade (estudos/), com variantes de grafia.
const FERRAMENTAS = [
  { id: "dspy", rotulo: "DSPy", re: /\bDSPy\b/gi },
  { id: "gepa", rotulo: "GEPA", re: /\bGEPA\b/g },
  { id: "miprov2", rotulo: "MIPROv2", re: /\bMIPROv2\b/gi },
  { id: "textgrad", rotulo: "TextGrad", re: /\bTextGrad\b/gi },
  { id: "ragas", rotulo: "RAGAS", re: /\bRAGAS\b/gi },
  { id: "deepeval", rotulo: "DeepEval", re: /\bDeepEval\b/gi },
  { id: "beir", rotulo: "BEIR", re: /\bBEIR\b/g },
  { id: "mteb", rotulo: "MTEB", re: /\bMTEB\b/g },
  { id: "bm25", rotulo: "BM25", re: /\bBM25\b/gi },
  { id: "mem0", rotulo: "Mem0", re: /\bMem0\b/gi },
  { id: "zep", rotulo: "Zep", re: /\bZep\b/g },
  { id: "letta", rotulo: "Letta / MemGPT", re: /\b(?:Letta|MemGPT)\b/g },
  { id: "graphrag", rotulo: "GraphRAG", re: /\bGraphRAG\b/gi },
  { id: "raptor", rotulo: "RAPTOR", re: /\bRAPTOR\b/g },
  { id: "self-rag", rotulo: "Self-RAG", re: /\bSelf-RAG\b/gi },
  { id: "crag", rotulo: "CRAG", re: /\bCRAG\b/g },
  { id: "flare", rotulo: "FLARE", re: /\bFLARE\b/g },
  { id: "adaptive-rag", rotulo: "Adaptive RAG", re: /\bAdaptive RAG\b/gi },
  { id: "owasp", rotulo: "OWASP LLM Top 10", re: /\bOWASP\b/g },
];

// Conceitos com verbete próprio no glossário.
const CONCEITOS = [
  { id: "rag", rotulo: "RAG", re: /\bRAG\b/g },
  { id: "mcp", rotulo: "MCP", re: /\bMCP\b/g },
  { id: "cot", rotulo: "Chain-of-Thought", re: /\b(?:Chain-of-Thought|CoT)\b/g },
  { id: "react", rotulo: "ReAct", re: /\bReAct\b/g },
  { id: "embedding", rotulo: "embedding", re: /\bembeddings?\b/gi },
  { id: "chunk", rotulo: "chunk", re: /\bchunks?\b/gi },
  { id: "reranking", rotulo: "reranking", re: /\breranking|reranker(?:s)?\b/gi },
  { id: "context-rot", rotulo: "context rot", re: /\bcontext rot\b/gi },
  { id: "prompt-injection", rotulo: "prompt injection", re: /\bprompt injection\b/gi },
  { id: "few-shot", rotulo: "few-shot", re: /\bfew-shot\b/gi },
  { id: "hyde", rotulo: "HyDE", re: /\bHyDE\b/g },
  { id: "step-back", rotulo: "step-back", re: /\bstep-back\b/gi },
  { id: "corpus", rotulo: "higiene do corpus", re: /\bcorpus\b/gi },
  { id: "llm-as-judge", rotulo: "LLM-as-judge", re: /\bLLM-as-judge\b/gi },
  { id: "prefix-cache", rotulo: "prefix caching", re: /\bprefix cach\w*|cache de prefixo\b/gi },
];

const ETAPAS = [
  "00 chat + porta LLM", "01 prompt em camadas", "02 raciocínio", "03 saída estruturada",
  "04 persona e regras", "05 otimizador de prompt", "06 eval de prompt", "07 orçamento",
  "08 índice e busca", "09 híbrido + rerank", "10 RAG agêntico", "11 memória",
  "12 compactação", "13 ferramentas", "14 eval do sistema", "15 defesa de injeção",
];

const GH = "https://github.com/GHDaru/rag/tree/main/contexto-zero";

function contar(re, texto) {
  const m = texto.match(re);
  return m ? m.length : 0;
}

export function gerarGrafo(itens, RAIZ, versao) {
  const capitulos = itens.filter((i) => /^\s*\d+\s*—/.test(i.titulo));
  const nos = [];
  const arestas = [];
  const addAresta = (de, para, peso) => { if (peso > 0 && de !== para) arestas.push({ de, para, peso }); };

  for (const c of capitulos) {
    const num = c.titulo.match(/^\s*(\d+)/)[1];
    nos.push({ id: "cap-" + num, tipo: "capitulo", rotulo: c.titulo, url: c.slug + ".html" });
  }
  for (const h of FERRAMENTAS) nos.push({ id: h.id, tipo: "ferramenta", rotulo: h.rotulo, url: "apendice-ecossistema.html" });
  for (const co of CONCEITOS) nos.push({ id: co.id, tipo: "conceito", rotulo: co.rotulo, url: "glossario.html" });
  ETAPAS.forEach((e, i) => {
    const n = String(i).padStart(2, "0");
    nos.push({ id: "etapa-" + n, tipo: "etapa", rotulo: "etapa " + e, url: GH });
  });

  for (const c of capitulos) {
    const caminho = resolve(RAIZ, c.arquivo);
    if (!existsSync(caminho)) continue;
    const num = c.titulo.match(/^\s*(\d+)/)[1];
    const id = "cap-" + num;
    // corpo sem blocos de código (código cita nomes por razões mecânicas, não conceituais)
    const texto = readFileSync(caminho, "utf8").replace(/```[\s\S]*?```/g, " ");

    // capítulo → capítulo ("cap. NN" / "capítulo NN")
    const porCap = {};
    for (const m of texto.matchAll(/\bcap(?:ítulos?|s?\.)\s*(\d{1,2})\b/gi)) {
      const alvo = String(parseInt(m[1], 10)).padStart(2, "0");
      if (alvo !== num && capitulos.some((x) => x.titulo.startsWith(alvo))) porCap[alvo] = (porCap[alvo] || 0) + 1;
    }
    for (const alvo of Object.keys(porCap)) addAresta(id, "cap-" + alvo, porCap[alvo]);

    for (const h of FERRAMENTAS) addAresta(id, h.id, contar(h.re, texto));
    for (const co of CONCEITOS) addAresta(id, co.id, contar(co.re, texto));

    // capítulo → etapa ("etapa N" — tipicamente na Mão na massa)
    const porEtapa = {};
    for (const m of texto.matchAll(/\betapas?\s+(\d{1,2})\b/gi)) {
      const n = String(parseInt(m[1], 10)).padStart(2, "0");
      if (parseInt(n, 10) <= 15) porEtapa[n] = (porEtapa[n] || 0) + 1;
    }
    for (const n of Object.keys(porEtapa)) addAresta(id, "etapa-" + n, porEtapa[n]);
  }

  // poda: nós sem nenhuma aresta saem (mantém o grafo honesto)
  const conectados = new Set();
  arestas.forEach((a) => { conectados.add(a.de); conectados.add(a.para); });
  const nosFinais = nos.filter((n) => conectados.has(n.id));

  return { versao, nos: nosFinais, arestas };
}
