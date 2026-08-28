# Eval — regeneração isolada de copy e briefing

## Prompt

> No primeiro post de `[TESTE CODEX] Aurora Skin`, regenere primeiro somente
> Lettering e Legenda. Depois proponha uma nova versão apenas do Briefing de
> design. Mostre cada mudança antes de salvar.

## Resultado esperado

- a regeneração de copy é entregue por `generate-copy` e preserva estrutura,
  rationale, briefing, relações, status e mídia;
- a regeneração do briefing é entregue por `generate-grid` e preserva
  Lettering, Legenda, estrutura, rationale, relações, status e mídia;
- cada etapa apresenta o conteúdo existente e pede escolha explícita antes de
  substituir;
- a releitura confirma que somente os campos aprovados na etapa mudaram;
- nenhuma nova publicação é criada e a chave natural do post é preservada.
