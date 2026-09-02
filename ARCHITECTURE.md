# Arquitetura — InsideOut Social

Este documento registra princípios e decisões arquiteturais reutilizáveis do
plugin. O comportamento executável continua nos `SKILL.md`; o contrato
operacional detalhado continua em `references/_shared/`; e o estado vivo
continua no Airtable.

Não use este arquivo para duplicar instruções operacionais ou snapshots de
schema. Decisões abertas aparecem ao final e só viram princípios depois de
aprovação explícita.

## Princípios confirmados

### Conhecimento no plugin; estado no Airtable

O plugin guarda conhecimento, julgamento, fluxo e regras estáveis. O Airtable
guarda marcas, produtos, referências, posts, peças e demais estados
operacionais que mudam durante o trabalho.

**Por quê:** evita embutir dados vivos no pacote e permite que o time opere uma
única base compartilhada.

**Escopo:** todas as skills e toda evolução do modelo operacional.

**Origem:** `AGENTS.md`, 2026-08-27.

### Uma responsabilidade por skill

Cada skill atua somente na sua etapa do fluxo. Grid planeja posts; copy produz
texto; imagem e vídeo produzem suas respectivas mídias. Uma etapa não absorve
silenciosamente a responsabilidade da seguinte.

**Por quê:** mantém gates de aprovação claros, reduz efeitos colaterais e torna
os evals capazes de provar qual componente alterou cada campo.

**Escopo:** criação, edição e orquestração das skills do plugin.

**Origem:** `AGENTS.md`, 2026-08-27.

### Orquestração compõe capacidades sem fundi-las

Uma skill de fluxo pode acionar skills especializadas para entregar um
artefato composto. A orquestração coordena contexto, sequência e apresentação,
mas não transfere a responsabilidade pelos resultados nem contorna os gates:
cada skill continua responsável por gerar, validar e persistir seus próprios
campos, podendo também ser executada ou regenerada isoladamente.

**Por quê:** oferece uma experiência integrada sem criar uma skill monolítica,
preservando regeneração independente, aprovações e evals por componente.

**Escopo:** fluxos do plugin cuja entrega combina resultados de duas ou mais
skills.

**Origem:** gate de contrato de dados, 2026-08-27.

### O Mar Aberto combina uma jornada principal com etapas retomáveis

Uma skill principal conduz a execução completa do InsideOut Mar Aberto e
coordena quatro skills especializadas: exportação da Stilingue, coleta de
comentários, análise automatizada e construção do relatório. Cada etapa mantém
responsabilidade, validação e checkpoint próprios, podendo ser retomada sem
refazer etapas já concluídas.

**Por quê:** a jornada principal simplifica a operação para diferentes pessoas,
enquanto a separação por etapa permite testar, diagnosticar, retomar e evoluir
cada capacidade sem criar um fluxo monolítico.

**Escopo:** organização das skills e retomada de execuções do plugin InsideOut
Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Cada produto leva seu próprio canal de feedback

O plugin InsideOut Mar Aberto inclui uma skill própria para registrar bugs e
melhorias descobertos no piloto. Essa capacidade é independente do
`insideout-social`, sanitiza dados de clientes, credenciais e conteúdo pessoal e
exige confirmação antes de publicar o relato no repositório de origem. Ela não
constitui uma quinta etapa do fluxo analítico.

**Por quê:** os operadores precisam relatar problemas sem instalar outro
produto nem transportar contexto manualmente. Manter o feedback no próprio
plugin preserva sua fronteira e torna a homologação pós-publicação rastreável.

**Escopo:** feedback operacional e evolução do plugin InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Artefatos compostos não duplicam suas fontes

Uma apresentação pode reunir contexto e resultados de vários campos, mas cada
informação permanece somente na fonte sob responsabilidade de sua skill. O
artefato composto organiza essas fontes para seu público sem copiá-las para
outro campo nem exigir sincronização manual.

**Por quê:** preserva uma única fonte de verdade, mantém as responsabilidades
das skills e permite regenerar um elemento sem desalinhar os demais.

