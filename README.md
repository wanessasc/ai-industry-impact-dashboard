# AI Industry Impact Dashboard

Projeto completo de analytics em Python para analisar impacto de IA por pais, industria e ano, com pipeline de dados, EDA e dashboard interativo em Streamlit.

## Estrutura

```text
ai-industry-impact-dashboard/
├── data/
│   ├── raw/
│   │   └── ai_market_clean_v2.csv
│   └── processed/
│       └── ai_market_clean_processed.csv
├── notebooks/
│   └── eda_ai_market.ipynb
├── src/
│   ├── __init__.py
│   ├── analysis.py
│   ├── config.py
│   ├── data_loader.py
│   ├── pipeline.py
│   ├── preprocessing.py
│   └── visualization.py
├── dashboard/
│   └── app.py
└── requirements.txt
```

## O que o projeto entrega

- Carregamento do dataset via modulo dedicado.
- Limpeza e padronizacao de dados.
- Ajuste de colunas percentuais para escala de 0 a 100.
- Enriquecimento com metricas derivadas:
  - `net_impact_percent`
  - `ai_maturity_score`
- EDA com pandas, matplotlib, seaborn e plotly.
- Dashboard Streamlit com:
  - filtros laterais
  - cards de KPIs
  - comparacoes por pais e industria
  - graficos interativos e insights.

## Como executar

1. Instale dependencias:

```bash
pip install -r requirements.txt
```

2. Gere a base tratada:

```bash
python -m src.pipeline
```

3. Abra o dashboard:

```bash
streamlit run dashboard/app.py
```

4. (Opcional) Explore o notebook:

```bash
jupyter notebook notebooks/eda_ai_market.ipynb
```

## KPIs principais

- Adocao media de IA (%)
- Ganho medio de receita (%)
- Perda media de empregos (%)
- Impacto liquido medio (pontos percentuais)
- Score medio de maturidade de IA

## Observacao sobre os dados

As colunas percentuais no CSV original aparentam estar em centesimos (ex.: `4429` representando `44.29%`). O pipeline converte automaticamente para escala percentual tradicional (0-100).
