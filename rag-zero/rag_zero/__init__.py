"""rag-zero — o livro executável.

Construção prática do livro *Engenharia de RAG*, uma etapa por capítulo.
**Custo zero, sem GPU, sem rede e sem credencial** para o núcleo (Princípio VI):
o pacote inteiro roda com a biblioteca padrão do Python.

Onde os modelos de verdade entrariam, há uma **porta** (`rag_zero.portas`) com
um adaptador falso do outro lado. Isso não é atalho: é a regra 2 da construção
(arquitetura hexagonal por refatoração), e o ponto pedagógico é que trocar o
adaptador não muda nenhuma outra linha.
"""

__all__ = ["portas", "ingestao", "chunking", "bm25", "recuperacao",
           "contexto", "avaliacao"]
