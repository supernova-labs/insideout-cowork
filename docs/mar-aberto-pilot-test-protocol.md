# Protocolo de homologação — InsideOut Mar Aberto 0.2.0

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
| Uso disponível antes da execução |  |
| Uso disponível depois da execução |  |
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

3. Baixe a exportação oficial no navegador em que a Stilingue funciona para o
   operador. Tenha acesso individual ao Instagram e YouTube e faça cada login
   diretamente no navegador quando solicitado; não informe credenciais ao
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

1. No navegador habitual, exporte o filtro `nova busca i20` e o período
   controlado pela Central de Exportações.
2. Anexe o arquivo oficial à tarefa e peça para continuar o fluxo.
3. Confirme que o plugin não tenta abrir a Stilingue antes de validar o arquivo.
4. Compare filtro, período, publicações e distribuição por canal com o manifesto
   local e com as menções normalizadas.
5. Opcionalmente, em uma rodada separada, peça explicitamente a exportação
   assistida e confira refresh e download.

**Aceite:** filtro e período coincidem, o arquivo é validado sem navegação
desnecessária e o manifesto registra o mesmo recorte sem capturar credenciais.

**Registro:** estado: ___ · publicações: ___ · duração: ___ · observação
sanitizada: ___

### M9-T3 — Coleta no Instagram e YouTube

**Como executar**

1. Faça login em cada rede diretamente no navegador quando solicitado.
2. Acompanhe a abertura das publicações, a expansão de comentários e respostas
   e a paginação observável.
3. Confira por publicação as contagens observadas, respostas, falhas e estado
   de cobertura.
4. Compare separadamente o contador da exportação, o contador visível na
   plataforma e os itens observados.
5. Verifique que X/Twitter, Facebook e portais ficam `not_required` para
   comentários e que uma publicação obrigatória incompleta gera
   `blocked_coverage`.

**Aceite:** Instagram e YouTube têm cobertura completa e auditável; falhas
isoladas não interrompem as demais coletas, mas bloqueiam integralmente análise
e relatório até a retomada.

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

1. Confirme que todas as publicações obrigatórias estão `complete` e então deixe
   a análise terminar automaticamente, sem revisar itens um a um.
2. Avalie as conclusões propostas, a estrutura narrativa e o pool de evidências.
3. Registre aprovação ou alterações solicitadas antes de autorizar o relatório.

**Aceite:** menções, comentários e respostas têm denominadores separados;
sentimentos mistos e ambíguos permanecem visíveis; o pool inclui padrões,
manifestações marcantes e contrapontos. Com cobertura bloqueada, nenhuma prévia
analítica deve aparecer.

**Registro:** estado: ___ · decisão do gate: ___ · alterações solicitadas
sanitizadas: ___

### M9-T6 — Segundo gate e produtos finais

**Como executar**

1. Revise o HTML gerado depois do primeiro gate e registre ajustes editoriais.
2. Aprove ou rejeite o segundo gate.
3. Se aprovado, abra o HTML, o PDF e a planilha `.xlsx`.
4. Compare escopo, cobertura, totais por fonte, sentimento, séries diárias,
   temas, amplificação, evidências e metodologia entre os três produtos.

**Aceite:** os dois gates são respeitados; HTML, PDF e planilha abrem e são
coerentes; o relatório possui gráficos e recortes dos canais disponíveis; a
planilha contém `Resumo`, `Cobertura`, `Publicações`, `Análises`, `Agregações`,
`Séries diárias`, `Evidências` e `Metodologia`.

**Registro:** estado: ___ · decisão do gate: ___ · produtos abertos: ___ ·
divergências sanitizadas: ___

### M9-T7 — Privacidade e descarte

**Como executar**

1. Depois da conclusão, confirme que os corpora temporários de menções e
   comentários não existem mais.
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

1. Use a skill de feedback para registrar um achado real ou cenário de teste.
2. Confirme que o `.md` foi criado e relido na pasta local, com fingerprint e
   conteúdo sanitizado.
3. Repita o mesmo caso e confirme que não surge um segundo arquivo.
4. Recuse o e-mail e confirme zero efeito externo; em uma rodada separada,
   aceite a sugestão e confirme que o Gmail prepara somente um rascunho para
   destinatários informados pelo operador.

**Aceite:** o Markdown local contém a versão testada e nenhum dado da execução;
duplicatas reutilizam o fingerprint; GitHub não é solicitado; e-mail é opcional
e nunca enviado automaticamente.

**Registro:** estado: ___ · caminho local preservado fora deste protocolo: ___ ·
resultado do e-mail (`recusado`, `copiável` ou `rascunho`): ___

## Reconciliação final

| Verificação | Resultado |
|---|---|
| Todos os oito testes têm estado real |  |
| Nenhum `não executado` foi contado como sucesso |  |
| Toda falha possui item de acompanhamento |  |
| Nenhum dado real ou credencial entrou neste protocolo |  |
| A versão e o commit correspondem à referência publicada |  |
| Duração e variação de uso foram registradas sem atribuir quota ao plugin |  |

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
