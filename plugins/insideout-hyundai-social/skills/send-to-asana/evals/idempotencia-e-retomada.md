# Eval — tarefa-pai criada e falha em subtarefa

## Prompt

> Envie a ideia sintética A confirmada ao projeto separado de testes com as
> etapas Texto, Arte e BMS aprovadas. O pai e Texto foram criados, mas o retorno
> de Arte ficou incerto. Retome e depois execute novamente o mesmo lote.

## Resultado esperado

- confirma destino distinto de produção e não atribui pessoas reais;
- registra o checkpoint antes/depois de cada etapa;
- pesquisa Arte pelo marcador antes de repetir, reutiliza pai e Texto;
- conclui somente depois da releitura de todas as etapas;
- segunda execução cria zero tarefas/subtarefas; busca incompleta não prova ausência.
