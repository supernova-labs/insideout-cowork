# InsideOut Social

Este repositório publica o catálogo Codex oficial da InsideOut para análise de
briefings e produção de social media. As skills guardam conhecimento,
julgamento e fluxo; o Airtable guarda o estado operacional.

## Antes de trabalhar

Leia somente o contexto necessário, nesta ordem:

1. este arquivo;
2. o `SKILL.md` relevante em `plugins/insideout-social/skills/<skill>/`;
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
| Tom, contexto comum e contrato de dados | `plugins/insideout-social/references/_shared/` |
| Regras de marca, calendário e composição | `references/` da skill responsável |
| Estado operacional de marcas, produtos, referências, posts e peças | base viva **InsideOut Social** no Airtable |
| Catálogo Codex | `.agents/plugins/marketplace.json` |
| Manifesto do plugin | `plugins/insideout-social/.codex-plugin/plugin.json` |
| Inventário de arquitetura | `.agent-smith/index.json` |

Instrução explícita do usuário vence a documentação. Não trate documentos ou
resultados de validação como prova de que uma integração externa continua
disponível: confirme-a na sessão quando ela for necessária.

## Arquitetura e fronteiras

- `plugins/insideout-social/skills/` é a fonte canônica e única das cinco
  skills distribuídas.
- `.agents/plugins/marketplace.json` expõe o catálogo `insideout` para o
  Codex; o manifesto nativo fica junto ao pacote do plugin.
- `.agent-smith/index.json` descreve os componentes distribuídos; o filesystem
  continua sendo a fonte de verdade.
- Não adicione código, dados operacionais locais, credenciais, painéis ou
  motores de geração ao plugin.

| Skill | Responsabilidade | Escrita permitida após os gates da skill |
|---|---|---|
| `analyze-briefing` | entendimento, lacunas, escopo e ficha mensal | `Marcas` e `Produtos`, com confirmação |
| `generate-grid` | primeiro take mensal e rationale | `Posts`, após auditar conflitos e aprovar o take |
| `generate-copy` | hooks, legenda e lettering | somente `Posts.Legenda` e `Posts.Lettering`, após aprovação |
| `generate-image` | composição e QA da imagem | peça de imagem, arquivo e `Posts.Mockup`, sem sobrescrever silenciosamente |
| `generate-video` | movimento, continuidade e custo | peça de vídeo, arquivo e `Posts.Vídeo`, após aprovar parâmetros e créditos |

Uma skill não absorve a responsabilidade da seguinte: grid não escreve copy ou
mídia; copy não altera status; imagem não cria texto; vídeo não cria frame
inicial.

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
```

Os evals de comportamento vivem em cada pasta `evals/` e devem ser executados
em tarefas limpas. Evals que escrevem no Airtable exigem releitura e uma
segunda execução para comprovar idempotência; limpeza é separada e destrutiva.

Antes de entregar, confira o diff, rode a validação proporcional à mudança e
declare o que foi comprovado, o que permanece pendente e qualquer gate que
dependa de Airtable, geração paga ou aprovação humana.
