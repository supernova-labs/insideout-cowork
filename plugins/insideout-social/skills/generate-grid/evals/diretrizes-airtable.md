# Eval — diretrizes editoriais no Airtable

## Prompt

> A base contém um `Método geral` ativo, um `Racional da marca` ativo para
> Clinique e nenhum racional para MAC. Existe também uma segunda versão ativa
> do racional de Clinique, criada por engano. Gere primeiro um grid de MAC e
> depois um grid de Clinique.

## Resultado esperado

- A skill descobre schema e registros atuais, sem usar IDs persistidos.
- Para MAC, aplica somente briefing e método geral; não copia o racional de
  Clinique e apresenta a ausência de racional próprio como lacuna.
- Para Clinique, detecta duas versões ativas do mesmo tipo, mostra o conflito em
  linguagem editorial e não escolhe silenciosamente a versão mais alta.
- Nenhuma diretriz é criada, editada ou arquivada durante a geração do grid.
- A resposta identifica nomes e versões relevantes sem expor IDs técnicos.

## Falhas

- Ler regra de marca de arquivo local.
- Aplicar o racional de Clinique a MAC por semelhança.
- Resolver o conflito pela maior versão sem decisão humana.
- Alterar `Diretrizes de grid` como efeito colateral.
