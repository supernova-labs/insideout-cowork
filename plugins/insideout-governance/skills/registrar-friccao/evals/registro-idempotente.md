# Eval — registro confirmado e idempotente

## Prompt

> Revisei a prévia sanitizada de uma melhoria do generate-grid e confirmo
> exatamente os valores apresentados. Registre e confira o resultado.

## Resultado esperado

- usa os campos confirmados e cria uma única linha na aba `Fricções e fixes`
  com `Status = Aberta`, `Recorrência = Isolada` e fingerprint na nota do ID;
- deixa H:K e M:N vazias, sem preencher fix, prazo ou decisão;
- relê a linha A:N e confirma os campos sem expor IDs operacionais;
- numa segunda execução, encontra a entrada e não cria duplicata;
- falha de criação ou releitura é relatada sem alegar sucesso.
