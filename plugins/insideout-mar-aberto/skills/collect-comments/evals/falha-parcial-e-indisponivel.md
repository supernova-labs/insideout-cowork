# Eval — coleta parcial e publicação indisponível

## Prompt

> A primeira publicação carregou 12 comentários e falhou antes do próximo lote;
> a segunda foi removida; a terceira terminou normalmente. Continue a coleta.

## Resultado esperado

- registra a primeira como `partial`, com 12 observados e motivo;
- registra a segunda como `unavailable`;
- coleta a terceira sem bloquear a execução;
- não chama a cobertura geral de completa;
- mantém todas as lacunas no checkpoint e no resumo.
