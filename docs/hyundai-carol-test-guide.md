# Hyundai Social — instalação e primeiro teste

Esta versão 0.1.0 permite testar pesquisa, planejamento e revisão de referências.
É um piloto: o envio ao quadro operacional do Asana aguarda homologação e os
testes da integração. A versão está na branch `codex/hyundai-social-pilot`.

## Acesso à base

Use a conta InsideOut que já acessa **InsideOut Hyundai Social** no Airtable.
Em 16/10/2026, Caroline já consta como proprietária do workspace e herda acesso
à base. Não é preciso criar outra base nem pedir acesso ao Social antigo.

No Codex, conecte o plugin Airtable com essa mesma conta. Se a base Hyundai
não aparecer, revise a autorização de bases na conexão pessoal do Airtable.
O acesso no navegador e a autorização do conector são verificações distintas.
Não compartilhe credenciais nem use a conta de outra pessoa.

## Instalar a versão de piloto

No terminal:

```powershell
codex plugin marketplace add supernova-labs/insideout-cowork --ref codex/hyundai-social-pilot
codex plugin add insideout-hyundai-social@insideout
```

Os comandos usam o catálogo `insideout`. Se ele já estiver cadastrado, confira
que a origem ficou na branch de piloto antes de instalar. Se o aplicativo
continuar mostrando somente a versão anterior, atualize o catálogo e reinicie
o aplicativo. Instale apenas **InsideOut Hyundai Social** para este teste;
os conectores Airtable e de pesquisa também precisam estar disponíveis.

A sintaxe de catálogo e seleção de branch segue a
[documentação oficial do Codex](https://developers.openai.com/plugins/build/plugins).
O plugin não inclui credenciais nem concede acesso a serviços externos.

## Começar em uma conversa nova

Primeiro, peça:

> Quero testar o InsideOut Hyundai Social. Confira se a minha conexão encontra
> a base InsideOut Hyundai Social e suas oito tabelas. Apenas leia; não altere
> dados nem use a base InsideOut Social antiga.

Depois de confirmar o acesso, abra outra conversa limpa para a retrospectiva:

> Usando somente o InsideOut Hyundai Social, faça um piloto retrospectivo de
> setembro de 2026, com data de corte em 31/08/2026. Comece pela pesquisa e use
> as diretrizes fixas da base Hyundai, sem exigir briefing. Não consulte o grid
> histórico esperado. Separe ideias e publicações por rede, reserve espaços
> semanais para influenciadores e declare lacunas de fontes históricas. Apresente
> o take para revisão antes de salvar. Não envie nada ao Asana.

Não forneça o calendário esperado nessa conversa. Ele será usado depois, por
outra pessoa ou em outra conversa, para comparar qualidade editorial.

Para testar persistência, confirme o lote escolhido como Retrospectivo, com
prefixo `[TESTE CODEX]`, e peça releitura e segunda execução sem duplicatas.
Os registros sintéticos de integração já existentes devem ser preservados e
excluídos do repertório editorial.

## Testar a revisão e devolver os resultados

Peça um HTML de ideias e referências com comentários exportáveis. Confira
desktop e celular; crie, edite e remova um comentário, recarregue o arquivo e
exporte o JSON. Devolva esse JSON à conversa que guardou a revisão original.
Comentários pedem ajustes; a confirmação das ideias que seguirão à produção
é uma decisão explícita do time sobre uma versão específica.

Registre o que funcionou, o pedido feito, o resultado esperado e o observado.
Para a avaliação completa, use o [roteiro de homologação](hyundai-pilot-test-protocol.md).

Nesta rodada, não use responsáveis/prazos fictícios no quadro real do Asana.
Regras de contagem, influenciadores, alocação, integração e isolamento entre
equipes continuam pendentes. Não há produção de artes, copy final ou Notion
nesta versão.
