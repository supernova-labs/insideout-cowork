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
