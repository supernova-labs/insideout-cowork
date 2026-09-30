---
name: generate-report
description: Gera relatório HTML autocontido e planilha analítica do InsideOut Mar Aberto a partir de templates limpos, após um gate editorial. Use quando a análise estiver concluída e a pessoa quiser obter os produtos finais.
---

# Gerar relatório HTML e planilha analítica

Entregue deliverables/report.html e deliverables/analytics.xlsx reconciliados
com a análise validada. A equipe pode corrigir o HTML e exportar um PDF pelo
navegador depois da entrega. O PDF não integra o checkpoint.

## Preparar

1. Leia ../../references/_shared/report-workbook-contract.md,
   ../../references/_shared/privacy-retention.md e
   ../../references/_shared/local-state.md por inteiro. Leia também
   references/html-layout.md para manter a estrutura visual.
2. Abra assets/report-template.html e assets/analytics-template.xlsx.
   Confira assets/template-manifest.json e seus hashes antes da cópia.
   Rejeite modelo ausente, ilegível ou com dado histórico, identidade pessoal,
   comentário, fórmula externa ou vínculo a período antigo. Registre hashes
   SHA-256 e a versão do plugin.
3. Valide o checkpoint de análise, agregações, os dois diagnósticos de cobertura
   e evidências candidatas. Lacuna real não bloqueia a geração por si só;
   divergência exclusiva da Stilingue é ressalva de auditoria.
4. Prepare pauta de panorama, recortes materiais, publicações que concentram
   o sinal, evidências, cobertura, conclusões e metodologia.

## Gate 1 — direção editorial

Apresente conclusões propostas separando fatos, interpretações e limitações;
estrutura narrativa; pool estratificado de evidências integrais anonimizadas; e
lacunas de coleta. Para cada conclusão principal, diga se a lacuna pode mudar
sua leitura. Quando puder, ofereça retomar a coleta ou reformular/omitir a
afirmação; não exija uma aprovação geral de “cobertura limitada”. Registre
aprovações, exclusões e ajustes em
review/editorial-gate-1.json. Aguarde aprovação antes de gerar arquivos.
Afirmações restritas aos registros observados podem seguir; generalizações,
maiorias ou comparações sensíveis a itens inacessíveis precisam ser ajustadas.

## Produzir a partir dos templates

- Copie os dois modelos para templates/ da execução. Trabalhe em arquivos
  temporários e substitua os entregáveis canônicos apenas após validar ambos.
- Preencha somente agregados canônicos e evidências aprovadas. Escape textos
  externos como conteúdo HTML, inclusive citações, títulos e rótulos. Não
  preserve números, textos, gráficos ou comentários históricos.
- Use o HTML modelo para a hierarquia de capa, resumo, página vertical, régua
  azul, destaques ciano, painéis claros, tipografia Inter, rodapé e marcas.
  Mantenha navegação, leitura em tela e composição de impressão de 10 × 13
  polegadas. Substitua a imagem da capa quando projeto ou produto diferir;
  incorpore fontes e imagens autorizadas para que o arquivo funcione sem rede.
- Monte páginas de panorama, canais com dados, séries, cobertura, conclusões,
  metodologia e encerramento. Omita canal sem dados. Acrescente ou divida
  páginas no mesmo estilo quando o conteúdo não couber com legibilidade; não
  reduza a fonte para esconder cortes. O texto permanece selecionável e
  editável no HTML.
- Preserve os cinco sentimentos: positivo, neutro, negativo, misto e
  indefinido. Separe menções, comentários e respostas em totais, percentuais,
  barras e legendas. Exponha o denominador junto a cada gráfico.
- Inclua séries empilhadas a 100% quando houver mais de um dia, temas
  proporcionais sem relações inventadas e publicações de destaque sem
  identidade pessoal. Evidências ilustram achados, não substituem contagens.
- Para um único dia de menções, use distribuição por publicação rotulada como
  tal. Séries de comentários e respostas usam published_at do registro;
  nunca chame essa data de observação nem invente dias vazios.
- Calcule temas por canal a partir dos registros relevantes daquele canal.
  Uma citação precisa estar aprovada, ter sentimento, canal, tipo de fonte e
  alvo corretos e sustentar o assunto. Perguntas neutras e avaliações mistas
  têm seções próprias; elogio à pessoa ou campanha não comprova avaliação do
  veículo.
- Use “recorte monitorado” na capa e “registros observados” nas bases dos
  gráficos. Não repita um selo de “cobertura limitada” em todas as páginas.
  Mostre estados e diferenças de contadores na página de cobertura e na
  metodologia; preencha `{{COUNTER_COMPARISON}}` com a distinção entre Stilingue,
  plataforma e itens observados. Anote lacunas junto às leituras que elas podem
  mudar. Os percentuais sempre descrevem os registros relevantes observados, sem
  projeção para itens não acessados ou para a internet inteira.
- Preencha as oito abas do XLSX conforme o contrato, com datas, números e
  percentuais tipados, filtros e cabeçalhos congelados. Texto integral de
  comentários e respostas entra apenas em Evidências, quando aprovado e
  anonimizado. Amplie tabelas e formatação até a última linha preenchida.
- Em Publicações, preencha por publicação rede, data, link público, ID,
  métricas e cinco contagens de comentários observados. A soma das cinco
  contagens é o total de comentários; respostas têm coluna e denominador
  separados. Reproduza a matriz de sentimento por tipo de fonte no Resumo.
- Em Séries diárias, preencha a série longa e replique os painéis do modelo
  para cada rede com dados. Cada painel traz contagens, percentuais e gráfico
  nativo empilhado a 100% para um tipo de fonte. Preserve cores, legenda e
  eixo percentual; mantenha os cinco nomes de sentimento explícitos nas
  séries, ajuste intervalos e remova gráficos vazios. Rejeite legenda que
  apareça como “Série 1” a “Série 5” na renderização.

## Validar e concluir

Reabra o HTML e o XLSX. Inspecione a estrutura do HTML, os dados visíveis e a
ausência de recursos externos, scripts, conteúdo histórico e identidade
pessoal. Renderize todas as páginas no navegador ou visualizador permitido,
em tela e no modo de impressão; confira contraste, legibilidade, quebras,
gráficos, legendas, citações, rodapé e sobreposições. Compare as páginas
equivalentes à referência visual de 23/09 e ao protótipo HTML aprovado.
Se a renderização estiver indisponível, registre a limitação e não declare a
revisão visual como concluída.

Na planilha, reabra e renderize as oito abas; confira tipos, formatos, filtros
até a última linha e ausência de vínculos antigos. Confirme gráficos
empilhados a 100% com cinco séries e matrizes preenchidas. Reconcilie
contagens e percentuais por rede, tipo de fonte, data e sentimento com os
JSON/JSONL canônicos; confira cobertura, totais por publicação e evidências.
Rejeite divergência, legenda ilegível, mapa sem proporção ou citação em classe
incorreta. Abertura dos arquivos, sem revisão dos conteúdos, não basta.

Só então registre hashes SHA-256 dos dois entregáveis e templates, versão do
plugin e contagens no checkpoint; atualize o manifesto por último. Edição
manual posterior cria versão fora do checkpoint validado. Entregue os dois
caminhos, período, canais, cobertura e limitações. Não abra Gate 2, não gere
PDF automaticamente e não publique nem envie arquivos sem autorização.

## Execuções anteriores

Execuções iniciadas com contratos 2.0.0, 3.0.0 e 4.0.0 mantêm seus checkpoints
e arquivos, sem migração automática. Novas execuções usam contrato 4.1.0.
