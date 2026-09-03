# Plano de desenvolvimento — InsideOut Mar Aberto

Status em 2026-09-02: arquitetura, construção e publicação do piloto concluídas;
validações e referência publicada registradas em `ACCEPTANCE_AUDIT.md`;
homologação operacional pela InsideOut (M9) aguarda execução.

Este plano transforma os princípios de `ARCHITECTURE.md` em etapas de
construção verificáveis. Cada milestone entrega um artefato demonstrável, fecha
somente quando seus critérios de aceite forem comprovados e habilita uma decisão
explícita sobre a etapa seguinte.

Os testes anteriores à publicação são estruturais, contratuais e baseados em
fixtures sintéticas ou sanitizadas. Os testes operacionais com sessões reais de
Stilingue, Instagram e YouTube acontecem depois da publicação do piloto e são
conduzidos pela equipe da InsideOut.

## Produto e fronteiras

- Plugin: `insideout-mar-aberto`, separado do `insideout-social` e publicado no
  marketplace Codex `insideout`.
- Fluxo: execução sob demanda coordenada por `run-mar-aberto`.
- Etapas especializadas: exportação da Stilingue, coleta de comentários,
  análise automatizada e geração dos produtos finais.
- Capacidade de suporte: feedback do próprio plugin, fora do fluxo analítico.
- Entrada do MVP: exportação válida da Stilingue.
- Canais analisados: Instagram e YouTube; demais canais são contabilizados como
  não suportados.
- Estado: pasta local por projeto e execução, com JSON e JSONL canônicos.
- Produtos finais: relatório HTML, PDF aprovado e planilha analítica `.xlsx`.
- Fora do MVP: agendamento, crawler ou backend permanente, APIs próprias,
  Airtable, outras redes e retenção do corpus bruto após análise concluída.

## Dependências entre milestones

```text
M0 Contratos e fixtures
 └─ M1 Fundação do plugin
     ├─ M2 Exportação Stilingue
     │   └─ M3 Coleta Instagram e YouTube
     │       └─ M4 Análise automatizada
     │           └─ M5 Relatório e planilha
     │               └─ M6 Orquestração ponta a ponta
     └─ M7 Feedback do piloto
         M6 + M7 ── M8 Publicação do piloto
                         └─ M9 Homologação pela InsideOut
```

M7 pode ser construído depois de M1 sem depender das etapas analíticas. M6 só
fecha quando os contratos de saída de M2–M5 forem compatíveis entre si.

## Regra comum de aceite e evidência

Para qualquer milestone ser concluído:

1. todos os critérios de aceite do milestone devem estar comprovados;
2. cada teste deve registrar resultado real como `passou`, `falhou` ou
   `não executado`, nunca por inferência;
3. `não executado` deve trazer o motivo e o milestone em que será executado;
4. a evidência deve ser registrada em `ACCEPTANCE_AUDIT.md`, com comando,
   fixture ou artefato inspecionado e data;
5. uma nova decisão surgida durante a construção deve ser registrada em
   `IMPLEMENTATION_DECISIONS.md` e confrontada com `ARCHITECTURE.md`;
6. dados reais, comentários, cookies, tokens e credenciais não entram no
   repositório nem nas evidências de teste.

## M0 — Contratos, rubrica e fixtures

**Artefato demonstrável:** contratos versionados de entrada, estado, cobertura,
análise, evidências e produtos finais, acompanhados por fixtures sem dados
pessoais.

### Critérios de aceite

- O contrato de entrada identifica campos obrigatórios da exportação Stilingue,
  filtro, período, publicação e rede.
- O manifesto da execução define identidade do projeto, intervalo, etapa atual,
  status, versões dos contratos e caminhos relativos dos artefatos.
- A cobertura diferencia publicação coletada, coleta parcial, indisponível e
  canal não suportado, sem transformar lacuna em cobertura completa.
- A rubrica define relevância, alvo, sentimento, temas e confiança; sentimento
  admite positivo, negativo, neutro, misto e ambíguo.
