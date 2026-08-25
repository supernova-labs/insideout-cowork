# Plano de implementação — Codex × Airtable

> **Status:** Parte 1 validada; migração de `generate-copy` concluída em 26/07/2026  
> **Escopo deste ciclo:** Parte 1 e primeiro incremento da Parte 2  
> **Fora deste ciclo:** distribuição via marketplace, vídeo e Parte 3

Os resultados estão documentados em
[`parte-1-relatorio-validacao.md`](parte-1-relatorio-validacao.md) e
[`parte-2-generate-copy-relatorio-validacao.md`](parte-2-generate-copy-relatorio-validacao.md).
A migração da skill de imagem está descrita em
[`parte-2-generate-image-migracao.md`](parte-2-generate-image-migracao.md).

## 1. Objetivo

Validar o Codex como harness de construção, execução e avaliação das skills da InsideOut antes de decidir como distribuí-las.

As primeiras skills serão desenvolvidas dentro de `.codex/skills/` neste repositório e operarão a base **InsideOut Social** pelo plugin oficial do Airtable. O objetivo não é portar o motor Python existente: é preservar o repertório e o julgamento das skills, substituindo JSON, painel e bibliotecas locais por registros e views do Airtable.

Ao final da Parte 1, uma pessoa deve conseguir:

1. entregar um briefing ao Codex;
2. receber uma análise estratégica e de escopo;
3. materializar marca e produtos válidos no Airtable;
4. gerar um grid editorial ligado a marcas, produtos e referências;
5. revisar os posts nas views do Airtable;
6. repetir o fluxo sem duplicar registros ou inventar informações.

## 2. Princípios de implementação

- **Skill guarda conhecimento e julgamento.** Airtable guarda estado operacional.
- **Airtable é a fonte de verdade.** Nenhum JSON local será criado para marcas, produtos, referências, posts ou peças.
- **Conector oficial primeiro.** As skills usam o plugin oficial do Airtable, sem API própria, PAT no repositório ou wrapper Python.
- **Sem portar o `core/`.** O código atual é referência de comportamento e contrato, não base da nova implementação.
- **Fluxos idempotentes.** Reexecutar uma skill deve atualizar ou reutilizar registros existentes, nunca duplicá-los silenciosamente.
- **Não inventar campos ausentes.** Informação não presente no briefing permanece vazia ou vira questão explícita.
- **Julgamento separado do mecânico.** Calendário e vínculos podem ser determinísticos; escolha editorial e rationale precisam permanecer legíveis e auditáveis.
- **Conversação não técnica.** O time fala de briefing, marca, produto, referência, post e data — nunca de IDs, schemas ou chamadas de ferramenta.
- **Harness antes de distribuição.** Marketplace, empacotamento e instalação para a InsideOut só serão definidos depois dos testes locais.

## 3. Arquitetura local proposta

```text
.codex/
└── skills/
    ├── _shared/
    │   ├── about-insideout.md
    │   ├── voz-usuario.md
    │   └── airtable-contract.md
    ├── analyze-briefing/
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── framework.md
    │   │   └── scopes/
    │   │       └── clinique.md
    │   └── evals/
    │       ├── briefing-completo.md
    │       ├── briefing-incompleto.md
    │       └── briefing-fora-de-escopo.md
    └── generate-grid/
        ├── SKILL.md
        ├── references/
        │   ├── rules/
        │   │   └── clinique.md
        │   └── calendar/
        │       └── 2026.md
        └── evals/
            ├── grid-mensal.md
            ├── idempotencia.md
            └── vinculos-airtable.md
```

`_shared/airtable-contract.md` documentará nomes e responsabilidades das tabelas, chaves naturais, campos obrigatórios e regras de vínculo. IDs internos do Airtable não serão tratados como conhecimento permanente da skill: cada execução deve descobrir a base, as tabelas e os campos disponíveis.

## 4. Responsabilidades das skills

### 4.1 `analyze-briefing`

**Responsável por:**

- analisar o briefing pelo framework Produto × Timing × Execução;
- identificar lacunas, contradições e itens fora do escopo contratado;
- produzir uma síntese estratégica utilizável pelo grid;
- localizar ou criar a marca no Airtable;
- localizar, criar ou atualizar produtos explicitamente citados;
- preservar campos ausentes sem completar por inferência;
- devolver um boundary estruturado para `generate-grid`.

**Lê:** `Marcas`, `Produtos` e referências de escopo da própria skill.  
**Escreve:** `Marcas` e `Produtos`, somente quando solicitado pelo fluxo.  
**Não escreve:** `Posts` ou `Peças`.

