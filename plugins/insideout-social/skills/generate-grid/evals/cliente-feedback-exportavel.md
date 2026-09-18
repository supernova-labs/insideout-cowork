# Eval — revisão de cliente com feedback exportável

## Prompt

> Para `[TESTE CODEX] Aurora`, outubro de 2026, gere o HTML compartilhável de
> cliente com feedback por post e exportação. Há três posts cronológicos: dois
> têm mockup correspondente a uma `Peça` aprovada; o terceiro não tem
> comprovação de mockup aprovado.

## Resultado esperado

- gera um terceiro formato, distinto do resumo estático, contendo apenas os
  dois posts elegíveis, em ordem cronológica e com suas imagens aprovadas;
- usa manifesto público com marca, mês, versão, fingerprint e chaves públicas
  por post, sem IDs, copy, rationale, briefing, status interno ou URLs privadas;
- cada card permite adicionar, editar e remover localmente um ajuste com
  mensagem e revisor opcional; o tipo fixo **Ajuste** aparece no overlay modal
  acessível, que mantém os campos fora dos cards e devolve o foco ao botão de
  origem ao fechar;
- persiste somente no navegador, recarrega os comentários e pede confirmação
  antes de limpar; oferece download local de JSON canônico e CSV escapado;
- não faz rede, upload, formulário remoto, analytics, colaboração em tempo
  real, leitura ou escrita de Airtable;
- explica que o cliente precisa exportar e encaminhar o JSON ao time.

## Caso de regressão

Ao pedir apenas o resumo para cliente, mantém o formato estático sem comentários
ou edição e continua excluindo posts sem mockup aprovado verificável.
