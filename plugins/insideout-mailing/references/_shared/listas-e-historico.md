# Listas e histórico

## Listas

Uma lista tem ID, versão inteira crescente, nome, finalidade e critérios.
Pode estar ligada a uma ação existente. Itens referenciam a versão exata.
Antes de montar, resolva tipo de contato, região, vínculo, finalidade e campos
necessários com fontes em escopo; pergunte somente o que muda a seleção.

Mostre incluídos, excluídos e pendentes, com razões. Cadastro ambíguo não entra
em exportação pronta para envio. Endereço completo não prova que foi validado;
explique o que foi conferido. Não expor CPF ou perfil sensível em exportações
logísticas se não forem necessários.

Rascunhos podem ser editados após aprovação das mudanças. Para fechar, mostrar
a seleção exata e pendências; obter decisão sobre cada pendência material.
Preencher destinatário, endereço e CEP da versão fechada com os valores
selecionados. Depois do fechamento, preservar a versão e criar outra para
qualquer alteração de conteúdo ou seleção. Repetir critérios e seleção idênticos
reutiliza a versão em vez de gerar duplicata.

## Participações

Convite, presença e envio são dimensões independentes. Todos começam como
`Não informado`/`Não informada` quando a fonte não declara o evento.
Lista de convidados não comprova presença. Confirmação não comprova entrega.
Uma seleção para seeding não é prova de envio.

Importação exige ação, significado da lista, origem e data do fato quando
disponível. Reutilize a participação Contato + Ação, atualizando somente os
fatos aprovados. Mesmo contato em várias listas da ação não aumenta a contagem.
Contradição entre fontes e regressão de estado precisam de revisão.
Data ausente permanece vazia; nunca usar data da importação como data do fato.

Ao registrar envio, preserve destinatário, endereço e CEP efetivamente usados,
fornecidos pela fonte ou escolhidos explicitamente antes do registro.
Atualização do cadastro não modifica esses valores. Mais de um envio com
destinos distintos na mesma ação excede a linha única: preservar fatos existentes
e pedir desdobramento explícito da ação antes de sobrescrever.

## Cruzamentos e consultas

Separe correspondências confirmadas, ambíguas e não encontradas usando
`identidade-e-qualidade.md`. Sem prova forte, não associe.
Uma linha importada guarda origem suficiente para ser reconhecida na reexecução.
Listas externas nunca autorizam sobrescrever dados do contato.
Apresente os cruzamentos e fatos a registrar antes da escrita.
Consultas distinguem selecionados, convidados, confirmados, presentes, enviados
e entregues. Declare escopo e não conte itens de listas como pessoas únicas.
