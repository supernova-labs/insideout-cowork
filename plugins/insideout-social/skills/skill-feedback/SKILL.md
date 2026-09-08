---
name: skill-feedback
description: Registra bugs e melhorias das skills do InsideOut Social na caixa de entrada do Airtable, com busca de duplicidade, sanitização, prévia e confirmação. Use quando alguém relatar falha, disparo inadequado, saída ruim ou sugestão sobre este plugin.
---

# Registrar feedback do InsideOut Social

Transforme uma observação do time em um registro factual e seguro na base
**InsideOut Social**. Esta skill reporta o problema; não corrige a instalação
local nem promete que a mudança será aceita.

## Preparar

1. Leia `../../references/_shared/airtable-contract.md` e
   `references/feedback-contract.md`.
2. Identifique a skill ou, quando isso não for possível, o plugin afetado.
3. Descubra a base, a tabela `Feedback do plugin` e seus campos atuais.
4. Não abra nem edite arquivos da instalação para aplicar um hotfix.

## Coletar o caso

Use o que a pessoa já informou e pergunte somente pelo que falta para tornar o
relato reproduzível:

- skill ou plugin afetado;
- caso de uso e contexto mínimo;
- comportamento esperado;
- comportamento observado;
- impacto;
- sugestão opcional.

Não solicite briefing completo, dados de cliente ou conteúdo privado. Quando um
exemplo real for necessário, peça uma versão anonimizada.

## Verificar antes de propor

1. Pesquise registros abertos e resolvidos por skill, ação e sintoma.
2. Quando encontrar possível duplicidade, mostre o resumo e o estado e ofereça:
   complementar o contexto existente, criar um registro distinto com a
   diferença ou cancelar. Não escreva silenciosamente.
3. Classifique como `Bug` quando o comportamento contradiz o contrato atual ou
   falha na execução; use `Melhoria` para ampliar ou melhorar a experiência.
4. Aplique a sanitização do contrato à entrada e à prévia final.

## Apresentar a prévia

Mostre exatamente os valores propostos para:

- título;
- tipo;
- skill;
- contexto;
- esperado;
- observado;
- impacto;
- autor, somente quando conhecido com segurança;
- status inicial `Novo`.

Informe o que foi generalizado por confidencialidade sem repetir o dado
sensível. Peça confirmação explícita para registrar essa versão. Qualquer
mudança posterior na prévia exige nova confirmação.

## Registrar e verificar

Após a confirmação:

1. crie um único registro em `Feedback do plugin` com `Status = Novo`;
2. não preencha `Link GitHub`;
3. releia o registro criado;
4. confirme os campos e devolva um resumo em linguagem de negócio.

Se a integração com Airtable estiver indisponível, entregue o mesmo conteúdo em
formato copiável e diga claramente que nada foi registrado. Não peça credencial
nem redirecione a pessoa para criar uma conta no GitHub.

## Limites

- Não criar formulário ou interface para este fluxo; o registro é feito pela
  skill.
- Não editar a skill instalada nem o cache do plugin.
- Não abrir issue, PR ou aplicar correção como parte do relato.
- Não registrar sem confirmação da prévia final.
- Não expor clientes, briefings, claims não públicos, URLs privadas,
  identificadores internos, credenciais, caminhos locais ou logs crus.
- Não alegar sucesso sem reler o registro.
