# Gates de release — InsideOut Mar Aberto 0.2.2

Esta candidata corrige a conclusão prematura da coleta e introduz o relatório
de cobertura limitada como uma decisão explícita. A publicação depende dos
gates abaixo e de autorização explícita antes de promoção à `main`.

Estados permitidos: `pendente`, `em implementação`, `passou` e `falhou`. Um
teste não executado nunca conta como sucesso.

## G0 — Decisão editorial registrada

**Tipo:** decision · **Estado:** passou

| ID | Teste | Evidência esperada |
|---|---|---|
| R022-G0-T1 | Cobertura limitada | D026, contratos e skills exigem confirmação registrada e não transformam lacuna em cobertura completa. |

## G1 — Coleta persistente e decisão de cobertura

**Tipo:** build · **Estado:** em implementação

| ID | Teste | Evidência esperada |
|---|---|---|
| R022-G1-T1 | Continuação observável | Painel rolável, controle de continuação ou resposta expansível impede encerramento prematuro. |
| R022-G1-T2 | Retomada de período longo | Fila canônica, checkpoints e nenhuma URL obrigatória omitida. |
| R022-G1-T3 | Sem confirmação | `blocked_coverage` oferece retomada e não cria análise nem relatório. |
| R022-G1-T4 | Com confirmação | `coverage-decision.json` promove o corpus observado para análise limitada. |

## G2 — Produtos transparentes

**Tipo:** gate · **Estado:** pendente

| ID | Teste | Evidência esperada |
|---|---|---|
| R022-G2-T1 | Relatório limitado | HTML, planilha e PDF identificam cobertura limitada e seus denominadores observados. |
| R022-G2-T2 | Privacidade e retenção | Sem identidade pessoal; corpus descartado apenas depois de derivados válidos. |
| R022-G2-T3 | Reconciliação | Cobertura, agregados e produtos coincidem, sem extrapolar publicações inacessíveis. |

## G3 — Pacote candidato

**Tipo:** gate · **Estado:** pendente

| ID | Teste | Evidência esperada |
|---|---|---|
| R022-G3-T1 | Validação estrutural | Validador do Mar Aberto e Agent Smith retornam zero erro. |
| R022-G3-T2 | Revisão e promoção | Commit e versão revisados; push depende de autorização explícita. |
