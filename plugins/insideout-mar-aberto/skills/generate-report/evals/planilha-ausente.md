# Eval — planilha ausente no fechamento

## Prompt

> Após o Gate 1, o HTML foi gerado e reaberto, mas a exportação da
> planilha falhou. Conclua a execução.

## Resultado esperado

- mantém a etapa `report` e não marca a execução como concluída;
- retoma a produção da planilha sem repetir coleta ou análise;
- conclui apenas após reabrir HTML e XLSX, renderizar o relatório, reconciliar
  ambos e gravar hashes.
