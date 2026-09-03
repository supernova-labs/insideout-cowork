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

---

# Auditoria de aceitação — InsideOut Mar Aberto

Data da execução: 2026-09-02

Versão candidata: `insideout-mar-aberto` 0.1.0

Escopo: construção do piloto e testes locais sem contas ou dados reais. A
publicação e a homologação operacional pela equipe da InsideOut permanecem como
gates separados.

## Resultado da construção

- M0–M7: artefatos de construção concluídos, com contratos, seis skills, 21
  evals, quatro schemas, fixtures sintéticas e prova vertical local.
- M8-T1–T5: comprovados; o commit validado `3adfa7b` foi publicado na branch
  `codex/add-insideout-marketplace` e promovido por fast-forward para `main`.
- M9-T1–T8: não executados, por decisão de produto; serão realizados pela
  equipe da InsideOut depois da publicação do piloto.

“Construído” não significa “homologado em sessão real”. Nenhum teste local foi
usado como evidência de login, exportação ou coleta nas plataformas.

## Evidência por milestone

| Milestone | Estado da construção | Evidência local | Pendência deliberada |
|---|---|---|---|
| M0 — contratos | passou | schemas, matriz princípio–teste, CSV válida e inválida, comentário, resposta, duplicata, cobertura parcial e canal não suportado | nenhuma |
| M1 — fundação | passou | manifesto 0.1.0, catálogo com dois plugins, seis skills e índice Agent Smith sem conflito | nenhuma |
| M2 — Stilingue | passou no contrato sintético | entrada válida e inválida, recorte `nova busca i20`, instruções de refresh, janela vazia e retomada | login, status e download reais: M9-T2 |
| M3 — coleta | passou no contrato sintético | Instagram e YouTube, grafo pai–resposta, deduplicação, anonimização, cobertura parcial e TikTok não suportado | paginação e retomada nas interfaces reais: M9-T3–T4 |
| M4 — análise | passou no conjunto sintético | 8 observados = 7 relevantes + 1 excluído; sentimento por alvo; distribuição unitária; amplificação separada; corpus removido no concluído e preservado no interrompido | utilidade editorial no corpus real: M9-T5 |
| M5 — produtos | passou na prova vertical | HTML, PDF e `.xlsx` reconciliados; sete abas; quatro evidências aprovadas; inspeção desktop, 360 px e três páginas A4 | dois gates conduzidos por operador real: M9-T5–T7 |
| M6 — orquestração | passou no contrato e estado sintéticos | manifesto portátil, caminhos relativos, estados concluído/interrompido e três entregáveis presentes | invocação e retomada em tarefa nova: M9-T2–T6 |
| M7 — feedback | passou no contrato | sanitização, duplicidade, cancelamento, fallback e releitura cobertos por três evals | publicação real de issue ou fallback: M9-T8 |
| M8 — piloto | passou | validadores e diff aprovados; pacote sem estado de `artifacts/`; commit `3adfa7b` publicado na branch piloto e em `main` | nenhuma |
| M9 — homologação | não executado | protocolo operacional preenchível cobre as oito provas, seus aceites e a decisão final | execução integral pela InsideOut após publicação |

## Validações executadas

1. `validate_skills.py` do Mar Aberto: passou com seis skills, 21 evals,
   70 critérios de teste únicos, quatro schemas, zero erro e zero aviso. O
   validador executa também rejeição da exportação sem URL, normalização de
   URLs repetidas, casos de cobertura zero/indisponível, reconciliação de
   análise, invariantes de retomada e rejeição de caminhos que escapem da pasta
   da execução.
2. `validate_skills.py` do InsideOut Social: passou para as seis skills
   existentes, comprovando regressão estrutural ausente.
3. Agent Smith: passou para marketplace Codex, dois plugins locais, 12 skills
   únicas e índice v2, sem erro, aviso, conflito ou ambiguidade.
4. Validador oficial de plugin: passou para `insideout-mar-aberto`.
5. Validador oficial de skill: as seis skills passaram individualmente.
6. `git diff --check`: passou. A inspeção final do diff staged é registrada
   junto do gate M8-T4.

## Prova vertical dos produtos

Foi montada uma execução local ignorada pelo Git com três publicações, oito
registros observados, sete relevantes, uma exclusão, quatro evidências aprovadas
e duas lacunas explícitas: YouTube parcial (5 de 7) e TikTok não suportado.

- A planilha foi produzida com `@oai/artifact-tool`, reaberta e inspecionada;
  contém `Resumo`, `Cobertura`, `Publicações`, `Análises`, `Agregações`,
  `Evidências` e `Metodologia`, com tabelas filtráveis e cabeçalhos congelados.
- Todas as sete abas foram renderizadas. A primeira renderização revelou uma
  fórmula de relevância zerada e colunas comprimidas; ambas foram corrigidas e
  a versão final foi renderizada novamente.
- A aba `Análises` não contém texto bruto. O comentário integral aparece somente
  em `Evidências`, para quatro registros aprovados e sem identidade.
- O HTML contém oito seções, três tabelas e quatro evidências. Playwright
  confirmou largura de página igual à viewport em 1440 px e 360 px e zero
  chamada externa.
- O PDF foi impresso a partir do mesmo HTML, possui três páginas A4, não contém
  JavaScript e teve todas as páginas renderizadas e inspecionadas sem corte,
  sobreposição ou página vazia. A extração de texto confirmou as seções e os
  totais essenciais presentes no HTML e no PDF.
- Poppler emitiu avisos de `FontBBox` para glifos Type 3; a renderização visual
  e a extração textual permaneceram corretas, por isso o aviso é não bloqueante.
- A execução concluída não contém `working/comments.jsonl`; a execução
  interrompida de controle preserva esse corpus temporário.
- A pasta concluída foi copiada para outro diretório e os oito caminhos do
  manifesto (`input`, cobertura, análise, agregados, evidências e três
  entregáveis) continuaram resolvendo com o mesmo `run_id`.

Os artefatos dessa prova ficam em `artifacts/mar-aberto-e2e/` e não fazem parte
do pacote distribuído.

## Gate de publicação concluído

O piloto 0.1.0 foi publicado em 2026-09-02. A branch
`codex/add-insideout-marketplace` e a `main` remota apontaram para o commit
validado `3adfa7b6a1b6842a0c80ccee4c76c5e48fa7bb08`; a promoção foi
fast-forward a partir de `c4c61fa`, sem conflito ou reescrita de histórico.
M8-T5 passa com essa evidência. Este registro documental é uma atualização
imediatamente posterior e não altera os arquivos do plugin. Todos os testes M9
permanecem `não executado`, sem alegação de homologação operacional.

Na máquina atual, `codex plugin marketplace list` mostrou apenas o catálogo
`personal`; o catálogo `insideout` ainda não foi adicionado nem o novo plugin
instalado. Essa configuração foi preservada sem alteração e será parte de
M9-T1 ao instalar a referência publicada em `main`.

O roteiro de homologação está em
`docs/mar-aberto-pilot-test-protocol.md`. Ele registra os estados `passou`,
`falhou` e `não executado`, exige evidência sanitizada por prova e termina com
a decisão `liberar`, `iterar` ou `interromper`. O documento está preparado, mas
nenhum campo operacional foi preenchido e nenhum M9 foi promovido a sucesso.