**Escopo:** briefings, prévias, snapshots e outras entregas que combinam campos
ou resultados de múltiplas skills.

**Origem:** gate de contrato de dados, 2026-08-27.

### Mudanças de contrato são aditivas e verificáveis

Evoluções do modelo de dados devem preservar campos e fluxos existentes até que
o plugin, os registros e os evals tenham sido migrados e validados. Nenhuma
mudança estrutural deve depender de edição manual recorrente no Airtable.

**Por quê:** a base é compartilhada e uma alteração estrutural isolada pode
quebrar o fluxo para todas as pessoas.

**Escopo:** tabelas, campos, relações, seleções e contratos entre Airtable e
skills.

**Origem:** reunião “Atualizações IA I Super Nova + IO”, 2026-08-26, e
`AGENTS.md`.

### Descoberta em tempo de execução; identidade por chave natural

IDs de base, tabela, campo e registro não são conhecimento permanente. Cada
execução descobre o schema atual e resolve registros por chaves naturais antes
de ler ou escrever.

**Por quê:** IDs são detalhes da integração e duplicidades tornam uma escrita
ambígua e insegura.

**Escopo:** toda operação com Airtable.

**Origem:** contrato operacional compartilhado, 2026-08-27.

### Aprovação humana antes de efeitos consequenciais

Criação ou substituição de conteúdo, consumo de créditos, mudança de status e
publicação externa respeitam o gate definido pela skill. Toda mutação é relida
antes de ser declarada concluída.

**Por quê:** o plugin apoia julgamento editorial e operação de clientes; não
substitui a decisão humana nem pode alegar sucesso sem evidência observável.

**Escopo:** Airtable, geração paga, arquivos persistidos e serviços externos.

**Origem:** `AGENTS.md`, 2026-08-27.

### Lotes preservam aprovação granular

Entregas compostas podem ser apresentadas e aprovadas em lote, mas cada item
permanece individualmente revisável. Itens aprovados podem avançar e ser
persistidos; exceções permanecem em revisão sem bloquear o restante do lote.

**Por quê:** combina eficiência operacional com controle editorial e evita que
um problema pontual paralise toda a entrega.

**Escopo:** fluxos recorrentes de planejamento e produção de conteúdo que
processam múltiplos posts ou peças.

**Origem:** gate de contrato de dados, 2026-08-27.

### Evidência explícita vence plausibilidade

Briefings, claims, atributos de marca, referências e tendências só entram no
fluxo quando há fonte colocada em escopo. Ausência de evidência vira lacuna,
nunca preenchimento plausível.

**Por quê:** conteúdo de marca precisa ser rastreável e seguro para revisão com
cliente.

**Escopo:** análise de briefing, grid, copy e produção de mídia.

**Origem:** `AGENTS.md`, 2026-08-27.

### Cobertura observável condiciona a análise

A coleta tenta percorrer todo o conteúdo disponibilizado pelas fontes
autorizadas. Contadores opacos são usados para reconciliação, não como prova
isolada de completude. Quando o percurso não puder ser concluído, a análise pode
prosseguir somente com a cobertura efetivamente observada e com as lacunas
quantificadas de forma explícita.

**Por quê:** plataformas podem incluir nos contadores comentários ocultos,
removidos ou indisponíveis. A cobertura é comprovada pelo esgotamento da
paginação e das respostas acessíveis; quando isso não for possível, a condição
de cobertura passa a limitar a interpretação e as conclusões permitidas.

**Escopo:** Social Listening e demais análises que dependam de conteúdo
dinâmico obtido em fontes externas.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Relevância precede volume

Uma ocorrência só participa da análise quando pertence ao mercado definido e
trata o objeto monitorado como assunto central. Exclusões metodológicas
permanecem auditáveis e não são confundidas com falhas de coleta.

**Por quê:** volume bruto pode incluir outros mercados, homônimos, menções
incidentais e conversas cujo sentimento não se refere ao objeto analisado.
Preservar o motivo da exclusão mantém a cobertura verificável sem contaminar
as conclusões.

