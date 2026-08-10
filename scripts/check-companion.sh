#!/usr/bin/env bash
# Portão: a força da afirmação sobre o companion não pode passar do estado real.
#
# Invariante bidirecional — e é a bidirecionalidade que importa:
#   companion_backend VAZIO      -> nenhuma afirmação no presente sobre publicação
#   companion_backend PREENCHIDO -> /health tem de responder
#
# Ou seja: afirmar sem publicar quebra, e publicar sem atualizar o texto também.
# A falha que este script previne já aconteceu duas vezes neste repositório e foi
# corrigida à mão nas duas (ver ADR 0010).
#
# `adr/` e `livro/HISTORICO.md` são imunes por desenho: registro histórico e
# decisão aceita não se reescrevem (Princípio IV).
set -uo pipefail
cd "$(dirname "$0")/.."

BACKEND=$(python3 -c "import json;print(json.load(open('publicar/sumario.json')).get('companion_backend',''))")
FALHAS=0

# O que a checagem OLHA: texto publicado e código. O que ela IGNORA, e por quê:
#   adr/, livro/HISTORICO.md  -> registro histórico e decisão aceita não se
#                                reescrevem (Princípio IV); são imunes por desenho
#   specs/                    -> artefato de planejamento discute a decisão,
#                                não a afirma
#   docs/, corpus.json        -> gerados pelo build; a fonte é que manda
afirmacoes() {
  grep -rInE "(companion|rag-zero)[^.?]{0,80}(está|é|roda|rodando)[^.?]{0,25}(em produção|no ar|ao vivo)" \
    --include="*.md" --include="*.py" --include="*.js" . 2>/dev/null \
    | grep -v "^\./adr/" | grep -v "^\./livro/HISTORICO.md" \
    | grep -v "^\./specs/" | grep -v "^\./docs/" \
    | grep -v "^\./scripts/check-companion.sh"
}

if [ -z "$BACKEND" ]; then
  echo "companion_backend vazio — o companion NÃO está publicado."
  SAIDA=$(afirmacoes)
  if [ -n "$SAIDA" ]; then
    echo "✗ afirmação no presente sobre publicação, sem instância publicada:"
    echo "$SAIDA"
    FALHAS=1
  else
    echo "✓ nenhuma afirmação mais forte que o estado"
  fi
else
  echo "companion_backend = $BACKEND — exigindo prova de vida."
  if curl -fsS --max-time 10 "$BACKEND/health" >/dev/null 2>&1; then
    echo "✓ /health respondeu"
  else
    echo "✗ companion_backend está preenchido mas /health não responde"
    FALHAS=1
  fi
fi

# Todo link relativo dos .md do companion resolve em disco. Pega a classe de erro
# `specs/016-…` — que o link-check do motor de publicação não cobre, porque ele
# só olha páginas publicadas.
while IFS= read -r arquivo; do
  while IFS= read -r alvo; do
    [ -z "$alvo" ] && continue
    case "$alvo" in http*|\#*|mailto:*) continue ;; esac
    caminho="$(dirname "$arquivo")/${alvo%%#*}"
    if [ ! -e "$caminho" ]; then
      echo "✗ link quebrado em $arquivo -> $alvo"
      FALHAS=1
    fi
  done < <(grep -oE "\]\([^)]+\)" "$arquivo" | sed 's/^](//;s/)$//')
done < <(find chat-companion -name "*.md")

[ "$FALHAS" -eq 0 ] && echo "✓ check-companion verde" || echo "✗ check-companion falhou"
exit "$FALHAS"
