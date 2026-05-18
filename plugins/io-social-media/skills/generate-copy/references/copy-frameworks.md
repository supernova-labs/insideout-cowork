# Frameworks de copy e lettering — o que funciona e o que não funciona

Base de conhecimento da skill `generate-copy`. Pesquisa consolidada (fontes no
fim). Dois artefatos diferentes, regras diferentes:

- **Copy do post** = a **legenda** (caption). Texto que acompanha a peça no feed.
- **Lettering** = o texto **dentro da imagem** (headline/arte). Tipográfico,
  visual, curtíssimo.

> **Princípio mestre:** a imagem leva o **gancho**, a legenda **expande**. Texto
> na imagem é title, não parágrafo. Menos palavras = mais impacto. Quando em
> dúvida sobre colocar mais texto na arte: não coloque — mande pra legenda.

---

## 1. Copy do post (legenda)

### Estrutura canônica: Hook → Valor → CTA

Toda legenda tem três blocos. O que muda por plataforma é o **tamanho** de cada
um, não a estrutura.

1. **Hook** (1ª linha) — para o scroll. ~1,5s de atenção. Só funciona se for a
   primeira coisa visível (ver cortes por plataforma abaixo).
2. **Valor/corpo** — entrega o insight, a história, o porquê. Linguagem humana,
   como quem conversa — não como quem anuncia.
3. **CTA** — uma ação clara, em **linha isolada** (o olho tem que pousar nela).

### Regras do hook

- **Sem emoji no hook.** Emoji na 1ª linha atrapalha leitura e dilui o impacto.
  Emoji só no corpo e antes do CTA (pra dirigir o olhar).
- **Big swing**: pergunta, hot take, número, afirmação que gera concordância ou
  discordância. Dá ao leitor algo pra reagir.
- **História > instrução**: "Como eu..." performa melhor que "Como fazer..." —
  o leitor quer a história real, não o tutorial.
- Escreva **2–3 hooks alternativos** e ofereça os melhores. Testar variações de
  hook é a alavanca de performance número um.

### Regras do CTA

- **Específico bate genérico ~3x.** "Comenta o número da dica que você vai testar
  primeiro" / "marca alguém que precisa ler isso" >>> "comenta aí", "o que acha?".
- Legenda com CTA claro gera **~70% mais comentários** que sem CTA.
- O CTA bom faz a próxima ação **óbvia, valiosa e de baixo atrito** — diz
  exatamente o que fazer e por quê.
- CTA em **linha própria**, nunca colado no fim de um parágrafo.

### Formatação e escaneabilidade

- 70% do consumo é **mobile** — quebras de linha e respiro são funcionais, não
  estéticos.
- Frases curtas (mire < 12 palavras). Um parágrafo = uma ideia.
- Linguagem humana e clara constrói confiança. **Buzzword, hype e ALL-CAPS
  derrubam credibilidade e engajamento.**

### Limites e sweet-spots por plataforma

| Plataforma | Limite | Sweet-spot | Corte visível (o "hook real") | Notas |
|---|---|---|---|---|
| **Instagram** (feed) | 2.200 chars | 150–500 chars | **~125 primeiros chars** antes do "...mais" | Mix saudável de portfólio: ~60% curtas (<150) p/ engajamento rápido e Reels, ~30% médias (150–300) p/ storytelling, ~10% longas (700–2.200) p/ educativo/caso |
| **Instagram** (Reels/Stories) | — | curtíssima | 1ª linha | Tom mais solto, direto, conversado |
| **LinkedIn** | ~3.000 chars | **1.300–1.900 chars** (+47% engajamento) | **~210 chars** antes do "ver mais" (60–70% decidem aqui) | Hook < 8 palavras; **rehook** na 2ª linha (desafia/expande o hook); estrutura Hook(~210) → Contexto(300–400) → Insight(500–700) → CTA(100–200); frases < 12 palavras; "wave" de whitespace pra guiar o olho |
| **Genérico / outras** | — | curto e direto | 1ª linha | Aplique Hook→Valor→CTA; assuma corte agressivo na 1ª linha |

> O número que mais importa é o **corte visível**: no Instagram tudo que importa
> tem que caber em ~125 chars; no LinkedIn em ~210. Escreva o hook pra esse
> espaço, não pro limite total.

---

## 2. Lettering (texto na imagem)

### Quantidade

- **Headline: 3–7 palavras.** Total na imagem: **≤ 15–20 palavras**.
- Sem parágrafo dentro da arte. Se precisa de frase explicativa, ela vai pra
  legenda — a imagem não é lugar de corpo de texto.

