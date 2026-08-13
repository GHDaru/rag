# DIFF — o que cada etapa acrescenta

> **Gerado** por [`ferramentas/diff_etapas.py`](ferramentas/diff_etapas.py) a partir
> do código. Não edite à mão: a próxima geração apaga. Decisão em
> [ADR 0014](../adr/0014-autocontencao-das-etapas.md).

No livro irmão, a lição de cada etapa está no `git diff` entre dois diretórios.
Aqui o núcleo é único e testado, e o diff é **calculado**: para cada etapa, os
módulos e símbolos do núcleo que ela passa a usar, mais a decisão que ela
introduz — a única parte declarada à mão, porque nenhuma máquina a infere.

| Etapa | Acrescenta | Decide | Prova |
|:---:|---|---|---|
| **00** | `contexto.Contexto`, `portas.LLMEco` | medir o contexto por bloco antes de otimizar qualquer coisa: sem o instrumento, toda decisão seguinte é palpite | `test_bloco_externo_e_delimitado_e_rotulado`, `test_contador_nunca_subestima_palavras`, `test_contador_reporta_composicao_por_bloco`, `test_montagem_e_deterministica` |
| **02** | `pipeline.CaminhoDeIndexacao`, `pipeline.NaiveRAG`, `pipeline.procedencia_sobreviveu`, `portas.LLMFundamentado` | fechar o circuito inteiro na forma mais burra possível — a linha de base contra a qual todo ganho posterior é medido | `test_citacao_fora_dos_candidatos_e_pega_no_pipeline`, `test_identificador_do_chunk_e_estavel`, `test_procedencia_atravessa_os_quatro_contratos` |
| **03** | `bm25.BM25`, `ingestao.Documento`, `ingestao.enriquecer`, `ingestao.filtrar_indexaveis`, `ingestao.ingerir` | a governança do corpus entra ANTES da técnica: proveniência e deduplicação são o que nenhum reranking conserta depois | `test_deduplicacao_por_hash`, `test_gerado_carrega_confianca`, `test_metadado_gerado_nao_filtra_de_forma_dura`, `test_normalizacao_preserva_o_rotulo_do_link`, `test_permissao_filtra_antes_da_busca`, `test_revogado_nao_e_recuperado_com_governanca`, `test_revogado_ranqueia_bem_sem_governanca` |
| **05** | `avaliacao.Caso`, `avaliacao.avaliar`, `portas.EmbedderHashing`, `portas.RerankerLexical`, `recuperacao.BuscaDensa`, `recuperacao.fundir`, `recuperacao.rerankear` | esparso e denso não competem, se somam — e a fusão é por posição, não por nota, porque as escalas não são comparáveis | `test_bm25_acha_identificador_literal`, `test_bm25_normaliza_por_comprimento`, `test_bm25_pondera_por_raridade`, `test_busca_densa_roda_sem_dependencia`, `test_embedder_hashing_e_deterministico_e_normalizado`, `test_embedder_hashing_nao_capta_parafrase`, `test_fusao_dispensa_escalas_comparaveis`, `test_fusao_premia_quem_aparece_nas_duas_listas` |
| **06** | `recuperacao.RecuperadorHibrido` | a nota do reranker vira limiar: é o único estágio que devolve número calibrável, e é ele que instala a abstenção | `test_abstencao_quando_nada_passa_do_limiar`, `test_reranker_usa_a_nota_como_limiar` |
| **07** | `consulta.Consulta`, `consulta.entender`, `consulta.precisa_resolver`, `consulta.rotear` | otimizar a pergunta, não o índice — e declarar que isso é custo por consulta, pago para sempre | `test_padroes_da_consulta_sao_conservadores`, `test_portao_de_reescrita_evita_chamada_desnecessaria`, `test_roteamento_separa_estruturado_global_e_texto` |
| **08** | `indexacao.ChunkIndexado`, `indexacao.IndiceDenso`, `indexacao.contexto_estrutural`, `indexacao.custo_estimado` | empurrar o trabalho para a indexação, onde se paga uma vez; contextual e late chunking medidos lado a lado | `test_contexto_estrutural_nao_contamina_a_entrega`, `test_late_chunking_nao_gasta_chamada_de_llm`, `test_vetor_com_vizinhanca_continua_normalizado` |
| **09** | `raptor.Raptor` | a pergunta global não se responde com trecho: exige um nível de agregação que o corpus não tem, e que a árvore constrói | `test_limiar_derivado_do_corpus_nao_e_chute`, `test_raptor_busca_em_qualquer_nivel`, `test_raptor_condensa_a_cada_nivel`, `test_resumo_extrativo_nao_inventa_frase` |
| **10** | `geracao.Trecho`, `geracao.gerar`, `portas.LLMAlucinado`, `portas.LLMDeMemoria` | a metade esquecida da sigla: citação verificável e abstenção, com a verificação pegando o defeito | `test_abstencao_conta_como_fundamentada`, `test_citacao_inexistente_e_pega`, `test_gerador_fundamentado_cita_o_que_existe`, `test_resposta_de_memoria_e_recusada_por_nao_ser_conferivel`, `test_sem_trechos_o_modelo_nao_e_chamado`, `test_trecho_externo_entra_delimitado_e_com_procedencia` |

## Por etapa

### Etapa 00 — Etapa 0 — o contador de tokens por bloco (cap. 01).

- **Vem de:** primeira etapa
- **Módulos novos:** `contexto`, `portas`
- **Rodar:** `python3 etapas/etapa00_contador.py`

### Etapa 02 — Etapas 1 e 2 — os contratos e o Naive RAG: **a linha de base** (caps. 02, 03).

- **Vem de:** vem da etapa 0
- **Módulos novos:** `pipeline`
- **Rodar:** `python3 etapas/etapa02_naive.py`

### Etapa 03 — Etapa 3 — ingestão e governança (cap. 04).

- **Vem de:** vem da etapa 2
- **Módulos novos:** `bm25`, `ingestao`
- **Rodar:** `python3 etapas/etapa03_ingestao.py`

### Etapa 05 — Etapa 5 — esparso, denso e a fusão, medidos com o mesmo conjunto (cap. 06).

- **Vem de:** vem da etapa 3
- **Módulos novos:** `avaliacao`, `recuperacao`
- **Rodar:** `python3 etapas/etapa05_busca.py`

### Etapa 06 — Etapa 6 — reranking, a nota como limiar, e o caminho de "não encontrei".

- **Vem de:** vem da etapa 5
- **Módulos novos:** —
- **Rodar:** `python3 etapas/etapa06_reranking.py`

### Etapa 07 — Etapa 7 — o lado da pergunta, medido contra a linha de base (cap. 08).

- **Vem de:** vem da etapa 6
- **Módulos novos:** `consulta`
- **Rodar:** `python3 etapas/etapa07_consulta.py`

### Etapa 08 — Etapa 8 — indexação refinada: as duas curas lado a lado (cap. 09).

- **Vem de:** vem da etapa 7
- **Módulos novos:** `indexacao`
- **Rodar:** `python3 etapas/etapa08_indexacao.py`

### Etapa 09 — Etapa 9 — RAPTOR reduzido: pergunta global × pergunta factual (cap. 10).

- **Vem de:** vem da etapa 8
- **Módulos novos:** `raptor`
- **Rodar:** `python3 etapas/etapa09_raptor.py`

### Etapa 10 — Etapa 10 — o gerador fundamentado, e a verificação da citação (cap. 15).

- **Vem de:** vem da etapa 9
- **Módulos novos:** `geracao`
- **Rodar:** `python3 etapas/etapa10_geracao.py`