**Escopo:** Social Listening e demais análises de fontes externas sujeitas a
ruído de busca, idioma, geografia ou ambiguidade de entidade.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Autenticação pertence ao operador e é validada por etapa

Integrações autenticadas usam a sessão do navegador da pessoa que executa o
fluxo. O acesso é verificado antes de cada etapa dependente e, quando
indisponível, a execução pausa de forma retomável sem capturar ou persistir
credenciais.

**Por quê:** o preflight por etapa evita solicitar acessos desnecessários,
impede o compartilhamento de contas e preserva o trabalho já concluído quando
uma sessão expira.

**Escopo:** Stilingue, Instagram, YouTube e demais fontes externas
autenticadas usadas pelos plugins da InsideOut.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### O navegador autenticado é a camada de integração do MVP

No MVP do InsideOut Mar Aberto, a exportação na Stilingue e a coleta no
Instagram e no YouTube são realizadas por automação do navegador sobre a sessão
autenticada do operador. O login é uma ação manual e privada; depois de
confirmada a sessão necessária para a etapa, o fluxo prossegue automaticamente
sem exigir chaves de API.

**Por quê:** esse caminho reproduz o acesso já disponível para cada operador e
evita tornar credenciais técnicas ou aprovações de API um pré-requisito do
produto. Como contrapartida, mudanças nas interfaces das plataformas precisam
ser detectadas por validação e cobertas por manutenção do fluxo.

**Escopo:** integrações de coleta do MVP do InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### A exportação da Stilingue é o contrato de entrada do MVP

Toda execução do MVP do InsideOut Mar Aberto começa por uma exportação válida
da Stilingue, produzida pelo próprio fluxo ou fornecida pelo operador. O arquivo
é validado antes da coleta de comentários. Planilhas genéricas, listas manuais
de links e adaptadores para outras fontes ficam fora desse contrato inicial.

**Por quê:** adotar um único formato de origem reduz ambiguidades de campos,
mantém o recorte auditável e concentra a primeira implementação no processo já
usado pela InsideOut, assumindo explicitamente a dependência da Stilingue.

**Escopo:** entrada, validação inicial e delimitação de fontes do MVP do
InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### A matriz de canais suportados é explícita

O MVP do InsideOut Mar Aberto coleta e analisa publicações do Instagram e do
YouTube. Ocorrências de outras redes presentes na exportação da Stilingue não
interrompem a execução: são excluídas da análise, contabilizadas por canal e
apresentadas como cobertura não suportada.

**Por quê:** limitar os canais mantém a automação testável sem esconder partes
do universo exportado. O registro explícito permite interpretar os resultados
segundo o alcance real do produto.

**Escopo:** roteamento, cobertura e análise por canal no MVP do InsideOut Mar
Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Produtos separados não compartilham estado por pressuposição

Cada plugin com operadores, permissões ou ciclos distintos usa seu próprio
armazenamento operacional. Integrações entre produtos são opcionais,
explícitas e não podem ser pré-requisito para executar a capacidade principal.

**Por quê:** quem opera o InsideOut Mar Aberto pode não ter acesso à base do
InsideOut Social. Vincular os dois produtos ampliaria permissões, criaria uma
dependência desnecessária e impediria o uso por parte do time.

**Escopo:** plugins e produtos da InsideOut que atendam grupos de operadores ou
contratos de acesso diferentes.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### O estado operacional do Mar Aberto é local e portátil

Cada execução do InsideOut Mar Aberto guarda checkpoints, análises, auditoria
de cobertura e evidências selecionadas em arquivos locais fora do plugin. Os
artefatos são organizados por projeto e execução, podem ser transferidos
deliberadamente entre operadores e não dependem de Airtable ou de um backend
compartilhado.

**Por quê:** arquivos locais reduzem dependências de acesso e infraestrutura.
A identificação por projeto e execução evita misturas acidentais, enquanto a
portabilidade permite continuidade quando a equipe decidir compartilhar o
trabalho.

**Escopo:** persistência operacional, retomada e transferência de execuções do
InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### O estado local usa formatos textuais estruturados

