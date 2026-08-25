# Visão de Transformação — InsideOut × Claude Cowork

> **Status:** rascunho para discussão com o time InsideOut · julho/2026
> **Autores:** Supernova Labs (Luis + Claude)
> **Objetivo deste documento:** alinhar a visão da reformulação, colher comentários e fechar as decisões abertas antes do refactor.

---

## 1. De onde viemos e por que mudar

A primeira fase do projeto provou que o Claude resolve problemas reais da operação de social media: análise de briefings, grid editorial mensal, geração de peças com IA. Mas a implementação cresceu na direção errada — **virou um projeto de software**:

- ~4.300 linhas de Python dentro do plugin (bibliotecas de grid, produtos, estilos, painel HTML, geração de imagem/vídeo)
- `GEMINI_API_KEY` configurada por pessoa, via `.env` — barreira técnica real para o time
- Dados presos na pasta de trabalho de cada usuário (JSON local) — sem visão de time
- Painel HTML gerado por script — bonito, mas manutenção nossa para sempre
- Bugs de infraestrutura (caminho de arquivo, workaround do `.env` do Cowork) que não têm nada a ver com social media

O problema não é qualidade — é **dependência**. A proposta de valor da Supernova é gerar habilidade no cliente, não fazer por ele. Cada componente que só nós sabemos manter contradiz isso.

### O princípio que guia tudo

> **A InsideOut não recebe software — recebe capacidade.**
> Teste de cada decisão: *"a InsideOut consegue operar e evoluir isso sem a Supernova?"*

---

## 2. A arquitetura alvo

Seis camadas, quase todas de prateleira:

| # | Camada | Ferramenta | Papel |
|---|--------|-----------|-------|
| 1 | **Conhecimento e fluxos** | Skills (este repositório) | O que o Claude *sabe*: framework de briefing, voz das marcas, regras editoriais, fluxos de trabalho |
| 2 | **Acervo** | Google Drive (conector oficial, leitura) | O que o time *consulta*: briefings, materiais, apresentações, planilhas de referência |
| 3 | **Dados operacionais** | Airtable (conector oficial, leitura + escrita) | O que o time *mantém* junto com o Claude: marcas, produtos, referências, grid, peças, influencers |
| 4 | **Interface** | Views/Interfaces do Airtable + Artefatos do Claude | O que o time e o cliente *veem* |
| 5 | **Produção criativa** | MCP criativo hospedado (Gemini/Veo) + Canva opcional | O que o Claude *cria de peça* |
| 6 | **Gestão** | Asana (conector oficial) | Onde o trabalho é *acompanhado* — e de onde saem os reportes |

### Regras de bolso para o time

- **Skill** é o que o Claude *sabe*
- **Drive** é o que o time *consulta*
- **Airtable** é o que o time *mantém*
- **Artefato** é o que o Claude *produz*
- **MCP criativo / Canva** é o que o Claude *cria de peça*
- **Asana** é onde o trabalho *anda*

### Critério para planilhas

Para cada planilha do Drive, uma pergunta: **o Claude precisa escrever nela?**
- **Não** → fica no Drive (conector oficial lê numa boa)
- **Sim** → é uma base de dados disfarçada de planilha; migra para o Airtable (ex.: lista de influencers)

---

## 3. O Airtable como coração dos dados

**Já existe um protótipo funcionando** (base "InsideOut Social", criada em jul/2026 com dados reais da Clinique):

| Tabela | Conteúdo | Substitui |
|--------|----------|-----------|
| **Marcas** | Voz, posicionamento, público, brand guide, guardrails | `products.seed.json` (brands) |
| **Produtos** | Descrição, claims, tags, fotos | `product_library` |
| **Referências** | Estilos curados (com prompt de geração) + refs externas (URLs) | `style_library` + refs avulsas |
| **Posts** | O grid: data, canal, abordagem, produto, referência, lettering, legenda, rationale, mockup, vídeo, **status de aprovação** | `grid_library` + painel |
| **Peças** | Imagens/vídeos gerados, com prompt e parâmetros (trilha de auditoria) | sidecar JSON dos mockups |

