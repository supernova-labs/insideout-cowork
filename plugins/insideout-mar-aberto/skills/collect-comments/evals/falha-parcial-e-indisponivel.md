# Eval — coleta parcial e publicação indisponível

## Prompt

> A primeira publicação carregou 12 comentários e falhou antes do próximo lote;
> a segunda foi removida; a terceira terminou normalmente. Continue a coleta.

## Resultado esperado

- registra a primeira como `partial`, com 12 observados e motivo;
- registra a segunda como `unavailable`;
- coleta a terceira e fecha toda a fila obrigatória;
- não chama a cobertura do recorte de completa;
- reconcilia JSON e Markdown do diagnóstico e mostra a visão legível;
- promove os itens observados para análise com `observed_with_gaps`, sem
  exigir aprovação prévia, mantendo a possibilidade de retomada.
