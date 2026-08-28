---
name: skill-feedback
description: Registra bugs e melhorias das skills do InsideOut Social como issues no repositório de origem, com busca de duplicidade, sanitização e confirmação antes da publicação. Use quando alguém relatar falha, disparo inadequado, saída ruim ou sugestão sobre este plugin.
---

# Registrar feedback do InsideOut Social

Transforme uma observação do time em uma issue factual e segura no repositório
`supernova-labs/insideout-cowork`. Esta skill reporta o problema; não corrige a
instalação local nem promete que a mudança será aceita.

## Preparar

1. Leia `references/issue-contract.md`.
2. Identifique a skill ou, quando isso não for possível, o plugin afetado.
3. Use uma integração autenticada com GitHub disponível na sessão. Se nenhuma
   estiver disponível, continue até produzir o draft e pare antes da publicação.
4. Não abra nem edite arquivos da instalação para aplicar um hotfix.

## Coletar o caso

Use o que a pessoa já informou e pergunte somente pelo que falta para tornar o
report reproduzível:

- skill ou plugin afetado;
- caso de uso e contexto mínimo;
- comportamento esperado;
- comportamento observado;
- impacto;
- sugestão opcional.

Não solicite briefing completo, dados de cliente ou conteúdo privado. Quando um
exemplo real for necessário, peça uma versão anonimizada.

## Verificar antes de propor

1. Pesquise issues abertas e fechadas no repositório por skill, sintoma e
   comportamento esperado.
2. Quando encontrar possível duplicidade, apresente os links e ofereça:
   complementar a existente, preparar uma issue distinta com a diferença ou
   cancelar. Não publique silenciosamente.
3. Classifique como `bug` quando o comportamento contradiz o contrato atual ou
   falha na execução; use `enhancement` para ampliar ou melhorar a experiência.
4. Aplique a lista de sanitização do contrato à entrada e ao draft final.

## Apresentar a prévia

Mostre exatamente:

- repositório de destino;
- label proposta;
- título;
- corpo completo;
- itens removidos ou generalizados por confidencialidade, sem repetir o dado
  sensível.

Peça confirmação explícita para publicar essa versão. Alteração de título,
corpo, label ou destino depois da confirmação exige nova prévia.

## Publicar e verificar

Após a confirmação:

1. crie uma única issue com o payload aprovado;
2. releia a issue criada;
3. confirme título, corpo, label e estado aberto;
4. devolva o link e esclareça que a triagem e a decisão pertencem aos
   mantenedores.

Se a label aprovada não existir, não repita sem ela automaticamente. Apresente
o novo payload sem label e peça confirmação. Se a integração falhar ou não
estiver autenticada, entregue o draft copiável e diga que nada foi publicado.

## Limites

- Não editar a skill instalada nem o cache do plugin.
- Não abrir PR, aplicar correção ou alterar o repositório como parte do report.
- Não publicar sem confirmação do payload final.
- Não expor clientes, briefings, claims não públicos, URLs privadas,
  identificadores internos, credenciais, caminhos locais ou logs crus.
- Não alegar publicação sem reler a issue.