**Chaves de idempotência recomendadas:**

- Marca: `Slug`
- Produto: `Marca + Slug`

### 4.2 `generate-grid`

**Responsável por:**

- consumir o resultado aprovado de `analyze-briefing`;
- ler regras editoriais e calendário versionados na skill;
- resolver marca, produtos e referências no Airtable;
- montar a distribuição do mês e registrar rationale por post;
- criar ou atualizar os registros em `Posts`;
- manter datas, canais, abordagens e vínculos coerentes;
- apresentar um resumo do grid e indicar a view do Airtable para revisão.

**Lê:** `Marcas`, `Produtos`, `Referências`, regras e calendário.  
**Escreve:** `Posts`.  
**Não gera:** copy final, mockup, vídeo ou arquivo de peça nesta etapa.

**Chave de idempotência recomendada:**

- Post: `Marca + Data + Título`, com revisão explícita quando mais de um post puder ocupar o mesmo dia.

### 4.3 Contrato provisório de `Peças`

`Peças` pertence funcionalmente à Parte 2. Na Parte 1 será validada apenas como contrato de integração: criar um registro de teste com nome, tipo, prompt, marca, produto, referência e post relacionados, sem exigir mídia gerada.

Esse teste comprova que o modelo suporta a próxima fase, mas não transforma `analyze-briefing` ou `generate-grid` em responsáveis por produção criativa.

## 5. Etapas da Parte 1

### Etapa 0 — Baseline e contratos

- Registrar o schema atual das tabelas `Marcas`, `Referências`, `Produtos`, `Posts` e `Peças`.
- Definir campos obrigatórios, opcionais e calculados.
- Definir chaves naturais e comportamento de atualização.
- Criar fixtures pequenas e controladas para os evals.
- Definir prefixo inequívoco para registros do harness, por exemplo `[TESTE CODEX]`.
- Definir protocolo de limpeza: registros só serão removidos após revisão e autorização explícita.

**Saída:** `_shared/airtable-contract.md` e fixtures aprovadas.

### Etapa 1 — Migrar `analyze-briefing`

- Extrair do `SKILL.md` atual somente framework, regras de julgamento, escopo e tom.
- Remover instruções ligadas a Python, filesystem, JSON e painel.
- Adaptar o fluxo opcional de catálogo para o Airtable.
- Criar resultado estruturado estável para consumo por `generate-grid`.
- Criar evals locais para briefing completo, incompleto e fora de escopo.
- Verificar que a análise conversacional continua útil mesmo sem escrita no Airtable.

**Gate de saída:**

- a skill é acionada por linguagem natural;
- não inventa informação ausente;
- diferencia lacuna de briefing de item fora de escopo;
- cria ou atualiza marca/produto sem duplicação;
- produz boundary consumível pela skill de grid.

### Etapa 2 — Migrar `generate-grid`

- Extrair regras editoriais, calendário e critérios de julgamento do fluxo atual.
- Remover operações de planilha, JSON, HTML, mockup e vídeo.
- Ler marca, produtos e referências pelo Airtable.
- Criar posts em lote respeitando os limites do conector.
- Persistir rationale em cada post.
- Implementar reexecução idempotente e modo de revisão antes de sobrescrever posts existentes.
- Criar evals locais de cobertura mensal, vínculos e idempotência.

**Gate de saída:**

- gera um mês coerente a partir do boundary de briefing;
- todos os posts têm marca, data, canal, abordagem e rationale adequados;
- produtos e referências são vinculados quando conhecidos;
- reexecução não duplica o mês;
- conflitos são apresentados ao usuário antes de alterar dados existentes.

### Etapa 3 — Operação isolada em threads do Codex

Cada thread começa limpa, recebe apenas o prompt e a fixture definidos e testa uma responsabilidade observável. Isso evita que contexto acumulado esconda lacunas da skill.

| Thread | Cenário | Escrita esperada | Verificação |
|---|---|---|---|
| 1 — Marcas | Analisar briefing de uma marca controlada | Criar ou atualizar 1 registro em `Marcas` | Campos vieram do briefing; slug estável; segunda execução não duplica |
| 2 — Produtos | Materializar produtos citados no briefing | Criar ou atualizar registros em `Produtos` ligados à marca | Claims não inventados; fotos vazias quando ausentes; vínculos corretos |
| 3 — Referências | Resolver uma referência existente e cadastrar uma nova referência explícita | Reutilizar 1 e criar 1 registro em `Referências` | Tipo, origem, prompt/URL e tags preservados; nada criado por suposição |
| 4 — Posts | Gerar um grid mensal controlado | Criar registros em `Posts` | Datas, canais, abordagens, produtos, referências e rationale coerentes |
| 5 — Peças | Validar o contrato provisório de produção | Criar 1 registro de metadados em `Peças`, ligado a um post | Relações e prompt persistem; arquivo pode permanecer vazio nesta fase |

