---
name: generate-video
description: Gera, anima, edita e refina vídeos curtos de posts da InsideOut com o Higgsfield, usando frame inicial, referências visuais e direção de movimento, e registra a peça e o vídeo no Airtable. Use quando o usuário pedir vídeo, Reel, Story animado, teaser, image-to-video, frame inicial ou final, extensão, variação ou ajuste de um vídeo de post.
---

# Gerar vídeo

Transformar um post ou uma peça estática aprovada em um vídeo curto, coerente
com a marca e estável ao longo do tempo. O Airtable guarda o estado e a trilha
da peça; esta skill guarda o julgamento de movimento, continuidade e custo.

## Contexto obrigatório

Ler antes de operar:

- `../_shared/voz-usuario.md`;
- `../_shared/about-insideout.md`;
- `../_shared/airtable-contract.md`;
- `references/video-prompting.md`.

Usar o conector oficial do Airtable para dados e o conector instalado do
Higgsfield para estimar, gerar, acompanhar e exibir vídeos. Não chamar SDK,
API própria ou script externo. Se o Higgsfield não estiver conectado, explicar
a dependência e parar antes de alterar dados ou prometer o vídeo.

## Boundary

Ler `Marcas`, `Produtos`, `Referências`, `Posts` e `Peças`.

Escrever somente:

- um registro de vídeo em `Peças`;
- a relação `Post` da peça, que atualiza `Peças` no post automaticamente;
- `Vídeo` do post;
- `Arquivo`, `Prompt` e `Status` da peça.

Não alterar briefing, marca, produto, referência, grid, legenda, lettering ou
mockup. Não gerar uma nova imagem dentro desta skill. Quando faltar um frame
inicial adequado, encaminhar para `generate-image`.

## Resolver o pedido

1. Se o vídeo pertencer ao grid, localizar exatamente um post por
   `Marca + Data + Título`.
2. Ler o post completo e os registros relacionados de marca, produto,
   referência e peças existentes.
3. Conferir se o briefing ou escopo proíbe vídeo para aquele período. Se
   proibir, sinalizar a divergência antes de gerar; um teste técnico só pode
   seguir quando o usuário o autorizar explicitamente.
4. Se o pedido for avulso, confirmar marca, finalidade e formato somente quando
   isso mudar materialmente o resultado.
5. Classificar o modo:
   - `imagem para vídeo`, usando uma peça ou imagem aprovada como frame inicial;
   - `início e fim`, quando os dois frames foram fornecidos ou aprovados;
   - `texto para vídeo`, somente quando o usuário pedir uma cena sem âncora;
   - `editar ou estender`, quando houver um vídeo-fonte.
6. Para `imagem para vídeo`, escolher a fonte nesta ordem:
   - imagem indicada explicitamente pelo usuário;
   - `Mockup` aprovado ou selecionado no post;
   - peça de imagem aprovada ligada ao post.
7. Não usar silenciosamente uma imagem apenas `Gerada` quando houver mais de
   uma candidata. Mostrar as opções em linguagem de negócio e pedir a escolha.

## Tratar conflitos

- Se o post já tiver `Vídeo` ou peça de vídeo, mostrar um resumo e perguntar:
  reutilizar, refinar, criar variante ou substituir o vídeo atual.
- Nunca sobrescrever, descartar ou mudar o status de uma peça silenciosamente.
- Se a mesma peça já tiver o mesmo prompt, parâmetros e arquivo, reutilizar sem
  consumir novos créditos.
- Nomear variantes com versão crescente e preservar as versões anteriores.
- Só trocar `Posts.Vídeo` depois de o usuário escolher qual versão deve ocupar
  o campo principal.

## Fidelidade e continuidade

Usar preservação como padrão quando o frame contém produto, veículo,
embalagem, pessoa ou identidade de marca:

- manter geometria, proporções, cores, materiais, logotipo, lettering, placa e
  detalhes identificáveis;
- animar câmera, luz, reflexos e ambiente antes de movimentar o produto;
- pedir movimento discreto quando uma transformação não foi solicitada;
- repetir as invariantes no prompt e em cada refinamento;
- não acrescentar texto, locução, música, personagens ou objetos por
  iniciativa própria.

Movimento estrutural, troca de ângulo, morphing, mudança de cenário ou
recriação do produto exigem intenção explícita e conferência visual reforçada.

## Preparar e estimar

1. Inspecionar todos os frames e vídeos de entrada antes de gerar.
2. Rotular o papel de cada entrada: frame inicial, frame final, referência de
   imagem, referência de vídeo ou referência de áudio.
3. Mapear o formato:
   - Story e Reel: `9:16`;
   - Feed: preferir `1:1` ou retrato quando o modelo aceitar;
   - horizontal: `16:9` ou `21:9` somente quando o destino ou conceito pedir.