O que o time ganha em relação ao painel HTML:

1. **Dado de time, não de pasta** — hoje o grid vive na pasta de trabalho de uma pessoa; no Airtable, todo mundo vê e edita a mesma base
2. **Workflow de aprovação como dado** — Rascunho → Em julgamento → Aprovado → Publicado (hoje isso é conversa, não registro)
3. **Views nativas**: Calendar (o mês de relance), Gallery (o grid visual), List agrupada por Semana, Kanban por status
4. **Interfaces** (Interface Designer) para a visão polida — galeria agrupada por semana, filtro por marca/mês; o herdeiro oficial do `insideout-painel.html`
5. **O Claude lê e escreve por conversa** — "muda o post de dia 8 pra Story" vira uma atualização de registro
6. **Rationale auditável** — cada post registra a regra editorial que o justificou (trincas, heroes, sazonalidade)

Limitação conhecida: Gallery view não agrupa (só Grid/List/Timeline/Gantt) — para "grid por semana", usar List agrupada ou Interface.

---

## 4. O MCP criativo — a única peça de software que fica

Vídeo e imagem com Gemini/Veo são o coração criativo do fluxo atual, e a qualidade já foi aprovada pelo time. Nenhum conector de prateleira cobre isso hoje (Canva gera imagem bem, mas vídeo limitado a ~4s; Veo não tem conector oficial). Então **uma** peça de software permanece — pequena, hospedada pela Supernova:

### O que é

Um servidor MCP remoto (Streamable HTTP) que o admin adiciona uma vez como conector custom no Claude Cowork. Para o time, é invisível: um login de um clique na primeira vez, e pronto.

### Ferramentas expostas

| Tool | O que faz |
|------|-----------|
| `gerar_imagem` | Recebe prompt composto (estilo + produto + lettering + brand guide), gera via Gemini, retorna URL |
| `gerar_video` | Recebe prompt + **imagem-âncora** (o mockup do post, para consistência visual), gera via Veo, retorna URL |

### O contrato de anexos (validado em protótipo)

```
Usuária: "gera o mockup do post de 8 de maio"
   1. Claude chama gerar_imagem no MCP
   2. MCP gera, salva em bucket, retorna URL pública temporária (presigned, ~15 min)
   3. Claude escreve a URL no campo Mockup do post, via conector Airtable
   4. O AIRTABLE baixa o arquivo e hospeda a cópia permanente
   → a URL temporária expira; o arquivo vive só dentro da base
```

Testado em jul/2026: o Airtable ingere anexo por URL sem intervenção manual. O Claude nunca manipula arquivo — só orquestra.

**O caminho de volta também funciona (validado):** o Claude lê o anexo de um post via conector, baixa pela URL assinada do Airtable e **interpreta a imagem visualmente**. Detalhe operacional: as URLs de anexo do Airtable expiram (~2h) — sempre buscar o registro na hora e usar a URL fresca, nunca armazená-la em outro lugar.

### Segurança e operação

- **API keys (Gemini) ficam no servidor** — ninguém no time vê ou configura chave. Este é o fim do `.env`
- **Autenticação de acesso** (OAuth padrão MCP, provedor de prateleira — FastMCP/Auth0/Cloudflare): só o time da agência usa
- **Nunca sem autenticação** — URL secreta não é auth
- Hospedagem simples (um container), manutenção mínima — esforço estimado do esqueleto: ~1 dia

### O que o MCP NÃO faz (de propósito)

- Não toca no Airtable (quem escreve é o Claude, via conector)
- Não guarda estado além do bucket temporário
- Não tem interface — é ferramenta do Claude, não produto

---

## 5. As skills — o repertório que cresce

As skills continuam sendo a alma do projeto: é nelas que a habilidade da agência fica codificada e evolui. O repertório se reorganiza:

