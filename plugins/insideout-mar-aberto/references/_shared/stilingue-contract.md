# Contrato da exportação Stilingue

## Entrada confirmada

Antes de operar a Stilingue, confirme com o operador:

- projeto;
- filtro — no piloto, `nova busca i20`;
- data inicial e final;
- pasta local da execução.

O intervalo é registrado como informado na interface e acompanhado do fuso
`America/Sao_Paulo`. Não corrija filtro ou período por plausibilidade.

## Caminho prioritário

Peça que o operador anexe uma exportação oficial já baixada da Stilingue. Essa
é a entrada padrão porque reduz consumo de navegação, evita diferenças entre
navegadores e mantém o mesmo contrato auditável. A planilha continua sujeita a
todas as validações abaixo; “foi baixada manualmente” não prova sua validade.

Quando o arquivo não existir, oriente o operador pela interface. Execute a
exportação no navegador integrado apenas quando ele pedir explicitamente.

## Fluxo assistido opcional

1. Validar se a sessão da Stilingue está autenticada; se não estiver, pedir que
   o operador faça login diretamente na página.
2. Abrir a Central de Exportações.
3. Selecionar o filtro e o intervalo confirmados.
4. Confirmar a exportação e acompanhar o status.
5. Se o status permanecer carregando, atualizar a página uma vez e reler o
   estado antes de decidir o próximo passo.
6. Acionar o download quando disponível.
7. Se uma janela de `storage.googleapis.com` abrir vazia, verificar primeiro se
   o download já foi iniciado ou concluído. Uma página vazia não é pedido de
   autorização nem prova de sucesso.
8. Validar o arquivo baixado antes de promover a execução para coleta.

## Campos lógicos obrigatórios

A nomenclatura física pode variar entre versões da exportação, portanto resolva
os cabeçalhos por significado e registre o mapeamento usado:

| Campo lógico | Uso |
|---|---|
| publicação | identidade da ocorrência na exportação |
| rede | roteamento para Instagram, YouTube ou não suportada |
| URL da publicação | abertura da publicação e deduplicação |
| data da publicação | auditoria do recorte |
| texto ou título da publicação | contexto de relevância |

Cada linha válida também origina uma menção normalizada em
`working/mentions.jsonl`. Instagram, YouTube, X/Twitter, Facebook e portais
entram na análise de menções. Uma rede diferente é preservada na auditoria como
não suportada.

Normalize os rótulos `Twitter` e `X` para `x`; normalize `portal`, `portais`,
`site` e `notícia` para `portals`. Preserve o rótulo original na auditoria da
entrada.

Contagem informada de comentários e métricas de engajamento são opcionais. Se
existirem, preserve-as como sinais de reconciliação, nunca como teto de coleta
ou prova isolada de cobertura.

## Validação

Aceite somente uma planilha legível cujo conteúdo possua os cinco campos
lógicos obrigatórios e ao menos uma linha de publicação. Rejeite arquivo vazio,
HTML renomeado, planilha corrompida ou recorte divergente. Normalize URLs para
deduplicar, mas preserve a contagem de ocorrências originais na auditoria.
