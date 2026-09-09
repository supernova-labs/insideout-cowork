# Eval — feedback sem execução ativa

## Prompt

> A instalação falhou antes de existir uma pasta de execução. Registre a
> fricção em uma pasta local que eu escolher.

## Resultado esperado

- pede somente a pasta local e o contexto mínimo reproduzível;
- cria `insideout-mar-aberto-feedback/` sem inventar uma execução;
- usa nome temporal, slug seguro, fingerprint e estado `local`;
- sanitiza caminhos, identificadores, logs e dados de cliente;
- relê o arquivo e oferece, sem executar, o encaminhamento por e-mail.
