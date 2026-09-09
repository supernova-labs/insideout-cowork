# Eval — exportação válida

## Prompt

> Valide `references/_shared/fixtures/stilingue-valid.csv` como representação
> sanitizada de uma exportação já baixada para o projeto i20, filtro
> `nova busca i20`, de 2026-08-26 a 2026-09-02.

## Resultado esperado

- trata a fonte como fixture, não como teste de download real;
- encontra seis publicações e seis URLs únicas;
- normaliza cinco menções analisáveis em Instagram, YouTube, X, Facebook e
  portais;
- roteia Instagram e YouTube para coleta de comentários, três canais como
  `not_required` e TikTok como não suportado;
- registra filtro, período e fuso sem corrigi-los por inferência;
- produz um checkpoint de entrada coerente.
