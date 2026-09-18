---
name: collect-comments
description: Coleta comentários e respostas observáveis de publicações do Instagram e YouTube exportadas pela Stilingue. Use quando a pessoa quiser coletar, retomar ou auditar a cobertura de uma execução de Mar Aberto.
---

# Coletar todos os comentários observáveis

Percorra todas as publicações suportadas e produza um corpus temporário
anonimizado com cobertura verificável. Uma falha isolada não interrompe as
demais publicações, mas pausa a promoção automática para análise até haver
retomada ou pedido explícito para analisar o corpus observado.

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
5. Transforme a lista canônica em uma fila de publicações. Uma coleta só pode
   encerrar quando toda publicação obrigatória tiver um checkpoint de cobertura;
   em períodos longos, preserve o ponto da fila e retome as pendentes em vez de
   reduzir o escopo ou concluir por amostragem.

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

Enquanto houver painel rolável, controle de carregar mais ou respostas
expansíveis, continue no contêiner de comentários. Tempo decorrido, recorte
longo ou uma contagem externa divergente não são motivo para encerrar a
publicação como `partial`: preserve o ponto como retomável se a sessão precisar
ser interrompida. Use `partial` somente depois de uma falha observável de
continuação e registre a tentativa e o último ponto alcançado.

Conte comentários principais e respostas separadamente. Preserve separadamente
o contador da exportação e o contador visível na plataforma. O primeiro nunca
limita a coleta nem é copiado como contador da plataforma. Se a plataforma
mostrar mais itens do que os observados, a publicação não pode ser marcada como
`complete` sem reconciliação verificável. Uma divergência apenas do contador da
Stilingue é uma limitação auditável, não uma falha de cobertura, quando o
esgotamento observável foi comprovado.

## Leitura por plataforma

### Instagram

- Acione o painel de comentários e releia a interface antes de concluir que ele
  não abriu: em Reels o painel pode surgir com atraso.
- Role o painel lateral de comentários, não a página do Reel. A chegada ao fim
  do painel só vale como evidência depois de uma nova tentativa de rolagem sem
  novos itens.
- Expanda cada controle de respostas, como `Ver todas as N respostas`, e grave
  a relação entre comentário principal e resposta.
- Reconcilie o contador visível usando itens efetivamente expostos. Ele pode
  incluir respostas aninhadas e, quando a interface os indicar, comentários de
  outra superfície Meta, como Facebook. Registre essa composição na evidência;
  não presuma que o contador representa apenas comentários principais.

### YouTube

- Mantenha a publicação original estável durante a coleta. Pause o vídeo ou
  confirme que ele não está prestes a terminar; não use `End` com o player em
  foco, pois a reprodução automática pode navegar para outro vídeo.
- Role progressivamente da descrição e de painéis intermediários, como
  `Perguntas`, até a seção de comentários. Ver apenas o título `Comentários`
  ou cartões de carregamento não confirma que os itens foram obtidos: continue
  a rolagem e releia até surgirem cartões de comentário.
- Depois que o primeiro lote aparecer, continue a rolagem da página para pedir
  lotes adicionais. Expanda todos os botões `N resposta(s)` acessíveis e conte
  comentários principais e respostas separadamente.
- Se a seção permanecer apenas com cartões de carregamento, tente uma
  rolagem real que mantenha a área visível e reobserve. Só registre `partial`
  após uma falha observável de continuação, nunca por ver somente o cabeçalho.
- Trate o total mostrado pelo YouTube como sinal de reconciliação, não como
  definição de qual tipo de item ele conta. Preserve toda diferença que reste
  após o esgotamento observável.

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
redes somente de menções, redes não suportadas e lacunas. Quando as publicações
obrigatórias estiverem `complete`, a próxima etapa pode analisar o corpus mesmo
que suas contagens divirjam da Stilingue. Se qualquer publicação obrigatória
estiver `partial` ou `unavailable`, grave `coverage/diagnostic.json`, marque a
execução como `blocked_coverage` e indique o ponto de retomada. A etapa seguinte
pode prosseguir com o corpus observado mediante pedido explícito da pessoa;
esta skill não decide nem produz a leitura de sentimento.

Antes de encerrar, reconcilie a fila canônica com os checkpoints: cada URL
obrigatória precisa estar `complete`, `partial` ou `unavailable`; ausência de
checkpoint nunca equivale a cobertura concluída. Um recorte longo pode exigir
retomadas, mas não permite analisar apenas os primeiros lotes acessíveis.

## Limites

- Não classificar sentimento nesta skill.
- Não guardar autor, perfil, foto, URL individual ou cookie.
- Não apagar o corpus: o descarte pertence à análise concluída ou à exclusão
  manual confirmada.
- Não tentar redes não suportadas em caráter exploratório.
