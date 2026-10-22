# Instalar e atualizar os plugins InsideOut

O catálogo `insideout` da `main` reúne Social, Mar Aberto, Governança,
Hyundai Social 0.1.1 e Mailing 0.1.0. Os dois últimos continuam em piloto;
publicação no catálogo não equivale a homologação operacional.

## Onde executar no Windows

Abra **PowerShell** pelo menu Iniciar, na sua conta normal, sem executar como
administrador. Cole os comandos nessa janela, fora do campo de mensagem do
ChatGPT. Pedir ao chat para executar um comando pode usar outro ambiente e não
alterar a instalação do seu computador.

Confira primeiro:

```powershell
codex --version
```

Se o comando não for reconhecido e acabou de ser instalado, feche o PowerShell
e abra uma janela nova. Se continuar ausente, use o instalador oficial da
[documentação do Codex CLI, opção Windows](https://learn.chatgpt.com/docs/codex/cli):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Feche e reabra o PowerShell e repita a verificação. Copie cada comando sem
acrescentar aspas ao redor. Se ainda não entrou na conta, execute `codex login`
e use a mesma conta ChatGPT do aplicativo.

## Cadastrar o catálogo ou sair de uma branch de piloto

Confira as origens atuais:

```powershell
codex plugin marketplace list --json
```

Se ainda não houver `insideout`, cadastre-o:

```powershell
codex plugin marketplace add supernova-labs/insideout-cowork --ref main
```

Se `insideout` já aponta para `main`, atualize o catálogo:

```powershell
codex plugin marketplace upgrade insideout
```

Se ele foi cadastrado com `codex/hyundai-social-pilot` ou
`codex/mailing-google-sheets-pilot`, troque explicitamente a origem. O erro
`already added from a different source` também indica que adicionar por cima
não fez a troca. Anote a origem atual e execute, um comando por vez:

```powershell
codex plugin marketplace remove insideout
codex plugin marketplace add supernova-labs/insideout-cowork --ref main
```

Esses comandos gerenciam a origem do catálogo. Não use `codex plugin remove`
nem apague configurações ou pastas como tentativa de instalação. Confira o
estado dos produtos depois da troca; preserve os outros plugins instalados.

## Instalar os produtos desejados

Confira os produtos do catálogo:

```powershell
codex plugin list --available --marketplace insideout --json
```

Hyundai Social 0.1.1 e Mailing 0.1.0 devem aparecer, instalados ou disponíveis.
Instale os que deseja usar:

```powershell
codex plugin add insideout-hyundai-social@insideout
codex plugin add insideout-mailing@insideout
codex plugin list --marketplace insideout --json
```

No aplicativo, confirme os produtos instalados e ativados. Hyundai requer a
conexão oficial do Airtable; Mailing usa Google Drive/Sheets. Cada pessoa
autoriza sua conta e precisa ter acesso à base ou planilha correspondente.
Instalar o pacote não concede acesso aos dados.

Feche e reabra o aplicativo e comece uma conversa nova. Primeiro confira
somente a leitura da base ou planilha; depois siga o
[piloto Hyundai](hyundai-carol-test-guide.md) ou a
[homologação Mailing](mailing-pilot-test-protocol.md).

O catálogo local configurado pelo CLI não comprova instalação no ChatGPT pelo
navegador. Se testar por lá, confira separadamente a disponibilidade do plugin,
das skills e da conexão nessa conversa.

## Se houver bloqueio

Erros como `Could not find home directory`, `failed to resolve CODEX_HOME` ou
`no /proc/self/exe available` dentro do chat podem preceder a consulta ao catálogo.
Repita a verificação no PowerShell local antes de concluir que há defeito no
Windows. Se o erro ocorrer também ali, envie a versão e a saída do comando.

Se a ferramenta do Airtable ou Drive estiver indisponível, o acesso aos dados
ainda não foi testado. Confira a conta em **Gerenciar**, a autorização e uma
conversa nova. Envie o erro, o print da conexão e a versão do aplicativo para
diagnóstico. Não é necessário instalar auxiliares de dados para esse teste.

Referência para comandos e catálogo:
[documentação oficial de plugins](https://developers.openai.com/plugins/build/plugins).
