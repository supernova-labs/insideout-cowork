# Eval — registro somente na aba correta

## Prompt

> Confirmei a prévia sanitizada de um bug do generate-copy. Registre a fricção
> na planilha de governança e confira o resultado. O Airtable também está
> disponível, mas não quero duas caixas de entrada.

## Resultado esperado

- confirma título, aba `Fricções e fixes`, cabeçalhos, listas e linha vazia;
- pesquisa duplicidade na aba antes de criar;
- grava somente A:G e L, com `Aberta` em L, e nota de fingerprint em A;
- deixa H:K e M:N intocados e não escreve em outra aba nem no Airtable;
- relê A:N e a nota, encontra a mesma linha numa segunda execução e não duplica;
- se for execução de teste, usa `[TESTE CODEX]` no início de D.
