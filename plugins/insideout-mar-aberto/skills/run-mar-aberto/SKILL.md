---
name: run-mar-aberto
description: Conduz ou retoma o fluxo completo de Mar Aberto da InsideOut, da exportação Stilingue aos relatórios e planilha. Use quando a pessoa pedir uma análise de mar aberto, uma leitura do i20 ou a continuação de uma execução existente.
---

# Executar o InsideOut Mar Aberto

Conduza uma execução sob demanda sem exigir que a pessoa coordene manualmente
as etapas especializadas. Preserve checkpoints e pare somente para login,
correção de contrato ou gates editoriais.

## Preparar

1. Leia `../../references/_shared/about-mar-aberto.md` e
   `../../references/_shared/local-state.md`.
2. Para uma execução nova, confirme projeto, filtro, data inicial, data final e
   pasta local. Use `nova busca i20` como proposta do piloto, nunca como escolha
   silenciosa.
3. Para uma retomada, abra `manifest.json`, valide caminhos e hashes e apresente
   etapa concluída, lacunas e próximo passo.
4. Não misture execuções nem grave estado dentro do diretório do plugin.

## Orquestrar

Avance nesta ordem:

1. `export-stilingue` obtém ou valida a planilha oficial e fecha o checkpoint de
   entrada.
2. `collect-comments` percorre Instagram e YouTube, preserva o corpus temporário
   anonimizado e registra cobertura.
3. `analyze-sentiment` produz os dados derivados e o pool de evidências e remove
   o corpus bruto somente após validar o checkpoint.
4. `generate-report` conduz os dois gates editoriais e produz HTML, planilha e
   PDF.

Cada etapa consome somente saídas validadas da anterior. Atualize o manifesto
depois que a etapa responsável gravar e verificar seus artefatos. Se as entradas
e hashes não mudaram, reutilize o checkpoint em vez de repetir a etapa.

## Pausas e falhas

- Peça ao operador que faça login diretamente na plataforma quando a etapa
  detectar sessão ausente ou expirada. Nunca solicite credenciais na conversa.
- Uma publicação com coleta parcial ou indisponível não bloqueia as demais;
  carregue a lacuna até a análise e os produtos finais.
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
- ausência do corpus bruto completo após análise bem-sucedida.

Apresente os caminhos dos três produtos, período, filtro, canais analisados e
lacunas. Não alegue sucesso para arquivo ausente, gate pendente ou teste não
executado.

## Limites

- Não agendar execuções.
- Não operar outras redes em modo exploratório.
- Não alterar classificações durante a revisão editorial sem retornar à etapa
  de análise e registrar uma nova versão.
- Não publicar ou compartilhar os produtos finais fora da pasta local sem
  autorização explícita.
