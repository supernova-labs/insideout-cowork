# Eval — idempotência da copy

## Prompt

> Salve novamente a legenda e o lettering já aprovados no post de lançamento
> da Aurora Skin e confirme o resultado.

## Resultado esperado

- localiza um único post pela chave natural;
- detecta que o texto aprovado já é igual ao salvo;
- trata o resultado como reutilizado, sem mudança material;
- cria zero registros;
- não altera nenhum outro campo;
- responde sem IDs ou detalhes do conector.
