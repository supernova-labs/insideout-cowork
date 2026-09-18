# Contrato de coleta observável

## Matriz de canais e fontes

- Instagram e YouTube: menções analisadas e comentários coletados.
- X/Twitter, Facebook e portais: menções analisadas; coleta de comentários não
  requerida nesta versão.
- Qualquer outra rede: não analisar nem coletar; registrar quantidade e nome.

Valide a sessão de uma rede somente quando a exportação contiver publicações
dela. O login pertence ao operador e acontece diretamente no navegador. Não
solicite nem armazene senha, segundo fator ou cookie.

## Cobertura por publicação

Abra cada URL canônica uma vez. Percorra a paginação ou rolagem do contêiner de
comentários, expanda respostas acessíveis e encerre quando duas inspeções
consecutivas, após uma tentativa real de carregar mais, não acrescentarem
comentários ou respostas e não houver controle de continuação disponível.
Enquanto houver painel rolável, controle de continuação ou resposta expansível,
a publicação permanece em coleta. Duração do recorte, tempo da sessão e número
de publicações restantes orientam uma retomada com checkpoint; não justificam
classificar uma coleta incompleta como `partial`.

Registre:

- rede e publicação;
- se a coleta é obrigatória;
- contagem informada pela exportação, quando existir;
- contagem informada pela plataforma, quando visível;
- comentários e respostas observados;
- estado `complete`, `partial`, `unavailable`, `not_required` ou `unsupported`;
- evidência de esgotamento observável;
- motivo e último ponto alcançado quando não estiver completo.

O contador da exportação nunca limita a coleta e não deve ser tratado como o
contador visível da plataforma. Uma divergência entre a Stilingue e os itens
observados é registrada como limitação de auditoria, mas não impede `complete`
quando o esgotamento observável foi comprovado. Contadores visíveis da
plataforma podem incluir conteúdo oculto ou removido; se forem maiores que o
total observado, impedem `complete` enquanto a diferença não for reconciliada.
Não invente registros para fechar nenhuma diferença.

## Fila completa em recortes longos

Monte a fila a partir de todas as URLs canônicas obrigatórias e registre um
checkpoint ao terminar cada publicação. Antes de promover a coleta, reconcilie
a fila com `coverage/records.jsonl`: toda publicação obrigatória precisa ter um
estado explícito. Se a execução for interrompida por duração ou limite da
sessão, ela permanece retomável a partir da próxima publicação pendente; não
reduza o recorte, não use amostra e não apresente cobertura completa.

## Particularidades observadas

### Instagram

Abra o painel de comentários da publicação, role o contêiner do painel em vez da
página principal e expanda controles de respostas. Releia o total observado a
cada ciclo para provar progresso.

### YouTube

Role até a seção de comentários, carregue lotes adicionais e expanda respostas.
Comentários fixados continuam sendo comentários normais para deduplicação.

## Falha e retomada

Uma publicação privada, removida, indisponível ou com falha de interface não
interrompe as demais. Grave o checkpoint após cada publicação. Ao final, porém,
qualquer publicação obrigatória `partial` ou `unavailable` gera
`coverage/diagnostic.json` e pausa a promoção automática para análise. A pessoa
pode retomar a coleta ou pedir explicitamente análise e relatório do corpus
observado. Sem esse pedido, não apresente sentimento, temas, percentuais,
evidências ou conclusões. Com ele, a análise pode processar apenas o corpus
observado e precisa carregar a lacuna real em todos os derivados. Divergência
apenas entre a Stilingue e o corpus observável não gera essa pausa.

Quando a sessão expirar, preserve o ponto atual, peça novo login e retome sem
duplicar itens.

Antes de persistir, aplique `privacy-retention.md` e valide cada registro pelo
schema correspondente.
