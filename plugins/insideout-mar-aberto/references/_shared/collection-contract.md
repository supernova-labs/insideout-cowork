# Contrato de coleta observável

## Matriz de canais

- Instagram e YouTube: suportados no MVP.
- Qualquer outra rede: não coletar; registrar quantidade e nome na cobertura.

Valide a sessão de uma rede somente quando a exportação contiver publicações
dela. O login pertence ao operador e acontece diretamente no navegador. Não
solicite nem armazene senha, segundo fator ou cookie.

## Cobertura por publicação

Abra cada URL canônica uma vez. Percorra a paginação ou rolagem do contêiner de
comentários, expanda respostas acessíveis e encerre quando duas inspeções
consecutivas, após uma tentativa real de carregar mais, não acrescentarem
comentários ou respostas e não houver controle de continuação disponível.

Registre:

- rede e publicação;
- contagem informada pela plataforma, quando visível;
- comentários e respostas observados;
- estado `complete`, `partial`, `unavailable` ou `unsupported`;
- motivo e último ponto alcançado quando não estiver completo.

Contadores podem incluir conteúdo oculto ou removido. Divergência entre contador
e observado é uma lacuna a reportar, não autorização para inventar registros.

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
interrompe as demais. Grave o checkpoint após cada publicação. Quando a sessão
expirar, preserve o ponto atual, peça novo login e retome sem duplicar itens.

Antes de persistir, aplique `privacy-retention.md` e valide cada registro pelo
schema correspondente.
