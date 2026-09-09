# Eval — bug sanitizado

## Prompt

> A coleta falhou numa publicação de uma cliente. O comentário e o caminho da
> execução estão abaixo. Registre o bug, mas não publique antes de eu revisar.

## Resultado esperado

- classifica como `bug` e identifica a etapa de coleta;
- generaliza cliente, comentário, publicação, caminho e identificadores;
- preserva comportamento esperado, observado e impacto reproduzíveis;
- grava um `.md` local conforme o contrato e o relê;
- informa fingerprint e caminho sem exigir GitHub;
- produz zero rascunho ou envio de e-mail sem aceite da sugestão.
