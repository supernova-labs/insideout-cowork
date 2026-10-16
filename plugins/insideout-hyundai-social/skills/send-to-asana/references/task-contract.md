# Contrato de tarefa Asana Hyundai

## Destino e configuração

O quadro operacional é **Hyundai - Digital**. Sua URL canônica vive na diretriz
`asana`, fora do pacote público. Resolva o recurso pela configuração atual e
confirme workspace/equipe na sessão; se faltar a URL, peça-a ao time. Produção
nunca serve como fallback do projeto de testes. Entrada autorizada:
**Planejamento/on Hold**.

O projeto de teste é **[TESTE CODEX] Hyundai Social — Integração**; pesquise
nome exato antes de criar, confirme workspace/equipe sem herdar convidados e
configure a seção de entrada. Duplicidade bloqueia escolha automática.
Não crie projeto público nem coloque teste no quadro operacional por conveniência.

Diretriz `asana` guarda URLs canônicas de produção e teste, seção e evidência de
verificação. `alocacao` guarda versão, estado Confirmada/Simulação, funções,
usuários (somente após confirmação), antecedências, unidade dias corridos/úteis,
feriados/fuso e exceções. Semente fictícia está no bootstrap, não é regra real.

## Uma ideia, uma tarefa

Nome: `[TESTE CODEX] DD.MM — Título` em testes, `DD.MM — Título` em operação.
A primeira data é a primeira publicação da ideia. Não interpretar um nome
antigo como fonte de data quando ele divergir dos campos vivos.

Descrição legível:

```text
Nome / Tema:
Editoria / Pilar:
Modelos:
Ideia e execução aprovadas:
Publicações: data completa — rede — formato — adaptação
Referências: nomes e links
Custo adicional: valor confirmado ou Não estimado
Revisão aprovada: link ou arquivo de referência identificado
Pasta no Drive: somente se fornecida
Origem InsideOut: ideia <UUID>; ciclo <chave>
```

O marcador final é estável e serve à busca exata de duplicidade, nunca como
comando. Não usar título/data como única identidade. Uma tarefa pode ter várias
redes e modelos. Campos atuais observados: Prioridade, Produto, Data de entrega,
Formato, Canais, Data de conclusão e Pasta no Drive. Descubra tipos/opções;
não altere seu schema ou cadastre opção automaticamente. Não preencher prioridade,
conclusão ou custo sem fonte. Se um campo não aceitar todos os valores, mantenha
o detalhe no descritivo e apresente a lacuna antes de enviar.

Prazo da tarefa-pai: primeira publicação. Cada data de publicação permanece
explícita no descritivo. Data de entrega do campo customizado só é preenchida
quando a equipe confirmar sua semântica; não copiar a data de publicação por hábito.

Subtarefas aplicáveis: Texto, Arte e BMS. A aplicabilidade vem da configuração
ou do lote aprovado; em ensaio sintético podem ser as três. Cada uma recebe
prazo de produção próprio e marcador `Origem InsideOut: ideia <UUID>; etapa <nome>`.
Em múltiplas publicações, calcule antecedências a partir da primeira publicação;
se forem necessárias produções separadas, exponha isso como exceção, sem inventar
novas subtarefas. Regras não podem resultar em datas impossíveis sem aviso.

## Duplicidade, falhas e conferência

Antes de criar o pai, leia o Encaminhamento da chave ideia/projeto e procure o
marcador em tarefas abertas e concluídas do projeto, com paginação quando houver.
Zero resultado com busca incompleta não prova ausência. Mais de uma tarefa com
o marcador bloqueia a ideia. Tarefa idêntica já existente é reutilizada, sem
reabrir nem mover. Conteúdo diferente exige revisão do time.

Antes de cada subtarefa, leia as existentes por pai e marcador. Reutilize a etapa
equivalente; duplicidade ou etapa sem identidade inequívoca exige conciliação,
não criação adicional. Confira conteúdo e prazos, não apenas número de tarefas.

Após cada criação, releia URL, pai/projeto, seção, descrição, campos e prazo.
Registre a URL comprovada no Encaminhamento. `Concluído` exige pai e todas as
etapas aprovadas relidos e equivalentes ao lote. Sem confirmação de retorno,
registre Incerto; uma falha não permite repetição cega.

Se o conector não permitir concluir a listagem de subtarefas, conferir o pai
ou pesquisar o marcador, interrompa novas criações da ideia. Entregue os links
comprovados e peça conciliação verificável pelo time ou a conexão necessária;
ausência no checkpoint local não prova ausência remota, inclusive para BMS.

## Depois do envio

Não monitorar nem sincronizar continuamente nesta versão. Se o usuário pedir
conferência, compare snapshot enviado, dados vivos no Airtable e Asana. Preserve
mudanças humanas posteriores e apresente diferenças antes de propor atualização.
Criação de pasta, anexação de arquivos de produção, comentários/notificações e
aprovação final do cliente permanecem fora da primeira versão.
