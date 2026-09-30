# Contrato do relatório HTML e da planilha

## Decisão editorial

O Gate 1 aprova conclusões propostas, narrativa, cobertura e pool de
evidências. A geração começa depois da aprovação registrada. Não há Gate 2:
a equipe revisa o HTML e exporta o PDF manualmente pelo navegador.

## Templates distribuídos

generate-report/assets/report-template.html contém a estrutura e o CSS
autocontido aprovados para a apresentação de Mar Aberto. É derivado da
hierarquia visual da capa, do resumo e das páginas analíticas do material
editável de 16/09 e do PDF de 23/09. O modelo tem espaços vazios para o
conteúdo de cada execução, sem números, comentários ou gráficos históricos.
Seu CSS define formato 10 × 13, azul escuro, ciano, painéis claros, tipografia
Inter, cartões e rodapé. A imagem da capa é fornecida na execução e precisa
corresponder ao projeto e produto.

generate-report/assets/analytics-template.xlsx tem oito abas analíticas e
campos vazios. Foi reconstruído a partir da estrutura de DADOS GERAIS e das
planilhas de gráficos compartilhadas pela Carol: base por publicação,
cabeçalhos azul claro, células brancas com bordas finas, Arial 10, matriz
diária de contagens ao lado da matriz percentual e gráfico de colunas
empilhadas a 100% à direita. Os modelos distribuem apenas o molde; cada
execução usa cópias locais. Não copie dados, links pessoais, prompts ou
fórmulas do período original.

## Arquitetura do relatório

Gere um único deliverables/report.html que funcione sem rede e contenha CSS,
fontes e imagens autorizadas. Abra com escopo, período, fonte, cobertura e
tese qualificada. O panorama mostra cinco sentimentos e volumes de menções,
comentários e respostas com denominadores distintos. Cada canal com dados
tem recorte próprio ou síntese comparativa quando houver pouco material;
não inclua canal vazio. Se a composição dos tipos de fonte divergir,
mostre-a separadamente. Inclua séries empilhadas a 100%, termos próprios e
leitura do que sustenta o resultado.

O dia da série é a data de publicação do registro (published_at);
identifique-o assim no HTML e na planilha. Para um único dia de menções,
um painel por publicação pode ocupar a área visual, desde que o eixo não
seja apresentado como série diária. Não invente datas ou relações entre
termos. Selecione destaques por identificador de publicação e métricas
agregadas, nunca identidade do autor.

Evidências aprovadas e anonimizadas são citações rotuladas por sentimento,
canal e tipo de fonte. Elas ilustram achados, sem substituir contagens.
O sentimento, tipo de fonte, canal e alvo da citação precisam concordar
com o registro analítico. Pergunta neutra não aparece como crítica;
elogio à pessoa ou campanha não ilustra avaliação do veículo.
Temas de uma página de canal vêm apenas dos registros relevantes desse canal.

Cobertura precede conclusões; lacunas aparecem junto das leituras afetadas.
A metodologia registra fonte, rubrica, período, universos e limitações.
No modo limited_approved, capa, resumo, recortes afetados, conclusões e
metodologia identificam cobertura limitada. Percentuais descrevem apenas o
corpus observado, sem estimar o universo completo de comentários.

Títulos, sínteses, rótulos, legendas e citações permanecem texto selecionável
e editável no HTML. Cada gráfico identifica fonte, período, total e
denominador. Crie páginas adicionais no mesmo visual quando o conteúdo não
couber legivelmente. Escape texto externo e não use scripts nem recursos
externos. A equipe pode exportar PDF manualmente depois de editar o HTML.

## Planilha analítica

Gere `deliverables/analytics.xlsx` com filtros, cabeçalhos congelados e tipos
reais de data, número e percentual:

| Aba | Conteúdo |
|---|---|
| `Resumo` | projeto, período, filtro, status, métricas e caminhos relativos dos dois entregáveis |
| `Cobertura` | uma linha por publicação e estado de coleta |
| `Publicações` | base por publicação: rede, URL canônica, data, ID, texto sanitizado, métricas agregadas, cinco contagens de sentimento dos comentários, total de comentários e total de respostas |
| `Análises` | uma linha por registro anonimizado, tipo de fonte e sem texto bruto |
| `Agregações` | distribuições e amplificação por rede, tipo de fonte e dimensão |
| `Séries diárias` | série longa canônica e painéis diários por rede e tipo, com contagens, percentuais e gráficos nativos |
| `Evidências` | comentários integrais aprovados e anonimizados |
| `Metodologia` | versões, rubrica, definições, cobertura e limitações |

Em `Análises`, inclua ID irreversível, publicação, pai opcional, rede, data,
tipo de fonte, relevância, motivo, alvos, sentimentos por alvo,
sentimento-resumo, temas, confiança, curtidas e respostas. Não inclua autor,
perfil, foto nem link individual de pessoa.

As tabelas estruturadas do modelo começam com espaço para 196 linhas de dados.
Se houver mais registros, estenda cada tabela e a formatação das linhas
novas, inclusive formatos de data, número e percentual, até a última linha
preenchida antes de exportar. Reabra o XLSX e confirme que o filtro cobre
todas as linhas, inclusive a última, sem perder os cabeçalhos congelados.

`Resumo!A18:G21` discrimina os cinco sentimentos e o total de menções,
comentários e respostas. Em `Publicações`, G:K contém as cinco contagens de
**comentários observados** da publicação; L é sua soma e M é o total de
respostas, sem somá-las novamente aos comentários. A data em C é um valor de
data, não texto. O link em B aponta para a publicação pública, nunca para a
pessoa que comentou. Se um campo de texto da publicação não puder ser
sanitizado, deixe-o vazio e registre a limitação em `Metodologia`.

Em `Séries diárias`, A:G é a fonte canônica longa. O molde J:AP contém três
painéis vazios para **uma rede**: menções nas linhas 4–36, comentários nas
49–81 e respostas nas 94–126. Cada painel tem matriz de contagens em J:P,
matriz percentual em R:W e gráfico à direita. Na execução, copie os três
painéis para cada rede com dados, com o nome da rede no título; omita tipo sem
dados e nunca deixe gráfico vazio no entregável. Amplie linhas e intervalos
dos gráficos quando o período exceder 31 dias. Datas das matrizes de contagem
são datas tipadas; rótulos do eixo percentual usam `dd/mm` como texto. Divida
cada sentimento pelo total **daquele dia, rede e tipo**; dias sem registros
ficam ausentes, sem divisão por zero ou barra falsa. As cinco séries usam
positivo `#38761D`, neutro `#F1C232`, negativo `#CC0000`, misto `#8E7CC3` e
indefinido `#999999`. Mantenha colunas empilhadas a 100%, eixo em percentual,
legenda e rótulos legíveis. Não una os denominadores dos três tipos.

## Reconciliação e checkpoint

Antes da entrega, prove que cobertura reconcilia com a entrada; análises
relevantes, excluídas e falhas reconciliam com o universo observado; menções,
comentários e respostas têm denominadores independentes; cada série diária
reconcilia com sua rede e tipo; as cinco contagens de `Publicações` somam seus
comentários observados e reconciliam com `Análises`; números e percentuais do
HTML, XLSX e agregados canônicos coincidem; `Evidências` coincide com o pool
aprovado.

Reabra ambos os arquivos e renderize todas as páginas do HTML em tela e
impressão. A execução só termina com os dois entregáveis válidos e hashes
SHA-256 registrados, junto da versão
e hashes dos dois templates usados. O PDF exportado manualmente não integra
esse checkpoint. Execuções de contratos 2.0.0 e 3.0.0 permanecem intactas.
