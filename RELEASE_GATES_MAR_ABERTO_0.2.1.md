# Gates de release — InsideOut Mar Aberto 0.2.1

Esta versão corrige dois comportamentos observados na homologação: o contador
da Stilingue não bloqueia uma coleta com esgotamento observável, e recortes
longos só avançam depois que toda a fila canônica tiver checkpoint. A publicação
depende dos gates abaixo e de autorização explícita antes de qualquer promoção à
`main`.

Estados permitidos: `pendente`, `em implementação`, `passou` e `falhou`. Um
teste não executado nunca conta como sucesso.

## G0 — Contrato e escopo aprovados

**Tipo:** decision · **Estado:** passou

| ID | Teste | Evidência esperada |
|---|---|---|
| R021-G0-T1 | Decisão de contagem | D025, contrato compartilhado, skill e evals distinguem contador da Stilingue de cobertura observável. |

## G1 — Coleta completa e retomável

**Tipo:** build · **Estado:** em implementação

| ID | Teste | Evidência esperada |
|---|---|---|
| R021-G1-T1 | Divergência Stilingue | Contador externo divergente, esgotamento comprovado e estado `complete`; a limitação é preservada. |
| R021-G1-T2 | Falha real | Paginação interrompida ou publicação indisponível permanece `partial` ou `unavailable` e bloqueia análise. |
| R021-G1-T3 | Período longo | Cada URL obrigatória da fila possui checkpoint antes da análise; retomada não duplica nem reduz o escopo. |

## G2 — Pacote candidato validado

**Tipo:** gate · **Estado:** pendente

| ID | Teste | Evidência esperada |
|---|---|---|
| R021-G2-T1 | Validador Mar Aberto | Validador estrutural retorna zero erro e zero aviso. |
| R021-G2-T2 | Catálogo Codex e índice | Manifesto 0.2.1, marketplace, índice e README apontam para a mesma árvore canônica. |
| R021-G2-T3 | Auditoria do diff | Sem dados reais, credenciais, estado operacional ou mudança fora do escopo. |

## G3 — Publicação controlada

**Tipo:** gate · **Estado:** pendente

| ID | Teste | Evidência esperada |
|---|---|---|
| R021-G3-T1 | Revisão do candidato | Commit exato, versão e evidências de validação são apresentados para revisão. |
| R021-G3-T2 | Autorização de promoção | Confirmação explícita antes de push ou promoção à `main`. |
