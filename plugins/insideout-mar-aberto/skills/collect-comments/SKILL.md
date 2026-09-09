---
name: collect-comments
description: Coleta comentários e respostas observáveis de publicações do Instagram e YouTube exportadas pela Stilingue. Use quando a pessoa quiser coletar, retomar ou auditar a cobertura de uma execução de Mar Aberto.
---

# Coletar todos os comentários observáveis

Percorra todas as publicações suportadas e produza um corpus temporário
anonimizado com cobertura verificável. Uma falha isolada não interrompe as
demais publicações, mas impede a promoção para análise até ser resolvida.

## Preparar

1. Leia `../../references/_shared/collection-contract.md`,
   `../../references/_shared/privacy-retention.md` e
   `../../references/_shared/local-state.md`.
2. Exija um checkpoint válido de `export-stilingue` e releia a lista canônica de
   publicações.
3. Leia `../../references/_shared/schemas/source-record.schema.json` e
   `../../references/_shared/schemas/coverage-record.schema.json` para os
   registros produzidos nesta etapa.
4. Verifique login apenas para as redes suportadas presentes na exportação. O
   operador entra diretamente na plataforma.

## Coletar por publicação

Para cada URL de Instagram ou YouTube:

1. abra a publicação e confirme que ela corresponde à rede esperada;
2. percorra o contêiner de comentários até o esgotamento observável definido no
   contrato;
3. expanda respostas acessíveis e preserve a relação pai–resposta;
4. normalize o texto e os sinais de engajamento disponíveis;
5. remova identidade antes de persistir e gere IDs irreversíveis;
6. deduplique o item dentro da publicação;
7. grave o checkpoint da publicação antes de seguir.

Conte comentários principais e respostas separadamente. Preserve separadamente
o contador da exportação e o contador visível na plataforma. O primeiro nunca
limita a coleta. Se a plataforma mostrar mais itens do que os observados, a
publicação não pode ser marcada como `complete` sem reconciliação verificável.

## Tratar exceções

- `complete`: percurso observável esgotado.
- `partial`: houve progresso, mas a continuação falhou.
- `unavailable`: conteúdo privado, removido ou inacessível.
- `not_required`: canal cuja menção será analisada, mas que não exige coleta de
  comentários nesta versão; não abrir para coleta.
- `unsupported`: rede fora da matriz analítica; não abrir para coleta.

Se a sessão expirar, preserve a publicação atual, solicite novo login e retome.
Uma segunda execução usa IDs e checkpoints para não duplicar o que já foi
coletado.

## Entregar

Produza `working/comments.jsonl` e `coverage/records.jsonl`, valide as contagens
e atualize o manifesto. Informe publicações por estado, comentários, respostas,
redes somente de menções, redes não suportadas e lacunas. Se qualquer publicação
com coleta obrigatória estiver `partial` ou `unavailable`, grave
`coverage/diagnostic.json`, marque a execução como `blocked_coverage` e indique
o ponto de retomada. Não apresente nenhuma leitura de sentimento.

## Limites

- Não classificar sentimento nesta skill.
- Não guardar autor, perfil, foto, URL individual ou cookie.
- Não apagar o corpus: o descarte pertence à análise concluída ou à exclusão
  manual confirmada.
- Não tentar redes não suportadas em caráter exploratório.
