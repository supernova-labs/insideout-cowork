---
name: registrar-friccao
description: Registra bugs, falhas, disparos inadequados e sugestões sobre os plugins InsideOut na caixa compartilhada de governança. Use quando alguém relatar uma fricção do Social, do Mar Aberto ou da própria governança, inclusive sem execução ativa.
---

# Registrar fricção dos plugins InsideOut

Transforme o relato em uma entrada factual, sanitizada e rastreável na base
**InsideOut Governança**. Esta skill recebe fricções dos plugins; não corrige a
instalação nem decide a prioridade da mudança.

Comentários do cliente sobre posts pertencem ao fluxo editorial
`review-grid-feedback`, não a esta caixa de fricções.

## Preparar

Leia `references/friction-contract.md`. Identifique o plugin e o componente ou
etapa afetados. Use apenas o contexto fornecido; peça somente os detalhes que
faltarem para distinguir esperado, observado e impacto. Uma execução ativa ou
acesso ao estado operacional dos produtos não é necessário.

Descubra a base de governança, a tabela `Fricções` e seus campos atuais nesta
sessão. Não use IDs guardados no plugin. Não abra briefings, corpus, comentários,
cookies, credenciais nem logs para enriquecer o relato.

## Preparar a entrada

1. Classifique como `Bug` se o comportamento contradiz o contrato ou falha na
   execução; use `Melhoria` para ampliar ou melhorar a experiência.
2. Sanitize o contexto antes de pesquisar ou apresentar qualquer prévia.
3. Calcule o fingerprint definido no contrato quando houver dados suficientes.
4. Pesquise a tabela por plugin, componente, ação e sintoma em todos os estados.
   Compare também o fingerprint quando disponível.

Quando houver possível duplicidade, mostre um resumo e o estado. Ofereça
acrescentar uma recorrência sanitizada ao registro existente, criar uma entrada
distinta com a diferença explícita ou cancelar. Não escreva silenciosamente.

## Confirmar e registrar

Mostre a prévia com os valores de todos os campos que serão escritos, inclusive
`Plugin`, `Componente`, `Tipo`, `Fingerprint` e `Status = Novo`. Informe as
categorias generalizadas sem repetir dados sensíveis. Peça confirmação explícita
da versão final; qualquer alteração posterior requer nova confirmação.

Depois da confirmação, crie um único registro ou acrescente somente a
recorrência aprovada ao registro escolhido. Releia o registro e confira os
campos antes de informar que foi registrado. Uma segunda execução do mesmo
caso deve reencontrar a entrada, não criar outra.

Se a base, a tabela ou a permissão de escrita estiver indisponível, entregue a
prévia sanitizada em formato copiável, marcada `não registrado`. Um arquivo
local só pode ser criado fora do plugin se a pessoa o pedir; ele continua sendo
um rascunho, não uma entrada da caixa compartilhada.

## Limites

- Não criar formulário, issue, PR, rascunho de e-mail ou correção como parte do
  registro. Encaminhamento externo é uma ação separada e requer autorização.
- Não alterar status de triagem ou registros históricos sem pedido explícito.
- Não expor cliente, campanha, briefing, claim privado, comentário, pessoa,
  email, URL privada, caminho local, ID operacional, credencial ou log cru.
- Não alegar sucesso sem reler a entrada da caixa compartilhada.
