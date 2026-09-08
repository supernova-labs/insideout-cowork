---
name: generate-grid
description: Gera, revisa e atualiza o primeiro take mensal da InsideOut, compondo estrutura, rationale, briefing de design, copy, tendências curadas e snapshot HTML. Use quando o usuário pedir para montar ou revisar um grid, distribuir posts entre redes ou preparar a validação visual de um mês.
---

# Gerar grid editorial InsideOut

Transforme uma ficha mensal aprovada em um primeiro take completo e revisável.
Orquestre capacidades especializadas sem absorver suas responsabilidades e
persista somente os posts aprovados.

## Preparar

1. Leia `../../references/_shared/voz-usuario.md`,
   `../../references/_shared/about-insideout.md` e `../../references/_shared/airtable-contract.md`.
2. Leia `references/planning-method.md` e `references/design-briefing.md`.
3. Leia `references/calendar/<ano>.md` para o mês solicitado.
4. Leia `references/trend-context.md` ao gerar um novo grid ou quando houver
   pesquisa, fonte ou candidato de tendência em escopo.
5. Leia `references/html-snapshot.md` quando o pedido incluir visualização ou
   quando o primeiro take aprovado precisar de snapshot para revisão.
   Leia também `references/site-access.md` quando a visualização for publicada.
6. Descubra a base **InsideOut Social**, o schema atual e os registros de marca,
   canais, produtos, referências e diretrizes necessários.
7. Use a ficha aprovada de `analyze-briefing` ou confirme marca, mês, focos,
   lançamentos e direcionais diretamente com o usuário.

## Executar

### 1. Auditar o mês

Antes de planejar, procure posts da mesma marca no mês e separe-os por rede.

- Se não houver, continue.
- Se houver, apresente quantidade e cobertura e peça uma escolha: revisar o que
  existe, preencher lacunas ou substituir.
- Não altere posts existentes até receber a escolha.
- Substituição nunca significa apagar automaticamente; atualize registros
  correspondentes e trate sobras separadamente.

### 2. Resolver ativos

- Localize a marca por `Slug`; não crie marca nesta skill.
- Localize `Canais da marca` por `Marca + Rede`; use somente canais ativos e
  formatos habilitados.
- Cada post novo recebe exatamente um `Canal da marca`. Zero, múltiplos ou
  duplicidade na chave bloqueiam esse post até a configuração ser corrigida.
- Localize produtos por `Marca + Slug`; reporte produtos ausentes antes de
  depender deles.
- Resolva as versões ativas de `Diretrizes de grid` conforme
  `references/planning-method.md`. Conflito entre versões ativas bloqueia o
  planejamento; ausência de regra de marca não autoriza copiar outra marca.
- Reutilize referências existentes.
- Só crie referência quando o usuário fornecer ou aprovar nome, tipo e
  prompt/URL explícitos.
- Um post pode ficar sem referência na Parte 1; não invente uma para completar.

### 3. Curar tendências quando aplicável

Com o contexto mínimo resolvido, consulte os perfis de referência cadastrados
para a marca e a rede e faça busca recente na internet aberta. Procure fenômenos
sociais em circulação, não padrões históricos ou boas práticas genéricas.
Apresente poucas candidatas com mecanismo, atualidade, evidência de circulação,
adaptação e risco. Candidata pendente, rejeitada, vencida ou sustentada por uma
única ocorrência não influencia o plano. A trilha de fontes fica na execução;
o grid não precisa atribuir cada post a uma fonte. Se nenhuma candidata for
adequada, continue sem trend. Não persista tendências nesta versão.

### 4. Montar o primeiro take

Aplique o briefing aprovado e as diretrizes ativas na ordem definida por
`references/planning-method.md`:

- construa o panorama mensal antes de detalhar os posts;
- respeite âncoras, intensidade, cadência, respiros e composição aprovados;
- não transforme padrão histórico em obrigação;
- registre uma frase de rationale em todos os posts;
- adapte cada ideia a uma única rede; reaproveitamento entre redes gera posts
  distintos, com intenção, formato e contexto próprios;
