AI Industry Impact Dashboard

Interactive data analytics project built in Python to analyze the economic impact of AI adoption across industries and countries.

Live Dashboard
https://ai-industry-impact-dashboard.streamlit.app/

🇧🇷 Sobre o Projeto

Projeto de análise de dados desenvolvido em Python para explorar o impacto da adoção de Inteligência Artificial em diferentes indústrias e países.

O projeto inclui:

- Pipeline completo de dados
- Análise exploratória (EDA)

Dashboard interativo desenvolvido com Streamlit
- Tech Stack
- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Matplotlib
- Seaborn

Estrutura do Projeto
ai-industry-impact-dashboard/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── dashboard/
└── requirements.txt

Como executar

Instalar dependências:

pip install -r requirements.txt

Executar pipeline:

python -m src.pipeline

Rodar dashboard:

streamlit run dashboard/app.py
Dashboard

O dashboard apresenta:

- adoção média de IA
- impacto em receita
- impacto no emprego
- score de maturidade em IA
- comparações entre países e indústrias

Author
Wanessa Carvalho
Aspiring Data Analyst
