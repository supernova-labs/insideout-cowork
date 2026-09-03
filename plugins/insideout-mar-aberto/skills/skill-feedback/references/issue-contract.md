# Contrato de feedback do Mar Aberto

## Destino e labels

- Repositório: `supernova-labs/insideout-cowork`
- Labels: `bug` ou `enhancement`

## Título

```text
[insideout-mar-aberto/<skill>] <sintoma observável>
```

Não use nome de cliente, campanha, período, publicação ou comentário.

## Corpo

```markdown
## Componente e versão
<plugin/skill e versão quando disponível>

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

---
Registrado via `insideout-mar-aberto:skill-feedback`. Nenhuma correção foi
aplicada; a decisão pertence aos mantenedores.
```

## Sanitização

Remova ou generalize clientes, pessoas, comentários, publicações, URLs,
caminhos, IDs de execução, nomes de arquivo, datas sensíveis, credenciais,
cookies, tokens, stack traces e logs crus. Use `projeto de teste`, `publicação de
exemplo`, `período controlado` ou descrição equivalente.

Uma issue é possível duplicata quando possui o mesmo componente, comportamento
esperado e sintoma, mesmo com outro projeto ou período.