### Hierarquia visual

- O maior elemento é lido primeiro — a informação-chave tem que ser legível
  **num relance**. Defina **primário** (headline) e **secundário** (apoio/claim
  curto), com contraste de tamanho/peso claro entre eles.
- No máximo 2 níveis. Mais que isso vira ruído na peça.

### Tipografia

- **≤ 2 fontes** na peça inteira. Sans-serif para digital (legível no pequeno).
- Evite fontes decorativas que somem em tela pequena.

### Contraste e legibilidade

- Contraste mínimo: **3:1** para texto grande (>18pt normal / >14pt bold),
  **4.5:1** para texto de corpo. Se a foto não garante, use fundo sólido atrás
  do texto ou overlay escuro na imagem.
- **Teste no mobile**: 70% verá em tela pequena. Cheque tamanho, espaçamento e
  comprimento de linha como se fosse num celular.

### Espaço seguro (costura com `image-generation`)

Quando o lettering vai ser **gravado na imagem**, ele entra como instrução
explícita de texto no prompt da `image-generation` — e a peça precisa de
**espaço seguro** reservado na composição (a `image-generation` já enriquece
com "espaço seguro para texto/logo quando a peça for receber copy"). Entregue o
lettering como bloco estruturado (headline / apoio / posição sugerida) pra ele
ser injetável, não como prosa solta.

---

## 3. O que NÃO funciona (anti-padrões)

**Na legenda:**
- Emoji no hook (atrapalha leitura, dilui impacto).
- CTA genérico ("comenta aí", "o que você acha?") — converte ~3x menos.
- Buzzword, hype publicitário, ALL-CAPS — derrubam credibilidade.
- Hook que só aparece depois do corte ("...mais"/"ver mais") — ninguém vê.
- Parede de texto sem quebra de linha (ilegível no mobile).
- Tom de anúncio em vez de tom de conversa.

**No lettering:**
- Mais de ~20 palavras / parágrafo dentro da imagem.
- Mais de 2 fontes; fonte decorativa ilegível no pequeno.
- Baixo contraste texto/fundo (texto some sobre a foto).
- Sem hierarquia (tudo do mesmo tamanho — nada captura primeiro).
- Repetir na imagem o que já está na legenda sem ganho (redundância morta).

---

## 4. Checklist rápido

**Copy do post:**
- [ ] Hook na 1ª linha, sem emoji, cabe no corte visível da plataforma
- [ ] 2–3 hooks alternativos oferecidos
- [ ] Corpo em linguagem humana, frases < 12 palavras, quebras pro mobile
- [ ] CTA específico, em linha isolada
- [ ] Tamanho dentro do sweet-spot da plataforma
- [ ] Voz = `brand.json` (voice/guardrails como restrição rígida)

**Lettering:**
- [ ] Headline 3–7 palavras; total ≤ 15–20
- [ ] Hierarquia primário/secundário explícita (≤ 2 níveis)
- [ ] Lembrete de ≤ 2 fontes, contraste mínimo, teste mobile
- [ ] Bloco estruturado (injetável pela `image-generation`), não prosa
- [ ] Mensagem-chave só virou texto-na-arte se o usuário pediu explicitamente

---

## Fontes

- Sprout Social — social media copywriting best practices: https://sproutsocial.com/insights/social-media-copywriting/
- Nilead — Hook-Value-CTA: https://nilead.com/article/how-to-write-captions-for-social-media
- Hire a Writer — Instagram captions 2025: https://www.hireawriter.us/social/instagram-captions-best-practices-for-2025
- ConnectSafely — ideal LinkedIn post length 2026: https://connectsafely.ai/articles/ideal-linkedin-post-length-engagement-guide-2026
- Zac Radbone — writing for LinkedIn 2025: https://www.linkedin.com/pulse/writing-linkedin-2025-hooks-formats-timing-actually-work-zac-radbone-xqhye
- Sendible — Instagram character limits: https://www.sendible.com/insights/instagram-character-limit
- Smashing Magazine — accessible text over images: https://www.smashingmagazine.com/2023/08/designing-accessible-text-over-images-part1/
- Faith Wachter — font readability on social graphics: https://faithwachter.com/an-essential-guide-to-font-readability-on-social-media-graphics/
- Penpot — typography hierarchy & readability: https://penpot.app/blog/typography-hierarchy-how-to-improve-readability/
