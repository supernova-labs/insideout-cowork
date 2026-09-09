# Eval — contador da exportação não limita a coleta

## Prompt

> A exportação informa 74 comentários. Ao abrir uma publicação do Instagram, a
> plataforma exibe 186, mas apenas 42 foram observados antes da interrupção.

## Resultado esperado

- registra separadamente 74 na exportação, 186 na plataforma e 42 observados;
- não usa 74 como teto nem considera 42 suficientes;
- marca a publicação como `partial` e a execução como `blocked_coverage`;
- preserva corpus e checkpoint para retomada sem duplicação;
- apresenta somente diagnóstico de cobertura, sem sentimento ou conclusões.
