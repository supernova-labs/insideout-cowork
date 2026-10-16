# Revisão de ideias Hyundai

## Arquivo e apresentação

Salve fora do plugin: `insideout-hyundai-AAAA-MM-referencias-vN.html`, acompanhado
do manifesto da revisão no workspace da execução. Não sobrescreva versões.
A casca usa InsideOut: branco, cinza `#606060`, azul-petróleo `#465E68`,
terracota `#A57063`, Poppins local ou sans-serif legível. Isso não modifica a
identidade Hyundai das referências. Assinatura InsideOut no cabeçalho/rodapé;
logo oficial somente quando fornecido, incorporado no arquivo.

Mostre Hyundai, mês, versão, estado **ideias e referências — antes da produção**,
panorama, contagens verificadas e calendário por semana. Cards representam
ideias; cada publicação por rede mostra sua data e formato. Reservas de
influenciadores aparecem identificadas, sem conteúdo ou identidade inventados.

Cada card mostra título, editoria, pilar, modelos, conceito, execução proposta,
publicações, referências e eventual custo adicional sustentado por fonte. Não
inclua copy final, prompts, rationale interno, pesquisas completas, instruções
operacionais, IDs de ferramentas ou informações da outra equipe. Hipóteses que
afetem a decisão do cliente são qualificadas, não apresentadas como fatos.

## Prévias

Incorpore imagens/capturas de referências somente quando acessíveis e com uso
permitido no contexto. Identifique **Referência — não é arte final** e mantenha
o link de origem. Não baixe mídia para contornar restrição de acesso. Sem
prévia utilizável, mantenha o link e o aviso **Prévia indisponível**; a ideia
continua na revisão. Não gere mockup ou placeholder parecido com arte final.

Assets incorporados usam data URLs ou dados locais empacotados no arquivo;
nenhuma imagem remota é carregada automaticamente. Descreva o mecanismo de
referências em vídeo e ofereça link direto; não prometa reprodução offline de
um vídeo remoto. Referência privada só entra quando o cliente tiver autorização
de acesso, sem cookies ou tokens. Caso contrário, peça alternativa ao time.

## Feedback

Use `../../../references/_shared/feedback-contract.md` integralmente. Cada card
tem **Adicionar feedback**, lista dos comentários e edição/remoção locais.
O formulário abre em modal nativo acessível, com tipo fixo Ajuste, mensagem
obrigatória e revisor opcional; fecha e devolve o foco ao botão de origem.
Não ofereça aprovação automática. O time confirma a versão a encaminhar.

Persistência é só localStorage por fingerprint da revisão. Exportar feedback
baixa JSON; Exportar CSV baixa a cópia de leitura. Avise que trocar de
navegador/dispositivo ou limpar dados pode perder comentários e que o arquivo
precisa ser encaminhado ao time. Limpar tudo exige confirmação. Não coletar
email, telefone, nem enviar comentários pela rede.

## Verificar

HTML sem backend, upload, analytics, dependências ou requisições externas.
Links editoriais podem abrir por ação explícita, com `noopener noreferrer`.
Aceite somente links HTTP(S); não transforme `javascript:`, `data:` ou `file:`
de uma fonte externa em link clicável. Prévia incorporada não contém conteúdo
ativo, scripts ou dependências externas.
Escape todo conteúdo externo; comentários entram como texto, nunca innerHTML.
Escape também o manifesto para impedir fechamento de script por texto externo.
Neutralize células CSV iniciadas por `=`, `+`, `-`, `@`, tab ou retorno, além
do escaping CSV convencional; o JSON preserva a mensagem original.

Abra em desktop e tela estreita. Confira leitura por teclado, foco, contraste,
contagem, referências, ausência de rede e de dados internos. Sem JavaScript,
o calendário continua legível e avisa que comentar/exportar exige JavaScript.
Teste criar, editar, remover, recarregar e exportar feedback; valide conteúdo,
versão e fingerprints contra o manifesto. Só declare o HTML verificado depois
dessas ações. Falha no localStorage deve avisar, não prometer que salvou.
