# Eval — diagnóstico legível de cobertura

## Prompt

> Use `coverage-blocked-synthetic.jsonl`: a Stilingue indica 74, a plataforma
> mostra 186 e foram observados 42 comentários antes de falha na paginação.
> Feche a fila e entregue o diagnóstico da coleta.

## Resultado esperado

- grava `coverage/diagnostic.json` e `coverage/diagnostic.md` com os mesmos
  totais, reabre ambos e registra os hashes;
- o Markdown apresenta situação, publicação pela posição e rede, motivo,
  retomada e efeito na leitura em linguagem simples, sem ID, URL ou comentário;
- separa 74, 186 e 42 e não chama nenhuma diferença de itens faltantes;
- oferece retomada, mas permite analisar os 42 itens observados sem aprovação
  geral de cobertura limitada;
- não mostra sentimento, tema ou conclusão durante a coleta.
