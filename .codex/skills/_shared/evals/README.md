# Harness de avaliação da Parte 1

Execute cada cenário em uma thread nova do Codex. Use os prompts versionados nas
pastas `evals/` das skills e registre:

1. prompt inicial;
2. resultado conversacional;
3. registros criados ou reutilizados;
4. verificação por releitura;
5. resultado da segunda execução;
6. falhas de julgamento ou contrato.

Os testes de escrita usam o prefixo `[TESTE CODEX]`. Não remova registros sem
confirmação explícita. Toda resposta final também deve passar por
`resposta-sem-ids.md`: IDs permanecem nas chamadas do conector e nunca aparecem
na conversa com o usuário.

## Thread de contrato de Peças

Depois de existirem marca, produto, referência e post de teste:

> Use o contrato da Parte 1 para criar uma peça de teste chamada
> `[TESTE CODEX] Contrato de imagem`, do tipo Imagem, ligada aos registros de
> teste. Não anexe arquivo. Registre no prompt: `Teste de contrato da Parte 1;
> nenhuma mídia foi gerada.` Depois releia a peça e confirme todos os vínculos.

## Resultado esperado

- exatamente uma peça com o nome definido;
- `Status = Gerada`;
- vínculos com marca, produto, referência e post;
- `Arquivo` vazio;
- segunda execução reutiliza o mesmo registro, sem mudança material ou
  duplicação;
- resposta final em linguagem de negócio, sem IDs ou detalhes do conector.
