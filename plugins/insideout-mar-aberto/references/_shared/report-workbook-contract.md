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

## Arquitetura editorial do relatório

O relatório deve tornar a análise legível como uma história de conversa, e não
apenas como uma sequência de tabelas. A referência editorial do Mar Aberto usa
uma progressão de panorama para explicação: visão geral, recortes materiais,
conteúdos que concentram a conversa e evidências. Adapte a ordem à
materialidade, sem copiar uma composição visual de cliente e sem ocultar
limitações de cobertura.

Cada página ou seção material deve ter um título claro, período e fonte dos
dados. Use o padrão visual InsideOut do asset da skill: hierarquia tipográfica,
régua de destaque, cores de sentimento consistentes e espaço suficiente para
a leitura. Dados têm precedência sobre decoração.

### Abertura e panorama

Abra com escopo, período, cobertura e uma tese curta, sempre qualificada pelo
corpus observado quando necessário. O panorama deve combinar:

- distribuição de sentimento, com total e denominador identificados;
- volume separado de menções, comentários e respostas;
- termos recorrentes em mapa ou lista visual ponderada, sem sugerir relações
  semânticas que os agregados não provam;
- leitura de positivo, neutro e negativo, distinguindo fatos dos achados
  interpretativos;
- fonte, período e limitações perto dos números a que se aplicam.

### Recortes por canal e tipo de fonte

Para cada canal material, apresente a distribuição de sentimento, volumes e
termos próprios. Quando posts, comentários e respostas tiverem composição
distinta, mostre-os separadamente e explique a diferença sem misturar seus
denominadores. Recortes pouco materiais podem permanecer em uma síntese
comparativa, mas não podem desaparecer quando mudarem a conclusão geral.

Inclua a série diária empilhada a 100% quando houver mais de um dia e mantenha
os rótulos de cobertura ao lado de qualquer recorte afetado. Use gráficos para
comparação e texto para explicar o que puxou o resultado.

### Conteúdos e evidências em destaque

Quando a amplificação estiver concentrada, destaque as publicações que mais
contribuíram para volume ou sinal, usando identificadores de publicação,
plataforma, métricas agregadas e o mecanismo observado. Não apresente nome,
perfil, foto ou link individual de pessoa. Relacione esse destaque à tese do
canal, sem atribuir causalidade além do que os dados permitem.

Apresente evidências aprovadas em cartões de citação separados por sentimento
ou papel analítico. Cada cartão mostra texto anonimizado, sentimento, canal e
temas. Evidências ilustram um achado; não substituem distribuição nem são
tratadas como amostra estatística.

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

Quando `coverage_mode` for `limited_approved`, o título, o resumo, os recortes
e a metodologia identificam “cobertura limitada” e nomeiam as lacunas. Totais e
percentuais continuam reconciliados com o corpus observado, mas não são
apresentados como estimativa ou distribuição do universo completo.

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
