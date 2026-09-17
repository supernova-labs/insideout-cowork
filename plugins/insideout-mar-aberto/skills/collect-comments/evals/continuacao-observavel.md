# Eval — continuação observável não encerra cedo

## Prompt

> Uma publicação do Instagram ainda mostra o painel de comentários rolável e o
> botão “carregar mais”, mas nenhum comentário novo apareceu na última rolagem.
> A execução já percorreu muitas outras publicações.

## Resultado esperado

- continua a interação no contêiner de comentários e tenta carregar mais antes
  de decidir o estado da publicação;
- não usa a duração do recorte nem a quantidade de URLs restantes para marcar
  `partial` ou encerrar a fila;
- se a sessão precisar parar, preserva o ponto como retomável;
- só registra `complete` depois das duas inspeções sem progresso e sem controle
  de continuação, ou `partial` após uma falha observável de continuação.
