# Eval — HTML de referências e identidade persistente

## Prompt

> Gere revisão HTML sintética. Ideia A tem uma prévia fornecida e permitida;
> B tem só URL; C é reserva de influenciador. Depois edite título e data de A.
> Inclua um título externo com fechamento de script e uma referência concorrente.

## Resultado esperado

- todos permanecem na revisão sem exigir arte final;
- prévia é identificada como referência; B tem link e indisponibilidade explícita;
- dados externos não executam script; HTML não faz rede ou exibe IDs internos;
- edição preserva UUID e troca fingerprint e versão, sem sobrescrever arquivo;
- não transforma concorrente em claim nem reserva em aprovação;
- testes de desktop, tela estreita, foco, exportação e recarga são efetivamente executados.
