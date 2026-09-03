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
│   └── comments.jsonl
├── coverage/
│   └── records.jsonl
├── analysis/
│   ├── records.jsonl
│   ├── aggregates.json
│   └── evidence-candidates.jsonl
├── review/
│   ├── editorial-gate-1.json
│   └── editorial-gate-2.json
└── deliverables/
    ├── report.html
    ├── report.pdf
    └── analytics.xlsx
```

Crie somente os diretórios necessários para a etapa atual. O arquivo
`working/comments.jsonl` é temporário: remova-o depois que a análise e o pool de
evidências forem persistidos com sucesso. Se a execução for interrompida antes
disso, preserve-o até retomada ou exclusão manual confirmada.

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

Uma retomada confia apenas em checkpoints cujos arquivos e hashes continuam
válidos. Não repita uma etapa concluída quando suas entradas não mudaram.

Leia os schemas em `schemas/` antes de criar ou validar os arquivos canônicos.
