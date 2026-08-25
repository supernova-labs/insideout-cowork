# Eval — produto preservado com referência e lettering

## Prompt

> Gere o mockup do post `[TESTE CODEX] Aurora 24H: lançamento`, de
> 12/05/2026. Use o produto e a referência ligados ao post. O lettering já foi
> aprovado.

## Resultado esperado

- resolve um único post e lê marca, produto, referência, lettering e peças;
- escolhe `produto + referência` e modo `preservar`;
- trata a foto principal do produto como alvo de edição intocável;
- injeta o lettering verbatim e reserva a área indicada;
- mostra direção, formato e prompt final antes de gerar;
- usa a geração nativa de imagens da OpenAI somente após aprovação;
- confere embalagem, texto, marca, formato e guardrails;
- cria uma peça `Imagem` com prompt auditável e status `Gerada`;
- anexa o arquivo à peça e ao `Mockup` do post sem alterar outros campos;
- relembra que `Aprovada` depende de aprovação humana.
