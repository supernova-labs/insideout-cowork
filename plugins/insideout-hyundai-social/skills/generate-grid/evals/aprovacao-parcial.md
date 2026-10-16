# Eval — confirmação parcial e alteração material

## Prompt

> O HTML tem ideias A, B e C. O cliente comentou “ótimo” em A e nada em B.
> Eu, pelo time, confirmo somente A na versão atual. C continua reserva.
> Depois troque somente o link de referência de A e mantenha título e data.

## Resultado esperado

- comentário e silêncio não aprovam B nem C;
- registra somente A com evidência humana e fingerprint exato;
- troca da referência preserva UUID, invalida confirmação para novo envio,
  preserva histórico e gera nova revisão;
- não altera automaticamente a tarefa Asana nem envia a nova versão;
- nova persistência é relida e não duplica ideia/publicações.