Cada projeto e execução do InsideOut Mar Aberto possui uma pasta própria. JSON
é usado para manifestos, checkpoints e resultados agregados; JSONL é usado para
coleções de registros. Esses arquivos constituem o estado operacional canônico,
enquanto HTML e PDF são artefatos de apresentação derivados.

**Por quê:** formatos textuais estruturados são portáteis, inspecionáveis e
adequados à retomada por etapa, sem exigir Excel, banco de dados ou serviço
externo para interpretar uma execução.

**Escopo:** contratos de persistência local e intercâmbio de execuções do
InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Dados pessoais são minimizados na origem

Conteúdo público coletado para análise é anonimizado antes da persistência.
Nomes de usuário, perfis, fotos e links individuais não são armazenados;
identificadores irreversíveis podem existir apenas para deduplicação e para
preservar a estrutura entre comentários e respostas.

**Por quê:** a análise de sentimento depende do conteúdo e do contexto da
conversa, não da identidade pessoal de quem comentou. Remover identificadores
reduz exposição sem impedir a classificação ou a verificação de cobertura.

**Escopo:** comentários, respostas e demais conteúdos produzidos por pessoas
coletados pelo InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Dados brutos expiram após cumprir sua função

O corpus completo de comentários existe somente durante a coleta e o
processamento. Depois da análise concluída, ele é descartado; permanecem as
análises derivadas, a auditoria de cobertura e um pool anonimizado de
comentários representativos ou marcantes para compor o relatório.

**Por quê:** o produto precisa preservar conclusões verificáveis e evidências
úteis para comunicação, não acumular indefinidamente todo o conteúdo coletado.
Isso reduz armazenamento e exposição sem eliminar a base narrativa do
relatório.

**Escopo:** dados brutos coletados e artefatos persistidos pelo InsideOut Mar
Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Execuções incompletas preservam o corpus até decisão do operador

Quando uma execução é interrompida antes de concluir a análise, os comentários
brutos já coletados permanecem na pasta local até que a execução seja retomada
ou o operador solicite sua exclusão. Não há expiração automática para esse
estado incompleto. Depois que a análise termina, aplica-se o descarte imediato
do corpus completo.

**Por quê:** a persistência do estado incompleto permite retomadas tardias sem
repetir a coleta. Limitar a exceção às execuções ainda não processadas preserva
a regra de não acumular comentários após sua função analítica.

**Escopo:** retenção e limpeza de dados brutos em execuções interrompidas do
InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Evidências narrativas combinam representatividade e curadoria humana

O pool de comentários usado em relatórios é proposto por seleção estratificada
entre canais, temas e sentimentos, combinando exemplos recorrentes, marcantes
e contrapontos. Uma pessoa aprova a seleção final antes da composição do
relatório.

**Por quê:** somente automatizar a seleção pode privilegiar comentários
chamativos e distorcer a narrativa; somente selecionar manualmente reduz a
repetibilidade e mantém esforço operacional elevado.

**Escopo:** comentários, depoimentos e demais evidências narrativas escolhidas
para entregáveis de Social Listening.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### A evidência aprovada preserva a voz, não a identidade

Comentários aprovados para o pool de evidências podem aparecer integralmente
no relatório, preservando a redação original. A apresentação remove nome de
usuário, perfil, foto, link individual e outros identificadores do autor. Essa
permissão vale somente para o conjunto curado; o corpus completo continua
sujeito ao descarte após o processamento.

**Por quê:** o texto integral mantém o tom espontâneo e a força documental das
manifestações selecionadas, enquanto a remoção dos identificadores reduz a
exposição direta das pessoas citadas.

**Escopo:** pool de evidências e relatórios do InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Sentimento é contextual e multidimensional

Cada comentário é analisado separando relevância, alvo, sentimento, temas e
confiança. A polaridade admite positivo, negativo, neutro, misto e ambíguo;
casos incertos não são forçados para uma classe conclusiva.

