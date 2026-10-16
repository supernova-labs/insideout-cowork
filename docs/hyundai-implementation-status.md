# Hyundai Social — implantação 0.1.0

Data: 16/10/2026. Estado: implementado para piloto, não liberado para operação.

## Pacote e distribuição

- Novo pacote `insideout-hyundai-social`, quatro skills, manifesto Codex,
  metadados de invocação, referências próprias e 12 cenários de regressão.
- Catálogo e inventário atualizados. Sem terceiro plugin compartilhado,
  symlinks, runtime de geração, painel ou dependência do Social.
- Social mantém identidade/instalação; versão 0.6.1 encaminha planejamento e
  feedback Hyundai ao pacote próprio e preserva os testes antigos.
- A entrega para testes usa a branch `codex/hyundai-social-pilot`, sem publicação
  direta na `main`. O [guia da Carol](hyundai-carol-test-guide.md) documenta
  instalação e limites. A instalação na conta dela ainda precisa ser conferida.
- A revisão para publicação retirou links de documentos internos e do quadro
  operacional do pacote. Entregáveis, dados e evidências locais não são versionados.

## Airtable comprovado

A base exclusiva **InsideOut Hyundai Social** foi criada no workspace Inside
Out. e relida. Oito tabelas e seis relações de ida, com cardinalidade conferida
pela skill. O conector não expõe restrição de cardinalidade única no schema
usado; listas ambíguas bloqueiam a operação pelo contrato.

Foram cadastradas nove diretrizes, seis modelos, cinco canais e 54 referências
do documento autorizado da Carol. Claims, assets e perfis de canais não foram
inventados. Canais permanecem pendentes de confirmação de formatos/perfis.
Os dados fornecidos foram comparados à releitura integral, sem diferenças.
Na segunda passagem, as 74 chaves foram reutilizadas, com zero criações.
Ciclos, ideias, publicações e encaminhamentos começaram vazios.

Depois da configuração, um ensaio controlado criou uma referência sintética,
um ciclo Sintético, uma ideia pendente e duas publicações relacionadas. Todos
os nomes de teste usam `[TESTE CODEX]`. A primeira conferência detectou que o
conector devolve relações como objetos, em vez de strings; o verificador foi
corrigido para comparar IDs sem repetir as criações. A retomada reutilizou os
registros existentes e completou as publicações. Uma segunda execução completa
reutilizou os cinco registros, com zero criações e valores/relacionamentos
relidos. Nenhuma aprovação de produção ou encaminhamento foi criado.

A base Social antiga não recebeu escritas. A criação de uma base não comprova
negação de acesso cruzado: testar contas reais e acessos herdados é gate pendente.
URLs e IDs operacionais ficam nos artefatos locais de implantação, fora do pacote.

Em 16/10/2026, a lista de colaboradores da base confirmou Caroline como Owner
herdado do workspace. Ela já possui acesso superior ao necessário para o piloto;
nenhum convite, ampliação de permissão ou mudança de papel foi necessário.
Isso não comprova o acesso pelo conector pessoal dela nem a negação cruzada
entre equipes. O papel de proprietária não foi removido ou reduzido.

## Validações

| Verificação | Estado |
|---|---|
| Estrutura Hyundai: quatro skills, referências internas, manifesto, catálogo e índice | Passou |
| Contrato de fingerprint: seis testes, incluindo edição sem trocar UUID e canonicalização Node/Python | Passou |
| Validador Social | Passou |
| Validador Mar Aberto: 70 testes de aceite, 10 gates e 10 schemas | Passou |
| Agent Smith: 18 skills, catálogo e índice | Passou |
| Avaliação independente de limites em quatro cenários sintéticos | Passou por leitura/raciocínio; sem escrita externa |
| Airtable: escrita, relações, retomada e segunda execução da fixture sintética | Passou; cinco registros reutilizados sem duplicação |
| Revisão HTML sintética funcional em navegador | Passou: criar, editar, remover, recarregar, exportar JSON/CSV, texto não executável e leitura desktop/móvel |
| Piloto retrospectivo em tarefa limpa, sem calendário esperado | Gerado para setembro/2026: 16 ideias, 42 publicações propostas e cinco reservas; homologação pendente |
| HTML retrospectivo no navegador | Conferidos comentário, edição, persistência, remoção e leitura móvel sem transbordamento |
| Homologação editorial por Carol/equipe | Pendente |

Os testes de contrato são um oráculo de teste fora do plugin, não um motor de
produção nem prova de que toda geração futura cumprirá o contrato.
Os arquivos do piloto e as evidências visuais ficam em
`artifacts/hyundai-social/`, ignorados pelo Git. O corte retrospectivo foi
31/08/2026; as fontes foram observadas em 16/10/2026. A falta de arquivos visuais
históricos foi declarada: há referências documentais e links, sem alegação de
licença ou de prévia histórica completa. Nenhuma trend atual foi aplicada.
O calendário esperado não foi fornecido à tarefa geradora; a comparação e a
avaliação editorial pela equipe ainda não ocorreram. O take retrospectivo não
foi gravado na base nem encaminhado ao Asana.

Na revisão sintética, os arquivos realmente baixados foram relidos; os testes
com JavaScript desligado e armazenamento local negado não foram executados.
A ausência de recursos remotos foi conferida no documento e em sua política
de segurança, sem captura detalhada de tráfego. Os comentários locais usados
nos testes de navegador foram removidos ao final.
Uma falha do validador Mar Aberto foi identificada durante a edição do README:
ele buscava a primeira ocorrência de “Versão candidata”. O texto Hyundai foi
ajustado para não interferir nessa identificação; o validador voltou a passar.

## Asana e bloqueios externos

O conector Asana passou a estar disponível, mas a leitura do projeto informado
retornou `Not Authorized`. A conta autenticada expõe um workspace diferente do
quadro Hyundai. O navegador autenticado permite leitura, o que não comprova
escrita pelo conector. Não foi criado projeto/tarefa em workspace alternativo.

O usuário autorizou ajustar a conexão. As ferramentas disponíveis não expõem
troca da conta/OAuth; a reconexão deve ocorrer nas conexões do app. O teste de
criação, subtarefas, releitura, retomada parcial e segunda execução aguarda essa
conexão. Não substituir por escrita no quadro operacional via navegador.

Regras provisórias de alocação estão marcadas Simulação. Operação real continua
bloqueada até a confirmação da Carol, a validação das contagens, os testes de
acesso e a homologação. Comentários não alteram esse estado.
