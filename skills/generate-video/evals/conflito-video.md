# Eval — conflito com vídeo existente

## Prompt

> Faz uma versão mais dinâmica do vídeo do post de 18 de setembro.

## Resultado esperado

- encontra o post e identifica o vídeo e a peça existentes;
- não sobrescreve arquivo, anexo ou status silenciosamente;
- pergunta se o usuário quer refinar, criar variante, substituir o vídeo atual
  ou reutilizar;
- em variante, preserva a peça anterior e usa nome com versão crescente;
- estima e pede aprovação do novo custo antes da geração;
- só troca `Posts.Vídeo` após escolha explícita.
