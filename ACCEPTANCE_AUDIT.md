# Auditoria de aceitação — frentes do fluxo de Grid

Data da execução: 2026-08-27/28
Versão candidata: `insideout-social` 0.2.0
Escopo: implementação das cinco frentes aprovadas; o piloto com Carol continua
como gate empírico separado.

## 1. Skill de feedback

### Implementado

- sexta skill distribuída, com metadata Codex e contrato de issue;
- classificação `bug`/`enhancement`, busca de duplicidade, sanitização, prévia
  completa e confirmação obrigatória;
- releitura após publicação e fallback copiável quando GitHub não estiver
  autenticado;
- cinco evals: bug sanitizado, melhoria, duplicidade/cancelamento, fallback e
  publicação verificada.

### Evidência

- autenticação do GitHub confirmada para o repositório de origem;
- labels `bug` e `enhancement` confirmadas;
- busca de duplicidade do cenário de harness retornou zero resultados;
- a issue de teste
  [`#30`](https://github.com/supernova-labs/insideout-cowork/issues/30) foi
  publicada com o payload aprovado, relida em estado aberto e encerrada como
  teste concluído;
- validações estruturais da skill aprovadas.

## 2. Canais e diretrizes por marca

### Implementado

- tabela `Canais da marca` com marca, rede, status, objetivo editorial,
  orientações e formatos habilitados;
- relação `Canal da marca` e campo `Briefing de design` em `Posts`;
- chave natural por marca e rede para canais e por marca, canal, data e título
  para posts;
- configuração pertence a `analyze-briefing`; `generate-grid` usa somente
  canais ativos e formatos habilitados.

### Evidência viva

- dois canais de harness criados para `[TESTE CODEX] Aurora Skin`: Instagram
  com Feed/Story/Reel e LinkedIn com Feed;
- releitura confirmou fórmula de nome, uma marca, status ativo, objetivo,
  orientação e formatos;
- segunda resolução encontrou exatamente um registro por chave e criou zero
  duplicatas.

## 3. Primeiro take orquestrado

### Implementado

- `generate-grid` compõe estrutura, rationale e briefing de design;
- `generate-copy` produz lettering e legenda antes da aprovação e escreve
  somente seus dois campos depois que o grid persiste os posts aprovados;
- aprovação em lote aceita exceções por post;
- a apresentação reúne os componentes no formato familiar da designer, embora
  o estado permaneça separado por responsabilidade.

### Evidência viva

- dois posts de harness com mesmo título e data foram criados, um para
  Instagram e outro para LinkedIn;
- a primeira escrita continha apenas estrutura, relações, rationale, briefing e
  status `Rascunho`;
- a segunda escrita alterou somente `Lettering` e `Legenda`, com linguagem e CTA
  distintos por rede;
- releitura confirmou relações, briefings, textos, status e ausência de mídia;
- nova resolução encontrou os dois registros existentes pela chave com rede e
  criou zero duplicatas.

## 4. Tendências como contexto curado

### Implementado

- fontes classificadas como permanentes, temporárias ou candidatas;
- cada candidato registra fonte, rede, captura, evidência, relevância, validade
  e autorização;
- candidato pendente, vencido ou indisponível não influencia o primeiro take;
- somente o uso aprovado entra no rationale do post compatível.

### Evidência

- eval cobre candidato pendente, aprovação, rede compatível, expiração e fonte
  indisponível;
- nenhuma tabela, campo ou registro de tendência foi criado no Airtable.

## 5. Snapshot HTML

### Implementado

- snapshot autossuficiente fora do pacote do plugin, com CSS e filtro local;
- cabeçalho com marca, mês, versão, estado e distribuição;
- três posts com rationale, briefing, lettering, legenda, tendência/lacuna e
  estado de revisão;
- nenhuma chamada externa, formulário ou persistência.

### Evidência técnica e visual

- arquivo servido localmente e inspecionado no navegador em desktop e viewport
  de 360 px;
- três cards preservados, sem rolagem horizontal e com controles de pelo menos
  42 px de altura;
- filtro de LinkedIn exibiu um post e a opção "Todos" restaurou os três;
- inspeção estática encontrou zero URL/chamada externa e zero identificador
  interno do Airtable.

- abertura por duplo clique, sem servidor, confirmada manualmente pelo usuário
  em 2026-08-28. O ambiente automatizado bloqueou `file://` por política de
  segurança, por isso essa evidência humana complementa o teste visual e a
  inspeção estrutural.

Artefato local: `artifacts/insideout-grid-aurora-skin-2026-05-v1.html`.

## Validações do pacote

- validador compartilhado das skills: aprovado para seis skills;
- Agent Smith: repositório e índice aprovados;
- `quick_validate.py`: seis skills aprovadas;
- verificação de whitespace/diff: aprovada;
- manifesto atualizado para 0.2.0, README, catálogo arquitetural e índice em
  sincronia.

## Estado da liberação

As cinco frentes e seus critérios de aceitação de construção estão concluídos.
A liberação para todo o time continua condicionada ao teste com Carol e à
decisão de liberar, iterar ou interromper registrada no gate do piloto; esse
gate é empírico e não altera a conclusão desta implementação.
