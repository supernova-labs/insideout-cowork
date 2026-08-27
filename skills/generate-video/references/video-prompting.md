# Direção de movimento e prompt para vídeos InsideOut

## Princípio

Vídeo não é uma imagem com adjetivos extras. O prompt deve dizer o que permanece
fixo, o que muda ao longo do tempo e como a câmera observa essa mudança. Em
image-to-video, a imagem aprovada manda na aparência; o prompt manda no
movimento.

## Escolha do modo

| Situação | Modo | Entradas mínimas |
|---|---|---|
| Animar uma peça aprovada | imagem para vídeo | frame inicial |
| Chegar a uma composição específica | início e fim | frames inicial e final |
| Criar uma cena sem arte anterior | texto para vídeo | direção aprovada |
| Alterar ou prolongar um clipe | editar ou estender | vídeo-fonte |

Preferir `imagem para vídeo` para campanhas, produtos e veículos reais. Usar
texto para vídeo apenas quando a liberdade visual for desejada.

## Ordem de composição

### 1. Uso e duração

- Destino: Feed, Story, Reel, teaser ou capa em movimento.
- Uma única ideia para um clipe curto.
- Orientação e área segura coerentes com o canal.

### 2. Fonte e invariantes

- Identificar o frame ou vídeo que define a aparência.
- Listar produto, logotipo, lettering, placa, pessoas e composição que não podem
  mudar.
- Em marca real, declarar explicitamente que nenhum texto ou detalhe novo deve
  ser criado.

### 3. Evolução temporal

Descrever em ordem simples:

1. estado inicial;
2. movimento principal;
3. estado final.

Evitar acumular ações que não cabem na duração. Um clipe curto deve ter um gesto
principal, não uma montagem inteira.

### 4. Movimento do assunto e ambiente

- Assunto: parado, deslocamento, rotação, gesto ou transformação autorizada.
- Ambiente: reflexos, folhas, tecido, água, partículas, luz ou tráfego.
- Usar movimento ambiental sutil para dar vida sem deformar o produto.

### 5. Câmera

- Estática para máxima estabilidade.
- Push-in ou pull-out lento para revelar profundidade.
- Pan, tilt ou travelling suave quando houver espaço visual.
- Órbita somente quando a geometria não precisar ser reconstruída com precisão.
- Evitar cortes, mudança brusca de lente e câmera complexa sem necessidade.

### 6. Luz, ritmo e final

- Descrever mudança de luz apenas quando tiver função narrativa.
- Definir ritmo: contemplativo, elegante, energético ou urgente.
- Pedir encerramento estável quando o último frame precisar receber lettering,
  CTA ou edição posterior.

### 7. Restrições

- Sem morphing, flicker, deformação ou troca de identidade.
- Sem texto, logotipo, placa, rótulo, claim ou objeto novo.
- Sem pessoas ou membros extras.
- Sem zoom ou movimento que corte o assunto principal.
- Sem áudio, música ou locução quando não aprovados.

## Template de prompt

Usar apenas as linhas relevantes e escrever o prompt final como direção fluida,
não como dados crus:

```text
Use case: social video — <Story, Reel, Feed ou teaser>
Mode: <image-to-video, start-and-end, text-to-video, edit ou extend>
Source: <o que o frame/vídeo fornecido define>
Preserve exactly: <produto, geometria, cores, logo, lettering, placa, pessoas>
Initial state: <como a cena começa>
Primary motion: <uma ação principal ao longo do clipe>
Environmental motion: <movimento de apoio sutil>
Camera: <movimento, velocidade, lente ou estabilidade>
Lighting and mood: <luz, atmosfera e ritmo>
End state: <como o clipe termina>
Audio: <none | descrição aprovada>
Avoid: <morphing, flicker, novos objetos/textos e falhas específicas>
```

## Veículos e produtos reais

Quando houver um carro ou produto real:

- preferir câmera e ambiente em movimento a girar ou reconstruir o objeto;
- travar modelo, carroceria, rodas, faróis, grade, emblemas, cor e placa;
- não inventar versões, acessórios, claims ou funcionalidades;
- usar reflexos plausíveis e consistentes com a direção da luz;
- evitar órbita ampla quando existir somente um ângulo de referência;
- checar o contorno e a posição das rodas ou embalagem frame a frame.

## Áudio

O padrão é não gerar áudio quando o usuário não o pediu. Isso reduz ambiguidade
criativa e deixa música, locução e efeitos para uma etapa própria. Quando houver
áudio aprovado, registrar no prompt o tipo, a intenção e o que não deve aparecer.

## Auditoria em `Prompt`

Persistir um bloco legível:

```text
GERAÇÃO DE VÍDEO
modo: imagem para vídeo
formato: Story 9:16
duração: 5s
resolução: 720p
áudio: não
modelo: <modelo usado>
custo estimado: <créditos aprovados>
entradas:
- imagem da peça v1 — frame inicial
motor: Higgsfield

PROMPT FINAL
<prompt enviado ao gerador>
```

Em refinamento, acrescentar a versão de origem, o defeito observado e a mudança
única solicitada. Nunca registrar uma nova tentativa como continuação silenciosa
da anterior.

## Checklist temporal

Antes de persistir:

- reproduzir o clipe inteiro;
- comparar primeiro, meio e último frame;
- conferir invariantes de produto e marca;
- procurar morphing, flicker, deriva de cor e detalhes que aparecem ou somem;
- conferir cortes no assunto e área segura;
- ouvir o áudio inteiro quando houver;
- confirmar que o começo e o fim servem à edição ou publicação pretendida.
