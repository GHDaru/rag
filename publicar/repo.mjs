// Base pública do repositório — a FONTE ÚNICA do ADR 0015.
//
// No fonte do livro, toda referência a arquivo do próprio repositório é escrita como
// **caminho relativo** (`../../rag-zero/rag_zero/bm25.py`). O motor a converte na URL
// pública; o GitHub a resolve nativamente quando alguém lê o `.md`. URL absoluta no
// fonte é proibida: codificaria a branch em dezenas de pontos, e — porque é um link
// externo — nenhum portão do build a validaria. Era exatamente o estado até este ADR.
//
// `ref` é a **tag da edição**, não `main`: o leitor da 1.0 deve ver o código da 1.0, e
// não o de amanhã. Um livro que data a captura no cabeçalho de cada capítulo não pode
// apontar para alvo móvel no corpo. Enquanto a tag não existe, cai para `main` — com
// aviso no log, nunca em silêncio, porque fallback mudo vira permanente.

import { readFileSync, existsSync } from "node:fs";
import { execSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import path from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
export const RAIZ = resolve(AQUI, "..");

const cfg = {
  base: "https://github.com/GHDaru/rag",
  ref: "main",
  ...(JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8")).repo || {}),
};

const refExiste = (ref) => {
  if (ref === "main") return true;
  try {
    execSync(`git -C "${RAIZ}" rev-parse --verify --quiet ${JSON.stringify(ref)}`, { stdio: "pipe" });
    return true;
  } catch {
    return false;
  }
};

export const REPO_URL = cfg.base;
export const REPO_REF = refExiste(cfg.ref) ? cfg.ref : "main";
export const REF_PEDIDA = cfg.ref;
export const GITHUB_BASE = `${REPO_URL}/blob/${REPO_REF}/`;
export const GITHUB_TREE = `${REPO_URL}/tree/${REPO_REF}/`;

/** Caminho relativo do fonte → caminho a partir da raiz do repositório.
 *  Usado nas duas superfícies (HTML e `.md` baixável), para que a regra seja a mesma. */
export const caminhoNoRepo = (srcDir, alvo) =>
  path.posix.normalize(path.posix.join(srcDir || ".", alvo)).replace(/^(\.\.\/)+/, "");

/** O alvo existe no disco? É o que torna a afirmação do livro verificável. */
export const existeNoRepo = (repoRel) => existsSync(resolve(RAIZ, repoRel));