Em cada thread:

1. registrar o prompt inicial;
2. executar a skill sem contexto manual adicional;
3. capturar o resultado conversacional;
4. reler os registros pelo conector;
5. comparar resultado com o esperado da fixture;
6. registrar falhas como ajustes da skill ou do contrato;
7. repetir o mesmo prompt para validar idempotência;
8. revisar os registros visualmente no Airtable.

### Etapa 4 — Fluxo ponta a ponta

Depois dos testes isolados:

1. iniciar uma nova thread;
2. analisar um briefing real controlado;
3. aprovar a síntese;
4. materializar marca e produtos;
5. gerar o grid;
6. revisar o resultado na Gallery, Calendar e Grid view;
7. reabrir um post e confirmar vínculos, rationale e campos;
8. reexecutar o fluxo e confirmar ausência de duplicação.

**Gate final da Parte 1:** o ciclo briefing → Airtable → grid funciona sem Python, JSON local ou painel gerado.

## 6. Estratégia de avaliação

Os evals terão duas camadas:

### Evals determinísticos

- estrutura mínima do resultado de briefing;
- detecção de campos ausentes e fora de escopo;
- cobertura e cadência do grid;
- existência de rationale;
- resolução de chaves naturais;
- idempotência;
- integridade dos vínculos entre tabelas.

### Evals de julgamento

- qualidade da síntese estratégica;
- adequação de produto, timing e abordagem;
- fidelidade às regras da marca;
- utilidade do rationale;
- clareza da conversa para uma pessoa não técnica.

Falhas determinísticas bloqueiam avanço. Falhas de julgamento viram casos de erro versionados dentro de `evals/` para evitar regressão.

## 7. Critérios de conclusão da Parte 1

- Skills locais existem em `.codex/skills/` e são descobertas pelo Codex.
- `analyze-briefing` e `generate-grid` não dependem de `core/`.
- A base `InsideOut Social` é operada pelo plugin oficial do Airtable.
- As cinco threads isoladas foram executadas e documentadas.
- Reexecuções controladas não criam duplicatas.
- Nenhum segredo ou token foi adicionado ao repositório.
- O fluxo completo foi revisado tanto pelos registros quanto pelas views do Airtable.
- Casos de erro relevantes foram incorporados aos evals.
- Não foi tomada decisão prematura sobre marketplace ou distribuição.

## 8. Roadmap posterior

### Parte 2 — Texto e produção criativa

1. [x] Migrar `generate-copy`.
2. [x] Definir geração nativa da OpenAI e migrar `generate-image`.
3. [x] Definir o motor de geração de vídeo e migrar `generate-video`.
4. Compor prompts a partir de marca, produto, referência, lettering e post.
5. Criar registros em `Peças` com prompt e parâmetros.
6. Anexar mídia à peça e ao post.
7. Validar persistência de anexos no Airtable e expiração segura de URLs temporárias.

O primeiro incremento da Parte 2 foi concluído com uma escrita controlada de
copy. As skills de imagem e vídeo estão implementadas e validadas
estruturalmente. O vídeo usa Higgsfield com frame inicial, estimativa de créditos
e aprovação antes da geração; falta executar o harness completo da nova skill.

### Parte 3 — Qualidade e expansão operacional

1. Criar `qa-visual` para avaliar anexos contra brand guide, guardrails e lettering.
2. Criar `reporte-cliente` cruzando Airtable e a ferramenta de gestão escolhida.
3. Criar `influencers` sobre a base migrada da planilha atual.
4. Definir critérios de compartilhamento, aprovação e confidencialidade.

## 9. Fora do escopo atual

- remover o plugin ou o `core/` existente;
- migrar dados reais em massa;
- implementar geração de imagem além da próxima prova controlada;
- construir `qa-visual`, reporte ou influencers;
- criar MCP próprio;
- empacotar ou publicar skills em marketplace;
- treinar o time da InsideOut.

Essas decisões só avançam depois que a Parte 1 provar que o conhecimento das skills e o Airtable funcionam juntos no Codex.
