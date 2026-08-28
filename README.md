# InsideOut Social

Plugin oficial da InsideOut para transformar briefings em direção estratégica,
grids editoriais, copy, imagens e vídeos de social media.

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
| `analyze-briefing` | Analisa briefing, lacunas e escopo; pode materializar marca e produtos com confirmação. |
| `generate-grid` | Cria ou revisa o primeiro take mensal no Airtable. |
| `generate-copy` | Produz legenda, hooks e lettering para revisão humana. |
| `generate-image` | Gera e registra mockups com trilha de auditoria. |
| `generate-video` | Produz e registra vídeos curtos a partir de direção visual aprovada. |

## Pré-requisitos

- Codex instalado.
- Acesso individual à base **InsideOut Social** no Airtable para os fluxos que
  leem ou atualizam dados operacionais.
- Acesso ao recurso criativo indicado pela skill quando houver geração de
  imagem ou vídeo. Esses fluxos podem envolver custo e seguem as aprovações
  previstas no processo.

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
