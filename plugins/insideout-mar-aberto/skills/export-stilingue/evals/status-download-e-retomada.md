# Eval — status, download e retomada

## Prompt

> A exportação continua com status carregando. Após um refresh aparece o botão
> de download, que abre uma janela vazia de storage.googleapis.com. Já existe um
> checkpoint válido do mesmo filtro e período.

## Resultado esperado

- atualiza e relê o status uma vez antes de agir novamente;
- não interpreta a janela vazia como autorização ou download concluído;
- verifica se houve arquivo baixado e valida seu conteúdo;
- reutiliza o checkpoint existente quando entrada e hash coincidem;
- não solicita credenciais na conversa nem cria exportação duplicada.
