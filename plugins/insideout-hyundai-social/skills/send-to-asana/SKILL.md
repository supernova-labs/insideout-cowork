---
name: send-to-asana
description: Prepara e encaminha ideias Hyundai confirmadas pelo time ao Asana, com verificação de duplicidade e retomada parcial. Use para enviar ou conferir tarefas Hyundai; regras fictícias operam somente em projeto de testes separado, nunca no quadro real.
---

# Encaminhar ideias Hyundai ao Asana

Leia `../../references/_shared/operating-contract.md`,
`../../references/_shared/airtable-contract.md`,
`../../references/_shared/feedback-contract.md`,
`../../references/_shared/release-gates.md` e `references/task-contract.md`.

## Verificar antes de escrever

Descubra o conector e comprove nesta sessão as operações disponíveis de projeto,
seção, tarefa, subtarefa, campos e releitura. Instalação não comprova conexão
nem escrita. Sem conector adequado, entregue somente a prévia e a dependência;
não use API própria ou atribua sucesso a uma leitura pelo navegador.

Resolva ciclo, ideias escolhidas, publicações e configuração atual. Reconstrua
o fingerprint e exija confirmação do time sobre a versão atual de cada ideia.
Comentários não substituem confirmação. Reservas e ideias incompletas não são
enviadas. Apresente exceções sem bloquear as demais ideias elegíveis.

Resolva projeto e seção por configuração e leitura atuais. Regras de Simulação
exigem projeto de testes comprovadamente distinto do operacional, prefixo
`[TESTE CODEX]` e nenhum responsável ou colaborador real. Criação do projeto de
testes, quando pedida, não convida pessoas. Sem destino inequívoco, não envie.
Para modo Operacional, todos os gates de liberação precisam estar comprovados.

## Preparar o lote

Apresente tarefas, publicações, subtarefas aplicáveis, datas e alocação previstas,
campos não resolvidos e destino. Mostre que prazo de Texto/Arte/BMS não é data
de publicação. Peça confirmação do lote exato, salvo se já foi autorizado nessa
conversa com os mesmos dados e destino.

Confirme equivalência pelo marcador de origem e Encaminhamentos antes de criar.
Crie um registro `Preparado` e releia-o antes da primeira escrita no Asana.
Mantenha o checkpoint por ideia/destino antes e depois de cada etapa externa.

## Executar e retomar

Siga `references/task-contract.md` para criar e verificar tarefa e subtarefas.
Em sucesso parcial, registre URLs já comprovadas e marque Parcial; tente apenas
as etapas faltantes após conferir o estado remoto. Em resposta incerta, marque
Incerto e pesquise o marcador antes de repetir. Nunca crie outro pai para resolver
uma falha de subtarefa. Releia cada tarefa, campo e subtarefa criados.

Se fingerprint ou dados enviados divergirem depois de um envio, apresente o
diff e marque Divergente. Não sincronize datas, responsáveis ou conteúdo, nem
crie tarefa substituta automaticamente. Uma atualização exige instrução exata
do time e releitura; preservar o trabalho de produção já existente.

Não mover tarefa existente, excluir tarefa, concluir, aprovar, comentar,
adicionar seguidores, notificar pessoas ou acionar Notion como parte do envio.

## Entregar

Informe ideias encaminhadas ou reutilizadas, links verificados das tarefas,
itens parciais/incertos e próximo passo. `Concluído` em Encaminhamentos comprova
somente o envio, não a produção ou publicação. Uma segunda execução equivalente
deve criar zero tarefas e subtarefas.
