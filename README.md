# Plugins InsideOut

Catálogo oficial da InsideOut para social media, planejamento Hyundai, mailing,
análise de mar aberto e governança dos plugins no Codex.

## Instalação para o time

No PowerShell do próprio computador, fora do chat, cadastre o catálogo da `main`
e instale somente os produtos necessários:

```powershell
codex plugin marketplace add supernova-labs/insideout-cowork --ref main
codex plugin add insideout-social@insideout
codex plugin add insideout-mar-aberto@insideout
codex plugin add insideout-governance@insideout
codex plugin add insideout-hyundai-social@insideout
codex plugin add insideout-mailing@insideout
```

Se o catálogo já estiver cadastrado, siga o [guia de instalação e atualização](docs/instalacao-plugins.md)
antes de repetir esses comandos. Ele cobre a troca das antigas branches de piloto
para a `main`, que agora reúne os dois produtos novos.

Para registrar ou priorizar fricções de
qualquer produto, instale também `insideout-governance`. Depois, abra uma nova
tarefa no Codex e peça o trabalho normalmente.

## InsideOut Estée Lauder Social

Versão atual: 0.6.2. Identificador de instalação mantido: `insideout-social@insideout`.

| Skill | Resultado |
|---|---|
| `analyze-briefing` | Analisa briefing, lacunas e escopo; pode materializar marca, produtos e canais com confirmação. |
| `curate-brand-pattern` | Analisa perfis de referência aprovados e versiona um padrão histórico da marca no Airtable. |
| `generate-grid` | Compõe o primeiro take mensal com estrutura, rationale, briefing de design, copy e trends sociais pesquisadas automaticamente; pode gerar revisão privada, planejamento de cliente sem mockups ou revisão de cliente com feedback local exportável. |
| `generate-copy` | Produz legenda, hooks e lettering adaptados à rede e ao formato. |
| `generate-image` | Gera e registra mockups com trilha de auditoria. |
| `generate-video` | Produz e registra vídeos curtos a partir de direção visual aprovada. |
| `review-grid-feedback` | Valida o JSON de feedback exportado pelo cliente, consolida retornos por post e encaminha ajustes aprovados à skill responsável. |

## InsideOut Hyundai Social

Versão inicial: 0.1.1 (piloto). Pacote independente para a equipe Hyundai, sem alterar
a instalação do Social das marcas Estée Lauder. O mês começa por pesquisa;
briefing é uma exceção de lançamento ou campanha. O cliente revisa ideias e
referências em HTML com feedback, antes da produção das artes.

O piloto está disponível no catálogo da `main`, junto ao Mailing.
Siga o [guia de instalação e teste da Carol](docs/hyundai-carol-test-guide.md)
para instalar o produto e conectar a base correta.
O pacote declara o conector oficial Airtable como dependência obrigatória e
solicita sua autenticação na instalação. Cada pessoa precisa autorizar sua
própria conta; a declaração não concede acesso a bases nem comprova conexão.

| Skill | Resultado |
|---|---|
| `research-month` | Pesquisa agenda, esportes, eventos, repertório e trends com fontes e data de corte. |
| `generate-grid` | Compõe ideias e publicações por rede, reservas de influenciadores e revisão HTML de referências. |
| `review-grid-feedback` | Valida a versão do feedback Hyundai, consolida ajustes e os encaminha à revisão do time. |
| `send-to-asana` | Prepara e envia somente ideias confirmadas pelo time, com retomada parcial e deduplicação. |

O estado vive na base exclusiva **InsideOut Hyundai Social**. A base começa
sem migração dos testes antigos. Regras permanentes são versionadas; contagem
entre redes e participação dos influenciadores nos totais aguardam o time.
Comentários não equivalem a aprovação. Mudança material invalida a confirmação
anterior para novo envio e exige uma nova revisão.

O envio começa em `Planejamento/on Hold`. Regras fictícias de alocação só
operam em projeto separado de testes, sem pessoas reais. Produção de copy,
imagem/vídeo, Notion, publicação, métricas e automações ficam fora da v1.
Base separada não comprova restrição de acesso: a liberação operacional exige
teste das permissões com contas representativas de cada equipe.

Veja o [protocolo de piloto Hyundai](docs/hyundai-pilot-test-protocol.md) e o
[registro de implantação e validação](docs/hyundai-implementation-status.md).
Nenhuma referência publicada ou integração externa é considerada validada
apenas por existir na documentação.

## InsideOut Mar Aberto

Versão candidata: 0.6.0.

| Skill | Resultado |
|---|---|
| `run-mar-aberto` | Conduz ou retoma a jornada completa sob demanda. |
| `export-stilingue` | Valida a exportação oficial fornecida pelo operador e orienta sua obtenção. |
| `collect-comments` | Coleta comentários e respostas observáveis e entrega diagnóstico de cobertura legível. |
| `analyze-sentiment` | Analisa menções, comentários e respostas observados, mesmo quando há lacunas registradas. |
| `generate-report` | Revisa conclusões afetadas no Gate 1 e gera HTML e planilha a partir de templates limpos. |

O piloto usa o filtro do Hyundai i20 e arquivos locais por execução. A pessoa
fornece por padrão a exportação oficial baixada da Stilingue e faz login
diretamente no Instagram e YouTube quando solicitado; o plugin não recebe nem
armazena credenciais. Menções de Instagram, YouTube, X/Twitter, Facebook e
portais são analisadas separadamente dos comentários.
O template do relatório mantém sua versão de conteúdo `0.5.0`; seu hash é
validado separadamente da versão do plugin.

