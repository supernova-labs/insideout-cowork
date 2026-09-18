---
name: analyze-sentiment
description: Analisa automaticamente relevância, alvo, sentimento, temas e amplificação de menções, comentários e respostas do Mar Aberto. Use quando a pessoa quiser processar o corpus completo, retomar a análise ou revisar seus agregados.
---

# Analisar sentimento e temas

Transforme o corpus temporário em dados analíticos anonimizados e agregações
auditáveis. A classificação é integralmente automática; revisão humana pertence
à construção do relatório.

## Preparar

1. Leia `../../references/_shared/analysis-rubric.md`,
   `../../references/_shared/privacy-retention.md` e
   `../../references/_shared/local-state.md`.
2. Valide o manifesto, `working/mentions.jsonl`, `working/comments.jsonl` e a
   cobertura produzida por `collect-comments`.
3. Se todas as publicações com coleta obrigatória estiverem `complete`, inicie a
   análise automaticamente. Divergência exclusiva entre a Stilingue e o corpus
   observado não é lacuna de coleta e não impede essa promoção. Se alguma
   publicação estiver `partial` ou `unavailable`, prossiga somente mediante
   pedido explícito registrado para analisar o corpus observado; nesse modo,
   mantenha a limitação em todos os derivados.
4. Leia `../../references/_shared/schemas/analysis-record.schema.json` e
   `../../references/_shared/schemas/evidence-record.schema.json`.
5. Preserve no checkpoint a versão da rubrica e a identidade do modelo ativo
   quando essa informação estiver disponível.

## Classificar

Para cada menção, comentário ou resposta:

- decida a relevância para Hyundai i20 no mercado brasileiro;
- registre motivo breve para exclusão;
- atribua um ou mais alvos e registre sentimento e confiança para cada alvo,
  sem transferir polaridade entre eles;
- classifique também o sentimento-resumo do registro como positivo, negativo,
  neutro, misto ou ambíguo para a distribuição principal;
- atribua temas normalizados e multirrótulo;
- registre confiança entre 0 e 1;
- preserve curtidas e respostas disponíveis como sinais, não como peso da
  distribuição principal.

Não peça revisão item a item. Casos incertos permanecem ambíguos em vez de
serem forçados para uma classe conclusiva.

## Agregar

Reconcilie todos os registros observados entre relevantes, excluídos e falhas.
Calcule sempre com `source_kind` explícito:

- distribuições de sentimento separadas para menções, comentários e respostas;
- alvos e temas, sem duplicar o denominador de sentimento;
- séries diárias por rede e tipo de fonte;
- amplificação separada por rede e tipo de fonte a partir dos sinais disponíveis;
- cobertura e limitações que condicionam cada leitura.

Quando houver lacuna real de coleta, cada agregado e percentual deve identificar
o corpus observado como denominador e não pode ser apresentado como distribuição
do universo completo de comentários. Uma divergência apenas da Stilingue é
registrada na auditoria, sem trocar esse denominador pelo total da exportação.

Não combine menções e comentários no mesmo denominador nem produza índice único
de engajamento entre plataformas.

## Selecionar evidências

Proponha um pool de trechos integrais anonimizados, estratificado por rede, tipo
de fonte, tema e sentimento. Inclua manifestações recorrentes, marcantes e
contrapontos. Engajamento pode informar a seleção, mas não dominá-la. Marque
todas como `approved: false` até o primeiro gate editorial.

## Persistir e descartar

Grave e valide `analysis/records.jsonl`, `analysis/aggregates.json` e
`analysis/evidence-candidates.jsonl`. Compare suas contagens com o corpus e a
cobertura. Somente depois de todos os artefatos e hashes serem válidos:

1. atualize o checkpoint de análise;
2. remova `working/comments.jsonl` e `working/mentions.jsonl`;
3. releia a pasta para provar que os corpora temporários não permaneceram.

Se a etapa for interrompida antes do checkpoint, preserve o corpus e retome
somente os registros ainda não concluídos.

## Encadear o relatório

Depois de validar o checkpoint de análise, encadeie `generate-report` na mesma
execução, sem exigir um novo pedido da pessoa. A chamada deve consumir somente
os derivados já validados, a cobertura e o pool de evidências candidatas.

Esse encadeamento abre o Gate 1 editorial: apresente as conclusões, a estrutura
e as evidências para decisão humana. Não aprove o gate, não gere HTML, planilha
ou PDF e não altere classificações automaticamente.

## Limites

- Não revisar classificações com uma segunda passagem automática.
- Não analisar uma execução com lacuna real de cobertura sem pedido explícito
  registrado para usar o corpus observado.
- Não mudar a rubrica silenciosamente durante uma execução.
- Não construir a narrativa ou aprovar evidências.
- Não descartar o corpus antes da validação completa dos derivados.
