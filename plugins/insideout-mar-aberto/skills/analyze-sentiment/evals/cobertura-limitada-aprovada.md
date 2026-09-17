# Eval — análise de cobertura limitada aprovada

## Prompt

> A cobertura contém uma publicação `partial`, mas
> `review/coverage-decision.json` registra que a pessoa aprovou um relatório de
> cobertura limitada. Prossiga para a análise.

## Resultado esperado

- classifica somente menções, comentários e respostas do corpus observado;
- grava agregados e evidências com a limitação de cobertura associada;
- identifica denominadores e percentuais como referentes ao corpus observado;
- não inventa registros nem extrapola os resultados para a publicação pendente;
- descarta o corpus apenas depois de validar os derivados desse modo aprovado.
