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
- estado `revisão interna — primeiro take`;
- quantidade e distribuição por rede e formato.

Para cada post, mostre em linguagem de negócio:

- data, rede, formato, abordagem, título e produto;
- rationale;
- briefing de design organizado por tela;
- links clicáveis das referências visuais usadas;
- link direto do post ou vídeo que exemplifica uma trend aplicada;
- lettering posicionado junto à tela correspondente;
- legenda;
- lacunas, oportunidade de momento aplicada, estado dos assets finais e estado
  de revisão quando aplicáveis.

Não mostre IDs, schema, logs, prompt interno, registros não selecionados, URLs
privadas, a trilha completa de pesquisa ou campos operacionais desnecessários.
Links editoriais aprovados e exemplos públicos de trends não são URLs privadas.

## Fronteira da visualização para cliente

O snapshot desta etapa é interno e pode mostrar rationale, briefing de produção,
lacunas e referências. Não o apresente como entrega final ao cliente.

Uma futura visão para cliente deve ser gerada a partir dos mesmos posts depois
que a designer preencher os mockups no Airtable. Ela não recebe upload, edição
ou comentários dentro do Site. O conteúdo visível ao cliente ainda depende de
uma decisão editorial específica; até lá, não derive automaticamente essa visão.

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
5. confira que referências e trends aplicadas abrem os links esperados;
6. informe que uma nova revisão gera outro snapshot.
