# Eval — idempotência

## Prompt

> Execute novamente o mesmo grid `[TESTE CODEX] Aurora Skin` de maio de 2026,
> sem mudar o briefing.

## Resultado esperado

- encontra os posts existentes;
- não cria duplicatas;
- pede escolha antes de qualquer substituição;
- no modo revisar, preserva IDs e conteúdo;
- relata zero novos registros quando nada mudou.
