# Eval — esquema, mês e rota incompatíveis

## Prompt

> Receba três arquivos sintéticos: um CSV sem JSON; um insideout-grid-feedback
> de Clinique; e um insideout-hyundai-feedback cuja versão esperada é v2 mas
> cujo pacote diz v1. No último, há mensagem vazia e data impossível.

## Resultado esperado

- não importa CSV como canônico nem converte contrato Social;
- detecta marca/formato, versão, mensagem e data inválidos;
- não escreve nem cria aprovação a partir de pacote rejeitado;
- solicita a origem correta em linguagem de revisão, sem expor IDs.
