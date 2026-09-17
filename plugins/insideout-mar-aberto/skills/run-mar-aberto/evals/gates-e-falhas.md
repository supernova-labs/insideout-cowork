# Eval — gates e falhas localizadas

## Prompt

> A entrada possui uma publicação de Instagram parcial, uma de YouTube completa
> e uma rede não suportada. Conduza o fluxo sem aprovar relatório de cobertura
> limitada.

## Resultado esperado

- continua além da falha isolada e carrega as três condições para cobertura;
- não apresenta o conjunto como completo;
- permanece em `collection` com estado `blocked_coverage`;
- não inicia análise, gate editorial ou relatório;
- informa o próximo passo, oferecendo retomar a coleta ou aprovar um relatório
  de cobertura limitada, sem apagar o estado necessário.
