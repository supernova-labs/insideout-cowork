---
name: generate-grid
description: Gera, revisa e atualiza grids editoriais mensais da InsideOut diretamente no Airtable, com regras de marca, calendário, vínculos e rationale auditável. Use quando o usuário pedir para montar o grid de um mês a partir de briefing, distribuir posts ou ajustar datas e conteúdos do calendário.
---

# Gerar grid editorial InsideOut

Transforme uma ficha mensal aprovada em um primeiro take completo de posts no
Airtable.

## Preparar

1. Leia `../../references/_shared/voz-usuario.md`,
   `../../references/_shared/about-insideout.md` e `../../references/_shared/airtable-contract.md`.
2. Leia `references/planning-method.md`.
3. Leia integralmente `references/rules/<slug-da-marca>.md` quando existir.
4. Leia `references/calendar/<ano>.md` para o mês solicitado.
5. Descubra a base **InsideOut Social**, o schema atual e os registros de marca,
   produtos e referências necessários.
6. Use a ficha aprovada de `analyze-briefing` ou confirme marca, mês, focos,
   lançamentos e direcionais diretamente com o usuário.

## Executar

### 1. Auditar o mês

Antes de planejar, procure posts da mesma marca no mês.

- Se não houver, continue.
- Se houver, apresente quantidade e cobertura e peça uma escolha: revisar o que
  existe, preencher lacunas ou substituir.
- Não altere posts existentes até receber a escolha.
- Substituição nunca significa apagar automaticamente; atualize registros
  correspondentes e trate sobras separadamente.

### 2. Resolver ativos

- Localize a marca por `Slug`; não crie marca nesta skill.
- Localize produtos por `Marca + Slug`; reporte produtos ausentes antes de
  depender deles.
- Reutilize referências existentes.
- Só crie referência quando o usuário fornecer ou aprovar nome, tipo e
  prompt/URL explícitos.
- Um post pode ficar sem referência na Parte 1; não invente uma para completar.

### 3. Montar o primeiro take

Aplique `references/planning-method.md` e as regras específicas da marca:

- ancore lançamentos e datas relevantes;
- organize trincas de feed quando fizer sentido;
- concentre produtos-foco no início sem repetir mecanicamente;
- use heroes e complementares como respiro;
- varie Feed, Story e Reel;
- evite intervalo maior que dois dias sem post, salvo direção explícita;
- registre uma frase de rationale em todos os posts.

Planeje o mês inteiro antes de escrever. Mostre uma síntese da distribuição e
obtenha aprovação para criar o primeiro take.

### 4. Escrever no Airtable

- Crie posts como `Rascunho`.
- Escreva lotes de até 10.
- Preencha `Título`, `Data`, `Marca`, `Canal`, `Abordagem` e `Rationale`.
- Vincule produto e referência quando resolvidos.
- Deixe `Lettering`, `Legenda`, `Mockup`, `Vídeo` e `Peças` vazios.
- Use `Marca + Data + Título` para localizar o mesmo post numa reexecução.
- Releia cada lote e verifique campos e relações.

### 5. Apresentar

Informe:

- quantidade de posts;
- distribuição por canal e abordagem;
- produtos-foco e datas-âncora;
- lacunas ou conflitos;
- que o grid está pronto como primeiro take para revisão nas views do Airtable.

Não exponha IDs ou detalhes do conector.

## Editar um grid existente

- Mover: atualize a data do registro e reavalie cadência e âncoras.
- Trocar: atualize os dois registros sem criar novos.
- Editar: altere somente os campos solicitados e preserve os demais.
- Esvaziar ou remover: explique o efeito e peça confirmação explícita.
- Depois de qualquer edição, releia o mês e avise se a mudança quebrar uma
  regra objetiva; não bloqueie uma decisão editorial humana.

## Validar

- O mês correto e a marca correta foram usados.
- Nenhum post existente foi alterado sem escolha explícita.
- Todo post novo tem título, data, marca, canal, abordagem, rationale e status.
- Produtos e referências apontam para os registros corretos.
- Repetir o mesmo fluxo não cria duplicatas.
- O primeiro take está completo; não apresente somente um calendário vazio.

## Limites

- Não criar ou atualizar marcas e produtos.
- Não escrever legenda ou lettering.
- Não gerar imagem, vídeo ou peça real.
- Não preencher referência por suposição.
- Não apagar posts automaticamente.
