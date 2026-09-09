---
feedback_version: 1.0.0
plugin: insideout-mar-aberto
plugin_version: 0.2.0
component: collect-comments
kind: bug
fingerprint: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
created_at: 2026-09-09T14:00:00-03:00
status: local
---

# Cobertura não avança depois de uma interrupção

## Etapa e caso de uso

Retomada de uma coleta em publicação de exemplo.

## Comportamento esperado

A coleta retoma do último checkpoint sem duplicar registros.

## Comportamento observado

A retomada preserva o checkpoint, mas não volta a carregar itens.

## Impacto

A execução permanece bloqueada na cobertura.

## Cobertura e retomada

Publicação obrigatória parcial, com ponto de retomada preservado.

## Sugestão

Nenhuma fornecida.

## Recorrências

- 2026-09-09 — primeira ocorrência em cenário sintético.

---
Registrado via `insideout-mar-aberto:skill-feedback`. Nenhuma correção foi
aplicada; a decisão pertence aos mantenedores.