- O contrato separa distribuição com peso igual de amplificação por engajamento
  dentro de cada plataforma.
- A planilha final possui contrato para as abas `Resumo`, `Cobertura`,
  `Publicações`, `Análises`, `Agregações`, `Evidências` e `Metodologia`.
- Fixtures não contêm usuários, perfis, fotos, links individuais, cookies ou
  comentários reais identificáveis.

### Testes

| ID | Cenário | Evidência esperada |
|---|---|---|
| M0-T1 | Exportação válida mínima | O validador aceita a fixture e resolve período, filtro, rede e publicações. |
| M0-T2 | Coluna obrigatória ausente ou tipo inválido | A validação rejeita o arquivo e nomeia a lacuna em linguagem operacional. |
| M0-T3 | Instagram, YouTube e uma terceira rede | Instagram e YouTube entram no escopo; a terceira rede é contabilizada como não suportada. |
| M0-T4 | Comentário, resposta e duplicata sintéticos | Os contratos preservam encadeamento e deduplicação por identificadores irreversíveis. |
| M0-T5 | Auditoria de fixture e schema | Busca por dados pessoais e segredos retorna zero ocorrência material. |
| M0-T6 | Matriz princípio–contrato | Cada princípio do Mar Aberto aponta para ao menos um contrato ou teste que o prova. |

**Ponto de decisão habilitado:** os contratos são suficientes para criar o
plugin sem deixar decisões arquiteturais para quem implementar cada skill?

## M1 — Fundação e distribuição do plugin

**Artefato demonstrável:** diretório `plugins/insideout-mar-aberto` descoberto
pelo marketplace Codex, ainda sem alegar validação operacional.

### Critérios de aceite

- O plugin possui manifesto Codex válido, identidade `insideout-mar-aberto`,
  versão inicial e nome de exibição `InsideOut Mar Aberto`.
- O marketplace `insideout` aponta para o novo diretório local sem alterar a
  origem do `insideout-social`.
- A árvore canônica contém as skills `run-mar-aberto`, `export-stilingue`,
  `collect-comments`, `analyze-sentiment`, `generate-report` e
  `skill-feedback`.
- Cada `SKILL.md` tem nome em kebab-case igual ao diretório, descrição com
  capacidade e gatilho e menos de 500 linhas.
- Referências comuns vivem uma única vez no plugin; artefatos operacionais,
  credenciais e dados de cliente ficam fora dele.
- Catálogo, manifesto, README e `.agent-smith/index.json` descrevem a mesma
  identidade, versão, skills e caminho canônico.

### Testes

| ID | Cenário | Evidência esperada |
|---|---|---|
| M1-T1 | Validação Agent Smith | Topologia marketplace Codex válida, dois plugins locais distintos e zero conflito. |
| M1-T2 | Manifesto e catálogo | JSON válido; nome, versão, caminho e diretório de skills resolvem corretamente. |
| M1-T3 | Descoberta das skills | Seis skills únicas, sem duplicação de fonte e com todas as referências resolvidas dentro do plugin. |
| M1-T4 | Regressão do plugin existente | O validador do `insideout-social` continua aprovando suas seis skills sem mudança comportamental. |
| M1-T5 | Auditoria de pacote | Nenhum dado operacional, segredo, cookie, comentário real, backend ou crawler entra no pacote. |
| M1-T6 | Documentação de instalação | README distingue os dois plugins e contém o comando correto para instalar o Mar Aberto. |

**Ponto de decisão habilitado:** a fundação está pronta para receber os fluxos
especializados sem criar dependência entre os dois produtos?

## M2 — Skill de exportação da Stilingue

**Artefato demonstrável:** `export-stilingue` produz um checkpoint de entrada
validado ou um diagnóstico acionável, sem armazenar credenciais.

### Critérios de aceite

- A skill solicita filtro e intervalo antes de iniciar e registra exatamente o
  recorte confirmado pelo operador.
- A sessão da Stilingue é validada nessa etapa; login, senha e segundo fator são
  realizados diretamente pelo operador.
