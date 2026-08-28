---
name: analyze-briefing
description: Analisa briefings mensais da InsideOut, valida completude e escopo contratado e, com confirmação, materializa marcas, produtos e canais no Airtable. Use quando o usuário pedir para entender, revisar, avaliar ou transformar um briefing em direção estratégica para o mês.
---

# Analisar briefing InsideOut

Transforme o briefing em uma direção estratégica fiel, acionável e pronta para
alimentar o grid editorial.

## Preparar

1. Leia `../../references/_shared/voz-usuario.md` e `../../references/_shared/about-insideout.md`.
2. Leia `references/framework.md`.
3. Identifique marca e, quando existir, leia
   `references/scopes/<slug-da-marca>.md`.
4. Se houver pedido de leitura ou escrita no Airtable, leia
   `../../references/_shared/airtable-contract.md` e descubra a base e o schema atuais.
5. Trabalhe somente com o briefing fornecido ou com fontes que o usuário colocou
   explicitamente em escopo.

## Executar

### 1. Confirmar entendimento

Apresente:

- cliente ou marca;
- período;
- serviços envolvidos;
- objetivo do mês;
- produtos-foco;
- redes, formatos e diferenças editoriais explicitamente informados;
- ações e datas principais.

Separe claramente o que está explícito do que não veio. Aguarde o OK do usuário
antes de aprofundar.

### 2. Levantar dúvidas

Faça somente perguntas que mudam a execução. Numere-as e priorize:

- informação crítica ausente;
- ambiguidade entre objetivo, produto, data ou entrega;
- conexão não explicada entre produção e veiculação;
- entregável que pode exceder ou escapar do contrato.

Não pergunte sobre orçamento, termo de imagem, construção do cronograma,
equipamentos ou tamanho da equipe de produção.

### 3. Produzir análise final

Entregue quatro blocos:

1. **Resumo estratégico** — objetivo, foco, timing e execução.
2. **Dúvidas para o cliente** — somente o que ainda está aberto.
3. **Pontos de atenção InsideOut** — dependências, timing, aprovação e riscos.
4. **Validação de escopo** — dentro do contrato, fora do contrato e cotas.

Quando não houver arquivo de escopo da marca, diga que o contrato ainda precisa
ser cadastrado para essa validação. Não interrompa o restante da análise.

### 4. Oferecer materialização no Airtable

Somente depois da análise e com confirmação explícita:

- localize a marca por `Slug`;
- mostre o que será criado ou atualizado e o que ficará vazio;
- crie ou atualize `Marcas` sem apagar campos existentes;
- localize cada produto por `Marca + Slug`;
- crie ou atualize apenas produtos citados explicitamente;
- use `Status = Ativo` para produtos do briefing atual;
- localize cada canal por `Marca + Rede`;
- para canais explícitos, mostre antes da escrita rede, perfil, status, objetivo,
  formatos e diferenças em relação à orientação geral da marca;
- crie ou atualize `Canais da marca` somente após confirmação, com
  `Status = Ativo` quando o briefing indicar uso atual;
- trate `Marca` como relação única e pare diante de canal duplicado ou ligado a
  mais de uma marca;
- se a rede ainda não existir na seleção, apresente essa mudança de
  configuração e aguarde aprovação específica;
- releia os registros e confirme o resultado em linguagem de negócio.

Não transforme ausência de canal em inativação e não copie a voz inteira da
marca para `Orientações do canal`: registre somente diferenças explícitas.
Não crie referências, posts ou peças nesta etapa.

### 5. Preparar a ficha para o grid

Quando houver plano editorial mensal e o usuário quiser continuar, apresente uma
ficha com:

- marca;
- mês `AAAA-MM`;
- lançamentos com data, produto e importância;
- produtos-foco;
- campanhas globais e datas conhecidas;
- canais ativos, objetivos editoriais e formatos habilitados;
- direcionais editoriais;
- lacunas que impedem decisões específicas.

Peça aprovação dessa ficha antes de acionar `generate-grid`. Não gere o grid em
silêncio.

## Validar

- Nenhum fato foi inventado.
- Cada dúvida afeta uma decisão real.
- Pedidos fora do contrato estão sinalizados sem serem recusados.
- Dados salvos foram relidos.
- Repetir a mesma materialização não cria duplicatas.
- Cada canal materializado tem uma marca, uma rede e uma chave inequívoca.
- Orientações de canal contêm apenas diferenças sustentadas pelo briefing.
- O usuário recebe resultado e próximo passo sem detalhes técnicos.

## Limites

- Não criar posts, referências ou peças.
- Não gerar copy, imagem ou vídeo.
- Não transformar inferência em atributo de marca ou claim de produto.
- Não cadastrar rede, perfil, objetivo, formato ou orientação por plausibilidade.
- Não sobrescrever conteúdo curado com campos vazios.
