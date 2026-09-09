---
name: export-stilingue
description: Exporta ou valida a planilha oficial da Stilingue para uma execução de Mar Aberto. Use quando a pessoa quiser iniciar o recorte, baixar publicações ou corrigir a entrada de uma análise.
---

# Validar a exportação oficial da Stilingue

Produza uma entrada auditável para a coleta de comentários. Uma tela de status
ou uma janela vazia não substitui a validação do arquivo.

## Preparar

1. Leia `../../references/_shared/stilingue-contract.md` e
   `../../references/_shared/local-state.md`.
2. Leia `../../references/_shared/schemas/source-record.schema.json` antes de
   normalizar menções.
3. Confirme projeto, filtro, período e pasta da execução.
4. Peça primeiro a exportação oficial já baixada pelo operador. Preserve o
   original em `input/` e siga diretamente para a validação, sem abrir a
   Stilingue nem consumir navegação desnecessária.

## Orientar a exportação quando faltar o arquivo

Se o arquivo não foi fornecido, explique o caminho pela interface: abrir a
Central de Exportações, selecionar o filtro e o período confirmados, confirmar,
acompanhar o status e baixar o arquivo. O operador pode fazer isso no navegador
em que a Stilingue funciona para ele e então anexar a planilha à tarefa.

Use o navegador integrado para executar esse caminho apenas quando a pessoa
pedir explicitamente. Nesse caso, valide a sessão da Stilingue. Se for
necessário entrar, peça que o operador faça login diretamente na página e
continue depois que ele confirmar.

Na Central de Exportações, selecione exatamente o filtro e o período
confirmados, solicite a exportação e acompanhe o status. Se ele permanecer
carregando, atualize a página uma vez e releia. Quando o download estiver
disponível, acione-o e confirme o arquivo recebido. Trate uma janela vazia de
`storage.googleapis.com` como estado indeterminado até verificar o download.

## Validar e registrar

Use capacidade de planilhas para provar que o arquivo:

- é uma planilha legível, não HTML renomeado;
- contém os cinco campos lógicos obrigatórios;
- possui ao menos uma publicação;
- corresponde ao filtro e período confirmados ou deixa qualquer divergência
  explícita para correção.

Normalize URLs para deduplicação. Classifique cada ocorrência como menção e
roteie Instagram, YouTube, X/Twitter, Facebook e portais para análise. Outras
redes ficam explicitamente não suportadas. Preserve contagens originais e gere
`working/mentions.jsonl` e um checkpoint com hash, mapeamento de cabeçalhos,
número de linhas, URLs únicas, duplicatas e distribuição por rede.

## Falhar com precisão

Não avance para coleta quando o arquivo estiver vazio, corrompido, incompleto ou
divergente. Informe o que foi comprovado, a correção necessária e o arquivo que
permaneceu preservado. Reutilize um checkpoint válido em retomadas.

## Limites

- Não aceitar planilha genérica ou lista manual de links como substituta.
- Não tratar a automação do navegador como caminho obrigatório.
- Não inventar cabeçalhos ausentes.
- Não registrar cookies, senha ou segundo fator.
- Não interpretar contagem informada como cobertura de comentários.
