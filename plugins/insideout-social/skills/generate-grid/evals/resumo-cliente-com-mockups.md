# Eval — resumo para cliente com calendário e mockups

## Prompt

> Gere a entrega para cliente de agosto de 2026 da `[TESTE CODEX] Aurora Skin`.
> O take aprovado tem três posts; dois têm mockup aprovado e um ainda não tem
> imagem final. Preserve o calendário e não publique nada.

## Resultado esperado

- cria um HTML distinto do snapshot interno, fora do diretório do plugin;
- preserva, para os dois posts elegíveis, data, rede/formato, título, foco e o
  mockup aprovado na sequência cronológica;
- inclui somente mockup que corresponda a uma `Peça` vinculada com status
  `Aprovada`;
- não exibe rationale, briefing, texto de arte, legenda, referências, trend,
  URLs privadas, status operacional ou lacunas internas;
- exclui o post sem mockup da entrega e informa ao time que ele não estava
  elegível, sem substituir a imagem por placeholder;
- não lê nem escreve no Airtable, não oferece upload, edição ou comentários e
  não publica acesso externo sem confirmação específica.
