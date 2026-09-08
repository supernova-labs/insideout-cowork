# Eval — idempotência da curadoria

## Prompt

> Rode novamente a curadoria da MAC com as mesmas fontes, período e síntese já
> aprovados ontem.

## Resultado esperado

- encontra as referências existentes pela URL e não cria duplicatas;
- encontra a diretriz ativa equivalente e apresenta que não há mudança
  material;
- reutiliza a versão atual, sem criar nova versão nem arquivar registros;
- se a amostra mudou, mostra as diferenças e volta ao gate de aprovação;
- releitura confirma uma única versão ativa para a marca e o tipo.
