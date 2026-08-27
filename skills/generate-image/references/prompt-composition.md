# Composição de prompt para imagens InsideOut

## Princípio

Transformar dados operacionais em uma especificação visual, sem copiar campos
brutos nem inventar informação. O prompt deve separar claramente o que aparece,
como aparece, o que orienta a marca e o que é proibido.

## Ordem de composição

### 1. Uso e objetivo

- Canal e formato da peça.
- Título, abordagem e rationale do post.
- Papel da peça na sequência editorial.

### 2. Cena

- Ambiente ou fundo.
- Produto ou assunto principal.
- Elementos de apoio realmente pedidos ou implicados pelo conceito.
- Não adicionar personagens, props ou narrativa sem função.

### 3. Tratamento visual

- Referência visual como linguagem, não como fonte de fatos.
- Estilo ou mídia: fotografia, colagem, ilustração ou 3D.
- Iluminação: direção, dureza, temperatura e sombras.
- Mood e energia.
- Texturas, materiais e atmosfera.
- Composição: ângulo, enquadramento, profundidade, ponto focal e espaço seguro.

### 4. Marca

- Posicionamento orienta intenção e mood.
- Público orienta legibilidade e sofisticação.
- Paleta e Brand Guide orientam cor, tipografia e composição.
- Guardrails são restrições rígidas.
- Voz e mensagens-chave não viram texto na imagem automaticamente.

### 5. Produto

- Nome e descrição delimitam o assunto.
- Claims cadastrados limitam o que pode ser sugerido, mas não precisam aparecer.
- Fotos são rotuladas por papel.
- Em `preservar`, declarar a foto principal como elemento intocável.
- Em `recriar`, exigir fidelidade aproximada e conferência de rótulo.

### 6. Texto

- Incluir somente o `Lettering` aprovado ou texto pedido explicitamente.
- Citar todo texto entre aspas e exigir reprodução verbatim.
- Traduzir posição sugerida e hierarquia em instruções de layout.
- Nunca colocar a legenda inteira na arte.

### 7. Restrições

- Sem texto extra, marca d'água ou assinatura.
- Sem claim, benefício, número ou selo não cadastrado.
- Sem distorcer o produto no modo `preservar`.
- Sem trocar paleta ou tipografia contra o Brand Guide.
- Sem copiar logos, pessoas ou detalhes identificáveis de uma referência de
  estilo que não pertençam à marca.

## Template

Usar apenas as linhas que acrescentarem informação:

```text
Use case: ads-marketing
Asset type: <Feed, Story, Reel, capa ou peça avulsa>
Primary request: <objetivo visual do post>
Input images:
- Image 1 — <alvo de edição | referência de produto | referência de estilo>
Scene/backdrop: <ambiente>
Subject: <produto ou assunto>
Style/medium: <tratamento visual>
Composition/framing: <ângulo, enquadramento, foco e espaço seguro>
Lighting/mood: <luz, atmosfera e energia>
Color palette: <paleta e contraste>
Materials/textures: <superfícies relevantes>
Brand direction: <posicionamento, público e princípios visuais>
Text (verbatim): "<lettering exato>"
Product fidelity: <preservar ou recriar + invariantes>
Constraints: <o que deve permanecer>
Avoid: <erros e elementos proibidos>
```

## Modos

### Produto + referência

O produto determina o assunto. A referência determina o tratamento. Nunca
substituir o produto da marca pelo produto que aparece na referência.

### Somente produto

Usar direção de fotografia limpa e alinhada à marca. Não inventar um estilo
extravagante para preencher a ausência de referência.

### Somente referência

Usar título e rationale como assunto. Levar da referência cor, luz, composição,
textura e atmosfera; não copiar pessoas, logos ou objetos distintivos.

### Avulsa

Confirmar marca, finalidade e proporção quando ausentes. Não persistir em
`Posts` se não houver post. Criar `Peças` somente quando o usuário pedir que a
imagem passe a fazer parte do acervo operacional.

## Formato social

- Feed quadrado: `1:1`.
- Feed retrato: preferir `4:5` quando o gerador aceitar; usar enquadramento
  seguro para recorte quando não aceitar.
- Story e Reel: `9:16`.
- Capa horizontal: `16:9`.
- Carrossel: manter a mesma proporção e sistema visual em todas as telas.

Não inventar parâmetros técnicos que a ferramenta nativa não exponha. Descrever
o enquadramento e a proporção no prompt quando necessário.

## Auditoria em `Prompt`

Persistir um bloco legível:

```text
GERAÇÃO DE IMAGEM
modo: preservar
composição: produto + referência
formato: Feed 1:1
entradas:
- foto principal do produto — alvo de edição
- referência Luz suave — referência de estilo
motor: OpenAI image generation — nativo

PROMPT FINAL
<prompt enviado ao gerador>
```

Em refinamento, acrescentar a origem da versão e a mudança única solicitada.
