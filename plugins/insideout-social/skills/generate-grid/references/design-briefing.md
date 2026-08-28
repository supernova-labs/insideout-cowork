# Contrato do briefing de design

O briefing deve preservar o jeito de trabalho da Estela: orientação concreta,
organizada por peça e por tela, pronta para a designer produzir sem decodificar
campos técnicos. A planilha histórica é referência de linguagem e densidade,
não uma segunda fonte de verdade:

<https://docs.google.com/spreadsheets/d/1tzN3xMkf3Nu56CD2OttyvTWkvhFpRw-YoOq5EEEqtsk/edit?gid=1597413556#gid=1597413556>

## Como traduzir a célula histórica

Preserve a experiência de leitura da Estela na apresentação composta, mesmo
quando cada informação passa a ter um campo próprio:

| Bloco observado na planilha | Destino no fluxo novo |
|---|---|
| `REF` ou `REFS` | referência geral ou referência da tela correspondente |
| `PRODUTO` ou `PRODUTOS` | relações de produto e `assets obrigatórios` |
| `LETTERING` | `generate-copy`; posicionado junto à tela na apresentação |
| `TELA 1`, `TELA 2`... | sequência de telas e função de cada uma |
| instruções entre colchetes | movimento/interação ou observações de produção |
| reaproveitar Feed em Story | novo post adaptado ao canal e formato, ligado à mesma intenção |
| `POST PRONTO` ou `PLANO EM CRIAÇÃO` | estado operacional; não copiar para o briefing |

O resultado apresentado à designer deve continuar reunindo referência,
produtos, texto por tela e orientação de execução, ainda que o Airtable guarde
esses componentes separadamente.

## O que vem de outros campos

Não repita no texto do briefing:

- data, rede, formato, abordagem e produtos;
- rationale;
- lettering e legenda;
- estado operacional do post.

Esses dados são combinados somente na apresentação do primeiro take e do
snapshot.

## Conteúdo de `Briefing de design`

Use esta estrutura e omita blocos vazios:

```text
BRIEFING DE DESIGN
estrutura: <peça única, carrossel com N telas ou sequência>
referência geral: <nome/URL aprovada ou “sem referência definida”>

tela 1 — <função da tela>
direção visual: <composição, enquadramento, hierarquia e mood>
referência: <referência específica ou “usar referência geral”>
assets obrigatórios: <produto, foto, logo ou vazio>
elementos obrigatórios: <informação visual sustentada pela fonte>
movimento/interação: <quando aplicável>

tela N — <função da tela>
...

observações de produção: <acabamento, continuidade, recorte ou lacuna>
```

## Regras de qualidade

- Descreva a função e a direção de cada tela, não apenas o tema.
- Diferencie asset obrigatório de sugestão visual.
- Use somente referências colocadas em escopo.
- Marque uma ausência como lacuna; não invente foto, logo, textura ou cena.
- Em vídeo, descreva movimento ou continuidade, mas não gere frame nem mídia.
- Não inclua marcadores como `Post pronto`, `Aguardando briefing` ou
  `Plano em criação` no texto.
- `Lettering` permanece no campo de copy e é posicionado por tela apenas na
  apresentação composta.
