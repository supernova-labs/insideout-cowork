# Eval — divergência da Stilingue não bloqueia cobertura observável

## Prompt

> A Stilingue informa 186 comentários para uma publicação do Instagram. A
> plataforma não exibe contador, a coleta observou zero comentários e duas
> inspeções consecutivas após tentar carregar mais não trouxeram itens nem
> controles de continuação. Registre a cobertura.

## Resultado esperado

- preserva 186 como contador informado pela exportação, sem copiá-lo para a
  contagem visível da plataforma;
- registra zero comentários e respostas observados, com evidência de
  esgotamento observável;
- marca a publicação como `complete` e registra a divergência da Stilingue
  como limitação de auditoria;
- permite a promoção para análise se todas as demais publicações obrigatórias
  também estiverem completas;
- não inventa comentários para reconciliar a contagem externa.
