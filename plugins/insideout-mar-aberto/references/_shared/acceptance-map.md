# Rastreabilidade entre princípios e testes

Esta matriz aponta onde cada princípio específico do InsideOut Mar Aberto é
materializado. O enunciado canônico permanece em `ARCHITECTURE.md`.

| Princípio | Contrato ou skill | Provas principais |
|---|---|---|
| Jornada principal com etapas retomáveis | `local-state.md`, `run-mar-aberto` | M6-T1–T8 |
| Canal próprio de feedback | `skill-feedback` | M7-T1–T5 |
| Cobertura observável condiciona análise | `collection-contract.md` | M3-T1, M3-T5, M5-T3 |
| Relevância precede volume | `analysis-rubric.md` | M4-T3 |
| Autenticação pertence ao operador | `stilingue-contract.md`, `collection-contract.md` | M2 operacional, M3-T4 |
| Execução sob demanda | `run-mar-aberto` | M6-T1 |
| Navegador autenticado no MVP | contratos de exportação e coleta | M2 e M3 operacionais |
| Exportação Stilingue como entrada | `stilingue-contract.md` | M2-T1–T5 |
| Instagram e YouTube suportados | `collection-contract.md` | M3-T7 |
| Estado independente do Social | `local-state.md` | M1-T4, M6-T6 |
| Estado local e portátil | `local-state.md` | M6-T2, M6-T6 |
| JSON e JSONL canônicos | schemas e `local-state.md` | M0-T1–T4 |
| Dados pessoais minimizados | `privacy-retention.md` | M3-T6, M5-T9 |
| Corpus descartado após análise | `privacy-retention.md` | M4-T8 |
| Corpus preservado quando incompleto | `privacy-retention.md` | M4-T9 |
| Evidências estratificadas e curadas | `analysis-rubric.md`, `generate-report` | M4-T7, M5-T1 |
| Evidência integral sem identidade | `privacy-retention.md` | M5-T9 |
| Sentimento contextual e multidimensional | `analysis-rubric.md` | M4-T1–T4 |
| Consistência pela rubrica | `analysis-rubric.md` | M4-T1–T4 |
| Análise automática e revisão editorial | `analyze-sentiment`, `generate-report` | M4-T1–T9, M5-T1 |
| Dois gates editoriais | `report-workbook-contract.md` | M5-T1, M5-T10 |
| HTML canônico e PDF derivado | `report-workbook-contract.md` | M5-T4, M5-T6 |
| Planilha analítica final | `report-workbook-contract.md` | M5-T7–T9 |
| Identidade padrão e opcional | `insideout-report.css` | M5-T4, M5-T5 |
| Núcleo fixo e narrativa adaptativa | `report-workbook-contract.md` | M5-T2 |
| Distribuição separada de amplificação | `analysis-rubric.md` | M4-T6 |
| Lacunas explícitas | `collection-contract.md`, `generate-report` | M3-T3–T5, M5-T3 |
| Pacote declarativo e enxuto | manifesto e árvore do plugin | M1-T5, M8-T3 |
| Publicação habilita validação real | plano M8–M9 | M8-T1–T5, M9-T1–T8 |

As faixas M2/M3 operacionais e M9 permanecem sem aprovação até a publicação do
piloto e a execução pela equipe da InsideOut.
