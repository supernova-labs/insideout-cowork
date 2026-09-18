---
name: run-mar-aberto
description: Conduz ou retoma o fluxo completo de Mar Aberto da InsideOut, da exportação oficial da Stilingue aos relatórios e planilha. Use quando a pessoa pedir uma análise de mar aberto, uma leitura do i20 ou a continuação de uma execução existente.
---

# Executar o InsideOut Mar Aberto

Conduza uma execução sob demanda sem exigir que a pessoa coordene manualmente
as etapas especializadas. Preserve checkpoints e pare somente para login,
correção de contrato ou gates editoriais.

## Preparar

1. Leia `../../references/_shared/about-mar-aberto.md` e
   `../../references/_shared/local-state.md`.
   Leia também `../../references/_shared/schemas/coverage-decision.schema.json`
   antes de registrar a opção de cobertura limitada.
2. Para uma execução nova, confirme projeto, filtro, data inicial, data final e
   pasta local. Use `nova busca i20` como proposta do piloto, nunca como escolha
   silenciosa.
3. Para uma retomada, abra `manifest.json`, valide caminhos e hashes e apresente
   etapa concluída, lacunas e próximo passo.
4. Não misture execuções nem grave estado dentro do diretório do plugin.

## Meta de execução

Toda execução desta skill deve ser orientada por uma Meta. Antes de iniciar ou
retomar o fluxo, crie uma Meta nativa quando o recurso estiver disponível no
ambiente. Formule o objetivo com o projeto, período, filtro e produtos
esperados conhecidos; por exemplo,
"Concluir a análise de Mar Aberto do período solicitado, com cobertura
auditável e os relatórios finais".

Se o ambiente não disponibilizar uma Meta nativa, preserve esse mesmo objetivo
como estado explícito da execução e aplique as regras desta seção. A ausência do
recurso não transforma a orientação por Meta em opcional.

Mantenha a Meta ativa enquanto houver uma ação segura e relevante para avançar:
retomar uma publicação, aguardar e reler comentários que carregam tardiamente,
continuar uma rolagem, validar um checkpoint ou processar as publicações que
não dependem de uma pendência isolada. Não a considere bloqueada por uma
primeira falha recuperável.

A Meta não amplia permissões nem substitui decisões da pessoa. Pare para login,
correção de contrato, gate editorial, aprovação de cobertura limitada ou outra
ação que exija sua intervenção. Marque-a como concluída somente após atender
aos critérios de `Concluir`; registre bloqueio somente quando não houver ação
segura restante e a mesma dependência externa persistir.

## Orquestrar

Avance nesta ordem:

1. `export-stilingue` valida a planilha oficial fornecida pelo operador ou,
   quando solicitado, orienta sua obtenção e fecha o checkpoint de entrada.
2. `collect-comments` percorre Instagram e YouTube, preserva o corpus temporário
   anonimizado e registra cobertura.
3. Ao esgotar a coleta observável de todas as publicações obrigatórias,
   `analyze-sentiment` processa separadamente menções, comentários e respostas,
   produz os dados derivados e remove o corpus temporário depois de validar o
   checkpoint. Divergência exclusiva entre totais da Stilingue e o corpus
   observado é limitação de auditoria: registre-a, mas não adie a análise nem o
   relatório. Se houver lacunas reais de coleta, conclua as demais publicações;
   um pedido explícito da pessoa para analisar ou gerar o relatório permite
   prosseguir com o corpus observado, com a limitação registrada em todos os
   derivados.
4. `generate-report` conduz os dois gates editoriais e produz HTML, planilha e
   PDF.

Cada etapa consome somente saídas validadas da anterior. Atualize o manifesto
depois que a etapa responsável gravar e verificar seus artefatos. Se as entradas
e hashes não mudaram, reutilize o checkpoint em vez de repetir a etapa.

## Pausas e falhas

- Peça ao operador que faça login diretamente na plataforma quando a etapa
  detectar sessão ausente ou expirada. Nunca solicite credenciais na conversa.
- Uma publicação com coleta parcial ou indisponível não bloqueia as demais.
  Finalize as demais coletas e grave o diagnóstico. Um pedido explícito para
  analisar ou gerar relatório autoriza o uso do corpus observado; rotule toda
  leitura afetada como referente a esse corpus, nunca ao universo completo.
  Divergência somente com a contagem da Stilingue não é lacuna real e não exige
  esse pedido.
- Um arquivo inválido, checkpoint incoerente ou gate não aprovado impede apenas
  a promoção para a etapa dependente.
- Preserve o corpus de execução incompleta. Exclusão manual exige confirmação e
  deve nomear exatamente a pasta e os arquivos afetados.

## Concluir

Só marque a execução como concluída quando existirem e estiverem reconciliados:

- `deliverables/report.html` aprovado;
- `deliverables/report.pdf` derivado do HTML aprovado;
- `deliverables/analytics.xlsx` com todo o conjunto analítico;
- cobertura e limitações da execução;
- ausência dos corpora temporários completos após análise bem-sucedida.

Apresente os caminhos dos três produtos, período, filtro, canais analisados e
lacunas. Não alegue sucesso para arquivo ausente, gate pendente ou teste não
executado.

## Limites

- Não agendar execuções.
- Não operar outras redes em modo exploratório.
- Não promover análise ou relatório diante de lacuna real de coleta sem pedido
  explícito registrado para usar o corpus observado.
- Não alterar classificações durante a revisão editorial sem retornar à etapa
  de análise e registrar uma nova versão.
- Não publicar ou compartilhar os produtos finais fora da pasta local sem
  autorização explícita.
