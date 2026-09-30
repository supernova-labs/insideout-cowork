# Eval — fila completa em período longo

## Prompt

> Uma exportação contém 64 publicações obrigatórias. Depois de concluir 41,
> a sessão precisa ser retomada. Continue a execução até a última publicação
> acessível.

## Resultado esperado

- mantém a fila canônica e os 41 checkpoints já concluídos;
- retoma pela primeira publicação pendente, sem repetir nem pular URLs;
- grava um estado explícito para as 64 publicações antes de encerrar a coleta;
- não promove para análise enquanto uma publicação obrigatória não tiver
  checkpoint;
- depois de fechar a fila, produz JSON e Markdown reconciliados e analisa os
  itens observados, mesmo se houver itens `partial` ou `unavailable`.
