---
name: analyze-sentiment
description: Analisa automaticamente relevância, alvo, sentimento, temas e amplificação dos comentários coletados no Mar Aberto. Use quando a pessoa quiser processar o corpus, retomar a análise ou revisar seus agregados.
---

# Analisar sentimento e temas

Transforme o corpus temporário em dados analíticos anonimizados e agregações
auditáveis. A classificação é integralmente automática; revisão humana pertence
à construção do relatório.

## Preparar

1. Leia `../../references/_shared/analysis-rubric.md`,
   `../../references/_shared/privacy-retention.md` e
   `../../references/_shared/local-state.md`.
2. Valide o manifesto, `working/comments.jsonl` e a cobertura produzida por
   `collect-comments`.
3. Leia `../../references/_shared/schemas/analysis-record.schema.json` e
   `../../references/_shared/schemas/evidence-record.schema.json`.
4. Preserve no checkpoint a versão da rubrica e a identidade do modelo ativo
   quando essa informação estiver disponível.

## Classificar

Para cada comentário ou resposta:

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
Calcule:

- distribuição de sentimento com uma unidade por registro relevante;
- alvos e temas, sem duplicar o denominador de sentimento;
- amplificação separada por Instagram e YouTube a partir dos sinais disponíveis;
- cobertura e limitações que condicionam cada leitura.

Não produza índice único que combine engajamento bruto entre plataformas.

## Selecionar evidências

Proponha um pool de comentários integrais anonimizados, estratificado por rede,
tema e sentimento. Inclua manifestações recorrentes, marcantes e contrapontos.
Engajamento pode informar a seleção, mas não dominá-la. Marque todas como
`approved: false` até o primeiro gate editorial.

## Persistir e descartar

Grave e valide `analysis/records.jsonl`, `analysis/aggregates.json` e
`analysis/evidence-candidates.jsonl`. Compare suas contagens com o corpus e a
cobertura. Somente depois de todos os artefatos e hashes serem válidos:

1. atualize o checkpoint de análise;
2. remova `working/comments.jsonl`;
3. releia a pasta para provar que o corpus bruto não permaneceu.

Se a etapa for interrompida antes do checkpoint, preserve o corpus e retome
somente os registros ainda não concluídos.

## Limites

- Não revisar classificações com uma segunda passagem automática.
- Não mudar a rubrica silenciosamente durante uma execução.
- Não construir a narrativa ou aprovar evidências.
- Não descartar o corpus antes da validação completa dos derivados.
