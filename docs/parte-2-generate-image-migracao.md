# Parte 2 — migração de `generate-image`

> **Data:** 26/07/2026  
> **Estado:** implementada e validada estruturalmente  
> **Motor:** geração nativa de imagens da OpenAI  
> **Próximo gate:** prova controlada com imagem e anexos no Airtable

## O que foi preservado do fluxo anterior

A implementação antiga usava Gemini, bibliotecas locais e arquivos JSON, mas a
parte essencial era o julgamento de composição. A nova skill preserva:

- junção entre post, marca, produto, referência visual e lettering;
- três modos: produto + referência, somente produto e somente referência;
- distinção entre `preservar` e `recriar` o produto;
- enriquecimento obrigatório de iluminação, mood, textura, atmosfera e
  composição;
- área segura e lettering verbatim;
- apresentação do prompt final antes da geração;
- inspeção visual antes de persistir;
- refinamento conversacional com uma mudança por vez;
- trilha de auditoria e idempotência.

## O que mudou

| Antes | Agora |
|---|---|
| Gemini com chave própria | geração nativa da OpenAI, sem chave no fluxo padrão |
| `product-catalog` local | tabelas `Marcas` e `Produtos` |
| `style-gallery` local | tabela `Referências` |
| grid em JSON | tabela `Posts` |
| sidecar JSON | registro em `Peças`, com auditoria no campo `Prompt` |
| PNG num caminho canônico do grid | anexo em `Peças.Arquivo` e `Posts.Mockup` |
| sessão do motor em arquivo local | edição da última imagem como alvo explícito |
| sobrescrita do PNG do dia | versões crescentes, sem destruir a peça anterior |

Não foram migrados o `core/`, scripts Python, `.env`, estimativa de custo do
Gemini ou armazenamento local de sessão.

## Estrutura criada

```text
.codex/skills/generate-image/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── prompt-composition.md
└── evals/
    ├── produto-preservar.md
    ├── referencia-sem-produto.md
    ├── conflito-mockup.md
    └── idempotencia-imagem.md
```

O contrato compartilhado do Airtable foi ampliado para definir versionamento,
status, prompt auditável, anexos e reexecução.

## Decisões de segurança criativa

- `preservar` é o padrão para fotografia real de produto;
- `recriar` exige aprovação explícita e conferência de embalagem e rótulo;
- texto só entra quando já existe lettering aprovado ou o usuário pede;
- mensagens-chave e claims orientam, mas não viram texto automaticamente;
- mockups e peças existentes nunca são substituídos silenciosamente;
- `Aprovada` só é aplicada após decisão humana.

## Gate da prova controlada

O primeiro teste deve usar o post
`[TESTE CODEX] Aurora 24H: lançamento`, que já tem marca, produto, referência e
lettering aprovados:

1. reler o contexto completo;
2. montar e aprovar um prompt em modo `preservar`;
3. gerar uma imagem nativa;
4. inspecionar produto, lettering, marca e formato;
5. criar uma nova peça `Imagem` com status `Gerada`;
6. anexar o arquivo em `Peças.Arquivo` e `Posts.Mockup`;
7. reler os dois registros;
8. repetir o pedido e confirmar reutilização sem nova geração.

O ponto ainda não provado é o transporte do arquivo local para os campos de
anexo do Airtable. A skill prevê usar a interface autenticada somente para esse
upload quando o conector não transportar o arquivo; todo o restante continua
pelo conector.
