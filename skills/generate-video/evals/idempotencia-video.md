# Eval — idempotência do vídeo

## Prompt

> Gere novamente o vídeo aprovado desse post usando o mesmo frame, prompt e
> parâmetros.

## Resultado esperado

- resolve a peça existente pela chave natural;
- compara prompt, modelo, duração, resolução, áudio e entradas;
- confirma que o arquivo já existe;
- não estima como se uma nova geração fosse necessária nem consome créditos;
- não cria peça, versão ou anexo duplicado;
- relata que o vídeo existente foi reutilizado;
- só regenera quando o usuário pedir nova variação ou substituição.
