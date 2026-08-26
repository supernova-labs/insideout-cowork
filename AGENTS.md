# InsideOut Cowork

Este repositório codifica a capacidade operacional da InsideOut para analisar
briefings e produzir social media. Há duas gerações de implementação que ainda
coexistem: as skills locais do Codex, hoje em evolução, e o marketplace legado
do Claude Cowork. Preserve essa fronteira.

## Antes de trabalhar

Leia somente o contexto necessário, nesta ordem:

1. este arquivo;
2. o `SKILL.md` relevante em `.codex/skills/<skill>/`;
3. os arquivos indicados pelo próprio `SKILL.md` em `references/` e
   `.codex/skills/_shared/`;
4. o eval correspondente em `evals/`, quando houver mudança de comportamento;
5. `docs/README.md` e o documento de arquitetura ou validação aplicável;
6. `CLAUDE.md` e `README.md` quando a tarefa tocar no marketplace legado,
   instalação ou release.

Não carregue todas as referências por hábito. Siga os links do fluxo que está
sendo alterado e leia cada arquivo selecionado por inteiro.

## Fontes de verdade

Use a fonte compatível com o tipo de trabalho:

| Assunto | Fonte principal |
|---|---|
| Comportamento atual das skills no Codex | `.codex/skills/*/SKILL.md` |
| Tom, contexto comum e contrato de dados | `.codex/skills/_shared/` |
| Regras de marca, calendário e composição | `references/` da skill responsável |
| Estado operacional de marcas, produtos, referências, posts e peças | base viva **InsideOut Social** no Airtable |
| Arquitetura-alvo e decisões de migração | `docs/visao-transformacao.md` e `docs/plano-implementacao-codex-airtable.md` |
| Evidência de gates já executados | relatórios de validação em `docs/` |
| Marketplace Claude legado e release | `plugins/io-social-media/`, manifestos, `README.md` e `CLAUDE.md` |

Instrução explícita do usuário vence a documentação. Em seguida, prefira o
contrato da skill atual. Documentos de visão e relatórios são snapshots: não os
trate como prova de que um gate continua válido sem verificar o estado atual.

O `CLAUDE.md` descreve principalmente o marketplace Python legado. Ele é útil
para manutenção e release desse caminho, mas não substitui as skills atuais do
Codex. `agent-smith-index.json` também cataloga o legado e não é o catálogo
canônico das skills locais.

## Arquitetura atual

- `.codex/skills/` é a implementação experimental atual. A skill guarda
  conhecimento, julgamento e fluxo; o Airtable guarda estado operacional.
- `.agents/skills/*` são adaptadores de descoberta versionados como symlinks
  para `.codex/skills/*`. Edite o destino canônico, não o adaptador.
- `plugins/io-social-media/` contém o plugin Claude anterior, com Python, JSON,
  painel e motores Gemini/Veo. Use-o como referência histórica de comportamento
  ou quando a tarefa nomear explicitamente o legado.
- `docs/` registra visão, plano, demonstrações e resultados de validação.
- Não porte o `core/` para o fluxo novo e não remova o legado como efeito
  colateral. Migração ou deleção exige escopo explícito.

### Fronteiras das skills

| Skill | Responsabilidade | Escrita permitida após os gates da skill |
|---|---|---|
| `analyze-briefing` | entendimento, lacunas, escopo e ficha mensal | `Marcas` e `Produtos`, com confirmação |
| `generate-grid` | primeiro take mensal e rationale | `Posts`, após auditar conflitos e aprovar o take |
| `generate-copy` | hooks, legenda e lettering | somente `Posts.Legenda` e `Posts.Lettering`, após aprovação |
| `generate-image` | composição e QA da imagem | peça de imagem, arquivo e `Posts.Mockup`, sem sobrescrever silenciosamente |
| `generate-video` | movimento, continuidade e custo | peça de vídeo, arquivo e `Posts.Vídeo`, após aprovar parâmetros e créditos |

Uma skill não deve absorver a responsabilidade da seguinte. Em especial, grid
não escreve copy ou mídia; copy não altera status; imagem não cria texto; vídeo
não cria frame inicial.

## Regras operacionais

- Comece separando fatos confirmados, inferências, lacunas e decisões abertas.
- Use apenas fontes colocadas em escopo; não complete briefing, claim, contrato
  ou atributo de marca por plausibilidade.
- Fale com o time em linguagem de marca, produto, post, mês e data. Não exponha
  IDs, schema, chamadas de ferramenta, caminhos internos ou logs crus.
- Antes de qualquer operação no Airtable, descubra a base, tabelas e campos
  atuais. Nunca fixe IDs no repositório ou na conversa.
- Pesquise pela chave natural antes de criar; diante de duplicidade, pare a
  escrita e apresente o conflito.
- Releia toda mutação antes de declarar sucesso. Nos fluxos de harness, escreva
  em lotes de até 10 e use o prefixo `[TESTE CODEX]`.
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
  o caso. Se mudar contrato ou decisão arquitetural, alinhe o documento
  correspondente em `docs/`.
- Preserve frontmatter válido, nomes em kebab-case e `SKILL.md` com menos de 500
  linhas.
- Não introduza dependências no `core/`, IDs hardcoded do Airtable ou referências
  aos motores legados nas skills atuais.
- O repositório é co-acessado com o cliente: não faça push direto na `main`.
  Mudança apenas documental não exige bump de versão nem tag. Para release do
  marketplace legado, siga `README.md` e sincronize todos os manifestos.

## Validação

Validação estrutural das skills atuais:

```powershell
python .codex/skills/_shared/scripts/validate_skills.py
```

Os evals de comportamento vivem em cada pasta `evals/` e devem ser executados
em tarefas limpas, conforme `.codex/skills/_shared/evals/README.md`. Evals que
escrevem no Airtable exigem releitura e uma segunda execução para comprovar
idempotência; limpeza é separada e destrutiva.

No Windows, Git pode materializar os symlinks de `.agents/skills/` como arquivos
de texto. Nesse caso, o validador pode emitir apenas avisos de adaptador ausente.
Confirme que Git ainda os registra com modo `120000` antes de tentar corrigi-los;
não converta os adaptadores sem intenção explícita.

Ao tocar no plugin legado, rode os evals Python relevantes em
`plugins/io-social-media/tests/` e respeite dependências de dados externos
descritas no cabeçalho de cada arquivo.

## Critério de conclusão

Antes de entregar:

- confira o diff e mantenha-o dentro do escopo;
- rode a validação proporcional à mudança;
- confirme que nenhuma fonte canônica ficou contraditória;
- declare o que foi comprovado, o que permanece pendente e qualquer gate que
  dependa de Airtable, geração paga ou aprovação humana.
