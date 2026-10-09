# Contrato da caixa de fricções

## Destino e escopo

A única caixa para **novos** relatos dos plugins InsideOut é a aba
[`Fricções e fixes`](https://docs.google.com/spreadsheets/d/1w5IWXgefqsb15149T9SlNj6UEKNsJVJxHH4XAixA0uM/edit?gid=1952697901#gid=1952697901)
da planilha **Acervo de Governança - Inside Out**. Confirme planilha, aba,
cabeçalhos A:N, opções de listas e intervalo da tabela na sessão. O link
identifica o destino; não reutilize índices de linha ou da aba de sessões
anteriores. A planilha precisa estar acessível a quem registra e mantém os
plugins; o acesso de uma sessão não comprova o de toda a equipe.
Verifique o compartilhamento atual quando possível. Se a planilha puder ser
aberta por quem tem o link, trate também notas e IDs como conteúdo exposto:
registre somente informação sanitizada. Se o caso exigir detalhe privado
para ser compreendido, entregue uma prévia `não registrado` e peça um destino
restrito antes de escrever esse detalhe.

A base InsideOut Governança no Airtable, a tabela `Feedback do plugin` do
InsideOut Social e os arquivos locais do Mar Aberto são históricos. Não os
use para novos registros, não os migre e não os apague automaticamente.
Comentários de clientes sobre posts pertencem a `review-grid-feedback`.

## Mapeamento de uma nova linha

Use os cabeçalhos atuais da aba, nunca a posição sem confirmá-los. As colunas
H:K e M:N pertencem à manutenção e à decisão de governança; deixe-as vazias
na criação. Escreva somente A:G e L, sem substituir uma linha ocupada.

| Coluna | Cabeçalho | Conteúdo na criação |
|---|---|---|
| A | `ID` | `FR-` + os 12 primeiros hexadecimais maiúsculos do fingerprint; nota com o SHA-256 completo |
| B | `ID da capacidade` | ID encontrado de forma unívoca no `Mapa de capacidades`; vazio se não houver vínculo confirmado |
| C | `Área` | `InsideOut Social`, `InsideOut Mar Aberto` ou `InsideOut Governança`, conforme o plugin afetado |
| D | `Fricção observada` | `[plugin/componente] sintoma`; linhas `Contexto:`, `Esperado:` e `Observado:` com fatos sanitizados |
| E | `Impacto` | `Baixo`, `Médio`, `Alto` ou `Crítico` quando a evidência sustentar a categoria; caso contrário, vazio |
| F | `Recorrência` | `Isolada` na primeira ocorrência registrada; não afirma que nunca ocorreu antes |
| G | `Evidência` | `Tipo: Bug/Melhoria`, `Versão: ...`, `Impacto relatado: ...`, `Fonte: relato não verificado`, e evidência sanitizada fornecida |
| L | `Status` | `Aberta` |

`Contexto`, `Esperado`, `Observado` e `Impacto relatado` são obrigatórios na
prévia. Não use `Hipótese de causa`, `Fix proposto`, `Responsável pelo fix`,
`Prazo`, `Evidência de resolução` ou `Decisão de governança` para dados de
entrada. Não invente capacidade, categoria de impacto, responsável ou fix.

## Fingerprint, ID e duplicidade

Para cada um de `Plugin`, `Componente`, `Esperado` e `Observado`, aplique
Unicode NFKC, remova espaço no início e no fim, substitua sequências de espaços
por um único espaço e converta para minúsculas. Una os quatro valores com `\n`
e calcule SHA-256 dos bytes UTF-8. A nota de A guarda o fingerprint completo,
`Plugin`, `Componente` e `Tipo`; não guarda dados privados. Se não houver meio
confiável de calcular o hash, não invente ID: entregue a prévia marcada
`não registrado` até ser possível gerar um ID verificável.

Leia as linhas ocupadas da aba em todos os estados. Pesquise o mesmo ID e
fingerprint, além de variações de componente, ação e sintoma. Um mesmo ID com
outro fingerprint indica colisão ou erro: pare. Um relato semanticamente
igual pode ter outro hash; apresente-o como possível duplicata. Não reabra
`Resolvida` nem altere uma decisão anterior automaticamente.

Quando a pessoa aprovar uma recorrência, preserve A, D, H:K e L:N; acrescente
em G uma entrada datada e sanitizada `Recorrência: ...` e mude F para
`Recorrente` apenas com pelo menos duas ocorrências distintas confirmadas.
Use `Sistêmica` só com evidência de alcance entre componentes ou produtos.
Mostre a linha e o texto exato a acrescentar antes de qualquer atualização.

## Escrita e conferência

Encontre a primeira linha inteiramente vazia da tabela a partir da linha 7.
Releia essa linha e os possíveis duplicados imediatamente antes da escrita.
Se a tabela estiver cheia, confirme que a linha seguinte está vazia, estenda
o intervalo nativo da tabela com seus formatos e opções e releia a estrutura
antes de escrever. Se houver conflito ou mudança concorrente, pare sem
sobrescrever. Nunca use uma aba alternativa, a base Airtable ou arquivo local
como substituto silencioso.

Apresente todos os valores e a nota propostos, com a linha de destino, antes
da escrita. Registre somente após confirmação explícita da prévia. Releia A:N
e a nota de A depois da mutação; confira ID, relato, listas, status e colunas
reservadas antes de declarar sucesso. Na segunda execução do mesmo caso,
reencontre a linha e não crie duplicata. Em testes, use `[TESTE CODEX]` no
início de D; a remoção de linhas de teste é uma ação separada.

## Sanitização e falha

Generalize cliente, pessoa, briefing, claim privado, campanha, comentário,
URL privada, caminho local, ID operacional, credencial, email e log cru.
Preserve apenas o detalhe necessário para reconhecer o sintoma. Um relato
fornecido pela pessoa é evidência do relato, não comprovação independente.

Quando a planilha ou a aba estiver indisponível, entregue a prévia copiável
com estado `não registrado`; não peça credenciais nem exija GitHub. Arquivo
local opcional é rascunho, não uma entrada da caixa compartilhada.
