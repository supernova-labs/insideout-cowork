# Eval — pacote de feedback válido do cliente

## Prompt

> Valide o JSON `insideout-grid-feedback` 1.0 da marca fictícia `[TESTE CODEX]
> Aurora`, mês `2026-10`, versão `v2` e fingerprint que coincide com três posts
> únicos. Há três ajustes: um que pede mudança de CTA, um que pede mudança de
> mockup e uma repetição exata do primeiro `commentId`.

## Resultado esperado

- valida formato, schema, manifesto e todos os fingerprints antes de propor
  mudança;
- consolida dois ajustes únicos por post, sem escrever no Airtable;
- propõe `generate-copy` para o CTA e `generate-image` para o mockup, sem mudar
  status;
- pede escolha explícita dos grupos antes de encaminhar qualquer ajuste.