- escreva um `Briefing de design` estruturado para cada post, sem duplicar
  `Lettering`;
- passe o contexto estruturado de cada post para `generate-copy` produzir
  `Lettering` e `Legenda` ainda sem persistência.

Planeje o mês inteiro antes de escrever. Apresente um artefato composto com
estrutura, rationale, briefing de design, lettering e legenda, além da síntese
por rede, formato e abordagem.

### 5. Aprovar o lote com exceções

Peça uma decisão para o lote e aceite exceções por post. A aprovação precisa
identificar os posts que avançam, os que permanecem em revisão e eventuais
ajustes. Um post pendente não bloqueia os aprovados e não é persistido.

### 6. Persistir por responsabilidade

- Crie somente os posts aprovados como `Rascunho`.
- Escreva lotes de até 10.
- Preencha `Título`, `Data`, `Marca`, `Canal da marca`, `Canal`, `Abordagem`,
  `Rationale` e `Briefing de design`.
- Vincule produto e referência quando resolvidos.
- Deixe `Mockup`, `Vídeo` e `Peças` vazios.
- Depois de criar ou reutilizar o post, entregue-o a `generate-copy` para que
  essa skill escreva e releia somente `Lettering` e `Legenda` aprovados.
- Use `Marca + Canal da marca + Data + Título` para localizar o mesmo post;
  para legado sem rede, use a chave anterior e pare diante de duplicidade.
- Releia cada lote e verifique campos e relações.

### 7. Gerar o snapshot quando solicitado

Depois de compor o take selecionado, gere o HTML conforme
`references/html-snapshot.md`. O arquivo é uma visão de revisão, não uma nova
fonte de verdade: vive fora do pacote, não lê nem escreve no Airtable e não
substitui as aprovações das skills.

Quando o pedido incluir um link de revisão, publique o snapshot conforme
`references/site-access.md`: valide e publique primeiro apenas para o
proprietário. Adicionar visitantes externos por email é uma mudança de acesso
separada, feita somente depois de mostrar a lista exata e receber confirmação.

### 8. Apresentar

Informe:

- quantidade de posts;
- distribuição por rede, formato e abordagem;
- produtos-foco e datas-âncora;
- posts aprovados, em revisão e não persistidos;
- lacunas ou conflitos;
- caminho do snapshot, quando gerado, com marca, mês e versão em linguagem de
  negócio;
- link e estado de acesso do Site, quando publicado, sem tratar convite como
  parte automática da publicação.

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
- Todo post novo pertence a um único canal ativo e formato habilitado.
- Nenhum post existente foi alterado sem escolha explícita.
- Todo post novo tem título, data, marca, canal da marca, formato, abordagem,
  rationale, briefing de design e status.
- Produtos e referências apontam para os registros corretos.
- As diretrizes aplicadas estavam ativas, pertenciam ao escopo correto e não
  tinham versões concorrentes.
- Lettering e legenda foram produzidos e persistidos por `generate-copy`.
- Somente posts aprovados foram persistidos; exceções permanecem em revisão.
- Tendências que influenciaram o take estão rastreáveis e dentro da validade.
- A ausência de tendência adequada não bloqueou nem empobreceu artificialmente
  o grid.
- Repetir o mesmo fluxo não cria duplicatas.
- O primeiro take está completo; não apresente somente um calendário vazio ou
  um conjunto de campos sem contexto visual.
- Site publicado começa restrito ao proprietário; acesso externo contém somente
  os emails confirmados.

## Limites

- Não criar ou atualizar marcas e produtos.
- Não criar ou atualizar `Canais da marca`.
- Não escrever legenda ou lettering; orquestrar `generate-copy` para isso.
- Não gerar imagem, vídeo ou peça real.
- Não preencher referência por suposição.
- Não permitir que tendência não aprovada ou vencida influencie o take.
- Não chamar padrão histórico, boa prática ou publicação isolada de trend.
- Não incluir aplicação, painel, hospedagem ou estado operacional no plugin.
- Não publicar Site aberto à internet nem adicionar visitantes externos sem
  confirmação específica da lista de emails.
- Não apagar posts automaticamente.
