# InsideOut Social

Plugin oficial da InsideOut para transformar briefings em direção estratégica,
grids multirrede completos, copy, snapshots de revisão, imagens e vídeos de
social media, com um canal seguro de feedback para os mantenedores.

## Instalação para o time

No terminal, execute uma vez para adicionar o catálogo da InsideOut e instalar
o plugin:

```powershell
codex plugin marketplace add supernova-labs/insideout-cowork --ref main
codex plugin add insideout-social@insideout
```

Depois, abra uma nova tarefa no Codex e peça o trabalho normalmente. Por
exemplo: “Analise este briefing da marca e destaque lacunas e escopo.”

## O que ele faz

| Skill | Resultado |
|---|---|
| `analyze-briefing` | Analisa briefing, lacunas e escopo; pode materializar marca, produtos e canais com confirmação. |
| `generate-grid` | Compõe o primeiro take mensal com estrutura, rationale, briefing de design, copy e tendências curadas; pode gerar snapshot HTML. |
| `generate-copy` | Produz legenda, hooks e lettering adaptados à rede e ao formato. |
| `generate-image` | Gera e registra mockups com trilha de auditoria. |
| `generate-video` | Produz e registra vídeos curtos a partir de direção visual aprovada. |
| `skill-feedback` | Prepara e, após confirmação, publica bugs ou melhorias no repositório de origem. |

## Pré-requisitos

- Codex instalado.
- Acesso individual à base **InsideOut Social** no Airtable para os fluxos que
  leem ou atualizam dados operacionais.
- Acesso ao recurso criativo indicado pela skill quando houver geração de
  imagem ou vídeo. Esses fluxos podem envolver custo e seguem as aprovações
  previstas no processo.
- Integração autenticada com GitHub para publicar feedback. Sem ela, a skill
  entrega um draft completo e não alega publicação.

As skills trabalham em linguagem de marca, produto, post e mês. Elas não
substituem aprovação humana nem completam informações ausentes por hipótese.

## Para quem mantém

O catálogo Codex fica em `.agents/plugins/marketplace.json`. O pacote
 distribuído está em `plugins/insideout-social/`: as skills em `skills/`, as
 referências comuns em `references/_shared/`, o manifesto em `.codex-plugin/`
 e o inventário de arquitetura na raiz, em
`.agent-smith/index.json`.

Antes de compartilhar uma nova versão, valide a estrutura:

```powershell
python plugins/insideout-social/references/_shared/scripts/validate_skills.py
```

E revise os evals da skill alterada. Evals que escrevem no Airtable exigem
confirmação, releitura e uma segunda execução para provar idempotência.

Decisões tomadas durante a implementação das frentes ficam em
`IMPLEMENTATION_DECISIONS.md` para auditoria antes da publicação.
