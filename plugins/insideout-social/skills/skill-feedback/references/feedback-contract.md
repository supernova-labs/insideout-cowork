# Contrato de feedback e sanitização

## Destino

Use a tabela `Feedback do plugin` da base **InsideOut Social**. Ela pode estar
oculta na interface, mas continua disponível às pessoas que usam o plugin e têm
permissão de edição na base. Não crie formulário.

## Título

Use:

```text
[<skill ou plugin>] <resumo observável>
```

Evite nome de cliente, mês de campanha, claim, URL ou trecho de briefing.

## Campos

- `Tipo`: `Bug` ou `Melhoria`;
- `Skill`: nome da skill ou `insideout-social`;
- `Contexto`: cenário mínimo e anonimizado;
- `Esperado`: resultado verificável;
- `Observado`: diferença factual, sem log cru;
- `Impacto`: pessoa, decisão ou etapa afetada;
- `Status`: `Novo` na criação;
- `Link GitHub`: vazio;
- `Autor`: opcional e somente quando conhecido com segurança.

## Sanitização obrigatória

Remova ou generalize antes da prévia final:

- nomes de clientes e pessoas não necessários para reproduzir o comportamento;
- textos de briefing, claims, campanhas ainda não públicas e anexos;
- URLs privadas, links temporários e parâmetros de acesso;
- identificadores de base, tabela, campo, registro ou tarefa;
- tokens, credenciais, endereços de email e dados pessoais;
- caminhos locais, nomes de usuário, stack traces e logs crus.

Substitua por termos como `marca de teste`, `post de exemplo`, `mês de teste`
ou uma descrição curta do sintoma. Diga que houve sanitização sem revelar o que
foi removido.

## Busca de duplicidade

Pesquise combinações do componente, ação e sintoma em todos os estados. Um
registro é possível duplicidade quando descreve o mesmo esperado e observado,
mesmo que o exemplo seja diferente. Um item `Resolvido` continua relevante para
saber se houve correção anterior; não o reabra ou altere sem nova confirmação.

## Fallback copiável

Quando o Airtable estiver indisponível, entregue título e todos os campos acima
em um bloco copiável. Identifique `não registrado` e preserve a sanitização.
