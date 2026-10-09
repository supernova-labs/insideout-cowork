---
name: registrar-friccao
description: Registra bugs, falhas, disparos inadequados e sugestões sobre os plugins InsideOut na aba Fricções e fixes do Acervo de Governança. Use quando alguém relatar uma fricção do Social, do Mar Aberto ou da própria governança, inclusive sem execução ativa.
---

# Registrar fricção dos plugins InsideOut

Transforme o relato em uma linha factual, sanitizada e rastreável na aba
**Fricções e fixes** da planilha **Acervo de Governança - Inside Out**. Esse é
sempre o destino de novos relatos dos plugins. Esta skill não corrige a
instalação nem decide a prioridade da mudança.

Comentários do cliente sobre posts pertencem ao fluxo editorial
`review-grid-feedback`, não a esta caixa de fricções.

## Preparar

Leia `references/friction-contract.md`. Identifique o plugin e o componente ou
etapa afetados. Use apenas o contexto fornecido; peça somente os detalhes que
faltarem para distinguir esperado, observado e impacto. Uma execução ativa ou
acesso ao estado operacional dos produtos não é necessário.

Abra a planilha indicada no contrato e confirme nesta sessão seu título, a aba
`Fricções e fixes`, o cabeçalho A:N, as opções das colunas de impacto,
recorrência e status e o intervalo da tabela. Não use a base Airtable para
novos relatos. Não abra briefings, corpus, comentários, cookies, credenciais
nem logs para enriquecer o relato.
Confirme a visibilidade da planilha quando disponível; se for acessível por
link, não inclua detalhe privado mesmo em notas ou evidências.

## Preparar a entrada

1. Classifique como `Bug` se o comportamento contradiz o contrato ou falha na
   execução; use `Melhoria` para ampliar ou melhorar a experiência.
2. Sanitize o contexto antes de pesquisar ou apresentar qualquer prévia.
3. Calcule o fingerprint e o ID estável definidos no contrato.
4. Leia todas as linhas ocupadas da aba e pesquise ID, plugin, componente, ação
   e sintoma em todos os estados. Compare o fingerprint guardado na nota do ID.

Quando houver possível duplicidade, mostre um resumo e o estado. Ofereça
acrescentar uma recorrência sanitizada à linha existente, criar uma entrada
distinta com a diferença explícita ou cancelar. Não escreva silenciosamente.

## Confirmar e registrar

Mostre a prévia por coluna da aba: `ID`, `ID da capacidade` quando confirmado,
`Área`, `Fricção observada`, `Impacto`, `Recorrência`, `Evidência` e
`Status = Aberta`. Mostre também o conteúdo da nota do ID. Informe as
categorias generalizadas sem repetir dados sensíveis. Peça confirmação explícita
da versão final; qualquer alteração posterior requer nova confirmação.

Depois da confirmação, releia a linha de destino imediatamente antes da
escrita. Preencha uma única linha vazia da tabela, ou acrescente somente a
recorrência aprovada à linha escolhida. Preserve as colunas reservadas para
governança. Releia a linha e confira os campos antes de informar que foi
registrado. Uma segunda execução do mesmo caso deve reencontrar a linha.

Se a planilha, a aba, sua estrutura ou a permissão de escrita estiver
indisponível, entregue a prévia sanitizada em formato copiável, marcada
`não registrado`. Um arquivo local só pode ser criado fora do plugin se a
pessoa o pedir; ele continua sendo um rascunho, não uma entrada compartilhada.

## Limites

- Não criar formulário, issue, PR, rascunho de e-mail ou correção como parte do
  registro. Encaminhamento externo é uma ação separada e requer autorização.
- Não alterar status de triagem, fixes, responsáveis, prazos, decisões ou
  registros históricos sem pedido explícito.
- Não expor cliente, campanha, briefing, claim privado, comentário, pessoa,
  email, URL privada, caminho local, ID operacional, credencial ou log cru.
- Não alegar sucesso sem reler a linha da planilha compartilhada.
