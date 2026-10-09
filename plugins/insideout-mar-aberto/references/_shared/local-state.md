# Contrato de estado local

## Pasta da execução

Use uma pasta escolhida pelo operador e crie um subdiretório por projeto e
execução. Todos os caminhos gravados no manifesto são relativos à raiz da
execução para que a pasta possa ser transferida. Rejeite caminhos absolutos e
qualquer segmento `..`; nenhum artefato pode escapar da pasta da execução.

```text
<projeto>/<run-id>/
├── manifest.json
├── input/
│   └── stilingue.xlsx
├── working/
│   ├── mentions.jsonl
│   └── comments.jsonl
├── coverage/
│   ├── records.jsonl
│   ├── diagnostic.json
│   └── diagnostic.md
├── analysis/
│   ├── records.jsonl
│   ├── aggregates.json
│   └── evidence-candidates.jsonl
├── review/
│   └── editorial-gate-1.json
├── templates/
│   ├── report-template.html
│   └── analytics-template.xlsx
└── deliverables/
    ├── report.html
    └── analytics.xlsx
```

Crie somente os diretórios necessários para a etapa atual. Os arquivos
`working/mentions.jsonl` e `working/comments.jsonl` são temporários: remova-os
depois que a análise e o pool de evidências forem persistidos com sucesso. Se a
execução for interrompida antes disso, preserve-os até retomada ou exclusão
manual confirmada.

As execuções antigas podem conter `feedback/<timestamp>-<slug>.md` ou uma pasta
`insideout-mar-aberto-feedback/` escolhida pelo operador. Preserve esses
arquivos locais sem migração automática. Novas fricções dos plugins são
registradas pela skill `registrar-friccao` do InsideOut Governança, fora do
estado da execução.

## Checkpoints

Cada etapa grava seu resultado em arquivo temporário na mesma pasta, valida o
conteúdo e só então substitui o arquivo canônico. Atualize `manifest.json` por
último. Um checkpoint válido registra:

- versão do contrato;
- etapa e estado;
- instante de conclusão;
- entradas consumidas e seus hashes;
- saídas produzidas e seus hashes;
- versão do plugin, hashes dos diagnósticos de cobertura e dos dois templates
  usados no relatório;
- contagens de reconciliação;
- lacunas ou falhas conhecidas.

Nas novas execuções, `coverage/diagnostic.json` e `coverage/diagnostic.md`
acompanham toda coleta fechada. O manifesto registra ambos os caminhos e
hashes. Com todas as publicações obrigatórias em estado explícito, a análise
segue sobre o observado; `coverage_mode` vale `complete` ou
`observed_with_gaps`. Falta de checkpoint mantém a etapa em `collection`.
Lacunas materiais para uma conclusão são tratadas no Gate 1: retome a coleta
ou reformule/omita a afirmação antes de aprovar o relatório. Divergência apenas
da Stilingue é ressalva de auditoria e não impede promoção.

`review/coverage-decision.json` e o estado `blocked_coverage` pertencem aos
contratos antigos; preserve-os nas execuções existentes, sem migração.

Uma retomada confia apenas em checkpoints cujos arquivos e hashes continuam
válidos. Não repita uma etapa concluída quando suas entradas não mudaram.

O checkpoint final é gravado somente após reabrir, renderizar e reconciliar
`report.html` e `analytics.xlsx`. Edição manual posterior não reescreve o
checkpoint; o PDF exportado pela equipe fica fora dele. Preserve sem migração
os manifests e artefatos de execuções antigas com contratos `2.0.0`,
`3.0.0` e `4.0.0`. Novas execuções usam `4.1.0`.

Leia os schemas em `schemas/` antes de criar ou validar os arquivos canônicos.
