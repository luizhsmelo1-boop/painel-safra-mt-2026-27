 # Painel Safra MT 2026/27

Painel web estático com mapa interativo, indicadores de plantio, precipitação estimada, previsão e histórico.

## Publicação
O repositório inclui workflow de GitHub Pages. Site esperado: https://luizhsmelo1-boop.github.io/painel-safra-mt-2026-27/ . Se não publicar, abra Actions, habilite workflows e execute Publicar painel no GitHub Pages. Em Settings → Actions → General, permita workflows se solicitado.

## Atualização
- Coleta meteorológica diária às 10:20 UTC (06:20 no MT, UTC−4), também pode ser executada manualmente.
- Usa Open-Meteo para precipitação recente de arquivo/reanálise e previsão por modelo. Isso não é observação oficial do INMET.
- Plantio está intencionalmente em branco até validar boletim oficial do IMEA; não divulgar números sem conferir fonte e data.
- O mapa mostra cidades de referência, não polígonos oficiais de macrorregiões.

## Fontes
- IMEA: https://www.imea.com.br/imea-site/relatorios-mercado
- INMET: https://portal.inmet.gov.br/
- Catálogo INMET: https://portal.inmet.gov.br/paginas/catalogoaut
- Open-Meteo: https://open-meteo.com/
- GitHub Pages: https://docs.github.com/en/pages
