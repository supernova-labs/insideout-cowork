# Plugins InsideOut

Catálogo oficial da InsideOut para produção de social media e análise de mar
aberto no Codex.

## Instalação para o time

No terminal, execute uma vez para adicionar o catálogo da InsideOut e instalar
o plugin:

```powershell
codex plugin marketplace add supernova-labs/insideout-cowork --ref main
codex plugin add insideout-social@insideout
codex plugin add insideout-mar-aberto@insideout
```

Instale somente o produto necessário. Depois, abra uma nova tarefa no Codex e
peça o trabalho normalmente.

## InsideOut Social

| Skill | Resultado |
|---|---|
| `analyze-briefing` | Analisa briefing, lacunas e escopo; pode materializar marca, produtos e canais com confirmação. |
| `generate-grid` | Compõe o primeiro take mensal com estrutura, rationale, briefing de design, copy e tendências curadas; pode gerar snapshot HTML. |
| `generate-copy` | Produz legenda, hooks e lettering adaptados à rede e ao formato. |
| `generate-image` | Gera e registra mockups com trilha de auditoria. |
| `generate-video` | Produz e registra vídeos curtos a partir de direção visual aprovada. |
| `skill-feedback` | Prepara e, após confirmação, publica bugs ou melhorias no repositório de origem. |

## InsideOut Mar Aberto

| Skill | Resultado |
|---|---|
| `run-mar-aberto` | Conduz ou retoma a jornada completa sob demanda. |
| `export-stilingue` | Exporta e valida o filtro e período oficiais da Stilingue. |
| `collect-comments` | Coleta comentários e respostas observáveis do Instagram e YouTube. |
| `analyze-sentiment` | Analisa automaticamente relevância, alvo, sentimento, temas e amplificação. |
| `generate-report` | Conduz os gates editoriais e gera HTML, PDF e planilha analítica. |
| `skill-feedback` | Registra bugs e melhorias do Mar Aberto sem expor dados da execução. |

O piloto usa o filtro do Hyundai i20 e arquivos locais por execução. A pessoa
faz login diretamente na Stilingue e nas redes quando solicitado; o plugin não
recebe nem armazena credenciais.

## Pré-requisitos

- Codex instalado.
- Acesso individual à base **InsideOut Social** no Airtable para os fluxos que
  leem ou atualizam dados operacionais.
- Acesso ao recurso criativo indicado pela skill quando houver geração de
  imagem ou vídeo. Esses fluxos podem envolver custo e seguem as aprovações
  previstas no processo.
- Integração autenticada com GitHub para publicar feedback. Sem ela, a skill
  entrega um draft completo e não alega publicação.
- Para o Mar Aberto, acesso individual à Stilingue, Instagram e YouTube pelo
  navegador do Codex. Os testes reais são feitos pela equipe da InsideOut após
  a publicação do piloto.

As skills trabalham em linguagem de marca, produto, post e mês. Elas não
substituem aprovação humana nem completam informações ausentes por hipótese.

## Para quem mantém

O catálogo Codex fica em `.agents/plugins/marketplace.json`. Cada pacote vive em
`plugins/<nome>/`, com skills em `skills/`, referências comuns em
`references/_shared/` e manifesto em `.codex-plugin/`. O inventário do catálogo
fica em `.agent-smith/index.json`.

Antes de compartilhar uma nova versão, valide a estrutura:

```powershell
python plugins/insideout-social/references/_shared/scripts/validate_skills.py
python plugins/insideout-mar-aberto/references/_shared/scripts/validate_skills.py
```

E revise os evals da skill alterada. Evals que escrevem no Airtable exigem
confirmação, releitura e uma segunda execução para provar idempotência.

O plano do Mar Aberto está em `DEVELOPMENT_PLAN_MAR_ABERTO.md`. Decisões tomadas
durante a implementação ficam em `IMPLEMENTATION_DECISIONS.md`; resultados
efetivamente comprovados ficam em `ACCEPTANCE_AUDIT.md`. Depois que existir uma
referência publicada, a equipe da InsideOut deve usar o
[`protocolo de homologação do piloto`](docs/mar-aberto-pilot-test-protocol.md),
preenchendo resultados reais sem incluir dados do cliente.
