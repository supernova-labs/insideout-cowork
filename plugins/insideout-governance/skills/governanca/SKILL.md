---
name: governanca
description: Lê as fricções da base InsideOut Governança, ordena por impacto e recorrência e sugere um fix verificável para cada caso em formato padronizado. Use quando a equipe pedir triagem, priorização ou propostas de correção dos plugins InsideOut.
---

# Governança das fricções dos plugins InsideOut

Produza uma fila de decisão a partir das fricções já registradas. Esta skill é
somente de leitura: sugere fixes, mas não altera registros, código, status,
issues ou prioridades em sistemas externos.

## Preparar a leitura

Leia `references/triage-contract.md` por inteiro. Descubra nesta sessão a base
**InsideOut Governança**, a tabela `Fricções` e os campos atuais. Não use IDs
guardados no plugin. Leia todas as páginas dos registros necessários ao escopo
pedido. Se a leitura for parcial, explicite a cobertura e não apresente a fila
como ranking completo.

Por padrão, priorize casos abertos na base de governança. Considere `Novo`,
`Em triagem` e `Encaminhado` como abertos quando essas opções existirem no
schema; mostre os resolvidos à parte se forem relevantes para uma recorrência.
Não presuma que um link para GitHub signifique fix concluído. Relatos históricos
do Social e arquivos locais do Mar Aberto só entram quando a pessoa os colocar
explicitamente em escopo; não os migre nem os conte como sincronizados.

## Analisar

1. Separe fatos observados, impacto declarado, inferências e lacunas. Leia
   `Contexto`, `Esperado`, `Observado`, `Impacto`, `Status`, `Recorrências` e a
   identificação de plugin/componente, sem buscar dados de cliente para
   completar o relato.
2. Agrupe possíveis duplicatas pelo fingerprint e pela equivalência do sintoma.
   Registros parecidos exigem revisão; não some ocorrências de causas apenas
   supostamente iguais. Conte o relato inicial como uma ocorrência e acrescente
   somente entradas distintas e verificáveis de `Recorrências`.
3. Classifique impacto e recorrência com a matriz do contrato. Priorize o
   impacto crítico mesmo com uma só ocorrência. Se faltar evidência para
   classificar, marque `A esclarecer`, diga o que falta e não invente nota.
4. Para cada caso, sugira a menor mudança capaz de corrigir o comportamento ou
   prevenir sua repetição. Aponte o alvo provável (skill, referência, eval,
   integração ou operação), indique quando a causa é hipótese e formule um
   critério de aceite observável. Não atribua responsável ou prazo sem fonte.
5. Gere o resumo e uma ficha para **cada caso no escopo**, no formato fixo do
   contrato, ordenados por prioridade e depois por recorrência verificada.
   Preserve a distinção entre proposta, decisão aprovada e fix implementado.

Se a tabela estiver vazia, informe `0 fricções registradas` e não crie fixes
fictícios. Se a conexão falhar, indique que a triagem não foi possível; não
trate um rascunho local como conteúdo da base.

## Limites

- Não expor cliente, pessoa, campanha, briefing, comentário, URL privada, ID
  operacional, caminho local, credencial ou log cru no output.
- Não alterar `Fricções`, abrir issue ou PR, publicar plano ou aplicar fix por
  conta desta skill. Execução de um fix requer um pedido separado.
- Não prometer redução de recorrência sem teste ou acompanhamento posterior.
