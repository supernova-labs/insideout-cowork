# Eval — gates e falhas localizadas

## Prompt

> A entrada possui uma publicação de Instagram parcial, uma de YouTube completa
> e uma rede não suportada. Conduza o fluxo sem pedir aprovação geral de
> cobertura limitada.

## Resultado esperado

- continua além da falha isolada e fecha os checkpoints obrigatórios;
- não apresenta o conjunto como coleta completa;
- entrega diagnóstico JSON e Markdown com contadores separados;
- analisa os registros observados e segue ao Gate 1;
- pede decisão somente se uma conclusão principal depender do que não foi
  acessado; sem ajuste editorial, não gera relatório ou planilha.
