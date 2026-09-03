# Eval — paginação e respostas

## Prompt

> Simule uma publicação com dois lotes de comentários e uma resposta escondida
> atrás de “ver respostas”. O segundo ciclo sem itens novos não oferece mais
> controles de continuação.

## Resultado esperado

- percorre os dois lotes e expande a resposta;
- exige duas inspeções sem progresso antes de declarar esgotamento observável;
- conta comentários principais e respostas separadamente;
- preserva a relação pai–resposta com identificadores irreversíveis;
- registra a publicação como `complete` sem usar o contador como prova isolada.
