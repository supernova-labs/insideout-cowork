# Eval — relevância e ambiguidade

## Prompt

> Analise quatro registros: uma pergunta em espanhol sobre preço do i20 no
> Brasil; um elogio em português a outro carro; “nossa, barato demais 🙃” sem
> contexto; e spam promocional.

## Resultado esperado

- usa mercado e assunto como critérios, sem filtrar somente por idioma;
- mantém a pergunta do i20 potencialmente relevante;
- exclui o comentário apenas sobre outro carro e o spam, com motivos;
- trata a ironia sem contexto como `ambiguous`;
- não força todos os itens para positivo, negativo ou neutro.