- O fluxo seleciona o filtro confirmado, solicita a exportação, acompanha o
  status e considera o refresh observado no processo real.
- O download só é aceito quando o arquivo é uma planilha Stilingue válida; uma
  página vazia ou arquivo HTML com extensão incorreta não conta como sucesso.
- O checkpoint registra arquivo, período, filtro, número de publicações,
  distribuição por rede e duplicatas encontradas.
- Retomar uma exportação concluída não cria outra execução nem baixa novamente
  o arquivo sem necessidade.

### Testes anteriores à publicação

| ID | Cenário | Evidência esperada |
|---|---|---|
| M2-T1 | Fixture Stilingue válida | Checkpoint completo e contagens reconciliadas com as linhas da planilha. |
| M2-T2 | Arquivo inválido, vazio ou HTML | Estado `falhou`, diagnóstico claro e nenhuma promoção para coleta. |
| M2-T3 | Período ou filtro divergente | O fluxo pede correção e não apresenta a entrada como validada. |
| M2-T4 | URLs repetidas | A lista canônica deduplica as publicações e preserva a contagem de ocorrências originais. |
| M2-T5 | Retomada após checkpoint | Segunda execução reutiliza o artefato válido e mantém a mesma identidade de execução. |

### Testes operacionais após a publicação

- Login manual em uma conta da equipe da InsideOut.
- Seleção do filtro `nova busca i20` e de um período controlado.
- Mudança de status após refresh e obtenção do arquivo pela janela de download.
- Comparação entre recorte exibido na Stilingue e manifesto local produzido.

**Ponto de decisão habilitado:** a exportação real funciona nas permissões da
InsideOut ou o fluxo precisa ser iterado antes de validar a coleta?

## M3 — Skill de coleta de comentários

**Artefato demonstrável:** `collect-comments` gera corpus temporário anonimizado,
grafo de respostas e auditoria de cobertura por publicação.

### Critérios de aceite

- A skill valida somente as sessões das redes presentes na planilha e nunca
  captura senha, segundo fator ou cookie.
- Instagram e YouTube percorrem comentários e respostas acessíveis até o
  esgotamento observável ou até uma falha registrada.
- Nomes, perfis, fotos e links individuais são removidos antes da persistência;
  IDs irreversíveis preservam deduplicação e encadeamento.
- Cada publicação registra contagem informada quando disponível, contagem
  observada, respostas, estado de cobertura, falha e canal.
- Falhas isoladas não interrompem a execução; seus dados não são apresentados
  como cobertura completa.
- Retomada reaproveita checkpoints, não duplica comentários e não reinicia
  publicações já concluídas.
- Canais fora de Instagram e YouTube são contabilizados, mas não coletados.

### Testes anteriores à publicação

| ID | Cenário | Evidência esperada |
|---|---|---|
| M3-T1 | Paginação com respostas aninhadas | Todos os itens da fixture são percorridos uma vez e o grafo pai–resposta é preservado. |
| M3-T2 | Publicação sem comentários | Cobertura concluída com zero observado, sem tratar zero como erro. |
| M3-T3 | Publicação privada, removida ou indisponível | Estado e motivo registrados; a próxima publicação continua. |
| M3-T4 | Sessão expirada no meio da coleta | Checkpoint preservado, solicitação de novo login e retomada sem duplicatas. |
| M3-T5 | Falha após coleta parcial | Quantidade coletada e lacuna permanecem explícitas em cobertura. |
| M3-T6 | Autor e links presentes na entrada | Persistência contém texto e contexto necessários, mas zero identificador pessoal reversível. |
| M3-T7 | Canal não suportado | Registro aparece na cobertura e não é enviado à análise de comentários. |
| M3-T8 | Nova execução sobre o mesmo checkpoint | Contagens e hashes permanecem estáveis; nenhum registro é duplicado. |

### Testes operacionais após a publicação

- Instagram autenticado: abrir uma publicação, expandir comentários e ao menos
  uma árvore de respostas, comparando observado com o checkpoint.
