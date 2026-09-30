# Layout HTML do Mar Aberto

## Estrutura aprovada

O relatório é um único arquivo HTML autocontido. O modelo distribuído em
assets/report-template.html fixa a linguagem visual derivada das páginas de
Mar Aberto do material editável de 16/09 e do PDF de 23/09: formato vertical
10 × 13, capa com imagem do produto, azul escuro, acento ciano, painéis
claros, tipografia Inter, gráficos amplos, cartões de evidência e rodapé com
fonte/período e marcas. A aprovação visual do protótipo do i20 definiu esse
caminho para novas execuções; seus números e comentários não fazem parte do
modelo.

O modelo contém espaços nomeados para capa, resumo, panorama, canal, séries,
cobertura, conclusões, metodologia e encerramento. Repita a página de canal
para cada rede com dados e a página de séries quando necessário. Retire
espaços não usados. A ordem de leitura é: escopo e resumo; corpus e canais;
evidências; cobertura; conclusões; método. Métricas de campanha ou CM que não
vieram da exportação de Mar Aberto não são inferidas.
Os elementos template no fim do arquivo mostram a estrutura exata de barra
de sentimento, mapa de temas, gráfico de colunas e cartão de citação. Use
essas estruturas com os dados canônicos; remova os elementos de exemplo do
arquivo final.

## Conteúdo e gráficos

- Use HTML sem scripts e sem recursos externos. Incorpore CSS, fontes e
  imagens autorizadas como dados locais; escape qualquer texto vindo de
  publicação, comentário ou evidência antes de inserir no documento.
- Mantenha títulos, números, rótulos, análises e citações como texto
  selecionável. Use elementos semânticos: section, figure, figcaption,
  table e blockquote. Navegação interna aponta apenas para âncoras do próprio
  documento.
- Barras horizontais e colunas empilhadas representam os cinco sentimentos
  com a paleta da planilha. Mostre legenda, fonte, período, tipo de registro e
  denominador. A soma das partes de cada barra deve ser 100% dentro de
  arredondamento; totais vêm dos agregados, não do desenho.
- Menções, comentários e respostas não compartilham denominador. Uma única
  data de menções pede barras por publicação, rotuladas como tal. Datas de
  comentários e respostas são published_at do registro, nunca instante de
  observação.
- Temas podem ter círculos proporcionais ou outra visualização de frequência.
  Mostre todos os temas materiais do canal e calcule-os apenas com registros
  desse canal. Não desenhe conexões sem coocorrência validada.
- Coloque citações somente do conjunto aprovado, com sentimento, canal e tipo
  de fonte visíveis. Neutros e mistos recebem títulos próprios, fora de uma
  seção classificada como negativa. Não exponha autor, perfil, foto ou link
  individual de pessoa.
- No modo de cobertura limitada, identifique a limitação na capa, resumo,
  canal afetado, cobertura, conclusões e metodologia. Não projete itens que a
  interface não revelou.

## Responsividade e impressão

A leitura em tela usa páginas de até 960 pixels com navegação e colunas
responsivas. A impressão mantém a proporção de 10 × 13 polegadas, cores de
fundo, cabeçalho e rodapé. Se um gráfico, citação ou parágrafo exceder a área
legível, crie outra página no mesmo estilo. Não reduza o corpo para caber à
força. Garanta contraste de texto sobre painéis, círculos e cartões; não use
somente cor para distinguir sentimentos. A equipe pode editar o HTML depois
da entrega e exportar PDF manualmente pelo navegador.
Na impressão, confira se o rodapé aparece em cada folha e se o conteúdo não o
cobre. Os gráficos devem reservar área própria para rótulos do eixo; quando
as datas couberem na horizontal, não as incline sobre as barras. Confira esses
pontos na exportação, pois o texto pode
continuar extraível do PDF mesmo quando não aparece na página renderizada.

## Verificação

Reabra o arquivo gerado. Confira que ele funciona sem rede, tem navegação
interna válida, fontes e imagem de capa disponíveis, todos os canais com dados,
oito abas no XLSX parceiro e nenhuma citação fora do Gate 1. Reconcilie cada
barra e número com agregados e planilha. Renderize todas as páginas na largura
normal de leitura e no modo de impressão, verificando que não há cortes,
sobreposições ou texto pequeno. Compare capa, panorama, canais, séries e
rodapé com as páginas equivalentes do PDF de referência. O arquivo abrir e
passar na checagem estática não substitui a inspeção visual. Se o ambiente
bloquear essa renderização, registre a pendência em vez de afirmar que passou.
