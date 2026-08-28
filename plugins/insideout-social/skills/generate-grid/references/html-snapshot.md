# Snapshot HTML do grid

Gere uma visão portátil para revisão do primeiro take. O arquivo não é painel,
aplicação nem fonte operacional.

## Local e nome

Salve fora do diretório do plugin, em local escolhido pelo usuário ou numa
pasta de artefatos do workspace. Use:

```text
insideout-grid-<slug-da-marca>-<AAAA-MM>-<versao>.html
```

Não sobrescreva arquivo existente; incremente a versão ou use momento de
geração inequívoco.

## Conteúdo

Mostre no cabeçalho:

- marca e mês;
- versão ou momento do snapshot;
- estado `primeiro take para revisão`;
- quantidade e distribuição por rede e formato.

Para cada post, mostre em linguagem de negócio:

- data, rede, formato, abordagem, título e produto;
- rationale;
- briefing de design organizado por tela;
- lettering posicionado junto à tela correspondente;
- legenda;
- lacunas, fontes de tendência usadas e estado de revisão quando aplicáveis.

Não mostre IDs, schema, logs, prompt interno, registros não selecionados, URLs
privadas ou campos operacionais desnecessários.

## Implementação do arquivo

- HTML sem dependências externas obrigatórias;
- CSS embutido e responsivo;
- JavaScript embutido opcional apenas para navegação ou filtros locais;
- nenhuma chamada de rede, formulário, persistência, upload ou escrita;
- estrutura semântica, contraste legível, foco visível e conteúdo utilizável sem
  JavaScript;
- indique lacunas com texto, não apenas cor;
- inclua `lang="pt-BR"`, título descritivo e viewport mobile.

## Verificação

Antes de entregar:

1. abra o arquivo localmente;
2. revise desktop e viewport estreito;
3. confira ausência de requisições externas e de dados internos;
4. compare contagem e conteúdo com o take selecionado;
5. informe que uma nova revisão gera outro snapshot.
