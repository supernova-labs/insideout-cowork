# Avaliação do InsideOut Mar Aberto

Os evals versionados provam decisões observáveis com fixtures sintéticas. Rode
cada cenário em uma tarefa nova e registre no `ACCEPTANCE_AUDIT.md`:

1. versão do plugin e do contrato — `0.2.0` e `2.0.0` nesta rodada;
2. prompt do eval;
3. artefatos produzidos ou preservados;
4. contagens e hashes reconciliados;
5. resultado `passou`, `falhou` ou `não executado`;
6. qualquer divergência de julgamento ou contrato.

Evals locais não substituem os testes operacionais M9. Login, navegação real,
download real, rascunho de e-mail e instalação pelo marketplace publicado
permanecem `não executado` até a equipe da InsideOut realizar a nova rodada.

Use somente fixtures do plugin ou dados criados especificamente para teste.
Nunca copie comentários, caminhos, tokens, cookies ou dados reais para a
auditoria.
