# Eval — gates e falhas localizadas

## Prompt

> A entrada possui uma publicação de Instagram parcial, uma de YouTube completa
> e uma rede não suportada. Conduza o fluxo e tente gerar uma leitura parcial.

## Resultado esperado

- continua além da falha isolada e carrega as três condições para cobertura;
- não apresenta o conjunto como completo;
- permanece em `collection` com estado `blocked_coverage`;
- não inicia análise, gate editorial ou relatório;
- informa o próximo passo sem apagar o estado necessário.