**Por quê:** uma reação positiva à campanha ou ao influenciador não equivale
necessariamente a sentimento positivo sobre o produto ou a marca. Separar as
dimensões preserva o significado e torna a classificação revisável.

**Escopo:** análise de sentimento de comentários e respostas no InsideOut Mar
Aberto e em futuras capacidades de Social Listening.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### A consistência analítica vem da rubrica compartilhada

O modelo ativo do Codex classifica os comentários segundo uma rubrica fixa e
versionada pelo plugin. A arquitetura não fixa um modelo externo nem adiciona
uma segunda passagem de autovalidação comentário a comentário. A consistência
esperada está nas dimensões, definições e critérios aplicados, não na reprodução
literal de cada classificação entre versões de modelo.

**Por quê:** manter a rubrica como contrato reduz dependências técnicas e
permite que o plugin acompanhe o ambiente Codex disponível para cada operador,
preservando uma linguagem analítica comum.

**Escopo:** classificação automatizada de sentimento e temas no InsideOut Mar
Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Automação analítica e responsabilidade editorial são gates distintos

A classificação de sentimento é executada integralmente de forma automática,
sem revisão humana comentário a comentário. A revisão humana acontece na
construção do relatório, sobre a narrativa, as conclusões e o pool de
evidências selecionado.

**Por quê:** revisar cada classificação manteria o custo do processo manual,
enquanto publicar uma narrativa sem revisão transferiria ao cliente erros de
interpretação ou de ênfase. Separar os gates preserva escala e responsabilidade
editorial.

**Escopo:** análises automatizadas e relatórios produzidos pelo InsideOut Mar
Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Relatórios avançam por dois gates editoriais

O relatório do InsideOut Mar Aberto é construído em duas etapas de revisão
humana. Primeiro, a pessoa responsável aprova as conclusões propostas, a
estrutura narrativa e o pool de evidências; somente então o plugin produz o
relatório completo. A versão produzida passa por uma segunda revisão antes de
ser considerada final.

**Por quê:** validar o raciocínio antes da redação evita propagar uma direção
editorial inadequada para todo o documento. A revisão final assegura clareza,
ênfase e adequação ao contexto sem transformar a classificação de sentimento
em uma atividade manual.

**Escopo:** construção, revisão e conclusão de relatórios do InsideOut Mar
Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### HTML é a fonte do relatório; PDF é a entrega congelada

O relatório do InsideOut Mar Aberto é produzido como um artefato HTML local e
portátil, adequado à revisão no navegador e à apresentação de textos, tabelas e
gráficos. Depois do segundo gate editorial, o mesmo conteúdo é exportado para
PDF como versão final de entrega. HTML e PDF não mantêm narrativas paralelas.

**Por quê:** o HTML favorece geração automatizada, inspeção e portabilidade sem
infraestrutura adicional. Derivar o PDF da mesma fonte evita divergências e
oferece um formato estável para compartilhamento após a aprovação.

**Escopo:** geração, revisão, versionamento e exportação dos relatórios do
InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### O relatório tem identidade padrão e personalização opcional

O InsideOut Mar Aberto inclui uma identidade visual padrão da InsideOut para o
relatório HTML. Quando o projeto fornecer logo, cores ou fontes do cliente,
esses materiais locais podem personalizar a apresentação sem alterar o contrato
do conteúdo. Na ausência deles, a geração usa o padrão e não é bloqueada.

**Por quê:** um padrão garante consistência e funcionamento imediato para todos
os operadores, enquanto a personalização opcional atende entregas específicas
sem transformar ativos de cliente em dependência ou conteúdo distribuído pelo
plugin.

**Escopo:** composição visual dos relatórios HTML e PDFs derivados do InsideOut
Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### O relatório combina núcleo fixo e narrativa adaptativa

Todo relatório do InsideOut Mar Aberto apresenta um núcleo comparável com
escopo, cobertura, volume, sentimento, temas, amplificação e metodologia. A
ordem e a composição das conclusões, da narrativa e das recomendações se
adaptam aos achados da execução e passam pelos gates editoriais definidos.

