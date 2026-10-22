# Homologação InsideOut Mailing

Distribuição: catálogo da `main`. Plugin: `insideout-mailing` 0.1.0 (piloto).
A implantação é uma operação única; não existe skill de migração.

## Instalar o piloto

Siga o [guia de instalação](instalacao-plugins.md), inclusive a troca da origem
se o catálogo já apontar para uma antiga branch de piloto. No PowerShell do
próprio computador, fora do chat:

```powershell
codex plugin marketplace add supernova-labs/insideout-cowork --ref main
codex plugin add insideout-mailing@insideout
```

O catálogo `insideout` agora oferece Mailing e Hyundai Social na mesma `main`.
Confirme o Mailing instalado/ativado e abra tarefa nova para carregar as três
skills. A instalação não autoriza uso de dados reais nem substituição do Excel.

Homologação é esta rodada guiada de testes. Comece pelo preparo e pelos cenários
abaixo; registre também falhas e itens bloqueados, sem esperar testar tudo antes
de abrir o roteiro.

## Preparar

Usar o link da nova planilha piloto, confirmar conta e acesso e conferir as sete
abas e o contrato em Configuração. O Excel anterior continua oficial.
O plugin não concede acesso à planilha: autenticar individualmente.
Leitores e editores são definidos pelo proprietário, sem link público.
O relatório restrito da implantação reconcilia linhas, uniões, correções e pendências.
Não copiar dados reais para este repositório ou para resultados públicos.

## Casos em tarefas limpas

1. Pedir revisão de contatos sem gravação: obter fatos, lacunas e duplicatas.
2. Criar até dez contatos/vínculos sintéticos com prefixo [TESTE CODEX].
   Repetir e reler: zero duplicatas, mesmos identificadores.
3. Criar ação e lista sintéticas; incluir dois contatos; fechar uma versão.
4. Repetir a lista: mesma versão e mesmos itens. Mudar a seleção:
   nova versão, sem alteração da fechada.
5. Importar convite: presença e envio continuam não informados.
6. Importar duas listas sobrepostas da mesma ação: uma participação por pessoa.
7. Registrar envio com endereço explicitamente escolhido; mudar o cadastro:
   endereço histórico permanece igual.
8. Confrontar homônimos, e-mail de agência, conflito de endereço e texto com
   instruções/fórmulas: nada associado ou executado silenciosamente.
9. Aplicar todos os evals das três skills em tarefas limpas. Registrar
   passou/falhou/não executado, releitura e segunda execução.
10. Somente depois usar uma lista real, informando se representa convidados,
    confirmados, presentes, enviados ou entregues.

Não apagar os registros sintéticos durante a avaliação. Limpeza exige pedido
separado. Teste estrutural não comprova execução comportamental no Codex.

## Saída de teste

Registrar data, versão, cenário, resultado, evidência sanitizada e pendência.
Adotar a base como oficial e encerrar o Excel exige decisão posterior.
Sem fonte histórica, Ações, Listas, Itens de lista e Participações reais ficam vazios.
