# Contrato operacional — InsideOut Social

Use este contrato ao operar a base **InsideOut Social** pelo conector oficial do
Airtable.

## Descoberta obrigatória

1. Localize a base pelo nome exato.
2. Liste tabelas e campos antes de ler ou escrever.
3. Resolva os IDs atuais de base, tabela, campo e registros em cada execução.
4. Nunca trate IDs observados numa sessão como conhecimento permanente.
5. Antes de declarar sucesso, releia os registros alterados.

As escritas exigem IDs de campo. Valores de seleção são escritos pelo nome
visível da opção. Relações são escritas como listas de IDs de registros.

## Fonte de verdade

| Tabela | Responsabilidade | Chave natural |
|---|---|---|
| `Marcas` | voz, posicionamento, público e identidade | `Slug` |
| `Canais da marca` | presença digital e diferenças editoriais por rede | `Marca + Rede` |
| `Produtos` | catálogo e claims ligados à marca | `Marca + Slug` |
| `Referências` | estilos curados e referências externas | `Slug`; para URL externa, reutilizar a mesma URL |
| `Posts` | grid editorial e fluxo de aprovação | com rede: `Marca + Canal da marca + Data + Título`; legado: `Marca + Data + Título` |
| `Peças` | mídia e trilha de geração | `Post + Tipo + Nome`; sem post, `Marca + Tipo + Nome` |

Quando uma chave natural encontrar mais de um registro, não escolha
silenciosamente: apresente a duplicidade e pare a escrita.

## Campos por tabela

### Marcas

- `Nome` — obrigatório
- `Slug` — obrigatório, lowercase kebab-case
- `Voz`
- `Mensagens-chave` — uma por linha
- `Público`
- `Posicionamento`
- `Brand Guide`
- `Guardrails`
- `Paleta`
- `Produtos`, `Posts`, `Peças` — relações reversas; não escrever diretamente

Criação mínima: `Nome + Slug`. Atualizações só alteram campos explicitamente
presentes no briefing e nunca apagam conteúdo existente com valores vazios.

### Canais da marca

- `Nome` — fórmula `Marca — Rede`; nunca escrever manualmente
- `Marca` — obrigatório, relação com exatamente um registro de `Marcas`
- `Rede` — obrigatório; seleção controlada
- `Perfil/URL`
- `Status` — `Ativo` ou `Inativo`
- `Objetivo editorial`
- `Orientações do canal` — somente diferenças em relação à marca
- `Formatos habilitados` — `Feed`, `Story` e/ou `Reel`
- `Posts` — relação reversa; não escrever diretamente

Criação mínima: `Marca + Rede + Status`. Pesquise sempre por essa chave antes
de criar. Um briefing pode propor canal, objetivo, formatos e orientações, mas
`analyze-briefing` só materializa a configuração após mostrar os valores e
receber confirmação explícita. Uma rede não cadastrada na seleção é decisão de
configuração: apresente-a antes de solicitar a nova opção.

Embora o Airtable transporte relações como listas, `Marca` deve conter
exatamente um registro. Zero ou múltiplas marcas tornam a chave ambígua e
bloqueiam a escrita.

### Produtos

- `Nome` — obrigatório
- `Slug` — obrigatório, lowercase kebab-case
- `Marca` — obrigatório, relação com um registro de `Marcas`
- `Descrição`
- `Claims` — um por linha; não inventar nem reescrever como fato científico
- `Tags` — somente opções já disponíveis
- `Fotos`
- `Status` — `Ativo` ou `Arquivado`
- `Posts`, `Peças` — relações reversas

Criação mínima: `Nome + Slug + Marca`. Um produto citado num briefing ativo pode
receber `Status = Ativo`; os demais campos ficam vazios quando não vierem da
fonte.

### Referências

- `Nome` — obrigatório
- `Tipo` — `Estilo curado` ou `Referência externa`
- `Slug` — obrigatório para material criado pelo fluxo
- `Categoria` — `Campanha`, `Produto` ou `Editorial`
- `Tags` — somente opções já disponíveis
- `Thumbnail`
- `Prompt` — necessário para estilo curado
- `URL` — necessário para referência externa
- `Quando usar`
- `Posts`, `Peças` — relações reversas

Só crie uma referência quando o usuário fornecer ou aprovar material explícito.
Não invente referência para preencher um post. Reutilize primeiro as referências
existentes.

### Posts

- `Título` — obrigatório
- `Data` — obrigatório, `AAAA-MM-DD`
- `Marca` — obrigatório
- `Canal da marca` — relação obrigatória para posts novos, com exatamente um
  registro ativo e compatível com o formato; pode estar vazio em registros
  legados durante a migração
- `Canal` — `Feed`, `Story` ou `Reel`
- `Abordagem` — `Produto`, `Data Oportunidade`, `Educacional`, `Editorial` ou `Spoiler`
- `Produto` — relação opcional
- `Referência` — relação opcional
- `Lettering` — vazio na Parte 1; na Parte 2 recebe somente o bloco aprovado de
  `generate-copy`