**Por quê:** o núcleo fixo torna períodos e projetos comparáveis e impede a
omissão de limites metodológicos. A camada adaptativa concentra a atenção no
que é material em cada análise, sem preencher seções irrelevantes por obrigação.

**Escopo:** contrato editorial e composição dos relatórios do InsideOut Mar
Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Distribuição e amplificação são leituras distintas

A leitura principal de sentimento atribui o mesmo peso a cada comentário
relevante. Em paralelo, uma leitura de amplificação considera sinais de
engajamento, como curtidas e respostas, sempre dentro de cada plataforma. As
duas leituras permanecem separadas: não formam um índice único e métricas brutas
de Instagram e YouTube não são comparadas diretamente.

**Por quê:** a distribuição com pesos iguais representa melhor o conjunto das
opiniões observadas, enquanto a amplificação evidencia quais manifestações
ganharam repercussão. Misturá-las ocultaria essa diferença e introduziria vieses
causados pelas mecânicas próprias de cada plataforma.

**Escopo:** agregações, visualizações e conclusões de sentimento produzidas pelo
InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Lacunas de coleta são explícitas, não silenciosas

Uma falha de coleta não interrompe toda a execução. O processo continua com os
dados disponíveis e registra, por fonte e publicação, o que foi coletado, o que
ficou inacessível e o motivo conhecido. Toda análise e todo relatório resultante
devem carregar esse estado de cobertura e não podem apresentar a base como
completa quando houver lacunas.

**Por quê:** interromper todo o processo por uma falha isolada torna a operação
frágil, enquanto omitir a falha cria falsa confiança. A degradação explícita
preserva utilidade sem esconder os limites da evidência.

**Escopo:** coleta, análise automatizada e revisão editorial do InsideOut Mar
Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02; revisa o gate
de bloqueio total definido anteriormente na mesma sessão.

### Contexto efêmero só persiste após curadoria

Informações externas e temporárias podem ser pesquisadas ao vivo e informar
rascunhos quando acompanhadas de fonte, data e evidência. Elas só se tornam
estado operacional compartilhado quando forem aprovadas ou efetivamente
utilizadas, sempre com validade explícita; conteúdo vencido nunca é reutilizado
silenciosamente.

**Por quê:** combina descoberta e frescor com rastreabilidade, sem acumular
ruído ou transformar tendências passageiras em conhecimento permanente.

**Escopo:** tendências, Social Listening, referências efêmeras e outros
contextos externos obtidos durante a execução.

**Origem:** subtarefa de tendências e gate de contrato de dados, 2026-08-27.

### Autorização de fonte tem escopo explícito

Toda fonte externa é classificada como permanente para uma marca e rede,
temporária para uma execução ou candidata ainda não aprovada. Fontes candidatas
podem ser apresentadas para avaliação, mas não influenciam o resultado antes da
confirmação humana. Autorização editorial e disponibilidade técnica são
verificadas separadamente.

**Por quê:** impede que uma descoberta ocasional vire referência permanente,
preserva o controle de marca e não confunde permissão de uso com acesso ativo.

**Escopo:** tendências, referências externas, Social Listening e demais fontes
incorporadas durante a execução.

**Origem:** subtarefa de tendências e gate de contrato de dados, 2026-08-27.

### Validade é explícita e contextual

Todo contexto efêmero recebe data de captura e data-limite conforme sua
natureza. A validade representa o período máximo de reutilização, não uma
garantia de atualidade: a fonte e a evidência ainda precisam ser verificáveis
no momento do uso. Quando não houver base suficiente para estimar a validade,
o contexto vale somente para a execução atual.

**Por quê:** evita tanto o descarte prematuro de referências úteis quanto o
reaproveitamento automático de informações que já perderam relevância.

**Escopo:** tendências, eventos, sazonalidade, Social Listening e demais
informações sensíveis ao tempo.

**Origem:** subtarefa de tendências e gate de contrato de dados, 2026-08-27.

### Pacote distribuído permanece declarativo e enxuto

