---
name: skill-feedback
description: Registra bugs e melhorias do InsideOut Mar Aberto em relatórios Markdown locais e oferece encaminhamento por e-mail. Use quando alguém relatar falha de exportação, coleta, análise, relatório, retomada ou sugestão sobre este plugin.
---

# Registrar feedback do InsideOut Mar Aberto

Transforme um achado do piloto em um relatório factual, sanitizado e acessível a
qualquer operador, sem exigir GitHub. Esta skill reporta o caso; não aplica
correção nem promete priorização.

## Preparar

1. Leia `references/feedback-contract.md`.
2. Identifique a skill, a etapa e a versão do plugin quando disponíveis.
3. Use a pasta da execução quando existir. Sem execução ativa, peça uma pasta
   local para `insideout-mar-aberto-feedback/`.
4. Não abra o corpus, cookies ou credenciais para enriquecer o relato.

## Tornar o caso reproduzível

Use o que a pessoa já informou e peça apenas contexto mínimo, comportamento
esperado, comportamento observado e impacto. Prefira estado de cobertura,
versão de contrato e etapa a textos de comentários ou dados do cliente.

Calcule o fingerprint definido no contrato e procure relatórios locais com o
mesmo fingerprint. Diante de duplicidade, apresente o caminho existente e não
crie um segundo arquivo; ofereça acrescentar uma recorrência sanitizada.

Classifique como `bug` quando o comportamento contradizer o contrato ou falhar;
use `enhancement` quando ampliar ou melhorar a experiência.

## Registrar localmente

Sanitize a entrada, grave um arquivo por fricção com nome temporal e slug na
pasta `feedback/`, valide o formato e releia o arquivo antes de alegar sucesso.
Mostre caminho, tipo, componente, versão, fingerprint e categorias removidas
sem repetir dados sensíveis.

## Oferecer encaminhamento por e-mail

Depois do registro local, sugira encaminhar o relatório aos mantenedores. O
e-mail não é obrigatório nem dependência do plugin. Se a pessoa aceitar e o
Gmail nativo estiver disponível, confirme os destinatários, apresente a versão
sanitizada e prepare somente um rascunho com o `.md` anexado ou resumido. Sem
Gmail, entregue assunto, corpo copiável e caminho do arquivo. Envie apenas após
autorização explícita em um pedido posterior.

## Limites

- Não editar a instalação ou corrigir o plugin como parte do relato.
- Não exigir conta no GitHub, abrir issue ou pesquisar o repositório.
- Não criar rascunho de e-mail antes de a pessoa aceitar a sugestão e confirmar
  os destinatários; não enviar sem autorização explícita.
- Não incluir cliente, comentário, autor, campanha, URL privada, caminho local,
  ID da execução, credencial, cookie ou log cru.
- Não alegar registro sem reler o arquivo local.
