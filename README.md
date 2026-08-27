# InsideOut Social

Plugin Codex da InsideOut para transformar briefings em direção estratégica,
grids editoriais, copy, imagens e vídeos de social media.

## O que ele faz

| Skill | Resultado |
|---|---|
| `analyze-briefing` | Analisa briefing, lacunas e escopo; pode materializar marca e produtos com confirmação. |
| `generate-grid` | Cria ou revisa o primeiro take mensal no Airtable. |
| `generate-copy` | Produz legenda, hooks e lettering para revisão humana. |
| `generate-image` | Gera e registra mockups com trilha de auditoria. |
| `generate-video` | Produz e registra vídeos curtos a partir de direção visual aprovada. |

## Pré-requisitos

- Codex com este plugin instalado.
- Acesso individual à base **InsideOut Social** no Airtable para os fluxos que
  leem ou atualizam dados operacionais.
- Acesso ao recurso criativo indicado pela skill quando houver geração de
  imagem ou vídeo. Esses fluxos podem envolver custo e sempre pedem a
  aprovação prevista no processo.

As skills trabalham em linguagem de marca, produto, post e mês. Elas não
substituem aprovação humana nem completam informações ausentes por hipótese.

## Para quem mantém

As skills em `skills/` são a fonte canônica do plugin. O manifesto Codex fica
em `.codex-plugin/` e o índice de arquitetura em `.agent-smith/`.

Antes de compartilhar uma nova versão, valide a estrutura:

```powershell
python skills/_shared/scripts/validate_skills.py
```

E revise os evals da skill alterada. Evals que escrevem no Airtable exigem
confirmação, releitura e uma segunda execução para provar idempotência.
