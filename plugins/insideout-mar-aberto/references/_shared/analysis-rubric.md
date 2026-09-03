# Rubrica de análise do Mar Aberto

Versão do contrato: `1.0.0`.

Analise cada comentário ou resposta separadamente. A rubrica é fixa; o modelo
ativo do Codex executa a classificação sem uma segunda revisão automática e sem
revisão humana item a item.

## Relevância

Um registro é relevante quando o mercado brasileiro e o Hyundai i20 são assunto
central ou contexto necessário da manifestação. Idioma, domínio e localização
são sinais, não filtros isolados. Marque como não relevante e explique
brevemente quando tratar apenas de outro veículo, outro mercado, spam ou assunto
sem relação material.

## Alvo

Use um ou mais alvos:

- `i20`;
- `hyundai`;
- `campaign`;
- `influencer`;
- `purchase-price`;
- `competitor`;
- `other`.

Uma opinião sobre influenciador ou campanha não herda automaticamente o
sentimento para o carro ou para a marca. Registre sentimento e confiança por
alvo em `target_sentiments`; `sentiment` resume o registro somente para a
distribuição principal e nunca substitui essa leitura multidimensional.

## Sentimento

- `positive`: avaliação favorável inequívoca do alvo;
- `negative`: avaliação desfavorável inequívoca do alvo;
- `neutral`: informação, pergunta ou manifestação sem valência relevante;
- `mixed`: reúne valências favoráveis e desfavoráveis sustentadas;
- `ambiguous`: ironia, contexto ausente ou sinais que não sustentam conclusão.

## Temas e confiança

Temas são multirrótulo e surgem do corpus; normalize sinônimos sem apagar
distinções materiais. Use confiança entre 0 e 1 para expressar a força da
classificação. Confiança baixa não muda a classe à força: preserve `ambiguous`
quando a evidência for insuficiente.

## Agregações

Na distribuição, cada registro relevante vale uma unidade, inclusive respostas.
Não multiplique registros multitema no denominador de sentimento. Calcule a
amplificação separadamente com curtidas e respostas disponíveis dentro de cada
plataforma. Nunca some engajamento bruto de Instagram e YouTube num índice
único.

## Evidências candidatas

Proponha um pool estratificado por plataforma, tema e sentimento. Inclua padrões
recorrentes, manifestações marcantes e contrapontos; não selecione apenas por
engajamento. Preserve texto integral somente nesse pool e sem identidade.
