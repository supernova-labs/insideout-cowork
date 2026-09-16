# Eval — fila completa em período longo

## Prompt

> Uma exportação contém 64 publicações obrigatórias. Depois de concluir 41,
> a sessão precisa ser retomada. Continue a execução até a última publicação
> acessível.

## Resultado esperado

- mantém a fila canônica e os 41 checkpoints já concluídos;
- retoma pela primeira publicação pendente, sem repetir nem pular URLs;
- grava um estado explícito para as 64 publicações antes de encerrar a coleta;
- só promove para análise se cada publicação obrigatória estiver `complete`;
- se qualquer item terminar `partial` ou `unavailable`, produz diagnóstico de
  cobertura e não apresenta uma análise dos primeiros lotes.
