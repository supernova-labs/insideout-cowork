# Contrato Airtable — Hyundai Social v1

## Descoberta e tipos

Use somente a base exata **InsideOut Hyundai Social**. Confira schema e opções
antes da leitura/escrita. Campos de relação são listas de IDs resolvidos na
sessão; escreva campos por ID e seleções pelo nome. Não escreva relações
reversas. Confira limites atuais do conector; lotes nunca excedem 10.

Na releitura, o conector pode devolver relações como objetos com `id` e `name`
e seleções como objetos com `name`. Compare IDs das relações e nomes das opções
com o lote enviado; não confunda diferença de representação com falha de escrita.

No schema abaixo: texto = singleLineText; longo = multilineText;
data = date ISO `AAAA-MM-DD`; URL = url; anexo = multipleAttachments;
inteiro = number de precisão 0. O primeiro campo de cada tabela é o primário.
Relações são multipleRecordLinks e obedecem a cardinalidade indicada.

## Tabelas e chaves

### Diretrizes

`Nome` (texto), `Chave` (texto), `Versão` (inteiro), `Estado` (seleção:
Confirmada/Pendente/Simulação/Arquivada), `Conteúdo` (longo), `Fontes` (longo),
`Confirmado em` (data), `Confirmado por` (texto).

Chave natural: `Chave + Versão`. No máximo uma versão não arquivada por chave.
O significado e os valores iniciais estão em `bootstrap.md`. Nunca promover
Simulação ou Pendente apenas porque o campo foi preenchido.

### Modelos

`Nome` (texto), `Slug` (texto), `Descrição` (longo), `Claims` (longo),
`Assets` (anexo), `Estado` (seleção: Ativo/Arquivado).
Chave: `Slug`. Semente: CRETA, HB20, KONA, PALISADE, i20 e IONIQ5; descrição,
claims e assets permanecem vazios até haver fonte explícita.

### Canais

`Nome` (texto), `Rede` (texto), `Perfil` (URL), `Formatos` (longo),
`Orientações` (longo), `Estado` (seleção: Confirmado/Pendente/Inativo).
Chave: `Rede`. Não limitar formatos ao vocabulário Feed/Story/Reel: distinguir
vídeo longo, Shorts, carrossel, estático e formatos específicos da rede.
Rede conhecida não confirma perfil, formatos e regras de reaproveitamento.

### Referências

`Nome` (texto), `URL` (URL), `Tipo` (seleção: Perfil/Exemplo/Agenda/Asset),
`Rede` (texto), `Papel` (texto), `Observado em` (data), `Publicado em` (data),
`Prévia` (anexo), `Direitos da prévia` (longo), `Limitações` (longo).
Chave: URL exata aprovada. Não remover parâmetros sem verificar equivalência.
Uma fonte de avaliação histórica não vira referência de geração independente.

### Ciclos mensais

`Nome` (texto), `Chave` (texto), `Mês` (texto `AAAA-MM`), `Modo` (seleção:
Operacional/Retrospectivo/Sintético), `Estado` (seleção:
Pesquisa/Proposta/Revisão/Validado pelo time), `Data de corte` (data),
`Pesquisa` (longo), `Exceções` (longo), `Pendências` (longo),
`Versões das diretrizes` (longo), `Versão da revisão` (inteiro),
`Fingerprint da revisão` (texto), `Revisão` (anexo), `Link da revisão` (URL).

Chave: `Hyundai|AAAA-MM|Modo|nome-do-piloto`; o nome-do-piloto é `mensal` em
operação. Não criar novo ciclo para cada edição. `Pesquisa` contém fontes,
publicação, observação, validade, cobertura e limites em linguagem legível.
Arquivos completos ficam no workspace da execução. Ciclo Validado pelo time
significa revisão interna, não aprovação automática de todas as ideias.

### Ideias

`Nome` (texto), `Chave pública` (texto UUID), `Ciclo` (relação única com Ciclos
mensais), `Editoria` (texto), `Pilar` (texto), `Modelos` (relação com Modelos),
`Descrição` (longo), `Execução proposta` (longo), `Referências` (relação com
Referências), `Custo adicional` (longo), `Tipo` (seleção: Ideia/Reserva influenciador),
`Semana reservada` (texto), `Lacunas` (longo), `Rationale interno` (longo),
`Fingerprint atual` (texto), `Aprovação` (seleção:
Pendente/Confirmada pelo time/Revogada), `Fingerprint aprovado` (texto),
`Evidência da confirmação` (longo), `Confirmado em` (data),
`Histórico de confirmações` (longo).

Chave primária operacional: UUID público imutável, atribuído antes da primeira
persistência. Antes de uma primeira criação, também pesquisar ciclo e proposta
(nome, publicações e conceito) para evitar recriar uma ideia com outro UUID.
Se houver candidata equivalente ou ambígua, reutilizar a inequívoca ou pedir
resolução; não deduplicar por semelhança automaticamente.

Reserva de influenciador pode ficar sem modelo, pessoa ou conceito. Não pode
receber aprovação de produção nem ser enviada enquanto estiver como reserva.

### Publicações

`Nome` (texto), `Chave pública` (texto UUID), `Ideia` (relação única com Ideias),
`Canal` (relação única com Canais), `Data de publicação` (data),
`Formato` (texto), `Adaptação` (longo), `Estado` (seleção: Proposta/Reserva/Retirada).

Uma publicação pertence a exatamente uma ideia e um canal; uma ideia pode ter
várias publicações. Chave: UUID imutável. Retirada preserva histórico, sai do
HTML e invalida aprovação material anterior; não apagar para ajustar o grid.
Data, rede e formato têm de estar definidos para enviar uma ideia à produção.

### Encaminhamentos

`Nome` (texto), `Chave` (texto), `Ideia` (relação única com Ideias),
`Projeto Asana` (URL), `Modo` (seleção: Teste/Operacional),
`Estado` (seleção: Preparado/Em envio/Parcial/Concluído/Incerto/Divergente),
`Fingerprint enviado` (texto), `Dados enviados` (longo),
`Tarefa Asana` (URL), `Texto Asana` (URL), `Arte Asana` (URL), `BMS Asana` (URL),
`Verificação` (longo), `Último erro` (longo).

Chave: `Chave pública da ideia + URL canônica do projeto`. Uma tarefa por ideia
e destino; variantes por rede ficam no descritivo. `Dados enviados` preserva o
lote aprovado e o retorno parcial, com datas de publicação separadas dos prazos
de produção. Nunca armazenar tokens, respostas cruas ou credenciais.

## Aprovação e integridade

Fingerprint da ideia segue `feedback-contract.md`, com os valores vivos de
modelos, referências e publicações. Nome ou URL de referência alterados também
exigem recálculo. Confirmação só vale se `Fingerprint aprovado = Fingerprint
atual` e houver evidência da confirmação humana explícita.

Antes de enviar, reconstruir o fingerprint a partir dos campos atuais; não
confiar apenas no texto salvo. Publições órfãs, relações múltiplas onde deveria
haver uma, duas chaves públicas iguais ou duas versões ativas bloqueiam os
itens afetados. Alterar campos derivados não corrige divergência silenciosamente.

## Implantação e gate

Criar primeiro as tabelas e campos simples; resolver IDs e acrescentar relações
depois. Relê-los antes de semear configuração. A base começa sem ciclos, ideias,
publicações ou encaminhamentos reais. Não migrar os testes da base antiga.
Cadastros mínimos e diretrizes são configuração autorizada, não piloto aprovado.
Ausência de conector, schema ou permissão deixa essa etapa explicitamente pendente.
