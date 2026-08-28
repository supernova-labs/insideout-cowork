# Contrato de issue e sanitização

## Destino e labels

- Repositório: `supernova-labs/insideout-cowork`
- Labels do MVP: `bug` e `enhancement`

## Título

Use:

```text
[<skill ou plugin>] <resumo observável>
```

Evite nome de cliente, mês de campanha, claim, URL ou trecho de briefing.

## Corpo

```markdown
## Componente afetado
<skill ou plugin>

## Caso de uso
<cenário mínimo e anonimizado>

## Comportamento esperado
<resultado verificável>

## Comportamento observado
<diferença factual, sem log cru>

## Impacto
<quem ou qual etapa é afetada>

## Sugestão
<sugestão ou “nenhuma fornecida”>

---
Registrado via `skill-feedback`. Nenhuma correção foi aplicada; a decisão
pertence aos mantenedores do plugin.
```

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

Pesquise combinações do componente, ação e sintoma. Uma issue é possível
duplicidade quando descreve o mesmo comportamento esperado e observado, mesmo
que o exemplo seja diferente. Uma issue fechada continua relevante para saber
se houve correção ou decisão anterior.
