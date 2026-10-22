# Verificação do piloto Mailing

As evidências de dados abaixo correspondem à implantação inicial de 16/10/2026.
Em 22/10/2026, a distribuição foi reunida à Hyundai Social no catálogo da `main`,
com autorização explícita do usuário. Isso não encerra as pendências funcionais
ou a homologação com a equipe.

## Comprovado nesta entrega

- Validadores estruturais do Social, Mar Aberto e Mailing, inventário Agent Smith
  e validação individual das três skills.
- Reconciliação integral dos campos migrados após a conversão nativa; diferenças
  de datas e texto introduzidas pela conversão foram corrigidas pela origem.
- Sete abas nativas, tabelas cobrindo os dados, opções de seleção, cabeçalhos
  congelados e proteção de identidades e cálculos.
- Oito registros sintéticos identificados com [TESTE CODEX], escritos com
  releitura em todas as entidades; segunda passagem sem novas criações.
- Duas versões de lista e uma participação para o mesmo contato e ação.
- Mudança de endereço do contato preservando o snapshot da lista fechada e
  do envio sintético. Convite, presença e envio permanecem independentes.
- Original e auditoria da implantação preservados fora do repositório, em
  destino privado aprovado pelo usuário.

## Não executado

- Instalação e invocação do plugin publicado em uma nova tarefa do Codex.
  A implantação inicial não trocou o catálogo da conta pela branch de testes.
  A disponibilidade posterior no catálogo não comprova invocação em tarefa limpa.
- Evals conversacionais completos em tarefas limpas: os cenários estão
  distribuídos, mas os testes diretos da planilha não substituem essa rodada.
- Importação de lista histórica real, dependente de fonte e significado
  fornecidos pelo time.
- Testes com credenciais de um segundo colaborador e decisão de adoção oficial.

Não remover dados de teste automaticamente. O piloto é uma cópia independente;
o Excel anterior permanece oficial até decisão posterior.
