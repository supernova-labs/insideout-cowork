# Parte 2 — relatório de migração e validação de `generate-copy`

> **Data:** 26/07/2026  
> **Resultado:** skill migrada e aprovada para uso experimental  
> **Próximo incremento:** geração de imagem nativa  
> **Adiado:** geração de vídeo

## O que foi implementado

- skill `generate-copy` dentro de `.codex/skills`;
- operação conversacional para criar e revisar legenda, hook, CTA e lettering;
- leitura do post, da marca e do produto antes da redação;
- aprovação humana obrigatória antes da escrita;
- escrita limitada aos campos `Legenda` e `Lettering`;
- preservação dos demais campos do post;
- tratamento de conflito quando já existe copy diferente;
- reexecução idempotente quando a copy aprovada já está salva;
- quatro evals: legenda sem claim, lettering injetável, conflito com copy
  existente e idempotência.

## Prova controlada no Airtable

O post `[TESTE CODEX] Aurora 24H: lançamento`, de 12/05/2026, foi localizado
pela chave natural composta por marca, data e título.

Após a escolha explícita do hook 1, a skill salvou exatamente a legenda
aprovada:

> Chegou um novo gesto de conforto.
>
> Aurora 24H estreia hoje e abre uma conversa sobre hidratação, rotina e pele sensível.
>
> Uma novidade apresentada com simplicidade e foco na experiência cotidiana.
>
> Conheça Aurora 24H e conte: o que faz um cuidado parecer confortável para você?

E o seguinte bloco de lettering:

```text
LETTERING
headline: Conforto começa na pele
apoio: Conheça Aurora 24H
posição sugerida: topo
hierarquia: headline primária; apoio secundário
```

## Verificações

- exatamente um post correspondeu à chave natural;
- `Legenda` e `Lettering` estavam vazios antes da aprovação;
- somente esses dois campos foram enviados para atualização;
- a releitura devolveu os textos aprovados sem alteração;
- título, data, marca, canal, abordagem, produto, referência, rationale,
  status e relação com a peça de teste foram preservados;
- nenhum claim clínico, número ou benefício não sustentado foi introduzido;
- a segunda execução encontrou conteúdo idêntico e foi tratada como
  reutilização, sem nova escrita material.

## Validação local

O validador compartilhado cobre agora `analyze-briefing`, `generate-grid` e
`generate-copy`. Ele verifica estrutura, referências, evals e descoberta das
skills pelo Codex.

A validação completa de marketplace continua fora deste ciclo. O bloqueio
anterior no manifesto do plugin Claude permanece independente desta migração e
não exigiu alteração.

## Próximo incremento

A geração de imagem deve consumir o post aprovado, o brand guide, o produto, a
referência visual e o lettering. O primeiro teste deve:

1. gerar uma imagem com o recurso nativo;
2. preservar prompt e parâmetros em `Peças`;
3. anexar o arquivo gerado à peça e ao post;
4. reler o Airtable e verificar vínculos e anexos;
5. repetir a operação sem duplicar a peça.

Vídeo será tratado depois que esse fluxo de imagem estiver estável.