- YouTube autenticado: percorrer mais de uma página de comentários e respostas.
- Interromper e retomar deliberadamente uma coleta.
- Induzir uma publicação inacessível e confirmar que a lacuna aparece na
  cobertura sem bloquear as demais.

**Ponto de decisão habilitado:** a cobertura e a retomada são confiáveis nas
interfaces reais ou os seletores e diagnósticos precisam ser ajustados?

## M4 — Skill de análise automatizada

**Artefato demonstrável:** `analyze-sentiment` produz análises anonimizadas,
agregações separadas e pool automático de evidências, descartando o corpus
bruto ao concluir.

### Critérios de aceite

- Todo comentário relevante recebe alvo, sentimento, temas e confiança segundo
  a rubrica versionada; não há revisão humana comentário a comentário.
- O i20 é o assunto central e o mercado brasileiro define relevância; idioma é
  apenas um sinal, não um filtro isolado.
- Sentimentos mistos e ambíguos não são forçados para classes conclusivas.
- O alvo distingue i20, Hyundai, campanha, influenciador, compra/preço,
  concorrente e outros contextos previstos pela rubrica.
- A distribuição principal atribui peso igual a cada comentário relevante.
- A amplificação usa curtidas e respostas dentro de cada plataforma e não cria
  um índice conjunto entre Instagram e YouTube.
- O pool proposto é estratificado por canal, tema e sentimento e inclui padrões
  recorrentes, manifestações marcantes e contrapontos.
- Após o checkpoint concluído, o corpus bruto é removido; análises, cobertura e
  pool permanecem. Em execução interrompida, o corpus permanece até retomada ou
  exclusão manual.

### Testes

| ID | Cenário | Evidência esperada |
|---|---|---|
| M4-T1 | Comentário positivo sobre influenciador e neutro sobre o carro | Alvos e polaridades não são fundidos. |
| M4-T2 | Ironia, emoji, ambivalência e contexto insuficiente | Saídas `misto` ou `ambíguo` quando a rubrica não sustenta classe conclusiva. |
| M4-T3 | Concorrente, mercado estrangeiro e comentário fora de assunto | Relevância e motivo de exclusão coerentes com o recorte Brasil/i20. |
| M4-T4 | Um comentário com vários temas | Temas permanecem multirrótulo sem duplicar o comentário na distribuição. |
| M4-T5 | Reconciliação de contagens | Relevantes + excluídos + falhas reconciliam com o universo observado. |
| M4-T6 | Distribuição versus amplificação | Percentuais de sentimento usam peso igual; engajamento aparece apenas na visão separada e por plataforma. |
| M4-T7 | Seleção de evidências | O pool contém estratos previstos e não é composto apenas pelos comentários mais engajados. |
| M4-T8 | Conclusão bem-sucedida | Arquivo de corpus bruto deixa de existir e artefatos derivados continuam íntegros. |
| M4-T9 | Interrupção antes do checkpoint final | Corpus permanece local e a retomada não reclassifica registros concluídos. |

**Ponto de decisão habilitado:** a rubrica produz dados suficientemente úteis
para construir narrativa e planilha sem calibração humana por comentário?

## M5 — Skill de relatório e planilha analítica

**Artefato demonstrável:** `generate-report` conduz dois gates editoriais e
entrega HTML, PDF e `.xlsx` reconciliados com o estado analítico.

### Critérios de aceite

- Antes da redação completa, a skill apresenta conclusões propostas, estrutura
  narrativa e pool de evidências para aprovação humana.
- O HTML só é produzido após o primeiro gate; o PDF final só é produzido após o
  segundo gate editorial.
- O relatório sempre contém escopo, cobertura, volume, sentimento, temas,
  amplificação e metodologia; narrativa e recomendações se adaptam aos achados.
- Lacunas, canais não suportados e limites da evidência aparecem junto das
  conclusões afetadas, não apenas em nota final.
- O HTML funciona localmente, não realiza chamadas externas e usa identidade
  InsideOut quando não houver ativos opcionais de cliente.
