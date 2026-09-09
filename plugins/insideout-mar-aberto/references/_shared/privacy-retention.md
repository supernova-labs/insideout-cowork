# Privacidade e retenção

## Durante coleta e processamento

Remova nome de usuário, nome exibido, perfil, foto e link individual antes de
persistir um comentário. Gere um identificador irreversível apenas para
deduplicação e encadeamento entre comentário e resposta. Não use esse
identificador para tentar recuperar a identidade.

O texto de menções, comentários e respostas pode existir em
`working/mentions.jsonl` e `working/comments.jsonl` enquanto a análise estiver
incompleta. Esses arquivos ficam locais, nunca entram no plugin, em evals, logs,
feedback ou controle de versão.

## Depois da análise

Persistem:

- registros analíticos sem texto bruto;
- agregações;
- auditoria de cobertura;
- pool curado de evidências, no qual o texto integral anonimizado é permitido.

Os corpora temporários são descartados assim que os artefatos derivados e suas
contagens forem validados. Uma execução incompleta não tem expiração automática:
o operador pode retomá-la ou confirmar sua exclusão manual.

## Produtos finais e feedback

A planilha contém todos os dados analíticos, mas não recompõe o corpus bruto.
Somente a aba `Evidências` pode conter texto integral e apenas para trechos
aprovados no primeiro gate editorial. Relatos de feedback devem generalizar
cliente, campanha, caminhos, URLs, conteúdo e qualquer identificador da
execução. O caminho exibido ao operador depois da gravação não deve ser copiado
para dentro do próprio relato.
