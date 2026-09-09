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

Registre:

- rede e publicação;
- se a coleta é obrigatória;
- contagem informada pela exportação, quando existir;
- contagem informada pela plataforma, quando visível;
- comentários e respostas observados;
- estado `complete`, `partial`, `unavailable`, `not_required` ou `unsupported`;
- evidência de esgotamento observável;
- motivo e último ponto alcançado quando não estiver completo.

O contador da exportação nunca limita a coleta. Contadores da plataforma podem
incluir conteúdo oculto ou removido, mas uma contagem visível maior do que o
total observado impede `complete` enquanto a diferença não for reconciliada.
Não invente registros para fechar a diferença.

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
qualquer publicação obrigatória `partial` ou `unavailable` bloqueia a análise e
gera `coverage/diagnostic.json`. Nesse estado, não apresente nem antecipe
sentimento, temas, percentuais, evidências ou conclusões.

Quando a sessão expirar, preserve o ponto atual, peça novo login e retome sem
duplicar itens.

Antes de persistir, aplique `privacy-retention.md` e valide cada registro pelo
schema correspondente.
