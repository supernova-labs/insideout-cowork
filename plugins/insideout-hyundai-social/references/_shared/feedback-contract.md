# Feedback de ideias Hyundai — v1.0

## Identidade e versão

Este contrato é independente do `insideout-grid-feedback` do Social. Aceite
somente `format: insideout-hyundai-feedback`, `schemaVersion: 1.0`, marca
Hyundai e ciclo explícito. Não converta arquivos do Social automaticamente.

`ideaKey` e `publicationKey` são UUIDs públicos imutáveis, não IDs do Airtable.
Editar título, canal ou data não troca as chaves. Repetir uma chave em dois
itens é erro, não forma de agrupar publicações.

## Canonicalização e fingerprints

Um conteúdo de ideia público tem exatamente estes campos:

```json
{
  "ideaKey": "UUID",
  "title": "Título",
  "editoria": "Informação",
  "pillar": "Product in Context",
  "models": ["KONA"],
  "kind": "ideia",
  "reservedWeek": "",
  "description": "Conceito",
  "execution": "Como será feito",
  "additionalCost": "Não estimado",
  "publications": [
    {"publicationKey":"UUID","date":"2026-09-08","network":"Instagram","format":"Carrossel","adaptation":"Execução desta rede"}
  ],
  "references": [
    {"url":"https://example.org/ref","label":"Exemplo","role":"Composição","previewDigest":"","previewRights":"","limitation":"Prévia indisponível"}
  ]
}
```

`kind` é `ideia` ou `reserva-influenciador`; strings ausentes são `""`, nunca
null. Campos extras são rejeitados. Publicações Retiradas não entram. Reservas
podem ter data vazia; ideias prontas para produção não podem. Timestamps de
comentário usam ISO 8601 UTC; mês e datas são validados como datas reais.

Antes de serializar, normalize strings em Unicode NFC e quebras CRLF/CR para LF,
sem remover espaços do conteúdo. Ordene chaves de objetos recursivamente por
ordem ordinal ASCII (todas as chaves deste contrato são ASCII); não use locale.
Ordene `models` por valor ordinal, `publications` por `publicationKey` e
`references` por URL, depois label e role. Rejeite duplicatas conflitantes.
Use JSON UTF-8 compacto, sem espaços adicionais, sem escapes ASCII de Unicode
e sem caracteres escapados desnecessariamente. Números não entram nos objetos
de hash; versão é string. Hash é `sha256:` + hexadecimal minúsculo.

`ideaFingerprint` é o hash do objeto público completo, não apenas título/data.
`previewDigest` é o SHA-256 dos bytes da prévia incorporada, ou vazio quando
ausente; não use a URL temporária do anexo como identidade. O manifesto incorpora
o conteúdo público completo para permitir reconstrução e conferência offline.

Uma revisão contém `brand`, `cycleKey`, `month`, `version` e `ideas`; cada item
de `ideas` tem `ideaKey`, `ideaFingerprint` e `content` (o objeto acima).
Ordene `ideas` por `ideaKey` para calcular o fingerprint da revisão sobre esse
objeto completo. A apresentação pode ordenar cronologicamente. O manifesto é
esse objeto mais `fingerprint`; este último fica fora do seu próprio hash.

O fingerprint muda ao alterar conceito, referência, prévia, custos, modelos,
execução ou qualquer publicação. Hash não autentica o cliente nem autoriza escrita.
Nunca aceite o hash declarado sem reconstruí-lo do manifesto e dos dados vivos.

## Pacote exportado

```json
{
  "format": "insideout-hyundai-feedback",
  "schemaVersion": "1.0",
  "exportedAt": "2026-10-16T15:00:00.000Z",
  "grid": {
    "brand": "Hyundai",
    "cycleKey": "Hyundai|2026-09|Sintético|piloto-v1",
    "month": "2026-09",
    "version": "v1",
    "fingerprint": "sha256:..."
  },
  "comments": [
    {
      "commentId": "UUID",
      "ideaKey": "UUID",
      "ideaFingerprint": "sha256:...",
      "kind": "ajuste",
      "message": "Propor outra referência.",
      "reviewer": "",
      "createdAt": "2026-10-16T14:50:00.000Z",
      "updatedAt": "2026-10-16T14:50:00.000Z"
    }
  ]
}
```

`commentId` é criado uma vez e preservado na edição. `message` não pode ser
vazia ou apenas espaço. Reviewer é opcional; não solicitar outros dados pessoais.
O JSON exportado não contém aprovações nem dados internos. Manifesto de origem
é guardado pelo time junto ao HTML; não confiar em manifesto fornecido só pelo
revisor para validar a versão esperada.

## Repetições e conflitos

LocalStorage usa formato, cycleKey e fingerprint. Mesmo commentId e mesmo
conteúdo é repetição; mesmo commentId com updatedAt posterior e mesma identidade
é revisão do comentário, não novo trabalho. Mesmo commentId com identidade
divergente ou mesmo timestamp e conteúdos diferentes é conflito. Textos iguais
com commentIds diferentes permanecem distintos.

A consolidação guarda fora do plugin um registro de importação por ciclo,
fingerprint e commentId com estado recebido/encaminhado/resolvido e digest do
comentário. Em outra sessão, reler esse checkpoint; sem ele não prometer
deduplicação entre execuções. Nenhum checkpoint concede aprovação.

CSV é cópia de leitura, nunca entrada canônica. Cabeçalho fixo:
`brand,month,version,grid_fingerprint,comment_id,idea_key,idea_fingerprint,kind,message,reviewer,created_at,updated_at`.
Para segurança de planilha, a cópia CSV neutraliza fórmulas; o JSON permanece
sem alteração de mensagem. Não incluir IDs, prompts, pessoas da equipe ou URLs
privadas de operação nos dois formatos.
