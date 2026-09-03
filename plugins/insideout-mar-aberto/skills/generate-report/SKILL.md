---
name: generate-report
description: Constrói e revisa o relatório HTML, o PDF e a planilha analítica do InsideOut Mar Aberto. Use quando a análise estiver concluída e a pessoa quiser revisar conclusões, evidências ou gerar os produtos finais.
---

# Gerar relatório e planilha analítica

Converta a análise automatizada em narrativa revisada e três produtos
reconciliados: HTML, PDF e `.xlsx`.

## Preparar

1. Leia `../../references/_shared/report-workbook-contract.md`,
   `../../references/_shared/privacy-retention.md` e
   `../../references/_shared/local-state.md`.
2. Leia `assets/insideout-report.css` para a identidade visual padrão.
3. Valide o checkpoint de `analyze-sentiment`, as agregações, a cobertura e o
   pool de evidências candidatas.
4. Quando houver ativos locais de cliente, verifique se foram fornecidos e se
   podem ser usados; se não, aplique o padrão InsideOut sem bloquear.

## Gate 1 — direção editorial

Apresente para aprovação:

- conclusões propostas, distinguindo fatos, interpretações e limitações;
- estrutura narrativa sugerida;
- pool estratificado de evidências com texto integral anonimizado;
- lacunas de cobertura e seu impacto.

Registre aprovações, exclusões e ajustes em
`review/editorial-gate-1.json`. Não gere o relatório completo antes da decisão.

## Produzir HTML e planilha

Após o Gate 1:

- gere `deliverables/report.html` com o núcleo fixo e narrativa adaptativa;
- incorpore o CSS no próprio HTML e não faça chamadas externas;
- mostre cobertura junto das conclusões afetadas;
- inclua somente evidências aprovadas;
- gere `deliverables/analytics.xlsx` com as sete abas e todos os dados
  analíticos definidos no contrato;
- congele cabeçalhos, habilite filtros e use tipos reais de data, número e
  percentual;
- valide visualmente o HTML em largura de desktop e tela estreita;
- abra e releia a planilha para provar abas, células e reconciliação.

Compare todas as contagens e percentuais com os JSON/JSONL canônicos. O texto
bruto não entra em `Análises`; somente `Evidências` contém comentários integrais
aprovados e anonimizados.

## Gate 2 — versão completa

Apresente HTML e planilha com um resumo das verificações. Registre aprovação ou
ajustes em `review/editorial-gate-2.json`. Ajustes narrativos regeneram o HTML e
a planilha afetada, mas não mudam classificações silenciosamente.

Depois da aprovação, exporte o mesmo HTML para
`deliverables/report.pdf`. Renderize todas as páginas para inspeção e compare o
conteúdo com o HTML aprovado. Se houver corte, sobreposição, página vazia ou
divergência, corrija e gere novamente antes de concluir.

## Entregar

Informe caminhos de HTML, PDF e planilha, versão editorial, cobertura e
limitações. Não publique, envie ou hospede os arquivos sem autorização
específica.

## Limites

- Não aprovar automaticamente nenhum gate.
- Não inserir identidade de autores.
- Não criar uma narrativa paralela no PDF.
- Não alterar dados analíticos para melhorar a história.
