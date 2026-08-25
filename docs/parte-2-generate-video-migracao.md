# Parte 2 — migração de `generate-video`

> **Data:** 21/08/2026  
> **Estado:** implementada e validada estruturalmente  
> **Motor:** Higgsfield  
> **Próximo gate:** executar os evals da skill em tasks isoladas

## O que foi preservado do fluxo anterior

- imagem-âncora como caminho preferencial para consistência;
- enriquecimento de câmera, movimento, ritmo, luz e atmosfera;
- prompt apresentado antes da geração;
- confirmação humana antes de um trabalho caro;
- formatos verticais para Story e Reel;
- vínculo obrigatório com o post quando a peça pertence ao grid.

## O que mudou

| Antes | Agora |
|---|---|
| Veo por script e chave própria | conector instalado do Higgsfield |
| custo aproximado | estimativa exata em créditos antes de gerar |
| imagem opcional por caminho local | frame inicial enviado no papel próprio |
| saída em `outputs/` | arquivo estável + `Peças.Arquivo` + `Posts.Vídeo` |
| conferência geral | inspeção do primeiro, meio e último frame |
| nova tentativa implícita | retry pago exige nova estimativa e aprovação |
| sobrescrita operacional | versões crescentes e preservação das anteriores |

## Estrutura criada

```text
.codex/skills/generate-video/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── video-prompting.md
└── evals/
    ├── conflito-video.md
    ├── custo-e-retry.md
    ├── frame-inicial-produto.md
    └── idempotencia-video.md
```

O contrato compartilhado do Airtable foi ampliado para definir anexos,
auditoria, versionamento e idempotência de vídeos.

## Decisões operacionais

- image-to-video é o padrão para marcas e produtos reais;
- a aparência vem do frame aprovado; o prompt dirige o movimento;
- áudio fica desligado quando não foi solicitado;
- custo, modelo, duração, resolução, áudio e quantidade precisam ser aprovados;
- nenhuma tentativa adicional paga acontece automaticamente;
- `Status = Aprovada` depende de aprovação humana explícita;
- uma URL temporária do gerador nunca é tratada como arquivo final persistido.

## Gate do harness

Executar os quatro prompts em `evals/`, cada um numa task nova, e conferir:

1. seleção correta do frame inicial e preservação do produto;
2. estimativa e aprovação antes de consumir créditos;
3. ausência de sobrescrita diante de vídeo existente;
4. ausência de geração e anexos duplicados na reexecução;
5. persistência em `Peças` e `Posts.Vídeo` com releitura no Airtable.
