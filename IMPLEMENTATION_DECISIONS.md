# Decisões de implementação — cinco frentes

Este registro reúne escolhas necessárias para implementar as frentes aprovadas
sem reabrir o gate de produto. Cada decisão pode ser auditada e revisada antes
da publicação da versão.

## D001 — Configuração de canais pertence à análise do briefing

**Decisão:** `analyze-briefing` propõe e, após confirmação, materializa
`Canais da marca`. `generate-grid` apenas lê os canais ativos e não altera sua
configuração.

**Racional:** canais, objetivos e diferenças editoriais são contexto da marca,
enquanto o grid deve permanecer responsável pelos posts.

**Alternativa descartada:** permitir que `generate-grid` crie canais durante o
planejamento, misturando configuração estrutural com produção mensal.

**Impacto:** atualizar `AGENTS.md`, o contrato do Airtable, a skill de análise e
seus evals.

## D002 — Redes usam vocabulário controlado e expansível

**Decisão:** `Canais da marca.Rede` é seleção única, inicialmente com
Instagram, LinkedIn, TikTok, Facebook e YouTube. Uma rede nova entra como nova
opção; nunca como uma nova coluna em `Marcas`.

**Racional:** evita variações de grafia na chave natural sem congelar o modelo
nas redes do piloto.

**Impacto:** a skill apresenta uma rede ausente antes de solicitar a adição da
opção; não escolhe uma aproximação silenciosamente.

## D003 — A rede participa da identidade operacional do post

**Decisão:** para posts com `Canal da marca`, a chave natural é
`Marca + Canal da marca + Data + Título`. Registros legados sem essa relação
continuam resolvidos por `Marca + Data + Título`, sempre com detecção de
duplicidade.

**Racional:** duas adaptações intencionais podem compartilhar data e título,
mas pertencem a redes diferentes.

**Impacto:** atualizar o contrato compartilhado, `generate-grid`,
`generate-copy` e os evals de idempotência.

## D004 — O snapshot é estático e não vira aplicação

**Decisão:** o HTML pode usar CSS embutido e JavaScript local opcional para
navegação, mas não realiza chamadas externas. Cada arquivo é gerado fora do
pacote e recebe marca, mês e versão no nome e no conteúdo.

**Racional:** valida a experiência sem introduzir painel, autenticação,
backend, hospedagem ou estado paralelo.

**Impacto:** a especificação e os evals ficam em `generate-grid`; nenhum motor
ou painel permanente entra no plugin.

## D005 — Tendências são contexto de `generate-grid`

**Decisão:** o experimento de tendências é uma etapa de preparação do grid,
não uma nova skill nem uma nova tabela nesta versão.

**Racional:** a capacidade só tem valor quando altera uma recomendação
editorial rastreável. Persistência permanente continua sendo decisão posterior
ao piloto.

**Impacto:** candidatos vivem na execução, com fonte, evidência, relevância e
validade; apenas candidatos aprovados podem influenciar o primeiro take.

## D006 — Relações únicas são invariantes de comportamento

**Decisão:** embora o Airtable represente relações como listas, `Marca` em
`Canais da marca` e `Canal da marca` em `Posts` devem conter exatamente um
registro. A skill interrompe escrita ou geração diante de zero ou múltiplas
relações quando o campo for necessário.

**Racional:** o conector disponível não expõe a configuração de relação única,
mas o produto exige identidade inequívoca.

**Impacto:** validação antes e depois de cada mutação, com evals de conflito.

## D007 — O briefing novo preserva a leitura da planilha, não sua estrutura

**Decisão:** o primeiro take continua apresentando em conjunto referência,
produto, lettering por tela e orientação de execução. No Airtable, porém, cada
elemento permanece no campo e na skill responsável.

**Racional:** a planilha histórica usa uma célula como pacote de briefing para
a designer. Replicar esse pacote num único campo criaria duplicidade e
dificultaria regenerar copy, canais ou estrutura de forma independente.

**Evidência consultada:** abas mensais da planilha histórica, incluindo
`CLINIQUE - JULHO 2025`, nas quais aparecem `REF/REFS`, `PRODUTO(S)`,
`LETTERING`, `TELA N` e instruções de produção entre colchetes.

**Impacto:** `design-briefing.md` explicita a tradução de cada bloco histórico;
o artefato composto e o snapshot reúnem os componentes para revisão.

## D008 — A issue do harness é encerrada após a prova

**Decisão:** a issue `[TESTE CODEX]` permanece aberta apenas durante a
releitura exigida pelo critério de aceitação e é encerrada como concluída logo
depois.

**Racional:** preserva uma evidência verificável do fluxo ponta a ponta sem
deixar um item artificial misturado ao backlog real dos mantenedores.

**Impacto:** a auditoria registra o link e os dois estados observados; nenhum
comentário, PR ou correção adicional é criado pelo harness.

## D009 — Sentimento é persistido também por alvo

**Decisão:** cada registro analítico mantém um sentimento-resumo para a
distribuição principal e uma lista `target_sentiments` com sentimento e
confiança para cada alvo identificado.

**Racional:** um comentário pode elogiar a campanha ou a influenciadora sem
expressar a mesma opinião sobre o i20. Um único rótulo no registro apagaria essa
distinção e contrariaria a arquitetura aprovada.

**Impacto:** o schema, a rubrica, a skill de análise e a aba `Análises` carregam
as duas leituras; as agregações principais continuam contando uma unidade por
registro relevante.

## D010 — A prova vertical sintética não integra o pacote distribuído

**Decisão:** HTML, PDF, planilha, capturas e estados usados na prova vertical
ficam em `artifacts/`, que já é ignorado pelo Git. O plugin distribui contratos,
fixtures sintéticas, skills e validadores, não um motor local permanente.

**Racional:** a arquitetura do repositório proíbe incorporar backend, crawler,
estado operacional ou motores de geração ao plugin.

**Impacto:** a auditoria pode referenciar a prova local sem transformar seus
artefatos em dependência do produto ou incluir dados de execução no pacote.

## D011 — Evals de interação permanecem separados da homologação real

**Decisão:** antes da publicação, fixtures e validadores comprovam contratos,
privacidade, reconciliação e produtos. Os evals descrevem os cenários de
interação; sua execução em tarefas novas, com sessões reais, pertence a M9 e é
conduzida pela equipe da InsideOut.

**Racional:** essa separação preserva a decisão de publicar o piloto antes dos
testes operacionais e impede que uma simulação seja apresentada como evidência
de acesso real à Stilingue, Instagram ou YouTube.

**Impacto:** cada resultado operacional permanece `não executado — M9` até ser
registrado pela equipe, mesmo quando o contrato correspondente passou no teste
sintético.

## D012 — Caminhos relativos também são confinados à execução

**Decisão:** o manifesto rejeita caminhos absolutos e qualquer segmento `..`,
mesmo quando o texto do caminho é tecnicamente relativo.

**Racional:** portabilidade não pode permitir que uma execução leia ou escreva
fora da pasta escolhida pelo operador. Um caminho como `analysis/../../arquivo`
violaria a fronteira local sem parecer absoluto.

**Impacto:** schema, contrato de estado e validador cobrem explicitamente path
traversal; a fixture negativa prova a rejeição.
