# Eval — PDF e reconciliação final

## Prompt

> O segundo gate foi aprovado. Gere o PDF e conclua a execução somente se os
> três produtos finais forem válidos.

## Resultado esperado

- deriva o PDF do HTML aprovado;
- renderiza e inspeciona todas as páginas;
- corrige qualquer corte, sobreposição, página vazia ou diferença textual;
- confirma que HTML, PDF, planilha e JSON/JSONL compartilham totais e versão;
- não conclui a execução diante de arquivo ausente ou inválido.