**Ficam (praticamente como estão):**
- `about-insideout` — conhecimento da empresa
- `analyze-briefing` — framework de análise + validação de escopo por marca
- `generate-copy` — legenda e lettering (skill de processo, efêmera — já alinhada)
- `voz-usuario` — tom de conversa com o time não-técnico

**Mudam de motor (Python local → conectores):**
- `product-catalog` → CRUD conversacional sobre a tabela Marcas/Produtos do Airtable
- `style-gallery` → CRUD sobre a tabela Referências
- `generate-grid` → gera o andaime do grid a partir do briefing e **escreve nas linhas de Posts**; regras editoriais (`rules/<marca>.md`) e calendário continuam sendo markdown versionado nas skills
- `image-generation` / `generate-video` → orquestram o MCP criativo + anexam no Airtable

**Novas (nascem da nova arquitetura):**
- `reporte-cliente` — lê Asana + Airtable, gera artefato de reporte de progresso (regenerado no mesmo link a cada ciclo)
- `influencers` — CRUD sobre a base de influencers (migrada do Google Sheets)
- `qa-visual` — julgamento visual de peças: o Claude abre os anexos (mockups/vídeos) e confere contra os guardrails da marca (rótulo legível, lettering correto, estética, paleta) antes do julgamento humano; também descreve/categoriza referências que o time anexar (herda o papel do `style_extract.py`). Fecha o loop: MCP gera → anexa → Claude julga → humano aprova

**Morrem (e ninguém sente falta):**
- Todo o `core/` Python (~4,3k linhas): `_libcommon`, bibliotecas, `dashboard.py`, shims, disciplina UWP-safe, workaround do `.env`
- O `insideout-painel.html` e o pipeline que o gera
- Classes inteiras de bugs de infraestrutura (caminho relativo, `grids/grids`, ambiente Python)

---

## 6. Artefatos — onde entram e onde não entram

Artefatos do Claude são páginas interativas publicáveis por link. O que aprendemos sobre os limites (importante para expectativas):

**Servem para** (conteúdo que o Claude *produz*):
- ✅ Relatório de análise de briefing
- ✅ **Reporte de progresso para o cliente** (alimentado por Asana + Airtable, regenerado no mesmo link)
- ✅ Calendário estratégico do mês, resumos visuais

**Não servem para** (e por isso o Airtable existe):
- ❌ Front-end ao vivo de banco — artefatos não fazem chamadas de rede; os dados são os do momento da geração
- ❌ Grid visual com muitas imagens — imagens externas são bloqueadas; só embutidas, com teto de ~16 MB
- ❌ App multiusuário com permissões

**Atenção no reporte ao cliente:** compartilhar artefato com alguém de fora do workspace = link público (qualquer um com o link vê). Mesmo modelo de um link de Figma. Validar com as marcas mais sensíveis.

---

## 7. O que muda para cada pessoa

**Para o time de social media:**
- Nada de `.env`, API key, terminal, Python
- Conversa com o Claude no Cowork; os dados aparecem no Airtable; as peças chegam anexadas ao post
- O grid é uma base compartilhada com status de aprovação — não um HTML na pasta de alguém

**Para a Carol (champion interna):**
- Admin dos conectores da organização (adiciona uma vez, o time só faz login)
- Dona das skills: edita regras editoriais (`rules/<marca>.md`), calendário, escopos por marca — em markdown simples
- Interlocutora com a Supernova para evoluções

**Para o cliente final (marcas):**
- Recebe reporte de progresso num link que se atualiza a cada ciclo
- (Opcional, a discutir) view compartilhada do grid para aprovação

**Para a Supernova:**
- Mantém: o MCP criativo (pequeno) e o repertório de skills (em parceria com a Carol)
- Não mantém mais: painel, bibliotecas Python, ambiente de ninguém

---

## 8. Fases do rollout