- O PDF deriva do HTML aprovado e não mantém conteúdo editorial paralelo.
- A planilha contém todos os dados analíticos processados e todas as abas do
  contrato, com filtros e tipos adequados.
- `Análises` não contém o texto bruto; `Evidências` contém somente comentários
  integrais aprovados e anonimizados.
- Totais de JSON/JSONL, planilha e relatório são reconciliados antes da entrega.

### Testes

| ID | Cenário | Evidência esperada |
|---|---|---|
| M5-T1 | Primeiro gate não aprovado | Nenhum relatório completo ou PDF final é apresentado como aprovado. |
| M5-T2 | Núcleo fixo e narrativa adaptativa | Todas as seções obrigatórias existem e não há seção narrativa vazia por obrigação. |
| M5-T3 | Cobertura parcial | A limitação aparece no resumo, na seção afetada e na aba `Cobertura`. |
| M5-T4 | HTML padrão sem ativos de cliente | Arquivo abre localmente, permanece legível em desktop e tela estreita e faz zero chamada externa. |
| M5-T5 | Personalização opcional válida ou ausente | Ativos fornecidos são aplicados; ausência ou falha usa o padrão InsideOut sem bloquear. |
| M5-T6 | Renderização do PDF | Todas as páginas são renderizadas e inspecionadas sem corte, sobreposição ou divergência textual do HTML aprovado. |
| M5-T7 | Integridade da planilha | Sete abas presentes, cabeçalhos e tipos válidos, filtros funcionais e arquivo abre sem aviso de corrupção. |
| M5-T8 | Reconciliação cruzada | Contagens e percentuais do relatório coincidem com planilha e agregados canônicos. |
| M5-T9 | Privacidade dos entregáveis | Zero autor, perfil, foto ou link individual; texto integral somente nas evidências aprovadas. |
| M5-T10 | Segunda revisão solicita alteração narrativa | HTML e PDF são regenerados sem alterar silenciosamente as classificações analíticas. |

**Ponto de decisão habilitado:** os três produtos finais são claros, íntegros e
adequados para a revisão e o uso da InsideOut?

## M6 — Skill orquestradora ponta a ponta

**Artefato demonstrável:** `run-mar-aberto` conduz uma execução nova ou retoma
uma existente, respeitando autenticação por etapa e gates editoriais.

### Critérios de aceite

- O fluxo solicita projeto, filtro, período e pasta de trabalho antes de criar a
  execução.
- A sequência é exportação → coleta → análise → primeiro gate → relatório e
  planilha → segundo gate → PDF final.
- Cada etapa consome somente o contrato da anterior e grava checkpoint atômico
  antes de avançar.
- Uma retomada identifica a última etapa válida e não repete trabalho concluído.
- Sessão expirada pausa apenas a etapa que depende dela e preserva o restante.
- Falhas de coleta prosseguem como lacunas explícitas; falha de contrato impede
  apenas a promoção para a etapa dependente.
- A conclusão aponta os três entregáveis e o resumo de cobertura, sem alegar
  sucesso para artefatos ausentes ou não aprovados.

### Testes anteriores à publicação

| ID | Cenário | Evidência esperada |
|---|---|---|
| M6-T1 | Execução sintética completa | Todos os checkpoints avançam na ordem e os três produtos finais são resolvidos. |
| M6-T2 | Retomada após cada uma das quatro etapas | O fluxo parte do último checkpoint válido e não duplica artefatos. |
| M6-T3 | Sessão expirada na coleta | O fluxo pede login da rede correta e não repete a exportação. |
| M6-T4 | Entrada inválida | Nenhuma coleta começa e o estado indica a correção necessária. |
| M6-T5 | Primeiro ou segundo gate rejeitado | O fluxo permanece no gate correspondente e não promove o produto seguinte. |
| M6-T6 | Pasta copiada para outro local | Caminhos relativos continuam válidos e a execução pode ser retomada. |
| M6-T7 | Segunda invocação após conclusão | O fluxo apresenta o estado concluído e não executa novamente ações com efeito. |
| M6-T8 | Regressão de responsabilidade | A orquestradora coordena, mas cada artefato continua produzido e validado pela skill responsável. |

