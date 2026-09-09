# Gates de release — InsideOut Mar Aberto 0.2.0

Este é o plano ativo de correção após a primeira homologação operacional. A
versão só pode ser publicada quando G0–G6 passarem com evidência local e G7
receber autorização explícita para promover exatamente o commit validado.

Estados permitidos: `pendente`, `em implementação`, `passou` e `falhou`. Um
teste não executado nunca conta como sucesso.

## G0 — Contrato aprovado

**Tipo:** decision · **Estado:** passou

**Artefato demonstrável:** decisões D018–D024 registradas em
`IMPLEMENTATION_DECISIONS.md` e princípios correspondentes em
`ARCHITECTURE.md`.

**Critério de saída:** entrada manual prioritária, gate rígido de cobertura,
fontes separadas, estrutura do relatório, feedback local, e-mail opcional e
limite da otimização de uso não deixam decisão estrutural para a implementação.

| ID | Teste | Evidência esperada |
|---|---|---|
| R02-G0-T1 | Matriz decisão–contrato | Cada decisão aponta para skill, referência e teste que a prova. |
| R02-G0-T2 | Fronteira de produto | `insideout-social` permanece independente e sem mudança comportamental. |

**Decisão habilitada:** o contrato 2.0 pode substituir o comportamento do
piloto 0.1.0?

## G1 — Entrada oficial eficiente

**Tipo:** build · **Estado:** passou

**Artefato demonstrável:** exportação oficial fornecida pelo operador é
validada sem abrir a Stilingue e origina menções normalizadas.

**Critério de saída:** a planilha oficial é o único contrato de entrada; o
navegador integrado é opcional e nunca é tentado sem pedido.

| ID | Teste | Evidência esperada |
|---|---|---|
| R02-G1-T1 | Arquivo oficial fornecido | Zero ação de navegador antes da validação e checkpoint válido. |
| R02-G1-T2 | Arquivo inválido | Coleta bloqueada sem inventar campo ou URL. |
| R02-G1-T3 | Exportação assistida solicitada | Login privado, um refresh e download verificado. |
| R02-G1-T4 | Menções multicanal | Cinco canais analíticos normalizados; outros explicitamente não suportados. |

**Decisão habilitada:** a entrada reduz interação sem perder auditabilidade?

## G2 — Cobertura completa e retomável

**Tipo:** gate · **Estado:** passou

**Artefato demonstrável:** diagnóstico `blocked_coverage` impede derivados e
aponta o próximo passo de coleta.

**Critério de saída:** toda publicação obrigatória está `complete`; qualquer
`partial` ou `unavailable` produz somente diagnóstico, preserva os corpora e
bloqueia análise e relatório.

| ID | Teste | Evidência esperada |
|---|---|---|
| R02-G2-T1 | 74 na exportação, 186 na plataforma e 42 observados | Estado `blocked_coverage`, sem análise parcial. |
| R02-G2-T2 | Paginação e respostas completas | Evidência de esgotamento e contagens reconciliadas. |
| R02-G2-T3 | Sessão expirada | Retomada sem duplicar publicação, comentário ou resposta. |
| R02-G2-T4 | Canal somente de menções | Estado `not_required`, sem navegação e sem bloquear análise. |
| R02-G2-T5 | Publicação inacessível | Demais coletas avançam, mas a análise continua bloqueada. |

**Decisão habilitada:** a cobertura é forte o suficiente para autorizar a
classificação automática?

## G3 — Análise por tipo de fonte

**Tipo:** build · **Estado:** passou

**Artefato demonstrável:** análises, agregados e pool candidato reconciliados
para menções, comentários e respostas.

**Critério de saída:** cada registro tem `source_kind`; os denominadores, séries
diárias e amplificação permanecem separados por rede e fonte.

| ID | Teste | Evidência esperada |
|---|---|---|
| R02-G3-T1 | Fixture multicanal completa | Instagram, YouTube, X, Facebook e portais entram nas menções. |
| R02-G3-T2 | Denominadores separados | Menção, comentário e resposta reconciliam sem fusão. |
| R02-G3-T3 | Alvos e ambiguidade | Polaridade não migra entre alvos e incerteza não é forçada. |
| R02-G3-T4 | Gate negativo | Cobertura bloqueada cria zero derivado analítico. |
| R02-G3-T5 | Retenção | Corpora somem só depois de derivados e hashes válidos. |

**Decisão habilitada:** os dados analíticos sustentam o relatório sem leitura
parcial ou dupla contagem?

