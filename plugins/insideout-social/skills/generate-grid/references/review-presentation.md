# Apresentação de revisão do grid

O primeiro take e seu snapshot são uma experiência de revisão da InsideOut:
uma leitura editorial, organizada e humana do mês. Este padrão se aplica à
apresentação do plano, não às artes que serão produzidas para cada marca.

## Assinatura da apresentação

O shell de revisão usa a identidade InsideOut de forma discreta:

- base branca, texto em cinza `#606060`, azul-petróleo `#465E68` e terracota
  `#A57063` para ênfases pontuais;
- Poppins quando estiver disponível localmente, com uma sans-serif legível como
  fallback; não importe fontes ou outros recursos externos;
- composição minimalista, com respiro, hierarquia tipográfica clara e poucas
  superfícies decorativas;
- textura ou granulação uniforme, quando usada, é sutil e nunca reduz a
  legibilidade nem compete com a informação.

Esta assinatura identifica o material de revisão. Ela não altera paleta,
tipografia, logo, assets, mood ou direção das peças do cliente: para o post, a
identidade da marca ou campanha sempre prevalece sobre a da InsideOut.

## Hierarquia da revisão

Apresente o primeiro take e o snapshot nesta ordem:

1. identificação: marca, mês, versão ou momento e estado `revisão interna —
   primeiro take`;
2. `Mês em foco`: somente os focos, campanhas e datas efetivamente confirmados
   no briefing;
3. indicadores calculados do take: publicações planejadas e distribuição por
   canal e formato;
4. calendário dividido por semanas, com intervalo de datas legível;
5. cards de post em ordem cronológica;
6. fechamento com versão e lembrete de que layouts e assets finais dependem de
   aprovação.

Não crie volume, campanhas, produtos, datas ou estados de aprovação para
preencher qualquer bloco. Quando um dado estiver ausente, mostre a lacuna em
texto claro ou omita o bloco quando ele não for aplicável.

## Card de post

Cada card contém, nesta hierarquia:

- data, rede/formato e abordagem;
- título e produto, quando houver;
- uma frase de contexto ou rationale;
- `Direção criativa`, derivada do briefing de design e organizada por tela;
- `Texto da arte`, vindo do lettering aprovado ou marcado como pendente;
- `Legenda`, vinda da copy aprovada ou marcada como pendente;
- referências visuais e de trend aplicadas, sempre com links diretos quando
  existirem;
- dependências de asset, produção ou aprovação ainda abertas.

No HTML, use elementos nativos expansíveis para os detalhes. A direção criativa
fica disponível de imediato; texto da arte e legenda podem ser recolhidos para
manter a leitura mensal escaneável. A informação continua acessível sem
JavaScript.

## Limites de implementação

- A apresentação é estática e não lê nem escreve no Airtable.
- Não requer fontes, imagens, bibliotecas ou chamadas de rede externas.
- O conteúdo precisa permanecer legível em viewport estreito e navegar por
  teclado, com foco visível e contraste suficiente.
- O snapshot não reproduz a identidade da marca usada como exemplo nem usa
  assets de cliente sem terem sido fornecidos para aquele grid.