### Teste operacional após a publicação

Um operador da InsideOut executa o fluxo completo a partir de uma tarefa nova,
com suas próprias sessões, e confirma que não precisou coordenar manualmente as
quatro skills nem classificar comentários individualmente.

**Ponto de decisão habilitado:** a jornada integrada está pronta para ser
publicada como piloto operacional?

## M7 — Skill de feedback

**Artefato demonstrável:** `skill-feedback` prepara relatos rastreáveis do Mar
Aberto sem vazar dados da execução.

### Critérios de aceite

- A skill classifica bug ou melhoria, reúne contexto técnico mínimo e procura
  duplicidade antes de propor nova issue.
- A prévia completa é sanitizada e exige confirmação antes de qualquer
  publicação externa.
- Comentários, nomes de usuário, links individuais, credenciais e ativos de
  cliente nunca aparecem no relato.
- Sem autenticação do GitHub, a skill entrega texto copiável e não alega que a
  issue foi publicada.
- Após publicação, a issue é relida e seu link é devolvido ao operador.

### Testes

| ID | Cenário | Evidência esperada |
|---|---|---|
| M7-T1 | Bug com trecho sensível | Prévia remove o conteúdo sensível e preserva passos reproduzíveis. |
| M7-T2 | Melhoria já registrada | Duplicata é apresentada e nenhuma nova issue é criada. |
| M7-T3 | Cancelamento no gate | Zero efeito externo. |
| M7-T4 | GitHub indisponível | Fallback copiável, com estado `não publicado`. |
| M7-T5 | Publicação aprovada no piloto | Issue relida com tipo, título e corpo aprovados; link registrado na auditoria. |

**Ponto de decisão habilitado:** a equipe consegue transformar achados do piloto
em backlog seguro e acionável?

## M8 — Publicação do piloto

**Artefato demonstrável:** versão piloto instalável do `insideout-mar-aberto` no
marketplace `insideout`.

### Critérios de aceite anteriores à publicação

- M0–M7 estão concluídos nos testes que não dependem de sessões reais; testes
  operacionais estão marcados como `não executado — M9`, não como aprovados.
- Validador das skills, Agent Smith, validação do marketplace, verificação de
  whitespace e auditoria de segredos passam sem erro.
- Manifesto, marketplace, índice e README concordam em nome, versão e caminho.
- O diff contém somente arquivos do escopo do Mar Aberto e documentação comum
  intencionalmente atualizada.
- A versão é identificada como piloto, sem alegação de homologação operacional.
- Commit, push e promoção à `main` acontecem somente após autorização explícita.

### Testes

| ID | Cenário | Evidência esperada |
|---|---|---|
| M8-T1 | Validação estrutural completa | Todos os validadores locais retornam sucesso e a auditoria registra comandos e versões. |
| M8-T2 | Coexistência no catálogo | `insideout-social` e `insideout-mar-aberto` resolvem diretórios diferentes sem conflito. |
| M8-T3 | Auditoria de conteúdo distribuído | Zero dado real, credencial, estado operacional, crawler ou backend no pacote. |
| M8-T4 | Revisão do diff preparado | Arquivos fora do escopo não estão staged; verificação do diff staged passa. |
| M8-T5 | Publicação autorizada | Referência publicada corresponde exatamente ao commit validado. |

**Resultado do gate:** publicação autorizada e concluída; a equipe da InsideOut
pode executar os testes reais de M9 a partir da referência registrada na
auditoria.

## M9 — Homologação operacional pós-publicação

**Artefato demonstrável:** matriz de resultados preenchida pelos operadores da
InsideOut e decisão registrada de liberar, iterar ou interromper.

