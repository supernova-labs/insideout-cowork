# Eval — planilha acima do espaço inicial do modelo

## Prompt

> Com Gate 1 aprovado e fixture sintética de 250 registros de análise,
> gere apresentação e planilha usando os templates distribuídos.

## Resultado esperado

- a aba `Análises` contém os 250 registros, sem truncamento;
- a tabela estruturada e seu filtro alcançam a linha do último registro;
- a linha 250 conserva bordas, fonte e formatos de data e número do corpo do
  modelo, sem voltar ao formato geral;
- as oito abas abrem, os cabeçalhos continuam congelados e os tipos de data,
  número e percentual são preservados;
- as contagens da planilha e da apresentação reconciliam com os agregados
  canônicos antes de concluir a execução.
