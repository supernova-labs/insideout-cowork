# Eval — execução 3.0.0 preservada ao adotar HTML

## Prompt

> Há uma execução concluída com contrato 3.0.0, report.pptx, analytics.xlsx e
> hashes válidos. O plugin foi atualizado para HTML. Retome a execução e crie
> uma nova análise de outro período.

## Resultado esperado

- reabre a execução antiga usando o schema 3.0.0 e seus hashes originais;
- não troca report.pptx por report.html, não altera seu checkpoint nem
  reescreve o manifesto antigo;
- inicia a nova execução com contrato 4.0.0 e templates HTML/XLSX;
- só conclui a nova execução quando HTML e XLSX passarem por abertura,
  reconciliação, revisão visual e registro de hashes.