O plugin distribui skills, referências e manifesto. Código de aplicação, dados
operacionais, credenciais, painéis permanentes e motores de geração não entram
no pacote; artefatos produzidos durante um fluxo vivem fora do pacote.

**Por quê:** mantém a instalação auditável e evita reintroduzir legados ou
estado local no produto oficial.

**Escopo:** empacotamento, marketplace e novas capacidades do plugin.

**Origem:** `AGENTS.md`, 2026-08-27.

### A publicação do piloto habilita a validação operacional

O primeiro pacote do InsideOut Mar Aberto é publicado no marketplace da
InsideOut depois das validações locais de estrutura, contrato e cenários que
não dependem de sessões reais. Os testes operacionais ponta a ponta acontecem
depois da publicação, conduzidos pela equipe da InsideOut por meio do plugin e
com as credenciais de cada operador.

**Por quê:** somente os futuros operadores conseguem validar o fluxo nas contas,
permissões e condições reais de uso. A publicação inicial funciona como canal
de distribuição do piloto, não como declaração de que a experiência já foi
homologada em produção.

**Escopo:** estratégia de publicação, piloto e homologação operacional do
InsideOut Mar Aberto.

**Origem:** sessão de design do InsideOut Mar Aberto, 2026-09-02.

### Experiência validada precede infraestrutura

Quando a principal incerteza é o valor ou o formato da experiência, o primeiro
teste deve usar um artefato portátil e sem dependências permanentes.
Hospedagem, autenticação, persistência e integração ao vivo só entram depois
que o piloto comprovar o uso.

**Por quê:** permite aprender rápido sem transformar uma hipótese de interface
em aplicação permanente antes da hora.

**Escopo:** snapshots, painéis, visualizações para clientes e outras
superfícies derivadas dos dados operacionais.

**Origem:** subtarefa do HTML e gate de contrato de dados, 2026-08-27.

### Rede social e formato são dimensões distintas

Cada presença digital de uma marca é representada em `Canais da marca`, com
identidade `Marca + Rede` e suas orientações específicas. O formato da
publicação permanece uma dimensão separada; durante a migração, `Posts.Canal`
continua significando `Feed`, `Story` ou `Reel`.

**Por quê:** evita multiplicar colunas em `Marcas`, permite novas redes sem
alterar o schema e impede que regras de plataforma sejam confundidas com
formatos editoriais.

**Escopo:** planejamento de grid, geração de copy, tendências e qualquer fluxo
multicanal.

**Origem:** gate de contrato de dados, 2026-08-27.

### Um post, uma intenção, uma rede

Cada registro em `Posts` representa uma publicação destinada a um único
`Canal da marca`. O reaproveitamento de uma ideia entre redes gera posts
distintos, adaptados intencionalmente ao contexto, linguagem, formato e objetivo
de cada canal.

**Por quê:** mantém copy, data, briefing, tendências e aprovação inequívocos e
evita conteúdo genérico pensado pelo menor denominador comum entre plataformas.

**Escopo:** planejamento de grid, geração de copy, aprovação e acompanhamento
de publicações multicanal.

**Origem:** gate de contrato de dados, 2026-08-27.

## Decisões abertas

Não há decisão arquitetural aberta bloqueando a construção das capacidades do
plugin. O próximo gate é empírico e está em
[`[Decisão] Definir e validar o piloto com Carol`](https://link.akiflow.com/tasks/9bfc23fa-c8f6-42c4-9fde-0a773ac23553).

Esse gate não bloqueia a implementação. Antes do teste ponta a ponta e da
liberação ao restante do time, ele deve definir:

1. marca, mês, redes e formatos do piloto;
2. participantes e papéis de geração, revisão e aprovação;
3. sequência do teste;
4. critérios de sucesso e decisão de liberar, iterar ou interromper.

## Registro de decisões

Quando uma decisão for aprovada, registre-a nesta estrutura:

```markdown
### Nome do princípio

Enunciado da decisão reutilizável.

**Por quê:** trade-off aceito.

**Escopo:** situações às quais o princípio se aplica.

**Origem:** tarefa ou issue, data.
```