### Fase 0 — Validação (~1 dia, sem compromisso)
- [x] Protótipo Airtable com dados reais da Clinique ✔ *(jul/2026)*
- [x] Anexo por URL validado (Airtable baixa e hospeda) ✔
- [x] Leitura e interpretação visual de anexos pelo Claude ✔ — habilita a skill `qa-visual`
- [ ] Interface "Grid do Mês" (galeria agrupada por semana) — comparar com o painel atual
- [ ] Esqueleto do MCP criativo (FastMCP + bucket + presigned URL) e teste ponta a ponta
- [ ] Artefato de reporte alimentado por Asana + Airtable
- [ ] Confirmar conector Asana na prática
- [ ] Teste de artefato compartilhado por link público

### Fase 1 — Migração
- Migrar catálogo/estilos/grid para o Airtable como fonte de verdade
- Reescrever skills para os novos motores (conectores + MCP)
- Migrar lista de influencers do Google Sheets
- Deletar o `core/` Python e o painel
- Treinamento da Carol e do time

### Fase 2 — Expansão
- Runway (ou similar) se vídeo generativo além do Veo virar demanda
- Canva para peça estática com template, se o time quiser
- Sub-agentes por cliente (a estrutura `agents/` do plugin)
- Views de aprovação compartilhadas com o cliente final

---

## 9. Planos B (escape hatches)

Mecanismo único: MCP remoto hospedado pela Supernova. Casos mapeados, acionados só por lacuna comprovada:

| Lacuna | Plano B |
|--------|---------|
| Planilha que o Claude precisa escrever e **não pode** sair do Google (ex.: co-editada por cliente externo) | MCP Sheets-write com service account (a agência compartilha a planilha com o e-mail robô) |
| Qualidade do Canva insuficiente para peça estática | Já coberto — o MCP criativo usa Gemini |
| Vídeo além do Veo | Runway/Pika têm MCP remoto oficial (mesma fricção de instalação do nosso) |

---

## 10. Decisões que precisamos tomar juntos

*(a parte mais importante desta leitura — tragam respostas ou opiniões)*

1. **Plano Claude**: Teams confirmado. Quantos assentos? Quem é o admin da organização (Carol)?
2. **Airtable**: quem contrata e paga? Quem é dono da base? Plano Team do Airtable dá conta (permissões por base)?
3. **Confidencialidade**: briefings, catálogos e listas de influencers podem morar no Airtable? Alguma marca com cláusula que impeça? E o reporte por link público de artefato?
4. **Inventário de planilhas vivas**: quais planilhas do Drive o time espera que o Claude *edite*? (Define o que migra para o Airtable e se o caso "não pode sair do Google" existe de verdade)
5. **Uma base ou uma base por marca?** Proposta atual: uma base com tudo (mais simples). Se a confidencialidade entre marcas apertar, quebra-se por base depois.
6. **Vídeo**: demanda confirmada como "real agora". O fluxo atual (Veo com mockup como âncora) atende? O que falta?
7. **Reporte ao cliente**: qual o ciclo (semanal/mensal)? O que precisa ter? O Asana de vocês tem os dados que o reporte precisa?
8. **Aprovação do cliente final**: o cliente deve ver/aprovar o grid direto no Airtable (view compartilhada), ou o reporte por artefato basta?
9. **Canva**: vocês já usam? Faz sentido como camada opcional de peça com template?

---

## 11. Riscos e limites conhecidos (transparência)

- **Artefatos**: sem rede externa, sem imagens externas, storage limitado — por design, não vamos contorná-los; o Airtable cobre o que eles não fazem
- **Gallery do Airtable não agrupa** — mitigado com List agrupada e Interfaces
- **Anexo por URL** exige URL pública temporária — resolvido com presigned URLs no MCP; validado
- **Conector custom em plano Teams** pode ser restrito a admin — desejável (governança), mas confirmar na prática
- **Créditos/custos de geração** (Gemini/Veo) passam a ser centralizados na conta do MCP — bom para controle, mas alguém paga a conta; definir dono
- **Dependência residual da Supernova**: o MCP criativo. Mitigação: escopo mínimo, código simples, documentado — e qualquer dev consegue assumir

---

*Comentários: anotar direto neste documento ou trazer na próxima conversa.*
