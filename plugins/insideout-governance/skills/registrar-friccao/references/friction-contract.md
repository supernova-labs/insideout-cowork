# Contrato da caixa de fricções

## Destino e escopo

A base **InsideOut Governança**, tabela `Fricções`, é a caixa de entrada única
para novos relatos sobre os plugins InsideOut, inclusive a própria governança.
Descubra base, tabela, campos e opções atuais antes de ler ou escrever. A base deve estar
acessível às pessoas que registram e às que mantêm os plugins; acesso do agente
em uma sessão não comprova acesso do restante da equipe.

Registros históricos na tabela `Feedback do plugin` da base InsideOut Social e
arquivos locais de Mar Aberto permanecem no destino original. Não os migre,
edite ou apague automaticamente. Se forem fornecidos como contexto, sanitize-os
antes de qualquer novo registro.

## Campos

| Campo | Conteúdo |
|---|---|
| `Título` | `[<plugin>/<componente>] <sintoma observável>` sem dado de cliente |
| `Plugin` | nome do plugin afetado, como `insideout-social`, `insideout-mar-aberto` ou `insideout-governance` |
| `Componente` | nome da skill ou etapa; use o plugin quando desconhecido |
| `Versão` | versão confirmada ou `desconhecida` |
| `Tipo` | `Bug` ou `Melhoria` |
| `Contexto` | caso de uso mínimo e anonimizado |
| `Esperado` | resultado verificável |
| `Observado` | diferença factual, sem log cru |
| `Impacto` | pessoa, decisão, etapa ou entrega afetada |
| `Fingerprint` | SHA-256 definido abaixo, se calculável |
| `Status` | `Novo` na criação |
| `Recorrências` | vazio na criação; ocorrências posteriores, após prévia e confirmação |
| `Autor` | opcional, somente quando conhecido com segurança |
| `Link GitHub` | vazio na criação; só a manutenção pode preencher depois |

Os campos existentes na tabela são a fonte de verdade operacional. Se o schema
divergir deste contrato, não invente opção nem escreva em campo aproximado;
apresente a divergência. Não grave uma entrada sem `Plugin`, `Componente`,
`Tipo`, `Contexto`, `Esperado`, `Observado`, `Impacto` e `Status`.

## Fingerprint e duplicidade

Para cada um de `Plugin`, `Componente`, `Esperado` e `Observado`, aplique
Unicode NFKC, remova espaço no início e no fim, substitua sequências de espaços
por um único espaço e converta para minúsculas. Una os quatro valores com `\n`
e calcule SHA-256 dos bytes UTF-8. Se não houver meio confiável de calcular o
hash, deixe `Fingerprint` vazio e faça a busca textual; não invente um valor.

Pesquise primeiro o mesmo fingerprint em todos os estados. Também pesquise
variações de componente, ação e sintoma, pois relatos semanticamente iguais
podem usar palavras diferentes. Uma entrada `Resolvido` é relevante para
recorrência, mas não deve ser reaberta automaticamente. Se a busca não puder
ser feita, informe a limitação na prévia antes de qualquer criação.

## Sanitização e confirmação

Generalize nomes de clientes e pessoas, textos de briefing, claims e campanhas
não públicos, comentários, URLs privadas, IDs, caminhos, datas sensíveis,
credenciais, emails e logs. Preserve apenas o detalhe necessário para
reproduzir o sintoma. Um exemplo pode virar `marca de teste`, `post de exemplo`
ou `publicação de exemplo`.

Apresente exatamente os valores propostos antes da escrita. Registre somente
após confirmação explícita daquela prévia. Para complementar uma recorrência,
mostre o texto que será acrescentado e confirme a escolha do registro.
Releia toda escrita e compare os campos; falha de criação ou releitura não é
sucesso confirmado.

Quando Airtable estiver indisponível, entregue todos os campos em formato
copiável com estado `não registrado`. Não peça credenciais nem exija GitHub.
Um arquivo local opcional é apenas rascunho fora do plugin, não substitui a
entrada compartilhada.
