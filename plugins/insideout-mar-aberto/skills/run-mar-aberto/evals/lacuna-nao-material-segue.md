# Eval — lacuna pequena sem bloqueio geral

## Prompt

> Em dez publicações obrigatórias, nove têm coleta completa e uma ficou
> parcial após falha observável. Há registros suficientes para uma conclusão
> explicitamente restrita aos comentários observados. Conduza o fluxo.

## Resultado esperado

- fecha os dez checkpoints e entrega diagnósticos JSON e Markdown coerentes;
- analisa automaticamente os registros observados, sem decisão prévia de
  cobertura limitada;
- leva a lacuna ao Gate 1, mas não força nova aprovação de cobertura para uma
  conclusão que não extrapola o corpus;
- gera HTML e XLSX após o Gate 1, com a lacuna na página e aba de cobertura;
- não repete alerta de cobertura em todas as páginas.
