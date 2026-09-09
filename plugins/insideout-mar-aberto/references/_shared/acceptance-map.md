# Rastreabilidade entre princípios e testes

Esta matriz aponta onde cada princípio específico do InsideOut Mar Aberto é
materializado. O enunciado canônico permanece em `ARCHITECTURE.md`.

| Princípio | Contrato ou skill | Provas principais |
|---|---|---|
| Jornada principal com etapas retomáveis | `local-state.md`, `run-mar-aberto` | M6-T1–T8 |
| Feedback local sem GitHub | `skill-feedback`, `feedback-contract.md` | R02-G5-T1–T6 |
| Cobertura incompleta bloqueia análise | `collection-contract.md` | R02-G2-T1–T5, R02-G3-T4 |
| Relevância precede volume | `analysis-rubric.md` | M4-T3 |
| Autenticação pertence ao operador | `stilingue-contract.md`, `collection-contract.md` | M2 operacional, M3-T4 |
| Execução sob demanda | `run-mar-aberto` | M6-T1 |
| Navegador autenticado somente quando necessário | contratos de exportação e coleta | R02-G1-T1–T3, R02-G2-T3 |
| Exportação oficial manual como entrada prioritária | `stilingue-contract.md` | R02-G1-T1–T4 |
| Menções em cinco canais e comentários em dois | `collection-contract.md` | R02-G2-T4, R02-G3-T1–T2 |
| Estado independente do Social | `local-state.md` | M1-T4, M6-T6 |
| Estado local e portátil | `local-state.md` | M6-T2, M6-T6 |
| JSON e JSONL canônicos | schemas e `local-state.md` | M0-T1–T4 |
| Dados pessoais minimizados | `privacy-retention.md` | M3-T6, M5-T9 |
| Corpus descartado após análise | `privacy-retention.md` | M4-T8 |
| Corpus preservado quando incompleto | `privacy-retention.md` | M4-T9 |
| Evidências estratificadas por fonte | `analysis-rubric.md`, `generate-report` | R02-G3-T2, R02-G4-T4 |
| Evidência integral sem identidade | `privacy-retention.md` | M5-T9 |
| Sentimento contextual e multidimensional | `analysis-rubric.md` | M4-T1–T4 |
| Consistência pela rubrica | `analysis-rubric.md` | M4-T1–T4 |
| Análise automática e revisão editorial | `analyze-sentiment`, `generate-report` | M4-T1–T9, M5-T1 |
| Dois gates editoriais | `report-workbook-contract.md` | M5-T1, M5-T10 |
| HTML canônico e PDF derivado | `report-workbook-contract.md` | M5-T4, M5-T6 |
| Planilha analítica final | `report-workbook-contract.md` | M5-T7–T9 |
| Identidade padrão e opcional | `insideout-report.css` | M5-T4, M5-T5 |
| Núcleo fixo, recortes e gráficos | `report-workbook-contract.md` | R02-G4-T1–T3 |
| Distribuição separada de amplificação | `analysis-rubric.md` | M4-T6 |
| Lacunas explícitas sem leitura parcial | `collection-contract.md`, `generate-report` | R02-G2-T1–T5, R02-G4-T5 |
| Pacote declarativo e enxuto | manifesto e árvore do plugin | M1-T5, M8-T3 |
| Publicação habilita validação real | gates G6–G7 e protocolo M9 | R02-G6-T1–T4, R02-G7-T1–T3, M9-T1–T8 |

As faixas M2/M3 operacionais e M9 permanecem sem aprovação até a publicação do
piloto e a execução pela equipe da InsideOut.
