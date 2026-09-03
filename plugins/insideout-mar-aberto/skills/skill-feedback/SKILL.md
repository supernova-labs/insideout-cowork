---
name: skill-feedback
description: Registra bugs e melhorias do InsideOut Mar Aberto como issues sanitizadas no repositório de origem. Use quando alguém relatar falha de exportação, coleta, análise, relatório, retomada ou sugestão sobre este plugin.
---

# Registrar feedback do InsideOut Mar Aberto

Transforme um achado do piloto em uma issue factual e segura no repositório
`supernova-labs/insideout-cowork`. Esta skill reporta o caso; não aplica correção
nem promete priorização.

## Preparar

1. Leia `references/issue-contract.md`.
2. Identifique a skill, a etapa e a versão do plugin quando disponíveis.
3. Use uma integração autenticada com GitHub se estiver disponível. Sem ela,
   continue até o draft e pare antes da publicação.
4. Não abra o corpus, cookies ou credenciais para enriquecer o relato.

## Tornar o caso reproduzível

Use o que a pessoa já informou e peça apenas contexto mínimo, comportamento
esperado, comportamento observado e impacto. Prefira estado de cobertura,
versão de contrato e etapa a textos de comentários ou dados do cliente.

Pesquise issues abertas e fechadas por componente, ação e sintoma. Diante de
possível duplicidade, apresente os links e peça uma escolha entre complementar,
criar uma issue distinta ou cancelar.

Classifique como `bug` quando o comportamento contradizer o contrato ou falhar;
use `enhancement` quando ampliar ou melhorar a experiência.

## Apresentar e confirmar

Sanitize a entrada e mostre exatamente repositório, label, título e corpo
completos, além das categorias generalizadas por confidencialidade sem repetir
o dado removido. Peça confirmação explícita. Qualquer alteração posterior no
payload exige nova prévia.

## Publicar e verificar

Após confirmação, crie uma única issue, releia título, corpo, label e estado e
devolva o link. Se a label não existir, apresente o payload revisado sem ela e
peça nova confirmação. Se a integração falhar, entregue o draft copiável e
declare que nada foi publicado.

## Limites

- Não editar a instalação ou corrigir o plugin como parte do relato.
- Não abrir PR nem publicar sem confirmação.
- Não incluir cliente, comentário, autor, campanha, URL privada, caminho local,
  ID da execução, credencial, cookie ou log cru.
- Não alegar publicação sem reler a issue.
