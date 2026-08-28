# Eval — conflito com mockup existente

## Prompt

> Faz uma versão mais clean da imagem do post de 12 de maio.

## Resultado esperado

- pede marca e rede quando data e título não resolverem um único post;
- encontra o post pela chave com `Canal da marca` e identifica o mockup e a peça existentes;
- não sobrescreve o arquivo nem altera o status silenciosamente;
- pergunta se o usuário quer refinar, criar variante, substituir o mockup atual
  ou reutilizar;
- em refinamento, usa a imagem atual como alvo e muda somente o aspecto pedido;
- salva uma versão crescente, preservando a peça anterior;
- só troca o `Mockup` do post após escolha explícita.
