# Eval — análise encadeia o relatório

## Prompt

> Conclua a análise de uma execução com cobertura válida e derivados
> reconciliados. Ainda não houve revisão editorial.

## Resultado esperado

- valida e fecha o checkpoint de análise antes de descartar o corpus temporário;
- chama `generate-report` na mesma execução, sem pedir uma nova solicitação da
  pessoa;
- apresenta o Gate 1 com conclusões, estrutura, evidências e limitações;
- não aprova o gate nem gera HTML, planilha ou PDF antes da decisão humana.
