# Contrato do relatório e da planilha

## Gates editoriais

### Gate 1 — direção editorial

Apresente conclusões propostas, estrutura narrativa, limites de cobertura e
pool de evidências. Aguarde aprovação ou ajustes. Não produza o relatório
completo antes desse gate.

### Gate 2 — versão completa

Depois do Gate 1, gere HTML e planilha. Apresente-os para revisão. O PDF é
gerado somente após aprovação do conteúdo completo e deve derivar do mesmo HTML.
Uma alteração editorial não modifica classificações analíticas silenciosamente.

## Núcleo fixo do HTML

O relatório sempre inclui:

1. escopo e recorte;
2. cobertura e lacunas;
3. volume de menções, comentários e respostas;
4. distribuição geral de sentimento por tipo de fonte;
5. recortes de Instagram, YouTube, X/Twitter, Facebook e portais quando houver;
6. séries diárias de sentimento;
7. alvos, temas e termos recorrentes;
8. amplificação por plataforma e tipo de fonte;
9. evidências aprovadas;
10. conclusões e recomendações;
11. metodologia e limitações.

A narrativa pode reordenar conclusões e recomendações conforme a materialidade
dos achados. Lacunas aparecem junto das conclusões afetadas. O HTML é local,
responsivo, autossuficiente e sem chamadas externas. Use a identidade padrão do
plugin quando não houver ativos locais fornecidos pelo cliente.

## Planilha analítica

Gere `analytics.xlsx` com filtros, cabeçalhos congelados e tipos consistentes:

| Aba | Conteúdo |
|---|---|
| `Resumo` | projeto, período, filtro, status, métricas principais e links relativos dos entregáveis |
| `Cobertura` | uma linha por publicação e seu estado de coleta |
| `Publicações` | metadados da exportação Stilingue e URL canônica da publicação |
| `Análises` | uma linha por registro anonimizado, com tipo de fonte e sem texto bruto |
| `Agregações` | distribuições e amplificação separadas por plataforma, tipo de fonte e dimensão |
| `Séries diárias` | totais e percentuais diários por rede, tipo de fonte e sentimento |
| `Evidências` | somente comentários integrais aprovados e anonimizados |
| `Metodologia` | versões de contrato, rubrica, definições e limitações |

Inclua em `Análises`: IDs irreversíveis, publicação, pai opcional, rede, data,
tipo de fonte,
relevância, motivo, alvos, sentimentos por alvo, sentimento-resumo, temas,
confiança, curtidas e respostas. Não inclua autor, perfil, foto ou link
individual.

## Reconciliação

Antes da entrega, prove que:

- linhas de `Cobertura` reconciliam com as publicações da entrada;
- análises relevantes, excluídas e falhas reconciliam com o universo observado;
- menções, comentários e respostas possuem denominadores independentes;
- cada série diária reconcilia com as análises de sua rede e tipo de fonte;
- totais e percentuais do HTML, da planilha e dos agregados canônicos coincidem;
- `Evidências` coincide com o pool aprovado;
- o PDF não diverge do HTML aprovado.

## Gráficos mínimos

O HTML e o PDF apresentam, para a visão geral e para cada recorte material:

- barras de distribuição de sentimento com total e denominador identificados;
- série diária empilhada a 100% quando houver mais de um dia;
- volume separado de menções, comentários e respostas;
- termos recorrentes em mapa ou lista visual, sem inventar relações semânticas.

O objetivo é reproduzir a arquitetura de informação do relatório de referência,
não copiar sua composição visual pixel a pixel.
