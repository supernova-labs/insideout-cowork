# Contrato de feedback local do Mar Aberto

## Destino

Com execução ativa, grave em:

```text
feedback/<timestamp>-<slug>.md
```

Sem execução ativa, peça uma pasta ao operador e grave em:

```text
insideout-mar-aberto-feedback/<timestamp>-<slug>.md
```

Use data e hora no fuso local em `YYYY-MM-DD-HHmm`. O slug descreve o sintoma
sem cliente, campanha, período, publicação ou comentário.

## Cabeçalho e corpo

```markdown
---
feedback_version: 1.0.0
plugin: insideout-mar-aberto
plugin_version: <versão ou desconhecida>
component: <skill ou etapa>
kind: <bug ou enhancement>
fingerprint: <sha256>
created_at: <ISO-8601>
status: local
---

# <sintoma observável>

## Etapa e caso de uso
<cenário mínimo e anonimizado>

## Comportamento esperado
<resultado verificável>

## Comportamento observado
<diferença factual, sem log cru>

## Impacto
<etapa ou produto final afetado>

## Cobertura e retomada
<estado não sensível relevante ou “não se aplica”>

## Sugestão
<sugestão ou “nenhuma fornecida”>

## Recorrências
- <data e contexto sanitizado da primeira ocorrência>

---
Registrado via `insideout-mar-aberto:skill-feedback`. Nenhuma correção foi
aplicada; a decisão pertence aos mantenedores.
```

## Fingerprint e duplicidade

Calcule SHA-256 sobre a concatenação normalizada de `component`,
`comportamento esperado` e `comportamento observado`. Antes de criar um arquivo,
procure o mesmo fingerprint na pasta de feedback escolhida. Uma repetição usa o
arquivo existente e só acrescenta uma recorrência depois de mostrar a entrada
sanitizada ao operador.

## Sanitização

Remova ou generalize clientes, pessoas, comentários, publicações, URLs,
caminhos, IDs de execução, nomes de arquivo, datas sensíveis, credenciais,
cookies, tokens, stack traces e logs crus. Use `projeto de teste`, `publicação de
exemplo`, `período controlado` ou descrição equivalente.

## Encaminhamento

O arquivo local é a fonte de verdade. Depois de registrá-lo, sugira um e-mail
aos mantenedores sem destinatário hardcoded. Com Gmail nativo disponível e após
aceite da sugestão, confirme destinatários e prepare somente um rascunho. Sem
Gmail, forneça assunto, corpo copiável e caminho do `.md`. O envio exige uma
autorização explícita separada.