4. Escolher o modelo pelas capacidades atuais do Higgsfield. Para um
   image-to-video comum, preferir o modelo geral recomendado pelo conector;
   consultar os detalhes do modelo quando houver frame final, edição, extensão,
   áudio, múltiplas referências ou resolução específica.
5. Usar duração curta suficiente para uma única ideia. Não montar sequência de
   vários clipes sem aprovação de escopo e custo.
6. Compor o prompt pelo guia de referência, descrevendo evolução temporal,
   movimento do assunto, movimento do ambiente, câmera e invariantes.
7. Estimar o custo com exatamente o mesmo modelo, duração, resolução, áudio,
   quantidade e modo que serão enviados à geração.
8. Mostrar antes de gastar:
   - direção e modo;
   - frame ou vídeo de origem;
   - formato, duração e áudio;
   - modelo escolhido;
   - prompt final;
   - custo exato estimado em créditos e quantidade de variações.
9. Aguardar aprovação, exceto quando o usuário já tiver aprovado explicitamente
   esses mesmos parâmetros e custo na conversa atual.

Se o Higgsfield retornar uma escolha entre créditos e plano ilimitado, fazer ao
usuário exatamente a pergunta exigida pelo conector. Nunca decidir por ele.

## Gerar com Higgsfield

- Enviar uma geração por peça ou variante; não misturar conceitos diferentes.
- Passar o frame inicial no papel próprio de `start_image`; não confiar apenas
  na descrição textual de uma imagem já fornecida.
- Manter os parâmetros aprovados. Qualquer mudança que altere custo exige nova
  estimativa e aprovação.
- Acompanhar o trabalho até conclusão, falha ou cancelamento e comunicar uma
  atualização curta se a espera passar de um minuto.
- Exibir o vídeo concluído com o recurso de visualização do conector.
- Não iniciar automaticamente uma segunda tentativa paga. Se houver defeito
  objetivo, explicar o problema, propor uma correção única, estimar novamente e
  pedir aprovação do crédito adicional.
- Em falha sem cobrança confirmada, relatar o essencial e oferecer nova
  tentativa. Em cobrança incerta, conferir o trabalho e o saldo antes de repetir.

## Conferir o resultado

Inspecionar o vídeo inteiro e, no mínimo, o primeiro frame, um frame central e
o último frame antes de persistir:

- arquivo reproduzível, duração, orientação e resolução coerentes;
- primeiro frame compatível com a imagem-âncora;
- produto, veículo, pessoa e cenário estáveis ao longo do clipe;
- logotipo, lettering, rótulo, placa e geometria sem deformação;
- movimento de câmera e assunto conforme o prompt;
- ausência de morphing, flicker, objetos, textos, marcas d'água ou cortes
  inventados;
- começo e final utilizáveis no destino proposto;
- áudio ausente quando não aprovado ou coerente quando solicitado.

Não salvar como resultado válido um arquivo cujo defeito comprometa marca,
produto ou mensagem. Também não gastar novos créditos para corrigi-lo sem o OK
do usuário.

## Persistir no Airtable

Depois do vídeo válido:

1. Copiar o arquivo final para um caminho estável no workspace antes de
   vinculá-lo ao projeto; preservar versões anteriores.
2. Montar a auditoria com modo, formato, duração, resolução, áudio, modelo,
   custo estimado, papéis das entradas e prompt final.
3. Localizar a peça pela chave `Post + Tipo + Nome`; para peça avulsa sem post,
   usar `Marca + Tipo + Nome`.
4. Criar ou atualizar a peça com:
   - `Tipo = Vídeo`;
   - relações de marca, produto, referência e post quando aplicáveis;
   - `Prompt` com a auditoria completa;
   - `Status = Gerada`;
   - arquivo final em `Arquivo`.
5. Anexar o mesmo arquivo em `Vídeo` do post somente após resolver qualquer
   conflito existente.
6. Se o conector não transportar arquivo local, usar a interface do Airtable
   somente para o upload nos registros já resolvidos; manter o conector para
   campos e relações.
7. Reler peça e post e confirmar arquivo, prompt, status e relações.
8. Marcar `Aprovada` somente após aprovação humana explícita.

Não declarar conclusão enquanto o vídeo existir apenas no Higgsfield, numa URL
temporária ou no diretório local sem registro quando o pedido incluía Airtable.

## Resposta

Mostrar o vídeo e informar:

- post ou finalidade;
- direção e fonte aplicada;
- formato, duração e presença de áudio;
- custo efetivamente conhecido ou, se indisponível, a estimativa aprovada;
- o que foi criado, reutilizado ou atualizado;
- se a peça está `Gerada` ou `Aprovada`;
- próximo passo: aprovar, refinar ou enviar para `qa-visual`.

Não expor IDs, caminhos internos, chamadas de ferramenta ou detalhes de upload.
