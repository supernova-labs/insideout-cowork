# Parte 1 — relatório de implementação e validação

> **Data:** 26/07/2026  
> **Resultado:** aprovado para uso experimental no repositório  
> **Distribuição:** ainda fora de escopo

## O que foi implementado

- `analyze-briefing`, com confirmação de entendimento, análise
  Produto × Timing × Execução, validação de escopo e materialização opcional de
  marca e produto;
- `generate-grid`, com auditoria do mês, primeiro take sujeito a aprovação,
  escrita em lotes, rationale e idempotência;
- contrato compartilhado das tabelas `Marcas`, `Produtos`, `Referências`,
  `Posts` e `Peças`;
- referências de marca, calendário e método editorial;
- três evals por skill e um eval compartilhado de resposta sem IDs;
- validador determinístico da Parte 1;
- descoberta pelo Codex por links em `.agents/skills`, mantendo
  `.codex/skills` como fonte experimental solicitada para este ciclo.

## Tarefas isoladas executadas

| Tarefa | Resultado |
|---|---|
| Smoke test do briefing | Skill descoberta; todos os critérios passaram; o fixture foi ajustado para representar as duas etapas da conversa |
| Acionamento por linguagem natural | Pedido “analise este briefing” selecionou `analyze-briefing` sem o nome da skill no prompt e aguardou o “OK” |
| Marcas | 1 marca criada; segunda execução reutilizou o mesmo registro; zero duplicatas |
| Produtos | 1 produto criado e ligado à marca; campos ausentes permaneceram vazios; zero duplicatas |
| Referências | 1 referência existente lida sem alteração; 1 estilo curado criado; segunda execução reutilizou o registro |
| Posts | Primeiro take aprovado antes da escrita; 13 posts criados em lotes de 10 e 3; segunda execução criou zero posts |
| Peças | 1 metadado de imagem criado sem arquivo e ligado a marca, produto, referência e post; segunda execução criou zero registros |

## Resultado do grid de harness

- 13 posts para maio de 2026;
- 8 Feed e 5 Story;
- 4 Produto, 4 Educacional, 3 Editorial e 2 Spoiler;
- lançamento ancorado em 12/05, com três conteúdos de Feed em 12, 14 e 16/05;
- 8 posts ligados ao produto de teste;
- 6 posts ligados ao estilo curado de teste;
- todos em `Rascunho`, com rationale;
- lettering, legenda, notas, mockup e vídeo vazios;
- os 24 posts preexistentes de outras marcas no mês permaneceram inalterados.

Depois do teste de integração de `Peças`, o post de lançamento passou a exibir
uma relação reversa com a peça de teste, como esperado.

## Auditoria independente

A releitura final por chave natural encontrou:

- 1 marca;
- 1 produto;
- 1 referência;
- 13 posts;
- 1 peça.

Todos os 13 posts têm título, data, marca, canal, abordagem, rationale e status
válidos. A distribuição lida da base coincide com o primeiro take aprovado.

## Revisão visual no Airtable

A Gallery exibiu os cards `[TESTE CODEX]` e o detalhe do post de lançamento
confirmou:

- data em 12/05/2026;
- canal Feed e abordagem Produto;
- vínculos com marca, produto e referência de teste;
- status `Rascunho`;
- lettering, legenda, mockup e vídeo vazios;
- relação reversa com a peça de teste.

## Regressões encontradas e corrigidas

1. O eval de briefing misturava confirmação e análise na mesma resposta. Foi
   separado em etapa anterior e posterior ao “OK”.
2. Um critério do fixture tinha redação incompleta. Foi corrigido para
   “somente perguntas que alterem a execução”.
3. A primeira resposta do teste de `Peças` mostrou IDs internos. O contrato e
   o harness agora proíbem IDs de base, tabela, campo e registro na conversa,
   e a resposta foi reavaliada com sucesso.
4. Filtros de data do Airtable exigem o objeto de data exata e fuso horário,
   não uma string simples. O fluxo foi adaptado durante o teste.

## Validação local

O validador da Parte 1 passa sem erros ou avisos. Ele verifica:

- estrutura e frontmatter das skills;
- arquivos compartilhados e evals mínimos;
- ausência de dependências legadas nos `SKILL.md`;
- ausência de IDs do Airtable hardcoded nos `SKILL.md`;
- links de descoberta do Codex.

A validação completa do marketplace pelo Agent Smith continua bloqueada por um
problema anterior a esta implementação no manifesto do plugin Claude:
`plugins/io-social-media/.claude-plugin/plugin.json` declara `skills` num
formato que o validador atual não aceita. Esse manifesto não foi alterado,
porque distribuição e compatibilidade do marketplace estão fora da Parte 1.

## Estado deixado no Airtable

Os registros de harness permanecem na base com prefixo `[TESTE CODEX]` para
revisão visual e novos testes. Eles não serão removidos automaticamente; limpeza
é uma ação separada e exige autorização explícita.
