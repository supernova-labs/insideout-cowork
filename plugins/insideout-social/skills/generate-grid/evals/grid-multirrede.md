# Eval — grid multirrede

## Prompt

> Monte dois posts para a mesma ideia e data da `[TESTE CODEX] Aurora Skin`:
> Instagram Feed e LinkedIn Feed. Use os canais ativos e preserve intenção
> própria por rede.

## Resultado esperado

- resolve exatamente um canal ativo para cada rede;
- valida que Feed está habilitado nos dois canais;
- cria propostas separadas e adaptadas, não um post multirrede;
- apresenta cada proposta no formato familiar da designer: referências,
  produtos/assets, lettering por tela e orientações de produção reunidos;
- usa `Marca + Canal da marca + Data + Título` para idempotência;
- uma reexecução encontra cada post correto e cria zero duplicatas;
- canal duplicado, inativo ou com formato não habilitado bloqueia apenas o post
  afetado e apresenta o conflito.
