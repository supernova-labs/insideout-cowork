# Hyundai Social — instalação e primeiro teste

Esta versão 0.1.1 permite testar pesquisa, planejamento e revisão de referências.
É um piloto: o envio ao quadro operacional do Asana aguarda homologação e os
testes da integração. A versão está disponível no catálogo da `main`, junto ao Mailing.

## Acesso à base

Use a conta InsideOut que já acessa **InsideOut Hyundai Social** no Airtable.
Em 16/10/2026, Caroline já consta como proprietária do workspace e herda acesso
à base. Não é preciso criar outra base nem pedir acesso ao Social antigo.

O pacote declara o conector oficial Airtable como dependência obrigatória. Na
instalação pelo aplicativo de desktop, conclua a conexão do Airtable com essa
mesma conta. Se a conexão já existir, confira se ela está ativa. Se a base Hyundai
não aparecer depois de uma busca real, revise a autorização de bases nessa conexão.
O acesso no navegador e a autorização do conector são verificações distintas.
Não compartilhe credenciais nem use a conta de outra pessoa.

## Instalar a versão de piloto

Siga o [guia comum de instalação e atualização](instalacao-plugins.md).
Execute os comandos no PowerShell do próprio computador, fora do chat. O guia
explica como trocar o catálogo de uma antiga branch de piloto para a `main`,
que oferece Hyundai Social e Mailing juntos, e como conferir a instalação.

Confirme **InsideOut Hyundai Social 0.1.1** instalado/ativado e a conexão
**Airtable** concluída com sua conta InsideOut. Pesquisa web também precisa
estar disponível. Reinicie o aplicativo e abra uma conversa nova antes do teste.

## Diagnosticar antes de iniciar o grid

São três verificações independentes:

| Verificação | Evidência necessária |
|---|---|
| Instalação do Hyundai | Produto 0.1.1 instalado e ativado no aplicativo; não apenas catálogo cadastrado |
| Conexão do Airtable | Conector oficial instalado e conta InsideOut conectada no aplicativo |
| Acesso à base | Busca real encontra a base exata e lista as oito tabelas na conversa nova |

Se a resposta disser **ferramenta indisponível nesta sessão**, o acesso à base
não chegou a ser testado. Confira plugin, conexão e conversa nova antes de pedir
novo convite ou alterar permissões. Se a busca funcionar e retornar acesso negado
ou não encontrar a base, então confira conta e bases autorizadas no Airtable.

Se continuar bloqueado, envie à pessoa que acompanha o piloto a resposta completa
dos comandos de instalação, o print do detalhe do plugin Hyundai e o estado da
conexão Airtable. Não envie senha, token ou códigos de autenticação.

O erro `marketplace 'insideout' is already added from a different source` foi
reproduzido em 19/10/2026 ao tentar adicionar a branch de piloto sobre o cadastro
existente. Nesse caso, repetir o comando de adicionar ou atualizar o catálogo
não resolve: é necessária a troca da origem cadastrada descrita acima.

## Começar em uma conversa nova

Primeiro, peça:

> Quero testar o InsideOut Hyundai Social. Confira se a minha conexão encontra
> a base InsideOut Hyundai Social e suas oito tabelas. Apenas leia; não altere
> dados nem use a base InsideOut Social antiga.

Depois de confirmar o acesso, abra outra conversa limpa para a retrospectiva:

> Usando somente o InsideOut Hyundai Social, faça um piloto retrospectivo de
> setembro de 2026, com data de corte em 31/08/2026. Comece pela pesquisa e use
> as diretrizes fixas da base Hyundai, sem exigir briefing. Não consulte o grid
> histórico esperado. Separe ideias e publicações por rede, reserve espaços
> semanais para influenciadores e declare lacunas de fontes históricas. Apresente
> o take para revisão antes de salvar. Não envie nada ao Asana.

Não forneça o calendário esperado nessa conversa. Ele será usado depois, por
outra pessoa ou em outra conversa, para comparar qualidade editorial.

Para testar persistência, confirme o lote escolhido como Retrospectivo, com
prefixo `[TESTE CODEX]`, e peça releitura e segunda execução sem duplicatas.
Os registros sintéticos de integração já existentes devem ser preservados e
excluídos do repertório editorial.

## Testar a revisão e devolver os resultados

Peça um HTML de ideias e referências com comentários exportáveis. Confira
desktop e celular; crie, edite e remova um comentário, recarregue o arquivo e
exporte o JSON. Devolva esse JSON à conversa que guardou a revisão original.
Comentários pedem ajustes; a confirmação das ideias que seguirão à produção
é uma decisão explícita do time sobre uma versão específica.

Registre o que funcionou, o pedido feito, o resultado esperado e o observado.
Para a avaliação completa, use o [roteiro de homologação](hyundai-pilot-test-protocol.md).

Nesta rodada, não use responsáveis/prazos fictícios no quadro real do Asana.
Regras de contagem, influenciadores, alocação, integração e isolamento entre
equipes continuam pendentes. Não há produção de artes, copy final ou Notion
nesta versão.
