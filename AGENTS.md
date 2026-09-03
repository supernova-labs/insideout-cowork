# Plugins InsideOut

Este repositório publica o catálogo Codex oficial da InsideOut para análise de
briefings, produção de social media e análise de mar aberto. As skills guardam
conhecimento, julgamento e fluxo; cada plugin usa o estado operacional definido
em seu contrato.

## Antes de trabalhar

Leia somente o contexto necessário, nesta ordem:

1. este arquivo;
2. o `SKILL.md` relevante em `plugins/<plugin>/skills/<skill>/`;
3. os arquivos indicados pelo próprio `SKILL.md` em `references/`, incluindo
   `../../references/_shared/` quando aplicável;
4. o eval correspondente em `evals/` quando houver mudança de comportamento;
5. `README.md` para instalação, distribuição ou release.

Não carregue todas as referências por hábito. Siga os links do fluxo alterado
e leia cada arquivo selecionado por inteiro.

## Fontes de verdade

| Assunto | Fonte principal |
|---|---|
| Comportamento das skills | `plugins/insideout-social/skills/*/SKILL.md` |
| Comportamento do Mar Aberto | `plugins/insideout-mar-aberto/skills/*/SKILL.md` |
| Tom, contexto comum e contrato de dados | `plugins/insideout-social/references/_shared/` |
| Regras de marca, calendário e composição | `references/` da skill responsável |
| Estado operacional de marcas, produtos, referências, posts e peças | base viva **InsideOut Social** no Airtable |
| Estado operacional do Mar Aberto | pasta local por projeto e execução, fora do plugin |
| Catálogo Codex | `.agents/plugins/marketplace.json` |
| Manifesto do plugin | `plugins/insideout-social/.codex-plugin/plugin.json` |
| Inventário de arquitetura | `.agent-smith/index.json` |

Instrução explícita do usuário vence a documentação. Não trate documentos ou
resultados de validação como prova de que uma integração externa continua
disponível: confirme-a na sessão quando ela for necessária.

## Arquitetura e fronteiras

- Cada plugin mantém uma única árvore canônica em `plugins/<plugin>/skills/`.
- `insideout-social` contém seis skills de produção editorial;
  `insideout-mar-aberto` contém a jornada principal, quatro etapas
  especializadas e feedback próprio.
- `.agents/plugins/marketplace.json` expõe o catálogo `insideout` para o
  Codex; o manifesto nativo fica junto ao pacote do plugin.
- `.agent-smith/index.json` descreve os componentes distribuídos; o filesystem
  continua sendo a fonte de verdade.
- Não adicione código, dados operacionais locais, credenciais, painéis ou
  motores de geração ao plugin.

| Skill | Responsabilidade | Escrita permitida após os gates da skill |
|---|---|---|
| `analyze-briefing` | entendimento, lacunas, escopo, canais e ficha mensal | `Marcas`, `Produtos` e `Canais da marca`, com confirmação |
| `generate-grid` | primeiro take mensal, rationale, briefing de design, tendências e snapshot | seus campos em `Posts`, após auditar conflitos e aprovar o take; HTML fora do plugin |
| `generate-copy` | hooks, legenda e lettering | somente `Posts.Legenda` e `Posts.Lettering`, após aprovação |
| `generate-image` | composição e QA da imagem | peça de imagem, arquivo e `Posts.Mockup`, sem sobrescrever silenciosamente |
| `generate-video` | movimento, continuidade e custo | peça de vídeo, arquivo e `Posts.Vídeo`, após aprovar parâmetros e créditos |
| `skill-feedback` | bug ou melhoria sobre o plugin | issue no repositório de origem, somente após sanitização e confirmação |

Uma skill não absorve a responsabilidade da seguinte: grid orquestra copy, mas
não escreve seus campos nem produz mídia; copy não altera status; imagem não
cria texto; vídeo não cria frame inicial; feedback não corrige a instalação
local.

| Skill do Mar Aberto | Responsabilidade | Saída própria |
|---|---|---|
| `run-mar-aberto` | coordenar etapas e retomada | manifesto e apresentação do estado |
| `export-stilingue` | obter e validar a entrada oficial | planilha original e checkpoint de entrada |
| `collect-comments` | percorrer Instagram e YouTube | corpus temporário anonimizado e cobertura |
| `analyze-sentiment` | classificar e agregar automaticamente | análises, agregados e pool candidato |
| `generate-report` | conduzir dois gates editoriais | HTML, PDF e planilha analítica |
| `skill-feedback` | registrar bug ou melhoria | issue confirmada ou draft sanitizado |

A orquestradora não refaz o trabalho das etapas. A análise não revisa o
relatório; o relatório não altera classificações; a coleta não mantém identidade
pessoal; feedback não corrige a instalação local.

## Regras operacionais

- Comece separando fatos confirmados, inferências, lacunas e decisões abertas.
- Use apenas fontes colocadas em escopo; não complete briefing, claim, contrato
  ou atributo de marca por plausibilidade.
- Fale com o time em linguagem de marca, produto, post, mês e data. Não exponha
  IDs, schema, chamadas de ferramenta ou logs crus.
- Antes de escrever no Airtable, descubra a base, as tabelas e os campos atuais.
- Pesquise pela chave natural antes de criar. Diante de duplicidade, pare a
  escrita e apresente o conflito.
- Releia toda mutação antes de declarar sucesso. Em harness, escreva em lotes
  de até 10 e use o prefixo `[TESTE CODEX]`.
- Nunca apague registros, substitua conteúdo existente, altere status para
  `Aprovada` ou consuma créditos sem a confirmação exigida pelo fluxo.
- URLs temporárias e arquivos apenas no gerador não são persistência concluída.
- Não adicione tokens, chaves, `.env` ou credenciais ao repositório.
- No Mar Aberto, nunca versionar comentários reais, estado de execução ou
  entregáveis de cliente. Evals usam somente fixtures sintéticas ou sanitizadas.

## Ao alterar o repositório

- Faça a menor mudança que satisfaz o pedido e preserve alterações locais não
  relacionadas.
- Mantenha cada fato em um único nível: regra compartilhada em `_shared/`,
  comportamento na skill, detalhe especializado em `references/` e cenário de
  regressão em `evals/`.
- Se mudar o comportamento de uma skill, atualize ou adicione o eval que prova
  o caso. Se mudar o contrato de distribuição, atualize o catálogo, o
  manifesto, o índice e o `README.md`.
- Preserve frontmatter válido, nomes em kebab-case e `SKILL.md` com menos de
  500 linhas.
- O repositório é co-acessado com o cliente: não faça push direto na `main` sem
  confirmação explícita.

## Validação

```powershell
python plugins/insideout-social/references/_shared/scripts/validate_skills.py
python plugins/insideout-mar-aberto/references/_shared/scripts/validate_skills.py
```

Os evals de comportamento vivem em cada pasta `evals/` e devem ser executados
em tarefas limpas. Evals que escrevem no Airtable exigem releitura e uma
segunda execução para comprovar idempotência; limpeza é separada e destrutiva.

Antes de entregar, confira o diff, rode a validação proporcional à mudança e
declare o que foi comprovado, o que permanece pendente e qualquer gate que
dependa de Airtable, geração paga ou aprovação humana.
