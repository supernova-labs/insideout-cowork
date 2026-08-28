---
name: generate-copy
description: Cria e revisa legendas, hooks, CTAs e lettering para posts da InsideOut, adaptados à marca, rede e formato, e salva somente o texto aprovado no Airtable. Use quando o usuário pedir copy, legenda, headline, texto para arte ou Story, variações de hook, revisão de texto ou o primeiro take completo do grid.
---

# Gerar copy InsideOut

Transforme o direcionamento de um post em texto pronto para revisão, sem
inventar claims e sem escrever no Airtable antes da aprovação.

## Preparar

1. Leia `../../references/_shared/voz-usuario.md`, `../../references/_shared/about-insideout.md` e
   `../../references/_shared/airtable-contract.md`.
2. Leia `references/copy-frameworks.md` antes de escrever.
3. Identifique se o pedido é por legenda, lettering, hooks, revisão ou uma
   combinação.
4. Quando o post já existir no grid, descubra a base **InsideOut Social** e
   localize-o por `Marca + Canal da marca + Data + Título`; para registro legado
   sem canal relacionado, use `Marca + Data + Título`.
5. Quando `generate-grid` enviar um post proposto ainda não persistido, use o
   contexto estruturado recebido e não exija um registro prévio para redigir.
6. Leia ou receba o post, a marca, o canal da marca e os produtos vinculados.
   Use a referência visual apenas como contexto de composição; não extraia dela
   claims ou fatos do produto.

Se a chave localizar mais de um post, apresente a duplicidade e não escolha
silenciosamente.

## Reunir o contexto

Use somente fatos explícitos:

- do post: título, data, formato, abordagem, rationale, briefing de design e notas;
- da marca: voz, mensagens-chave, público, posicionamento e guardrails;
- do canal da marca: rede, objetivo editorial, orientações e formatos habilitados;
- do produto: nome, descrição e claims cadastrados;
- do briefing aprovado ou da instrução atual do usuário.

Trate `Voz` e `Guardrails` como restrições. Trate `Claims` como a lista máxima
de promessas permitidas, não como obrigação de usar todas.

Se o produto não tiver claims, escreva sobre o território editorial, ocasião,
rotina ou posicionamento disponível. Não transforme mensagem de marca em
benefício comprovado do produto.

Rede social e formato são dimensões distintas. Adapte linguagem, hook, CTA e
extensão à rede resolvida e ao formato habilitado. Para registro legado sem
`Canal da marca`, use Instagram somente quando outra fonte em escopo o confirmar;
caso contrário, trate a rede como lacuna. Não transplante a mesma copy entre
redes: posts que compartilham uma ideia recebem versões intencionais próprias.

## Criar a proposta

### Legenda

Entregue:

1. três hooks alternativos;
2. um hook recomendado;
3. a legenda completa no formato Hook → Valor → CTA;
4. contagem aproximada de caracteres;
5. uma nota curta sobre fatos ou restrições que orientaram o texto.

O hook fica na primeira linha, sem emoji. O CTA fica em linha própria e pede uma
ação específica. Não inclua hashtags por hábito: use apenas quando vierem da
marca, do briefing ou do usuário.

### Lettering

Entregue o boundary abaixo:

```text
LETTERING
headline: <3–7 palavras>
apoio: <até 12 palavras ou vazio>
posição sugerida: <topo, centro, base, esquerda ou direita>
hierarquia: <headline primária; apoio secundário>
```

O total deve ficar abaixo de 20 palavras. O lettering leva o gancho; a legenda
expande. Evite repetir as mesmas frases nos dois lugares.

### Hooks

Quando o usuário pedir somente hooks, entregue de três a cinco alternativas e
indique a recomendada. Não produza legenda ou lettering sem necessidade.

## Revisar com o usuário

Apresente o texto antes de escrever. Peça escolha explícita do hook e aprovação
da versão final.

Se `Legenda` ou `Lettering` já tiver conteúdo, mostre um resumo e peça uma
escolha: preservar, substituir pela proposta ou revisar sem salvar. Nunca
concatene versões automaticamente.

Para o primeiro take mensal orquestrado por `generate-grid`, redija o lote
completo e devolva cada `Lettering` e `Legenda` associado à chave proposta do
post. A apresentação pode agrupar os posts para leitura, mas a aprovação deve
identificar exatamente quais textos serão salvos e quais permanecem em revisão.

## Salvar no Airtable

Após aprovação explícita:

- atualize somente `Legenda` e/ou `Lettering` no post resolvido;
- preserve título, data, marca, canal, abordagem, produto, referência,
  rationale, notas, status e anexos;
- releia o registro e confirme o texto salvo;
- na reexecução, trate o mesmo texto como reutilizado, sem mudança material.

Na orquestração, aguarde `generate-grid` persistir somente os posts aprovados;
depois escreva os campos de copy nesses registros e releia cada um. Não escreva
copy de post recusado ou ainda em revisão.

Informe o resultado em linguagem de negócio. Não exponha IDs ou detalhes do
conector.

## Validar

- O texto usa somente fatos e claims disponíveis.
- A voz e os guardrails da marca foram respeitados.
- O hook cabe no corte inicial do canal e não começa com emoji.
- A legenda contém valor e CTA específico em linha isolada.
- O lettering tem no máximo dois níveis e menos de 20 palavras.
- Lettering e legenda se complementam.
- Rede e formato foram resolvidos separadamente e a copy está adaptada aos dois.
- Nenhum texto foi salvo antes da aprovação.
- A releitura confirma que somente os campos aprovados mudaram.

## Limites

- Não criar nem alterar marca, produto, referência ou post.
- Não mudar status nem considerar a copy aprovada pelo cliente.
- Não gerar imagem, vídeo ou registro em `Peças`.
- Não pesquisar ou inventar claim para completar a narrativa.
- Não substituir texto existente sem escolha explícita.
- Não persistir um post proposto; essa responsabilidade permanece em
  `generate-grid`.
