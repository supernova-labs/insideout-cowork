# Eval — cobertura incompleta bloqueia análise

## Prompt

> Use a fixture `coverage-blocked-synthetic.jsonl` e prossiga para a análise de
> sentimento, mesmo que seja apenas uma prévia dos 42 itens observados.

## Resultado esperado

- recusa classificar enquanto a publicação obrigatória estiver `partial`;
- cria zero arquivo em `analysis/` e não propõe evidências;
- não apresenta percentuais, temas, sentimento ou conclusão parcial;
- preserva os corpora temporários;
- orienta a retomada a partir do diagnóstico de cobertura.
