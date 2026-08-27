# Eval — idempotência da imagem

## Prompt

> Gere novamente a imagem aprovada do post de lançamento usando o mesmo prompt.

## Resultado esperado

- resolve a peça existente pela chave natural;
- compara o prompt normalizado e confirma que o arquivo já existe;
- não chama a geração nativa novamente;
- não cria peça, versão ou anexo duplicado;
- relata que a imagem existente foi reutilizada;
- só regenera quando o usuário pedir nova variação ou substituição.
