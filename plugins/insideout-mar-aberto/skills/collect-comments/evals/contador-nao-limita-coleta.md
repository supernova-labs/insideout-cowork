# Eval — contador da exportação não limita a coleta

## Prompt

> A exportação informa 74 comentários. Ao abrir uma publicação do Instagram, a
> plataforma exibe 186, mas apenas 42 foram observados antes da interrupção.

## Resultado esperado

- registra separadamente 74 na exportação, 186 na plataforma e 42 observados;
- não usa 74 como teto nem considera 42 suficientes para `complete`;
- marca a publicação como `partial` porque a continuação falhou;
- preserva corpus, checkpoint e ponto de retomada sem duplicação;
- após fechar toda a fila, gera diagnóstico legível e permite análise somente
  dos 42 observados; a coleta não apresenta sentimento ou conclusões.
