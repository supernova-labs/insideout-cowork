# Saídas HTML do grid

Gere uma visão portátil para revisão do primeiro take ou um resumo de
calendário para cliente. O arquivo não é painel, aplicação nem fonte
operacional.

## Local e nome

Salve fora do diretório do plugin, em local escolhido pelo usuário ou numa
pasta de artefatos do workspace. Para revisão interna, use:

```text
insideout-grid-<slug-da-marca>-<AAAA-MM>-<versao>.html
```

Para o resumo para cliente, use:

```text
insideout-grid-<slug-da-marca>-<AAAA-MM>-cliente-<versao>.html
```

Não sobrescreva arquivo existente; incremente a versão ou use momento de
geração inequívoco.

## Snapshot de revisão interna

Siga também `review-presentation.md` para a identidade da apresentação, a
hierarquia semanal e a estrutura dos cards. Essa referência vale para a casca
de revisão; os briefs das peças preservam a identidade visual da marca ou
campanha.

Mostre no cabeçalho:

- marca e mês;
- versão ou momento do snapshot;
- estado `revisão interna — primeiro take`;
- quantidade e distribuição por rede e formato.

Para cada post, mostre em linguagem de negócio:

- data, rede, formato, abordagem, título e produto;
- rationale;
- briefing de design organizado por tela;
- links clicáveis das referências visuais usadas;
- link direto do post ou vídeo que exemplifica uma trend aplicada;
- lettering posicionado junto à tela correspondente;
- legenda;
- lacunas, oportunidade de momento aplicada, estado dos assets finais e estado
  de revisão quando aplicáveis.

Organize os posts cronologicamente em blocos semanais. Use elementos nativos
expansíveis para que direção criativa, texto da arte e legenda sejam fáceis de
consultar sem tornar o mês difícil de escanear.

Não mostre IDs, schema, logs, prompt interno, registros não selecionados, URLs
privadas, a trilha completa de pesquisa ou campos operacionais desnecessários.
Links editoriais aprovados e exemplos públicos de trends não são URLs privadas.

## Resumo para cliente

O snapshot de revisão é interno e pode mostrar rationale, briefing de produção,
lacunas e referências. Não o apresente como entrega final ao cliente.

Quando o pedido incluir uma entrega para cliente, gere um segundo HTML a partir
dos mesmos posts. Não aplique a este formato as regras do snapshot de revisão
interna nem `review-presentation.md`.

Antes de montar o resumo, releia `Posts.Mockup` e as `Peças` vinculadas de cada
post. Um post é elegível somente quando o mockup selecionado corresponde ao
arquivo de uma `Peça` vinculada com status `Aprovada`. Preserve no resumo
cronológico apenas os posts elegíveis, com data, rede/formato, título, foco de
conteúdo e a imagem aprovada. O resumo não recebe upload, edição ou comentários
dentro do Site.

No cabeçalho, mostre somente marca, mês, versão e quantidade de posts entregues.
O resumo para cliente omite rationale, briefing de produção, lettering, legenda,
referências, links de trend, lacunas internas, dados operacionais, estado de
revisão e URLs privadas. Um post sem mockup aprovado verificável fica fora da
entrega, com o motivo relatado ao time antes da geração. Nunca use placeholder
como se fosse arte final.

## Revisão para cliente com feedback

Gere este terceiro formato somente quando o pedido pedir explicitamente coleta
de feedback post a post. Ele parte das mesmas regras de elegibilidade e do
mesmo conteúdo seguro do resumo para cliente, mas permite interação local no
navegador. Use este nome:

```text
insideout-grid-<slug-da-marca>-<AAAA-MM>-cliente-feedback-<versao>.html
```

No cabeçalho, inclua marca, mês, versão, quantidade de posts e um aviso claro:
os comentários ficam naquele navegador, o cliente deve exportar o JSON e
encaminhá-lo ao time, e trocar de dispositivo ou limpar dados pode perder o
histórico local. Não inclua qualquer dado interno adicional para viabilizar o
feedback.

Em cada card cronológico elegível, mostre somente data, rede/formato, título,
foco de conteúdo e mockup aprovado. Acrescente **Adicionar feedback**, lista
resumida de comentários do próprio post e ações locais de editar ou remover.
Abra o formulário em um overlay modal nativo, associado ao post selecionado;
não deixe campos ou formulário expandidos nos cards. O overlay mostra o tipo
fixo **Ajuste**, mensagem e revisor opcional. Mensagem é obrigatória. Ao abrir,
mova o foco para o título ou o primeiro campo; ao salvar ou cancelar, feche o
overlay e devolva o foco ao botão do card. Use rótulos visíveis, foco acessível
e botões utilizáveis em tela estreita.

Incorpore um manifesto público com marca, mês, versão, fingerprint do grid e,
em cada post, `postKey` e `postFingerprint` determinísticos. Derive a chave de
data, canal e título normalizados; não exponha IDs, URLs privadas ou campos
operacionais. Siga integralmente
`../../references/_shared/client-feedback-package.md` para o formato do
manifesto, `localStorage`, JSON canônico, CSV complementar e restrições de
segurança.

O botão **Exportar feedback** baixa o JSON canônico localmente e
**Exportar CSV** baixa a cópia complementar. Não ofereça envio, upload ou
sincronização. Desabilite ou explique a exportação quando ainda não houver
comentários. Ofereça limpar comentários somente com confirmação explícita.

## Implementação do arquivo

- HTML sem dependências externas obrigatórias;
- CSS embutido e responsivo;
- JavaScript embutido opcional para navegação, filtros ou interação local da
  revisão de cliente com feedback;
- nenhuma chamada de rede, formulário remoto, upload, escrita remota ou
  persistência fora do navegador; `localStorage` e downloads locais são
  permitidos apenas no formato de feedback;
- estrutura semântica, contraste legível, foco visível e conteúdo utilizável sem
  JavaScript;
- indique lacunas com texto, não apenas cor;
- inclua `lang="pt-BR"`, título descritivo e viewport mobile.

## Verificação

Antes de entregar:

1. abra o arquivo localmente;
2. revise desktop e viewport estreito;
3. confira ausência de requisições externas e de dados internos;
4. compare contagem e conteúdo com o take selecionado;
5. confira que referências e trends aplicadas abrem os links esperados na
   revisão interna;
6. no resumo para cliente, confira que cada imagem vem do mockup aprovado do
   post correto e que o calendário preserva todas as datas entregues;
7. na revisão com feedback, crie, edite, remova, recarregue e exporte ao menos
   um comentário; confira JSON, cabeçalho CSV, escaping e ausência de rede;
8. informe que uma nova revisão gera outro arquivo, sem sobrescrever o anterior.
