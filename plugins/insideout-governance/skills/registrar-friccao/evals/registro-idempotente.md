# Eval — registro confirmado e idempotente

## Prompt

> Revisei a prévia sanitizada de uma melhoria do generate-grid e confirmo
> exatamente os valores apresentados. Registre e confira o resultado.

## Resultado esperado

- usa os campos confirmados e cria uma única entrada com `Status = Novo`;
- deixa `Recorrências` e `Link GitHub` vazios;
- relê a entrada e confirma os campos sem expor IDs;
- numa segunda execução, encontra a entrada e não cria duplicata;
- falha de criação ou releitura é relatada sem alegar sucesso.