- `Legenda` — vazio na Parte 1; na Parte 2 recebe somente a legenda aprovada de
  `generate-copy`
- `Rationale` — obrigatório na geração do grid
- `Briefing de design` — estrutura da peça, referências, direção visual por
  tela, assets, elementos obrigatórios, movimento ou interação e observações de
  produção; não duplica `Lettering`
- `Notas`
- `Mockup`, `Vídeo`, `Peças` — vazios na Parte 1; na Parte 2, `Mockup` recebe
  somente a imagem selecionada para o post e `Peças` permanece relação reversa
- `Status` — criar como `Rascunho`
- `Mês`, `Semana` — fórmulas; nunca escrever

Se já houver posts para a mesma marca e mês, não regenerar ou sobrescrever sem
mostrar o conflito e obter uma escolha explícita: revisar existentes, preencher
lacunas ou substituir.

Na geração de copy, use a chave com `Canal da marca` quando a relação existir;
para legado, `Marca + Data + Título` ainda deve resolver um único post.
`Legenda` e `Lettering` são independentes: atualizar um não apaga o outro.
Texto existente nunca é substituído ou concatenado sem escolha explícita. A
skill de copy não altera título, data, relações, rationale, notas, status ou
anexos.

### Peças

- `Nome` — obrigatório
- `Tipo` — `Imagem` ou `Vídeo`
- `Arquivo`
- `Marca`
- `Produto`
- `Referência`
- `Post`
- `Prompt`
- `Status` — `Gerada`, `Aprovada` ou `Descartada`

Na Parte 1, esta tabela é somente um teste de contrato. Um registro marcado
`[TESTE CODEX]` pode ser criado sem arquivo, ligado aos registros de teste e com
prompt explícito. A produção real pertence à Parte 2.

Na geração de imagem da Parte 2:

- `Nome` identifica a peça e sua versão; variantes usam versão crescente;
- `Tipo = Imagem`;
- `Prompt` guarda modo de fidelidade, composição, formato, papéis das imagens de
  entrada e o prompt final;
- `Status = Gerada` após a criação e só muda para `Aprovada` após aprovação
  humana explícita;
- `Arquivo` recebe o resultado final;
- `Marca`, `Produto`, `Referência` e `Post` reproduzem somente as relações
  efetivamente usadas;
- o mesmo arquivo selecionado é anexado a `Posts.Mockup`;
- uma peça ou mockup existente nunca é sobrescrito sem escolha explícita.

Na geração de vídeo da Parte 2:

- `Nome` identifica a peça e sua versão; variantes usam versão crescente;
- `Tipo = Vídeo`;
- `Prompt` guarda modo de geração, formato, duração, resolução, áudio, modelo,
  custo estimado aprovado, papéis das entradas e prompt final;
- `Status = Gerada` após a criação e só muda para `Aprovada` após aprovação
  humana explícita;
- `Arquivo` recebe o resultado final;
- `Marca`, `Produto`, `Referência` e `Post` reproduzem somente as relações
  efetivamente usadas;
- o mesmo arquivo selecionado é anexado a `Posts.Vídeo`;
- uma peça ou vídeo existente nunca é sobrescrito sem escolha explícita;
- URL temporária do gerador não substitui o arquivo persistido.

Se o conector não transportar um arquivo local, use a interface do Airtable
somente para o upload nos registros já resolvidos e continue usando o conector
para campos e relações. Releia peça e post pelo conector antes de declarar
sucesso. URLs temporárias de anexos servem para leitura ou download imediato,
nunca como referência durável.

## Escrita segura

- Pesquise pela chave natural antes de criar.
- Faça upsert apenas quando a chave for inequívoca.
- Escreva em lotes de até 10 registros durante o harness.
- Releia todos os registros escritos e confira relações e seleções.
- Use IDs somente nas chamadas do conector. Nunca exponha IDs de base, tabela,
  campo ou registro na resposta ao usuário.
- Nunca apague registros como parte automática de um eval.
- Use prefixo `[TESTE CODEX]` em títulos e nomes criados pelo harness.
- Limpeza é uma ação separada, destrutiva e exige confirmação explícita.

## Idempotência

Uma segunda execução com a mesma fixture deve:

- encontrar os mesmos registros;
- preservar os IDs;
- atualizar somente os campos fornecidos;
- criar zero duplicatas;
- relatar em linguagem de negócio o que foi reutilizado e o que foi atualizado,
  sem exibir os IDs preservados.

Para imagem, prompt idêntico e arquivo existente significam reutilização: não
chamar novamente o gerador, não criar nova versão e não duplicar anexos.

Para vídeo, entradas, prompt e parâmetros idênticos com arquivo existente
significam reutilização: não chamar novamente o gerador, não consumir créditos,
não criar nova versão e não duplicar anexos.
