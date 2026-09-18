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
│   └── diagnostic.json
├── analysis/
│   ├── records.jsonl
│   ├── aggregates.json
│   └── evidence-candidates.jsonl
├── review/
│   ├── coverage-decision.json
│   ├── editorial-gate-1.json
│   └── editorial-gate-2.json
├── feedback/
│   └── <timestamp>-<slug>.md
└── deliverables/
    ├── report.html
    ├── report.pdf
    └── analytics.xlsx
```

Crie somente os diretórios necessários para a etapa atual. Os arquivos
`working/mentions.jsonl` e `working/comments.jsonl` são temporários: remova-os
depois que a análise e o pool de evidências forem persistidos com sucesso. Se a
execução for interrompida antes disso, preserve-os até retomada ou exclusão
manual confirmada.

Feedback não depende de uma execução. Quando ela não existir, use uma pasta
escolhida pelo operador e crie
`insideout-mar-aberto-feedback/<timestamp>-<slug>.md`. O arquivo continua local,
portátil e fora do plugin.

## Checkpoints

Cada etapa grava seu resultado em arquivo temporário na mesma pasta, valida o
conteúdo e só então substitui o arquivo canônico. Atualize `manifest.json` por
último. Um checkpoint válido registra:

- versão do contrato;
- etapa e estado;
- instante de conclusão;
- entradas consumidas e seus hashes;
- saídas produzidas e seus hashes;
- contagens de reconciliação;
- lacunas ou falhas conhecidas.

O estado `blocked_coverage` mantém a etapa em `collection` e aponta para
`coverage/diagnostic.json`. A pessoa pode retomar a coleta ou pedir
explicitamente análise e relatório do corpus observado, registrando o modo
`limited_approved` em `review/coverage-decision.json`. Esse registro inclui
decisão, instante, lacunas e a confirmação de que o relatório descreverá
somente o corpus observado. Só então a execução muda para `in_progress` na
etapa `analysis`; sem esse registro, derivados analíticos são proibidos.

Divergência entre a Stilingue e os itens observados, quando a coleta chegou ao
esgotamento observável, não é `blocked_coverage`, não exige
`limited_approved` e não impede análise ou relatório.

O arquivo segue `schemas/coverage-decision.schema.json`. A decisão `continue`
mantém a etapa em coleta; somente `limited_approved` permite iniciar análise e
relatório com cobertura limitada.

Uma retomada confia apenas em checkpoints cujos arquivos e hashes continuam
válidos. Não repita uma etapa concluída quando suas entradas não mudaram.

Leia os schemas em `schemas/` antes de criar ou validar os arquivos canônicos.