## InsideOut Governança

Versão atual: 0.3.0.

| Skill | Resultado |
|---|---|
| `registrar-friccao` | Prepara um relato sanitizado, pesquisa recorrências e, após confirmação, registra bugs ou melhorias na aba `Fricções e fixes` do **Acervo de Governança**. |
| `governanca` | Lê os casos da mesma aba, prioriza por impacto e recorrência e propõe um fix verificável para cada fricção em formato padronizado, sem alterar registros. |

A aba [`Fricções e fixes`](https://docs.google.com/spreadsheets/d/1w5IWXgefqsb15149T9SlNj6UEKNsJVJxHH4XAixA0uM/edit?gid=1952697901#gid=1952697901)
é a caixa compartilhada para novos relatos dos plugins, inclusive da própria
governança. Se a conexão estiver indisponível, a skill entrega um rascunho
copiável marcado como não registrado. A antiga base Airtable, relatos antigos
no Social e arquivos locais do Mar Aberto permanecem como histórico, sem
migração automática. Feedback de cliente sobre posts continua no fluxo
`review-grid-feedback` do Social.

## Pré-requisitos

- Codex instalado.
- Acesso individual à base **InsideOut Social** no Airtable para os fluxos do
  Social. O Hyundai Social usa somente **InsideOut Hyundai Social**, com a conta
  pessoal da equipe autorizada no conector.
- Acesso ao recurso criativo indicado pela skill quando houver geração de
  imagem ou vídeo. Esses fluxos podem envolver custo e seguem as aprovações
  previstas no processo.
- Para fricções dos plugins, acesso à planilha
  **Acervo de Governança - Inside Out**. A triagem requer leitura; o registro
  requer edição da aba `Fricções e fixes`. As skills não usam formulário nem
  exigem GitHub.
- Para o Mar Aberto, acesso à exportação oficial da Stilingue e acesso
  individual a Instagram e YouTube pelo navegador do Codex. Os testes reais
  são feitos pela equipe da InsideOut após a publicação.

As skills trabalham em linguagem de marca, produto, post e mês. Elas não
substituem aprovação humana nem completam informações ausentes por hipótese.
Os campos `Slug` são identificadores internos usados para encontrar registros
sem duplicá-los; a Carol não precisa operá-los no dia a dia e eles permanecem
ocultos nas visualizações principais de marcas e produtos.

## Para quem mantém

O catálogo Codex fica em `.agents/plugins/marketplace.json`. Cada pacote vive em
`plugins/<nome>/`, com skills em `skills/`, referências comuns em
`references/_shared/` e manifesto em `.codex-plugin/`. O inventário do catálogo
fica em `.agent-smith/index.json`.

Antes de compartilhar uma nova versão, valide a estrutura:

```powershell
python plugins/insideout-social/references/_shared/scripts/validate_skills.py
python plugins/insideout-mar-aberto/references/_shared/scripts/validate_skills.py
python scripts/validate_hyundai_skills.py
python scripts/validate_mailing_skills.py
python -m unittest discover -s tests/hyundai -v
```

E revise os evals da skill alterada. Evals que escrevem no Airtable ou na
planilha exigem confirmação, releitura e segunda execução para provar
idempotência.

O plano do Mar Aberto está em `DEVELOPMENT_PLAN_MAR_ABERTO.md`. Decisões tomadas
durante a implementação ficam em `IMPLEMENTATION_DECISIONS.md`; resultados
efetivamente comprovados ficam em `ACCEPTANCE_AUDIT.md`. Depois que existir uma
referência publicada, a equipe da InsideOut deve usar o
[`protocolo de homologação do piloto`](docs/mar-aberto-pilot-test-protocol.md),
preenchendo resultados reais sem incluir dados do cliente.

Para novas execuções, a equipe revisa o HTML e exporta o PDF manualmente pelo
navegador. O arquivo HTML funciona sem rede e mantém o conteúdo selecionável.
O diagnóstico de cobertura combina JSON de auditoria e Markdown para a equipe;
uma coleta parcial não paralisa a análise dos itens observados. Lacunas que
podem mudar conclusões principais são decididas no Gate 1. O relatório mostra
o recorte monitorado e as lacunas relevantes sem repetir um alerta geral em
todas as páginas.
O template incorpora a fonte Inter; sua licença está em
`plugins/insideout-mar-aberto/skills/generate-report/assets/INTER-LICENSE.txt`.
Execuções anteriores permanecem no contrato original, sem migração. Os gates
históricos da versão 0.2.2 estão em
`RELEASE_GATES_MAR_ABERTO_0.2.2.md`.

## InsideOut Mailing

Piloto 0.1.0 disponível no catálogo da `main`, junto ao Hyundai Social.

Três skills: gerir-contatos (cadastros e qualidade), montar-listas (seleções
versionadas) e gerir-historico (ações, cruzamentos e participações).
O estado vive em uma planilha Google Sheets nativa, com Contatos, Vínculos,
Ações, Listas, Itens de lista, Participações e Configuração. A implantação
inicial não é uma skill; arquivos reais e relatório restrito ficam fora
do repositório. O Excel anterior permanece oficial durante o teste.

Instalação pela `main` e critérios de teste no
[protocolo do Mailing](docs/mailing-pilot-test-protocol.md).
Validação local: python scripts/validate_mailing_skills.py.
