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
3. volume observado;
4. distribuição de sentimento;
5. alvos e temas;
6. amplificação por plataforma;
7. evidências aprovadas;
8. conclusões e recomendações;
9. metodologia e limitações.

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
| `Análises` | uma linha por registro anonimizado, sem texto bruto |
| `Agregações` | distribuições e amplificação separadas por plataforma e dimensão |
| `Evidências` | somente comentários integrais aprovados e anonimizados |
| `Metodologia` | versões de contrato, rubrica, definições e limitações |

Inclua em `Análises`: IDs irreversíveis, publicação, pai opcional, rede,
relevância, motivo, alvos, sentimentos por alvo, sentimento-resumo, temas,
confiança, curtidas e respostas. Não inclua autor, perfil, foto ou link
individual.

## Reconciliação

Antes da entrega, prove que:

- linhas de `Cobertura` reconciliam com as publicações da entrada;
- análises relevantes, excluídas e falhas reconciliam com o universo observado;
- totais e percentuais do HTML, da planilha e dos agregados canônicos coincidem;
- `Evidências` coincide com o pool aprovado;
- o PDF não diverge do HTML aprovado.
