# Protocolo de homologação — InsideOut Mar Aberto

Use este roteiro somente depois que a pessoa responsável pela publicação
informar uma referência exata e instalável do piloto. O protocolo comprova o
comportamento em contas reais da equipe da InsideOut; ele não substitui os
testes locais já registrados na auditoria.

Não cole neste documento senhas, códigos de autenticação, cookies, nomes de
perfis, links individuais de comentários, comentários reais, arquivos
exportados ou logs brutos. Registre apenas contagens, estados, tempos,
descrições sanitizadas e caminhos locais que não serão enviados ao repositório.

## Identificação da rodada

| Campo | Preenchimento |
|---|---|
| Referência publicada | `<ref-publicada>` |
| Commit publicado |  |
| Versão do plugin |  |
| Data e horário |  |
| Papel do operador |  |
| Ambiente |  |
| Período analisado |  |
| Filtro Stilingue | `nova busca i20` |

Use em cada prova um dos estados: `passou`, `falhou` ou `não executado`. Toda
falha precisa de uma descrição sanitizada e de um item de acompanhamento. Todo
teste não executado precisa registrar o motivo; ele nunca conta como sucesso.

## Preparação

1. Confirme com quem publicou o piloto a referência exata, o commit e a versão.
2. Em uma tarefa nova do Codex, instale a referência informada:

   ```powershell
   codex plugin marketplace add supernova-labs/insideout-cowork --ref <ref-publicada>
   codex plugin add insideout-mar-aberto@insideout
   ```

3. Tenha acesso individual à Stilingue, ao Instagram e ao YouTube. Faça cada
   login diretamente no navegador quando solicitado; não informe credenciais ao
   plugin.
4. Escolha um período controlado, curto o suficiente para conferência, e uma
   pasta local vazia para a execução.
5. Não envie a pasta da execução ao repositório. Compartilhe somente este
   protocolo sanitizado e os itens de acompanhamento.

## Provas operacionais

### M9-T1 — Instalação e descoberta

**Como executar**

1. Abra uma tarefa nova depois da instalação.
2. Peça para iniciar uma análise de Mar Aberto.
3. Confirme que o fluxo principal e as capacidades de exportação, coleta,
   análise, relatório e feedback são reconhecidos.

**Aceite:** a versão instalada coincide com a referência publicada e as seis
skills ficam disponíveis sem conflito com `insideout-social`.

**Registro:** estado: ___ · versão: ___ · ambiente: ___ · observação
sanitizada: ___

### M9-T2 — Exportação da Stilingue

**Como executar**

1. Inicie o fluxo sob demanda e confirme o filtro `nova busca i20` e o período.
2. Faça login na Stilingue diretamente no navegador.
3. Solicite a exportação; se o status não mudar, atualize a página como orientado.
4. Confirme que a janela de download entrega uma planilha válida, e não uma
   página vazia ou HTML.
5. Compare filtro, período e número de publicações exibidos com o manifesto
   local.

**Aceite:** filtro e período coincidem, o arquivo é validado e o manifesto
registra o mesmo recorte sem capturar credenciais.

**Registro:** estado: ___ · publicações: ___ · duração: ___ · observação
sanitizada: ___

### M9-T3 — Coleta no Instagram e YouTube

**Como executar**

1. Faça login em cada rede diretamente no navegador quando solicitado.
2. Acompanhe a abertura das publicações, a expansão de comentários e respostas
   e a paginação observável.
3. Confira por publicação as contagens observadas, respostas, falhas e estado
   de cobertura.
4. Verifique que uma publicação inacessível ou um canal não suportado aparece
   como lacuna e não bloqueia as demais.

**Aceite:** Instagram e YouTube têm cobertura auditável, falhas isoladas
continuam explícitas e nenhuma cobertura parcial é apresentada como completa.

**Registro:** estado: ___ · Instagram observado: ___ · YouTube observado: ___ ·
falhas/lacunas sanitizadas: ___ · duração: ___

### M9-T4 — Interrupção e retomada

**Como executar**

1. Interrompa deliberadamente a coleta depois que ao menos uma publicação tiver
   checkpoint.
