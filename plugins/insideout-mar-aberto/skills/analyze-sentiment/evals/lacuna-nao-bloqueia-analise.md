# Eval — lacuna com checkpoint não bloqueia análise

## Prompt

> Use a fixture `coverage-blocked-synthetic.jsonl` com uma publicação parcial.
> Todas as publicações obrigatórias têm checkpoint. Analise o corpus observado,
> sem pedir uma aprovação geral de cobertura limitada.

## Resultado esperado

- classifica os 42 comentários observados e não inventa os não acessados;
- registra `coverage_mode: observed_with_gaps` e preserva a lacuna nos derivados;
- separa contagem da Stilingue, plataforma e itens observados;
- usa apenas registros relevantes observados como denominador dos percentuais;
- não apresenta esses percentuais como opinião da internet inteira;
- não exige `review/coverage-decision.json` para iniciar a análise.
