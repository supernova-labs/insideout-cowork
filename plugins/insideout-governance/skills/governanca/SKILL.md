---
name: governanca
description: Lê as fricções da aba Fricções e fixes do Acervo de Governança, ordena por impacto e recorrência e sugere um fix verificável para cada caso em formato padronizado. Use quando a equipe pedir triagem, priorização ou propostas de correção dos plugins InsideOut.
---

# Governança das fricções dos plugins InsideOut

Produza uma fila de decisão a partir das fricções já registradas. Esta skill é
somente de leitura: sugere fixes, mas não altera registros, código, status,
issues ou prioridades em sistemas externos.

## Preparar a leitura

Leia `references/triage-contract.md` por inteiro. Confirme nesta sessão a
planilha **Acervo de Governança - Inside Out**, a aba `Fricções e fixes`, os
cabeçalhos e o intervalo da tabela. Leia todas as linhas ocupadas necessárias
ao escopo pedido. Se a leitura for parcial, explicite a cobertura e não
apresente a fila como ranking completo.

Por padrão, priorize casos com status `Aberta`, `Em análise`, `Priorizada` ou
`Em execução`. Mostre `Resolvida` e `Não priorizada` à parte quando relevantes
para a recorrência ou para uma decisão existente. Não presuma que um fix ou
uma decisão escritos na linha já foram executados. A antiga base Airtable e
os relatos históricos do Social e do Mar Aberto só entram se a pessoa os
colocar explicitamente em escopo; não os conte como sincronizados.

## Analisar

1. Separe fatos observados, impacto declarado, inferências e lacunas. Leia
   `Fricção observada`, `Impacto`, `Recorrência`, `Evidência`, `Hipótese de
   causa`, `Fix proposto`, `Status` e `Decisão de governança`, sem buscar dados
   de cliente para completar o relato.
2. Agrupe possíveis duplicatas pelo ID, pela nota de fingerprint quando
   existir e pela equivalência do sintoma.
   Registros parecidos exigem revisão; não some ocorrências de causas apenas
   supostamente iguais. Conte o relato inicial como uma ocorrência e acrescente
   somente entradas distintas e verificáveis de `Recorrência: ...` em
   `Evidência`. A categoria em F, sozinha, não prova uma contagem.
3. Classifique impacto e recorrência com a matriz do contrato. Priorize o
   impacto crítico mesmo com uma só ocorrência. Se faltar evidência para
   classificar, marque `A esclarecer`, diga o que falta e não invente nota.
4. Para cada caso, considere primeiro o fix e a decisão já registrados na
   linha; não os trate como concluídos sem evidência de resolução. Sugira a
   menor mudança capaz de corrigir o comportamento ou prevenir sua repetição.
   Aponte o alvo provável (skill, referência, eval,
   integração ou operação), indique quando a causa é hipótese e formule um
   critério de aceite observável. Não atribua responsável ou prazo sem fonte.
5. Gere o resumo e uma ficha para **cada caso no escopo**, no formato fixo do
   contrato, ordenados por prioridade e depois por recorrência verificada.
   Preserve a distinção entre proposta, decisão aprovada e fix implementado.

Se a aba não tiver fricções, informe `0 fricções registradas` e não crie fixes
fictícios. Desconsidere linhas marcadas `[TESTE CODEX]` da fila real e relate
quantas foram excluídas. Se a conexão falhar, indique que a triagem não foi
possível; não trate um rascunho local como conteúdo da planilha.

## Limites

- Não expor cliente, pessoa, campanha, briefing, comentário, URL privada, ID
  operacional, caminho local, credencial ou log cru no output.
- Não alterar a planilha, abrir issue ou PR, publicar plano ou aplicar fix por
  conta desta skill. Execução de um fix requer um pedido separado.
- Não prometer redução de recorrência sem teste ou acompanhamento posterior.
