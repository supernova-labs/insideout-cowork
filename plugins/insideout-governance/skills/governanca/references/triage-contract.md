# Contrato de triagem de fricções

## Fonte e cobertura

A fonte padrão é a aba
[`Fricções e fixes`](https://docs.google.com/spreadsheets/d/1w5IWXgefqsb15149T9SlNj6UEKNsJVJxHH4XAixA0uM/edit?gid=1952697901#gid=1952697901)
da planilha **Acervo de Governança - Inside Out**. Confirme os cabeçalhos A:N,
as opções de `Status` e o intervalo da tabela na sessão. Leia todas as linhas
ocupadas antes de declarar total ou ordem global. Exclua `[TESTE CODEX]` da
fila real e informe quantas linhas de teste encontrou. `Resolvida` e
`Não priorizada` ficam fora da fila aberta, mas podem fundamentar uma
recorrência ou decisão existente. Não altere nenhuma linha.

`Impacto` em E é uma categoria registrada; confira também o efeito descrito em
`Evidência` antes de aceitar a classificação. `Recorrência` em F é uma
categoria, não a contagem: conte o relato inicial e somente entradas
`Recorrência: ...` distintas em G. Se não for possível distingui-las, registre
a contagem como indeterminada. Um segundo ID com sintoma parecido é possível
duplicata, não uma ocorrência confirmada até revisão da equivalência.

## Classificação

| Impacto | Evidência mínima |
|---|---|
| Crítico | exposição de dados, escrita externa indevida, perda de dados ou entrega essencial bloqueada sem recuperação conhecida |
| Alto | entrega ou etapa essencial comprometida, com recuperação custosa ou paliativo disponível |
| Médio | perda material de qualidade, retrabalho ou atraso, com fluxo ainda viável |
| Baixo | inconveniência ou apresentação sem efeito material na entrega |
| Indeterminado | descrição insuficiente para distinguir os níveis anteriores |

Para a matriz, `Única` significa um relato inicial e nenhuma repetição
confirmada na linha; pode corresponder ao valor `Isolada` em F. `Recorrente`
significa pelo menos duas ocorrências distintas confirmadas, incluindo o
relato inicial. O valor `Sistêmica` em F exige evidência de alcance entre
componentes ou produtos e não substitui a contagem. Use `Indeterminada` se
o registro não permite contar com segurança. Ausência de anotações não prova
que o problema nunca voltou.

| Impacto | Única | Recorrente | Recorrência indeterminada |
|---|---|---|---|
| Crítico | P1 | P1 | P1 |
| Alto | P2 | P1 | P2 provisório |
| Médio | P3 | P2 | P3 provisório |
| Baixo | P4 | P3 | P4 provisório |
| Indeterminado | A esclarecer | A esclarecer | A esclarecer |

`P1` pede decisão imediata dos mantenedores; `P2` entra na próxima rodada de
fixes; `P3` entra no planejamento; `P4` pode aguardar. Esses rótulos são
recomendações, não mudam `Status` ou compromisso de prazo. Para a ordem,
coloque P1 a P4 primeiro, depois `A esclarecer`; em empate, maior número de
ocorrências confirmadas vem antes. Explique qualquer dependência que torne a
ordem prática diferente da ordem calculada.

## Formato obrigatório de saída

Use títulos legíveis, nunca IDs internos. Não inclua detalhes sensíveis mesmo
que estejam nos registros. Mantenha exatamente estas seções e campos; use
`não informado` ou `a esclarecer` quando faltar evidência.

```markdown
## Escopo e cobertura
- Fonte e data da leitura: ...
- Linhas lidas: ...; casos abertos: ...; resolvidos/não priorizados fora da fila: ...; testes excluídos: ...
- Limitações: ...

## Fila priorizada
| Ordem | Fricção | Plugin/componente | Status | Impacto | Ocorrências confirmadas | Prioridade |
|---|---|---|---|---|---:|---|
| 1 | ... | ... | ... | ... | ... | ... |

## Propostas de fix
### 1. Título legível da fricção
- Evidência: esperado, observado e efeito confirmados em frases curtas.
- Lacunas e hipóteses: o que não foi comprovado, inclusive causa provável.
- Impacto: nível e motivo.
- Recorrência: número ou indeterminada; origem da contagem.
- Prioridade: rótulo e aplicação da matriz.
- Fix sugerido: mudança delimitada e alvo provável.
- Critério de aceite: resultado verificável e cenário de regressão.
- Dependências e decisão: acesso, investigação ou aprovação necessária; estado da proposta.

## Pendências para decidir
- Perguntas que podem mudar a prioridade ou o fix, se houver.
```

Repita uma ficha em `Propostas de fix` para cada linha da fila, inclusive casos
`A esclarecer`: neles, o fix pode ser apenas uma hipótese limitada e a próxima
ação é obter evidência. Para uma fila vazia, mantenha `Escopo e cobertura`,
informe `0 fricções abertas` em `Fila priorizada` (ou `0 fricções registradas`
se a tabela inteira estiver vazia), e use `não há propostas` e `não há
pendências` nas seções finais. Se a leitura falhar, explique a falha em
`Escopo e cobertura` e não produza uma fila inventada.
