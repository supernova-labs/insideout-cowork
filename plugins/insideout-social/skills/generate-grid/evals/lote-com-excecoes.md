# Eval — aprovação em lote com exceções

## Prompt

> Aprove o primeiro take mensal da `[TESTE CODEX] Aurora Skin`, exceto os posts
> dos dias 12 e 18, que devem permanecer em revisão. Persista os demais e
> confirme o resultado.

## Resultado esperado

- identifica individualmente aprovados e exceções antes da escrita;
- persiste somente os posts aprovados;
- generate-grid escreve estrutura, rationale e briefing de design;
- generate-copy escreve somente lettering e legenda dos mesmos posts;
- posts dos dias 12 e 18 não são criados nem alterados;
- releitura confirma o conjunto persistido e os dois pendentes sem IDs;
- uma segunda execução cria zero duplicatas.
