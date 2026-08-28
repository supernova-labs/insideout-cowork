# Eval — snapshot HTML local

## Prompt

> Gere um snapshot HTML do primeiro take de maio de 2026 da `[TESTE CODEX]
> Aurora Skin` para revisão. Use dados de teste, não conecte a página ao
> Airtable e não sobrescreva um snapshot anterior.

## Resultado esperado

- cria arquivo autossuficiente fora do diretório do plugin;
- nome e cabeçalho identificam marca, mês e versão;
- mostra distribuição e os detalhes de cada post, incluindo briefing por tela,
  lettering e legenda;
- omite IDs, schema, logs e campos internos;
- não contém chamadas externas, formulário ou escrita;
- abre localmente e permanece legível em desktop e viewport estreito;
- uma nova geração produz outro arquivo sem sobrescrever o anterior.
