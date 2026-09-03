---
name: export-stilingue
description: Exporta ou valida a planilha oficial da Stilingue para uma execução de Mar Aberto. Use quando a pessoa quiser iniciar o recorte, baixar publicações ou corrigir a entrada de uma análise.
---

# Exportar publicações da Stilingue

Produza uma entrada auditável para a coleta de comentários. Uma tela de status
ou uma janela vazia não substitui a validação do arquivo.

## Preparar

1. Leia `../../references/_shared/stilingue-contract.md` e
   `../../references/_shared/local-state.md`.
2. Confirme projeto, filtro, período e pasta da execução.
3. Se a pessoa já forneceu uma exportação, preserve o original em `input/` e
   siga diretamente para a validação.

## Exportar pelo navegador

Valide a sessão da Stilingue. Se for necessário entrar, peça que o operador faça
login diretamente na página e continue depois que ele confirmar.

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

Normalize URLs para deduplicação. Classifique as linhas em Instagram, YouTube e
canal não suportado. Preserve contagens originais e gere um checkpoint com
hash, mapeamento de cabeçalhos, número de linhas, URLs únicas, duplicatas e
distribuição por rede.

## Falhar com precisão

Não avance para coleta quando o arquivo estiver vazio, corrompido, incompleto ou
divergente. Informe o que foi comprovado, a correção necessária e o arquivo que
permaneceu preservado. Reutilize um checkpoint válido em retomadas.

## Limites

- Não aceitar planilha genérica ou lista manual de links como substituta.
- Não inventar cabeçalhos ausentes.
- Não registrar cookies, senha ou segundo fator.
- Não interpretar contagem informada como cobertura de comentários.