2. Retome a mesma execução usando sua identidade e pasta originais.
3. Compare contagens e identificadores antes e depois da retomada.

**Aceite:** a execução retoma do checkpoint, não reinicia publicações concluídas
e não duplica comentários ou respostas.

**Registro:** estado: ___ · etapa interrompida: ___ · contagem antes/depois: ___
· duplicatas: ___ · observação sanitizada: ___

### M9-T5 — Primeiro gate editorial

**Como executar**

1. Deixe a análise de sentimento terminar automaticamente, sem revisar ou
   classificar comentários um a um.
2. Avalie as conclusões propostas, a estrutura narrativa e o pool de evidências.
3. Registre aprovação ou alterações solicitadas antes de autorizar o relatório.

**Aceite:** a análise é útil para a construção editorial, sentimentos mistos e
ambíguos permanecem visíveis, lacunas limitam as conclusões afetadas e o pool
inclui padrões, manifestações marcantes e contrapontos.

**Registro:** estado: ___ · decisão do gate: ___ · alterações solicitadas
sanitizadas: ___

### M9-T6 — Segundo gate e produtos finais

**Como executar**

1. Revise o HTML gerado depois do primeiro gate e registre ajustes editoriais.
2. Aprove ou rejeite o segundo gate.
3. Se aprovado, abra o HTML, o PDF e a planilha `.xlsx`.
4. Compare escopo, cobertura, totais, sentimento, temas, amplificação,
   evidências e metodologia entre os três produtos.

**Aceite:** os dois gates são respeitados; HTML, PDF e planilha abrem e são
coerentes; a planilha contém `Resumo`, `Cobertura`, `Publicações`, `Análises`,
`Agregações`, `Evidências` e `Metodologia`.

**Registro:** estado: ___ · decisão do gate: ___ · produtos abertos: ___ ·
divergências sanitizadas: ___

### M9-T7 — Privacidade e descarte

**Como executar**

1. Depois da conclusão, confirme que o corpus bruto temporário não existe mais.
2. Inspecione relatório e planilha procurando nomes, perfis, fotos, links
   individuais ou outros identificadores pessoais.
3. Confirme que textos integrais aparecem somente nas evidências aprovadas e
   anonimizadas; a aba `Análises` não deve conter texto bruto.

**Aceite:** corpus bruto descartado, identidades ausentes e somente evidências
aprovadas preservadas dentro da política de retenção.

**Registro:** estado: ___ · corpus ausente: ___ · achados de privacidade
sanitizados: ___

### M9-T8 — Feedback seguro

**Como executar**

1. Use a skill de feedback para registrar um achado real ou um cenário de teste.
2. Confirme tipo, título, versão testada e corpo sanitizado antes de publicar.
3. Se o GitHub estiver indisponível, confirme que o fallback copiável permanece
   marcado como não publicado.
4. Não publique se o texto contiver dados do cliente.

**Aceite:** issue relida ou fallback contém a versão testada e nenhum dado da
execução; duplicatas são apresentadas e cancelamento produz zero efeito externo.

**Registro:** estado: ___ · resultado (`issue` ou `fallback`): ___ · referência
sanitizada: ___

## Reconciliação final

| Verificação | Resultado |
|---|---|
| Todos os oito testes têm estado real |  |
| Nenhum `não executado` foi contado como sucesso |  |
| Toda falha possui item de acompanhamento |  |
| Nenhum dado real ou credencial entrou neste protocolo |  |
| A versão e o commit correspondem à referência publicada |  |

## Decisão do piloto

Escolha exatamente uma opção e registre o racional sanitizado:

- `liberar` — todos os critérios foram atendidos e não há falha crítica aberta;
- `iterar` — o valor foi comprovado, mas há falhas corrigíveis antes de ampliar
  o uso;
- `interromper` — cobertura, confiabilidade ou custo operacional tornam o fluxo
  inadequado para continuidade.

Decisão: ___

Racional: ___

Responsável pela decisão: ___

Data: ___

## Referências

- [Plano de desenvolvimento](../DEVELOPMENT_PLAN_MAR_ABERTO.md)
- [Auditoria de aceitação](../ACCEPTANCE_AUDIT.md)
