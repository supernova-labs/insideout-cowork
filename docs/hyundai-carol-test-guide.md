# Hyundai Social — instalação e primeiro teste

Esta versão 0.1.1 permite testar pesquisa, planejamento e revisão de referências.
É um piloto: o envio ao quadro operacional do Asana aguarda homologação e os
testes da integração. A versão está na branch `codex/hyundai-social-pilot`.

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

### No Windows: abrir o PowerShell do próprio computador

Abra o menu Iniciar, procure **PowerShell** e abra-o normalmente, sem executar
como administrador. Os comandos desta seção são digitados nessa janela, fora
do campo de mensagem do ChatGPT. Primeiro, confira se o comando está disponível:

```powershell
codex --version
```

Se aparecer uma versão, continue abaixo. Se o Windows disser que `codex` não é
reconhecido, o comando não está disponível nessa janela: o CLI pode estar ausente
ou fora do PATH. Se ele acabou de ser instalado, feche o PowerShell e abra uma
janela nova antes de repetir o teste.

Se continuar indisponível, instale o **Codex CLI** com o comando da
[documentação oficial, opção Windows](https://learn.chatgpt.com/docs/codex/cli).
Abra o PowerShell normalmente na conta da pessoa que usa o aplicativo e cole
a linha inteira, sem acrescentar aspas ao redor do comando:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Esse instalador oficial disponibiliza o CLI no perfil do usuário e não exige
Node/npm. A documentação de [instalação no Windows](https://learn.chatgpt.com/docs/enterprise/windows-deployment)
descreve a instalação por usuário e a atualização do PATH. Aguarde a conclusão,
feche o PowerShell e abra outro. Confira novamente:

```powershell
codex --version
codex plugin marketplace list --json
```

Se a instalação falhar, envie a saída completa desse instalador antes de tentar
os comandos do catálogo. Disponibilizar o CLI permite gerenciar o catálogo;
isso não comprova nem corrige a conexão Airtable do aplicativo.

Se o chat responder `failed to resolve CODEX_HOME` / `Could not find home directory`,
a execução falhou antes de consultar o catálogo. Repita o teste no PowerShell
local. O print do chat, sozinho, não prova defeito no perfil do Windows. Não
crie diretórios, defina variáveis ou copie credenciais para o ambiente do chat
como tentativa de conserto. Se o mesmo erro ocorrer no PowerShell, envie o erro
completo e a versão do Codex para diagnóstico do ambiente local.

Antes, no terminal local, confira se o catálogo já existe:

```powershell
codex plugin marketplace list --json
```

Se `insideout` já estiver cadastrado, anote sua origem atual. Para trocar da
versão normal para o piloto, remova somente o cadastro dessa origem:

```powershell
codex plugin marketplace remove insideout
```

Este comando gerencia a origem do catálogo. Não use comandos para desinstalar
plugins ou apagar configurações. A seleção do piloto vale para o catálogo
InsideOut nesta conta; durante o teste, não atualize os outros produtos a partir
dessa branch. A versão normal pode ser recadastrada pela `main` após o teste.

Em seguida, cadastre a origem de piloto e instale o Hyundai:

```powershell
codex plugin marketplace add supernova-labs/insideout-cowork --ref codex/hyundai-social-pilot
codex plugin add insideout-hyundai-social@insideout
```

Os comandos devem ser executados no terminal local, não somente colados como
mensagem de planejamento no chat. O primeiro seleciona o catálogo da branch
de piloto; o segundo instala o produto Hyundai. Cadastrar o catálogo não
comprova a instalação. A `main` ainda não oferece esse plugin.

Se o catálogo já aponta para o piloto e precisa buscar uma revisão nova,
atualize-o e confira os produtos disponíveis:

```powershell
codex plugin marketplace upgrade insideout
codex plugin list --available --marketplace insideout --json
```

**InsideOut Hyundai Social 0.1.1** deve aparecer. Se não aparecer, não continue
o grid: guarde a resposta completa dos comandos. Atualizar um catálogo que ainda
aponta para `main` não muda sua branch; é preciso trocar sua origem conforme
o procedimento acima. Não remova plugins nem apague configurações como tentativa.

No diretório de plugins do aplicativo, confira **InsideOut Hyundai Social**
instalado/ativado e a conexão **Airtable** concluída. Instale somente o produto
Hyundai para este teste. Pesquisa web também precisa estar disponível.

A sintaxe de catálogo e seleção de branch segue a
[documentação oficial do Codex](https://developers.openai.com/plugins/build/plugins).
O plugin não inclui credenciais nem concede acesso a serviços externos.
Depois de concluir instalação e conexão, reinicie o aplicativo e abra uma
conversa nova. Uma conversa anterior pode não dispor das ferramentas recém-conectadas.

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
