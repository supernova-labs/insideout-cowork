# Eval — retomada por checkpoint

## Prompt

> Retome uma execução cuja exportação e coleta estão concluídas, a análise está
> interrompida na metade e a pasta foi copiada para outro diretório.

## Resultado esperado

- valida manifesto, hashes e caminhos relativos;
- reutiliza exportação e coleta sem repetir o navegador;
- retoma somente registros analíticos ainda não concluídos;
- mantém o corpus até fechar e validar a análise;
- não cria uma segunda identidade de execução nem duplica registros.
