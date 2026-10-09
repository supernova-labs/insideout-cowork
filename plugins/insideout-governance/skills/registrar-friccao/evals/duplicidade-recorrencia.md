# Eval — duplicidade entre produtos e recorrência

## Prompt

> Quero reportar de novo que a coleta não retoma depois do login. Já existe
> uma fricção resolvida com o mesmo comportamento. Não crie outra entrada.

## Resultado esperado

- pesquisa ID, nota de fingerprint e sintoma na aba `Fricções e fixes` em todos os estados;
- mostra a possível duplicidade e seu estado sem reabri-la;
- oferece acrescentar uma recorrência sanitizada ou cancelar;
- só acrescenta a entrada `Recorrência: ...` em G e muda F quando houver
  evidência, depois de mostrar o texto e receber confirmação;
- preserva o status da linha, relê a alteração e não cria segundo registro.
