---
name: generate-image
description: Gera, edita e refina imagens de posts da InsideOut com a geração nativa de imagens da OpenAI, compondo post, marca, produto, referência visual e lettering e registrando a peça no Airtable. Use quando o usuário pedir imagem, arte, mockup, visual, key visual, capa, Feed, Story, variante ou ajuste visual de um post, com ou sem produto e referência.
---

# Gerar imagem

Criar uma peça visual alinhada ao post e à marca, usando a ferramenta nativa
de geração de imagens. O Airtable guarda o estado e a trilha da peça; esta skill
guarda o julgamento de composição.

## Contexto obrigatório

Ler antes de operar:

- `../_shared/voz-usuario.md`;
- `../_shared/about-insideout.md`;
- `../_shared/airtable-contract.md`;
- `references/prompt-composition.md`.

Usar o conector oficial do Airtable para dados e a ferramenta nativa
`image_gen` para gerar ou editar. Não chamar SDK, API própria ou script
externo. Não pedir chave de API para o caminho nativo.

## Boundary

Ler `Marcas`, `Produtos`, `Referências`, `Posts` e `Peças`.

Escrever somente:

- um registro de imagem em `Peças`;
- a relação `Post` da peça, que atualiza `Peças` no post automaticamente;
- `Mockup` do post;
- `Arquivo`, `Prompt` e `Status` da peça.

Não alterar briefing, marca, produto, referência, grid, legenda ou lettering.
Não gerar vídeo. Encaminhar texto ausente ou inadequado para `generate-copy`.

## Resolver o pedido

1. Se a imagem pertencer ao grid, localizar exatamente um post por
   `Marca + Data + Título`.
2. Ler o post completo e os registros relacionados de marca, produto,
   referência e peças existentes.
3. Se o pedido for avulso, confirmar marca, finalidade e formato somente quando
   isso mudar materialmente o resultado.
4. Classificar a composição:
   - `produto + referência`;
   - `somente produto`;
   - `somente referência`;
   - `avulsa`, quando o usuário pediu explicitamente uma imagem sem post.
5. Para um post, não inventar produto ou referência ausentes. Se não houver
   nenhum dos dois e o título/rationale não bastar, pedir uma direção visual.

## Tratar conflitos

- Se o post já tiver `Mockup` ou peça de imagem, mostrar um resumo e perguntar:
  reutilizar, refinar, criar variante ou substituir o mockup atual.
- Nunca sobrescrever ou descartar uma peça silenciosamente.
- Se a mesma peça já tiver o mesmo prompt e arquivo, reutilizar sem chamar
  `image_gen`.
- Nomear variantes com versão crescente; manter as versões anteriores.

## Fidelidade do produto

Usar `preservar` como padrão para produto real:

- tratar a foto principal como alvo de edição;
- manter embalagem, rótulo, proporções, cores e material inalterados;
- compor cenário, luz e sombra ao redor;
- repetir essas invariantes no prompt e em cada refinamento.

Usar `recriar` somente com aprovação explícita quando for necessário mudar
ângulo, pose ou integração:

- usar as fotos disponíveis como referências;
- avisar que detalhes de embalagem e rótulo podem variar;
- exigir conferência visual antes de salvar.

## Preparar e aprovar

1. Mapear o canal:
   - Feed e carrossel: composição quadrada ou retrato social;
   - Story e Reel: composição vertical;
   - capa horizontal: composição paisagem.
2. Inspecionar toda imagem de entrada antes de gerar.
3. Rotular o papel de cada imagem: alvo de edição, referência de produto ou
   referência de estilo.
4. Compor o prompt estruturado pelo guia de referência.
5. Incluir o `Lettering` exatamente como aprovado. Sem lettering, não colocar
   headline, claim, logotipo textual ou mensagem-chave por iniciativa própria.
6. Mostrar antes da geração:
   - direção visual;
   - modo `preservar` ou `recriar`;
   - formato;
   - texto exato que entrará na imagem;
   - prompt final.
7. Aguardar aprovação, exceto quando o usuário já aprovou explicitamente esse
   prompt final na mesma conversa.

## Gerar com OpenAI

- Para uma imagem nova sem entradas, chamar `image_gen` sem imagens anexadas.
- Para entradas locais, usar `referenced_image_paths`.
- Para imagens já visíveis na conversa sem caminho local, usar apenas o menor
  `num_last_images_to_include` que inclua todas.
- Nunca usar `referenced_image_paths` e `num_last_images_to_include` juntos.
- Gerar uma chamada por peça ou variante; não juntar peças distintas numa
  única chamada.
- Em edição, declarar o alvo e repetir o que deve permanecer invariável.
- Em refinamento, alterar um aspecto por vez e usar a última imagem aprovada
  como alvo.

## Conferir o resultado

Inspecionar a imagem antes de persistir:

- produto e embalagem fiéis ao modo escolhido;
- lettering verbatim, legível e na área segura;
- marca, paleta, mood, composição e guardrails coerentes;
- proporção adequada ao canal;
- ausência de claims, logos, marcas d'água, dedos, objetos ou textos
  inventados;
- luz e sombra coerentes entre produto e cenário.

Se houver defeito objetivo, fazer no máximo uma correção direcionada sem
ampliar o conceito. Se a correção exigir nova direção criativa, mostrar o
problema e pedir escolha.

## Persistir no Airtable

Depois da imagem válida:

1. Copiar o arquivo final para um caminho estável no workspace antes de
   vinculá-lo ao projeto.
2. Montar a auditoria com modo, tipo de composição, formato, papéis das imagens
   de entrada e prompt final.
3. Localizar a peça pela chave `Post + Tipo + Nome`; para peça avulsa sem
   post, usar `Marca + Tipo + Nome`.
4. Criar ou atualizar a peça com:
   - `Tipo = Imagem`;
   - relações de marca, produto, referência e post quando aplicáveis;
   - `Prompt` com a auditoria completa;
   - `Status = Gerada`;
   - arquivo final em `Arquivo`.
5. Anexar o mesmo arquivo em `Mockup` do post somente após resolver qualquer
   conflito existente.
6. Se o conector não transportar arquivo local, usar a interface do Airtable
   somente para o upload nos registros já resolvidos; manter o conector para
   campos e relações.
7. Reler peça e post e confirmar arquivo, prompt, status e relações.
8. Marcar `Aprovada` somente após aprovação humana explícita.

Não declarar conclusão enquanto o arquivo existir apenas no diretório local.

## Resposta

Mostrar a imagem inline e informar:

- post ou finalidade;
- direção aplicada;
- modo de fidelidade;
- o que foi criado, reutilizado ou atualizado;
- se a peça está `Gerada` ou `Aprovada`;
- próximo passo: aprovar, refinar ou enviar para `qa-visual`.

Não expor IDs, caminhos internos, chamadas de ferramenta ou detalhes de upload.