O roteiro preenchível desta etapa está em
[`docs/mar-aberto-pilot-test-protocol.md`](docs/mar-aberto-pilot-test-protocol.md).
Quem publicar o piloto deve informar a referência exata usada na instalação;
o roteiro não presume promoção à `main`.

### Critérios de aceite do piloto

- O plugin é instalado a partir do marketplace publicado e suas seis skills são
  descobertas em uma tarefa nova.
- Um operador inicia o fluxo sob demanda, faz login com suas próprias contas e
  completa uma execução real do i20 sem coleta ou classificação manual.
- O período e o filtro da Stilingue coincidem com o manifesto local.
- Instagram e YouTube produzem cobertura observável; falhas e canais não
  suportados permanecem explícitos.
- Uma interrupção controlada comprova retomada sem duplicação.
- As análises são consideradas úteis para a construção editorial sem revisão
  comentário a comentário.
- Os dois gates editoriais funcionam e produzem HTML, PDF e `.xlsx` coerentes.
- A planilha contém todo o conjunto analítico e não contém corpus bruto ou
  identidade pessoal fora das evidências permitidas.
- Ao menos um feedback real ou cenário de teste é encaminhado pela skill própria
  sem exposição de dados do cliente.
- Cada falha vira item rastreável; nenhuma lacuna é convertida em sucesso.

### Roteiro de testes da equipe InsideOut

| ID | Prova operacional | Registro esperado |
|---|---|---|
| M9-T1 | Instalar e descobrir o plugin em tarefa nova | Versão, operador, ambiente e skills visíveis. |
| M9-T2 | Exportar `nova busca i20` em período controlado | Captura do recorte e manifesto correspondente. |
| M9-T3 | Coletar Instagram e YouTube | Contagens por publicação, respostas, falhas e tempo de execução. |
| M9-T4 | Interromper e retomar | Checkpoint retomado e ausência de duplicatas. |
| M9-T5 | Revisar conclusões, estrutura e evidências | Aprovação ou alterações solicitadas no primeiro gate. |
| M9-T6 | Revisar produtos finais | Resultado do segundo gate e inspeção de HTML, PDF e planilha. |
| M9-T7 | Verificar privacidade e descarte | Corpus ausente após análise e identidades ausentes dos entregáveis. |
| M9-T8 | Registrar feedback | Issue ou fallback sanitizado ligado à versão testada. |

**Ponto de decisão final:**

- **Liberar:** critérios atendidos e nenhuma falha crítica aberta.
- **Iterar:** valor comprovado, mas existem falhas corrigíveis antes de ampliar o
  uso.
- **Interromper:** cobertura, confiabilidade ou custo operacional tornam o fluxo
  inadequado para continuidade.

## Matriz de rastreabilidade resumida

| Capacidade | Construção | Teste local | Teste real |
|---|---|---|---|
| Distribuição do plugin | M1 | M1, M8 | M9-T1 |
| Exportação Stilingue | M2 | M2-T1–T5 | M9-T2 |
| Coleta Instagram/YouTube | M3 | M3-T1–T8 | M9-T3–T4 |
| Análise automatizada | M4 | M4-T1–T9 | M9-T5 |
| HTML, PDF e planilha | M5 | M5-T1–T10 | M9-T5–T7 |
| Orquestração e retomada | M6 | M6-T1–T8 | M9-T2–T6 |
| Feedback seguro | M7 | M7-T1–T4 | M9-T8 |
| Publicação do piloto | M8 | M8-T1–T5 | M9-T1 |

## Ordem de execução e gates

1. Construir e aprovar M0.
2. Construir M1 e provar coexistência com `insideout-social`.
3. Construir sequencialmente M2–M5, fechando contrato e testes de cada etapa
   antes de ligar a próxima.
4. Integrar as etapas em M6 e construir M7.
5. Consolidar a auditoria de aceitação e solicitar autorização para M8.
6. Publicar o piloto somente após essa autorização.
7. A equipe da InsideOut executa M9 pelo plugin publicado.
8. Registrar a decisão de liberar, iterar ou interromper antes de tratar o
   piloto como versão homologada.
