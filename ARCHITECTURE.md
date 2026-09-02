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

### Cobertura observável precede análise

Uma análise só pode ser produzida quando todo o conteúdo disponibilizado pelas
fontes autorizadas tiver sido percorrido. Contadores opacos são usados para
reconciliação, não como prova isolada de completude.

**Por quê:** plataformas podem incluir nos contadores comentários ocultos,
removidos ou indisponíveis. A cobertura é comprovada pelo esgotamento da
paginação e das respostas acessíveis; se esse percurso falhar, a análise é
bloqueada em vez de apresentar conclusões parciais.

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
