# Eval — fidelidade e legibilidade do relatório HTML

## Prompt

> Com Gate 1 aprovado e dados sintéticos, gere o relatório com o template
> HTML distribuído. Compare todas as páginas com a estrutura do PDF padrão de
> 23/09 e o protótipo HTML aprovado. O recorte tem publicações de um só dia,
> comentários em datas posteriores, cinco sentimentos e somente Instagram e
> YouTube. Inclua uma citação longa e uma pergunta neutra.

## Resultado esperado

- usa o CSS e a hierarquia do modelo: capa, resumo, régua azul, painéis
  claros, mapas proporcionais, gráficos amplos, cartões, rodapé e fim;
- gera arquivo HTML autocontido, sem scripts ou chamadas de rede; fontes e
  imagem autorizadas estão disponíveis offline;
- contém só canais com dados e acrescenta páginas quando necessário;
- mantém texto selecionável, navegação interna e visual responsivo;
- renderiza todas as páginas em tela e impressão e compara as áreas
  equivalentes com a referência; não aceita corte, sobreposição, baixo
  contraste ou texto que exija zoom para leitura; exige rodapé visível em cada
  página analítica e rótulos dos eixos sem colisão com barras ou notas;
- preserva cinco sentimentos e os três denominadores separados;
- identifica barras por publicação quando há um só dia de menções, sem
  chamá-las de série diária; chama o eixo de comentários de data de publicação;
- calcula temas do Instagram somente com registros do Instagram e não inventa
  relação entre termos;
- rotula pergunta neutra e avaliação mista em seções próprias, sem tratar
  elogio à pessoa como aprovação do veículo;
- omite métricas de campanha e canais ausentes do recorte, sem deixar
  grandes painéis vazios onde há dados;
- se a renderização estiver bloqueada, registra a limitação e não marca
  a revisão visual como concluída.
