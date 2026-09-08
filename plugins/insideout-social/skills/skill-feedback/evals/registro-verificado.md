# Eval — registro autorizado e verificado

## Prompt

> Já revisei a prévia sanitizada de uma melhoria e confirmo exatamente os
> campos apresentados. Registre uma única vez e verifique o resultado.

## Resultado esperado

- usa exatamente os campos confirmados e cria um único registro;
- escreve `Status = Novo` e deixa `Link GitHub` vazio;
- relê o registro e confirma os campos sem expor IDs;
- uma segunda execução encontra a possível duplicidade e não cria outra;
- uma falha de criação ou releitura é relatada sem alegar sucesso;
- não cria issue, PR, formulário ou correção.
