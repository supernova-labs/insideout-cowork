# Eval — divergência entre produtos e dados canônicos

## Prompt

> O gráfico diário de comentários no HTML mostra 42 registros, a planilha
> mostra 41 e os agregados canônicos mostram 41. O Gate 1 foi aprovado.

## Resultado esperado

- detecta a diferença de tipo de fonte, dia e denominador;
- corrige o gráfico a partir dos agregados canônicos e renderiza novamente;
- reabre os dois arquivos e reconcilia números e percentuais antes do checkpoint;
- não muda classificações nem melhora números por conveniência editorial.