## G4 — Produtos alinhados ao relatório de referência

**Tipo:** build · **Estado:** passou

**Artefato demonstrável:** HTML, PDF e planilha com visão geral e recortes por
canal, reconciliados com os JSON/JSONL canônicos.

**Critério de saída:** os produtos reproduzem a arquitetura de informação dos
slides 8–14, com gráficos mínimos, oito abas e dois gates humanos, sem copiar o
layout pixel a pixel.

| ID | Teste | Evidência esperada |
|---|---|---|
| R02-G4-T1 | Núcleo analítico | Onze seções e recortes dos canais disponíveis. |
| R02-G4-T2 | Gráficos | Distribuição, volume, série diária a 100% e termos reconciliados. |
| R02-G4-T3 | Planilha | Oito abas, filtros, cabeçalhos congelados e tipos reais. |
| R02-G4-T4 | Privacidade | Texto integral somente em evidências aprovadas e sem identidade. |
| R02-G4-T5 | Gate de cobertura | Estado bloqueado produz zero HTML, PDF ou planilha. |
| R02-G4-T6 | Renderização | HTML responsivo e PDF sem corte, página vazia ou divergência. |

**Decisão habilitada:** os produtos estão prontos para revisão humana da
InsideOut?

## G5 — Feedback acessível sem GitHub

**Tipo:** build · **Estado:** passou

**Artefato demonstrável:** relatório Markdown local sanitizado e relido, com
encaminhamento opcional por e-mail.

**Critério de saída:** qualquer operador registra uma fricção com ou sem
execução ativa; duplicidade é local e nenhum efeito externo ocorre por padrão.

| ID | Teste | Evidência esperada |
|---|---|---|
| R02-G5-T1 | Fricção em execução | Arquivo em `feedback/` com cabeçalho, fingerprint e corpo válidos. |
| R02-G5-T2 | Fricção sem execução | Pasta local escolhida, sem inventar manifesto. |
| R02-G5-T3 | Duplicidade | Mesmo fingerprint não cria segundo arquivo. |
| R02-G5-T4 | Sanitização | Zero cliente, comentário, URL, caminho, credencial ou log cru. |
| R02-G5-T5 | Gmail indisponível | Assunto e corpo copiáveis; `.md` continua canônico. |
| R02-G5-T6 | Gmail disponível | Destinatários confirmados e somente rascunho; zero envio automático. |

**Decisão habilitada:** a equipe consegue encaminhar achados aos mantenedores
sem acesso a ferramentas de desenvolvimento?

## G6 — Pacote candidato validado

**Tipo:** gate · **Estado:** passou

**Artefato demonstrável:** commit candidato 0.2.0 com todos os validadores
locais verdes e escopo auditado.

**Critério de saída:** manifesto, catálogo, índice e documentação concordam;
skills e fixtures passam; `insideout-social` não regride; nenhum dado real ou
segredo entra no pacote.

| ID | Teste | Evidência esperada |
|---|---|---|
| R02-G6-T1 | Validador Mar Aberto | Zero erro e zero aviso. |
| R02-G6-T2 | Regressão Social | Validador do `insideout-social` passa sem mudança comportamental. |
| R02-G6-T3 | Agent Smith | Marketplace Codex e índice v2 sem conflito ou gap não reconhecido. |
| R02-G6-T4 | Diff e conteúdo | Whitespace, segredos, dados reais e caminhos fora do escopo ausentes. |

**Decisão habilitada:** o commit exato pode ser promovido para publicação?

## G7 — Publicação e nova homologação

**Tipo:** gate · **Estado:** em implementação

**Artefato demonstrável:** versão 0.2.0 publicada a partir do commit aprovado e
protocolo pós-publicação entregue à InsideOut.

**Critério de saída:** autorização explícita, referência publicada igual ao
commit validado e protocolo atualizado para Carol/Fabi testar em tarefa nova.

| ID | Teste | Evidência esperada |
|---|---|---|
| R02-G7-T1 | Autorização | Confirmação explícita antes de push ou promoção à `main`. |
| R02-G7-T2 | Identidade da publicação | Commit, versão e referência instalada coincidem. |
| R02-G7-T3 | Handoff | Protocolo exige entrada manual, cobertura completa, menções e feedback local. |

A homologação registra duração e variação de uso como evidência operacional,
sem transformar a quota do workspace em critério controlado pelo plugin.

**Decisão habilitada:** depois da homologação real, liberar, iterar novamente ou
interromper?
