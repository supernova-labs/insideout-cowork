# Eval — exportação válida

## Prompt

> Valide `references/_shared/fixtures/stilingue-valid.csv` como representação
> sanitizada de uma exportação já baixada para o projeto i20, filtro
> `nova busca i20`, de 2026-08-26 a 2026-09-02.

## Resultado esperado

- trata a fonte como fixture, não como teste de download real;
- encontra três publicações e três URLs únicas;
- roteia uma publicação para Instagram, uma para YouTube e uma como não
  suportada;
- registra filtro, período e fuso sem corrigi-los por inferência;
- produz um checkpoint de entrada coerente.
