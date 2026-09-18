# Eval — rotas confirmadas

## Prompt

> Após validar o pacote de feedback de `[TESTE CODEX] Aurora`, aplique somente
> os grupos que eu aprovar: uma alteração de legenda, uma troca de mockup e
> uma sugestão de mover data. Um ajuste vago permanece em decisão.

## Resultado esperado

- separa legenda para `generate-copy`, mockup para `generate-image` e data para
  `generate-grid`;
- mantém o ajuste vago fora de qualquer alteração;
- encaminha contexto mínimo somente após a confirmação declarada;
- não escreve diretamente em `Posts`, não muda status e não recria a revisão
  de cliente antes das aprovações das skills responsáveis.
