from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.analysis import (  # noqa: E402
    calculate_kpis,
    country_benchmark,
    generate_insights,
    industry_benchmark,
    metric_delta_vs_previous_year,
    opportunity_and_risk,
    yearly_overview,
)
from src.data_loader import load_processed_data  # noqa: E402
from src.pipeline import run_pipeline  # noqa: E402


st.set_page_config(
    page_title="Impacto da IA | Painel Premium",
    page_icon="bar_chart",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        :root {
            --bg: #000000;
            --card: #0B0B0B;
            --surface: #111111;
            --grid: #1A1A1A;
            --text: #EAEAEA;
            --text-soft: #A6A6A6;
            --primary: #00F5FF;
            --secondary: #7C4DFF;
            --accent: #FF2E88;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        .main .block-container {
            max-width: 100%;
            padding-top: 1.2rem;
            padding-left: 2.1rem;
            padding-right: 2.1rem;
            padding-bottom: 2.2rem;
        }

        section[data-testid="stSidebar"] {
            background: #000000;
            border-right: 1px solid #111111;
            box-shadow: inset -1px 0 0 #111111;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-left: 0.55rem;
            padding-right: 0.55rem;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div {
            width: 100%;
            max-width: 320px;
        }

        section[data-testid="stSidebar"] * {
            color: var(--text) !important;
        }

        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            color: var(--text) !important;
            margin-bottom: 0.35rem !important;
            text-align: center !important;
        }

        section[data-testid="stSidebar"] .stRadio,
        section[data-testid="stSidebar"] .stMultiSelect,
        section[data-testid="stSidebar"] .stSelectbox,
        section[data-testid="stSidebar"] .stSlider,
        section[data-testid="stSidebar"] .stMarkdown {
            width: 100% !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        section[data-testid="stSidebar"] .stRadio > div {
            background: #0B0B0B;
            border: 1px solid rgba(0, 245, 255, 0.35);
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 0.7rem;
            box-sizing: border-box;
        }

        section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
            text-align: center !important;
            width: 100%;
            color: var(--text-soft) !important;
            font-size: 0.9rem !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stMultiSelect"],
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"],
        section[data-testid="stSidebar"] div[data-testid="stSlider"] {
            background: #0B0B0B;
            border: 1px solid rgba(0, 245, 255, 0.45);
            border-radius: 12px;
            padding: 10px 10px 8px 10px;
            margin-bottom: 0.6rem;
            box-sizing: border-box;
            transition: all 0.18s ease;
        }

        section[data-testid="stSidebar"] div[data-testid="stMultiSelect"]:hover,
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"]:hover,
        section[data-testid="stSidebar"] div[data-testid="stSlider"]:hover {
            border-color: #00F5FF;
            box-shadow: 0 0 0 1px rgba(0, 245, 255, 0.20), 0 0 14px rgba(0, 245, 255, 0.16);
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label {
            background: #0B0B0B;
            border: 1px solid #1A1A1A;
            border-radius: 12px;
            margin: 0;
            padding: 8px 10px;
            transition: all 0.18s ease;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            border-color: #00F5FF;
            box-shadow: 0 0 0 1px rgba(0, 245, 255, 0.20), 0 0 14px rgba(0, 245, 255, 0.18);
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label [data-testid="stMarkdownContainer"] p {
            text-align: left !important;
            font-size: 0.92rem !important;
            color: #EAEAEA !important;
            line-height: 1.25 !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(120deg, rgba(0,245,255,0.12), rgba(124,77,255,0.12));
            border-color: #00F5FF;
            box-shadow: 0 0 0 1px rgba(0, 245, 255, 0.24), 0 0 16px rgba(0, 245, 255, 0.20);
        }

        section[data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: #0B0B0B;
            border: 1px solid rgba(0, 245, 255, 0.40);
            border-radius: 999px;
            transition: all 0.18s ease;
            width: 100%;
            min-height: 40px;
            padding-top: 2px;
            padding-bottom: 2px;
        }

        section[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
            border-color: #00F5FF;
            box-shadow: 0 0 0 1px rgba(0, 245, 255, 0.20), 0 0 14px rgba(0, 245, 255, 0.16);
        }

        section[data-testid="stSidebar"] [data-baseweb="tag"] {
            background: #111111 !important;
            border: 1px solid #00F5FF !important;
            border-radius: 999px !important;
            max-width: 96px;
            min-height: 20px !important;
            padding: 0 6px !important;
            margin-right: 4px !important;
            flex-shrink: 1 !important;
        }

        section[data-testid="stSidebar"] [data-baseweb="tag"] span {
            color: #00F5FF !important;
            font-size: 10px !important;
            line-height: 1.05 !important;
            max-width: 66px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            display: inline-block;
        }

        section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
            width: 10px !important;
            height: 10px !important;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdown"] {
            margin-bottom: 0.35rem;
        }

        section[data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {
            background: #00F5FF !important;
            box-shadow: 0 0 10px rgba(0, 245, 255, 0.55);
        }

        .hero {
            background: linear-gradient(120deg, rgba(0,245,255,0.10), rgba(124,77,255,0.13), rgba(255,46,136,0.11));
            border: 1px solid rgba(0,245,255,0.24);
            border-radius: 16px;
            padding: 24px 26px;
            margin-bottom: 14px;
            box-shadow: 0 0 0 1px rgba(0,245,255,0.10), 0 0 20px rgba(0,245,255,0.10);
            text-align: center;
        }

        .hero h1 {
            margin: 0;
            font-size: 38px;
            font-weight: 760;
            letter-spacing: 0.3px;
            color: #F7F7F7;
            line-height: 1.15;
        }

        .hero p {
            margin: 12px auto 0 auto;
            color: #BFBFBF;
            font-size: 15px;
            font-weight: 420;
            line-height: 1.5;
            max-width: 920px;
        }

        .kpi-card {
            background: #0B0B0B;
            border: 1px solid #1A1A1A;
            border-radius: 14px;
            padding: 14px;
            min-height: 108px;
            box-shadow: 0 0 0 1px rgba(124,77,255,0.14), 0 0 16px rgba(124,77,255,0.08);
        }

        .kpi-title {
            color: #9C9C9C;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .kpi-value {
            color: #F4F4F4;
            font-size: 31px;
            line-height: 1;
            font-weight: 760;
            margin-bottom: 8px;
        }

        .kpi-delta-up, .kpi-delta-down {
            display: inline-block;
            font-size: 12px;
            font-weight: 700;
            border-radius: 999px;
            padding: 4px 10px;
            border: 1px solid transparent;
        }

        .kpi-delta-up {
            color: #00F5FF;
            background: rgba(0,245,255,0.09);
            border-color: rgba(0,245,255,0.42);
            box-shadow: 0 0 12px rgba(0,245,255,0.14);
        }

        .kpi-delta-down {
            color: #FF2E88;
            background: rgba(255,46,136,0.10);
            border-color: rgba(255,46,136,0.45);
            box-shadow: 0 0 12px rgba(255,46,136,0.16);
        }

        .section-title {
            color: #EAEAEA;
            font-size: 19px;
            font-weight: 700;
            margin-top: 8px;
            margin-bottom: 8px;
        }

        .insight-card {
            background: #111111;
            border: 1px solid #1A1A1A;
            border-radius: 12px;
            padding: 12px;
            color: #D8D8D8;
            margin-bottom: 8px;
        }

        .stDataFrame, .stTable {
            border: 1px solid #1A1A1A;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def get_data() -> pd.DataFrame:
    try:
        return load_processed_data()
    except FileNotFoundError:
        run_pipeline()
        return load_processed_data()


def style_plot(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#000000",
        plot_bgcolor="#111111",
        font={"color": "#EAEAEA", "family": "Inter, Segoe UI, sans-serif"},
        title_font={"size": 20, "color": "#EAEAEA"},
        legend={"orientation": "h", "y": 1.05, "x": 0, "bgcolor": "rgba(0,0,0,0)"},
        hoverlabel={"bgcolor": "#0B0B0B", "font_color": "#EAEAEA"},
        margin={"l": 20, "r": 20, "t": 64, "b": 22},
    )
    fig.update_xaxes(gridcolor="#1A1A1A", zerolinecolor="#1A1A1A")
    fig.update_yaxes(gridcolor="#1A1A1A", zerolinecolor="#1A1A1A")
    return fig


def pct_delta(value: float, base: float) -> float:
    if base == 0:
        return 0.0
    return ((value - base) / abs(base)) * 100.0


def render_kpi_card(title: str, value: str, delta_pct: float, inverse_good: bool = False) -> str:
    good = delta_pct >= 0
    if inverse_good:
        good = not good
    cls = "kpi-delta-up" if good else "kpi-delta-down"
    arrow = "▲" if good else "▼"
    return (
        '<div class="kpi-card">'
        f'<div class="kpi-title">{title}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="{cls}">{arrow} {delta_pct:+.1f}% vs referencia</div>'
        "</div>"
    )


def narrativa_automatica(df: pd.DataFrame) -> list[str]:
    por_pais = country_benchmark(df)
    por_industria = industry_benchmark(df)
    delta_adocao = metric_delta_vs_previous_year(df, "ai_adoption_rate_percent")
    delta_impacto = metric_delta_vs_previous_year(df, "net_impact_percent")

    melhor_pais = por_pais.iloc[0]
    pior_pais = por_pais.iloc[-1]
    melhor_industria = por_industria.iloc[0]

    tendencia = "aceleracao" if delta_impacto["delta"] >= 0 else "desaceleracao"
    return [
        (
            f"Adocao media em {int(delta_adocao['year'])}: {delta_adocao['value']:.2f}% "
            f"({delta_adocao['delta']:+.2f} p.p. vs {int(delta_adocao['previous_year'])})."
        ),
        (
            f"Impacto liquido em {tendencia}: {delta_impacto['value']:.2f} p.p. "
            f"({delta_impacto['delta']:+.2f} p.p. vs ano anterior)."
        ),
        (
            f"Pais lider no recorte: {melhor_pais['country']} "
            f"(indice de maturidade {melhor_pais['ai_maturity_score']:.2f})."
        ),
        (
            f"Melhor alavanca setorial: {melhor_industria['industry']} "
            f"({melhor_industria['net_impact_percent']:.2f} p.p. de impacto liquido)."
        ),
        (
            f"Pais em monitoramento: {pior_pais['country']} "
            f"(indice de maturidade {pior_pais['ai_maturity_score']:.2f})."
        ),
    ]


df = get_data()

TRADUCAO_PAISES = {
    "Australia": "Austrália",
    "Canada": "Canadá",
    "China": "China",
    "France": "França",
    "Germany": "Alemanha",
    "India": "Índia",
    "Japan": "Japão",
    "South Korea": "Coreia do Sul",
    "UK": "Reino Unido",
    "USA": "Estados Unidos",
}

TRADUCAO_INDUSTRIAS = {
    "Automotive": "Automotivo",
    "Education": "Educação",
    "Finance": "Finanças",
    "Gaming": "Games",
    "Healthcare": "Saúde",
    "Legal": "Jurídico",
    "Manufacturing": "Manufatura",
    "Marketing": "Marketing",
    "Media": "Mídia",
    "Retail": "Varejo",
}

TRADUCAO_REGULACAO = {
    "Lenient": "Flexível",
    "Moderate": "Moderada",
    "Strict": "Rigorosa",
}

st.sidebar.markdown("<h3 style='text-align:center;'>Menu</h3>", unsafe_allow_html=True)
secao = st.sidebar.radio(
    "Navegacao",
    [
        "📊 Visao Geral",
        "💸 Impacto Economico",
        "🌍 Comparacao entre Paises",
        "🤖 Maturidade de IA",
        "💡 Insights",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("<h3 style='text-align:center;'>Filtros</h3>", unsafe_allow_html=True)
paises = st.sidebar.multiselect(
    "País",
    sorted(df["country"].unique()),
    default=sorted(df["country"].unique()),
    format_func=lambda x: TRADUCAO_PAISES.get(x, x),
)
industrias = st.sidebar.multiselect(
    "Indústria",
    sorted(df["industry"].unique()),
    default=sorted(df["industry"].unique()),
    format_func=lambda x: TRADUCAO_INDUSTRIAS.get(x, x),
)
ferramentas = st.sidebar.multiselect(
    "Ferramenta de IA",
    sorted(df["top_ai_tools_used"].unique()),
    default=sorted(df["top_ai_tools_used"].unique()),
)
regulacoes = st.sidebar.multiselect(
    "Status Regulatorio",
    sorted(df["regulation_status"].unique()),
    default=sorted(df["regulation_status"].unique()),
    format_func=lambda x: TRADUCAO_REGULACAO.get(x, x),
)
ano_min, ano_max = int(df["year"].min()), int(df["year"].max())
intervalo_anos = st.sidebar.slider("Intervalo de anos", ano_min, ano_max, (ano_min, ano_max))

df_filtrado = df[
    (df["country"].isin(paises))
    & (df["industry"].isin(industrias))
    & (df["top_ai_tools_used"].isin(ferramentas))
    & (df["regulation_status"].isin(regulacoes))
    & (df["year"].between(intervalo_anos[0], intervalo_anos[1]))
].copy()

if df_filtrado.empty:
    st.warning("Nao ha dados para os filtros selecionados. Ajuste os filtros.")
    st.stop()

kpis_ref = calculate_kpis(df)
kpis = calculate_kpis(df_filtrado)
visao_ano = yearly_overview(df_filtrado)
comp_pais = country_benchmark(df_filtrado)
comp_industria = industry_benchmark(df_filtrado)
op_risk = opportunity_and_risk(df_filtrado)

st.markdown(
    """
    <div class="hero">
        <h1>Impacto Econômico da Inteligência Artificial — Análise Global</h1>
        <p>
            Dashboard analítico sobre adoção de IA, impacto em receita, emprego e maturidade digital em
            economias globais (2020–2025).
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown(
    render_kpi_card(
        "Adocao de IA",
        f"{kpis['avg_ai_adoption_percent']:.2f}%",
        pct_delta(kpis["avg_ai_adoption_percent"], kpis_ref["avg_ai_adoption_percent"]),
    ),
    unsafe_allow_html=True,
)
c2.markdown(
    render_kpi_card(
        "Aumento de Receita",
        f"{kpis['avg_revenue_gain_percent']:.2f}%",
        pct_delta(kpis["avg_revenue_gain_percent"], kpis_ref["avg_revenue_gain_percent"]),
    ),
    unsafe_allow_html=True,
)
c3.markdown(
    render_kpi_card(
        "Perda de Empregos",
        f"{kpis['avg_job_loss_percent']:.2f}%",
        pct_delta(kpis["avg_job_loss_percent"], kpis_ref["avg_job_loss_percent"]),
        inverse_good=True,
    ),
    unsafe_allow_html=True,
)
c4.markdown(
    render_kpi_card(
        "Impacto Liquido",
        f"{kpis['avg_net_impact_percent']:.2f} p.p.",
        pct_delta(kpis["avg_net_impact_percent"], kpis_ref["avg_net_impact_percent"]),
    ),
    unsafe_allow_html=True,
)
c5.markdown(
    render_kpi_card(
        "Indice de Maturidade",
        f"{kpis['avg_maturity_score']:.2f}",
        pct_delta(kpis["avg_maturity_score"], kpis_ref["avg_maturity_score"]),
    ),
    unsafe_allow_html=True,
)

if secao.endswith("Visao Geral"):
    st.markdown('<div class="section-title">Visao Geral do Portfolio</div>', unsafe_allow_html=True)

    serie_long = visao_ano.melt(
        id_vars="year",
        value_vars=[
            "ai_adoption_rate_percent",
            "revenue_increase_due_to_ai_percent",
            "job_loss_due_to_ai_percent",
            "net_impact_percent",
        ],
        var_name="metrica",
        value_name="valor",
    )
    serie_long["metrica"] = serie_long["metrica"].map(
        {
            "ai_adoption_rate_percent": "Adocao de IA",
            "revenue_increase_due_to_ai_percent": "Aumento de Receita",
            "job_loss_due_to_ai_percent": "Perda de Empregos",
            "net_impact_percent": "Impacto Liquido",
        }
    )

    fig_linha = px.line(
        serie_long,
        x="year",
        y="valor",
        color="metrica",
        markers=True,
        title="Evolucao Temporal das Metricas Principais",
        labels={"year": "Ano", "valor": "Percentual / p.p.", "metrica": "Metrica"},
        color_discrete_sequence=["#00F5FF", "#7C4DFF", "#FF2E88", "#00F5FF"],
    )
    fig_linha.update_traces(line={"width": 3}, marker={"size": 7})
    fig_linha.update_layout(height=460, hovermode="x unified", legend_title_text="")
    st.plotly_chart(style_plot(fig_linha), use_container_width=True)

    left, right = st.columns([1.2, 1])
    with left:
        top_setores = comp_industria.head(10)
        fig_setor = px.bar(
            top_setores,
            x="net_impact_percent",
            y="industry",
            orientation="h",
            color="ai_adoption_rate_percent",
            title="Top Industrias por Impacto Liquido",
            color_continuous_scale=[[0, "#111111"], [0.5, "#7C4DFF"], [1, "#00F5FF"]],
            labels={
                "net_impact_percent": "Impacto Liquido (p.p.)",
                "industry": "Industria",
                "ai_adoption_rate_percent": "Adocao de IA (%)",
            },
        )
        fig_setor.update_layout(height=420, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(style_plot(fig_setor), use_container_width=True)

    with right:
        fig_disp = px.scatter(
            df_filtrado,
            x="ai_adoption_rate_percent",
            y="revenue_increase_due_to_ai_percent",
            size="market_share_of_ai_companies_percent",
            color="regulation_status",
            title="Adocao vs Receita (bolha = market share)",
            hover_data=["country", "industry", "top_ai_tools_used", "year"],
            labels={
                "ai_adoption_rate_percent": "Adocao de IA (%)",
                "revenue_increase_due_to_ai_percent": "Aumento de Receita (%)",
                "regulation_status": "Regulacao",
            },
            color_discrete_sequence=["#00F5FF", "#7C4DFF", "#FF2E88", "#00F5FF"],
        )
        fig_disp.update_layout(height=420)
        st.plotly_chart(style_plot(fig_disp), use_container_width=True)

elif secao.endswith("Impacto Economico"):
    st.markdown('<div class="section-title">Impacto Economico</div>', unsafe_allow_html=True)

    econ_long = visao_ano.melt(
        id_vars="year",
        value_vars=[
            "revenue_increase_due_to_ai_percent",
            "job_loss_due_to_ai_percent",
            "net_impact_percent",
        ],
        var_name="metrica",
        value_name="valor",
    )
    econ_long["metrica"] = econ_long["metrica"].map(
        {
            "revenue_increase_due_to_ai_percent": "Aumento de Receita",
            "job_loss_due_to_ai_percent": "Perda de Empregos",
            "net_impact_percent": "Impacto Liquido",
        }
    )

    fig_econ_line = px.line(
        econ_long,
        x="year",
        y="valor",
        color="metrica",
        markers=True,
        title="Evolucao Economica ao Longo dos Anos",
        labels={"year": "Ano", "valor": "Percentual / p.p.", "metrica": "Metrica"},
        color_discrete_sequence=["#00F5FF", "#FF2E88", "#7C4DFF"],
    )
    fig_econ_line.update_traces(line={"width": 3}, marker={"size": 7})
    fig_econ_line.update_layout(height=430, hovermode="x unified", legend_title_text="")
    st.plotly_chart(style_plot(fig_econ_line), use_container_width=True)

    col_a, col_b = st.columns([1.15, 1])
    with col_a:
        econ_ind = (
            df_filtrado.groupby("industry", as_index=False)
            .agg(
                revenue_increase_due_to_ai_percent=("revenue_increase_due_to_ai_percent", "mean"),
                job_loss_due_to_ai_percent=("job_loss_due_to_ai_percent", "mean"),
                net_impact_percent=("net_impact_percent", "mean"),
            )
            .sort_values("net_impact_percent", ascending=False)
        )
        econ_ind_long = econ_ind.melt(id_vars="industry", var_name="metrica", value_name="valor")
        econ_ind_long["metrica"] = econ_ind_long["metrica"].map(
            {
                "revenue_increase_due_to_ai_percent": "Aumento de Receita",
                "job_loss_due_to_ai_percent": "Perda de Empregos",
                "net_impact_percent": "Impacto Liquido",
            }
        )
        fig_bar_setor = px.bar(
            econ_ind_long,
            x="industry",
            y="valor",
            color="metrica",
            barmode="group",
            title="Comparativo Economico por Industria",
            labels={"industry": "Industria", "valor": "Percentual / p.p.", "metrica": "Metrica"},
            color_discrete_sequence=["#00F5FF", "#FF2E88", "#7C4DFF"],
        )
        fig_bar_setor.update_layout(height=430, xaxis_tickangle=-25, legend_title_text="")
        st.plotly_chart(style_plot(fig_bar_setor), use_container_width=True)

    with col_b:
        fig_risk_return = px.scatter(
            econ_ind,
            x="job_loss_due_to_ai_percent",
            y="revenue_increase_due_to_ai_percent",
            size="net_impact_percent",
            color="net_impact_percent",
            text="industry",
            title="Mapa Risco-Retorno por Industria",
            labels={
                "job_loss_due_to_ai_percent": "Perda de Empregos (%)",
                "revenue_increase_due_to_ai_percent": "Aumento de Receita (%)",
                "net_impact_percent": "Impacto Liquido",
            },
            color_continuous_scale=[[0, "#111111"], [0.5, "#7C4DFF"], [1, "#00F5FF"]],
        )
        fig_risk_return.update_traces(textposition="top center")
        fig_risk_return.update_layout(height=430)
        st.plotly_chart(style_plot(fig_risk_return), use_container_width=True)

elif secao.endswith("Comparacao entre Paises"):
    st.markdown('<div class="section-title">Comparacao entre Paises</div>', unsafe_allow_html=True)

    pais_perf = (
        df_filtrado.groupby("country", as_index=False)
        .agg(
            ai_adoption_rate_percent=("ai_adoption_rate_percent", "mean"),
            revenue_increase_due_to_ai_percent=("revenue_increase_due_to_ai_percent", "mean"),
            job_loss_due_to_ai_percent=("job_loss_due_to_ai_percent", "mean"),
            net_impact_percent=("net_impact_percent", "mean"),
            ai_maturity_score=("ai_maturity_score", "mean"),
            consumer_trust_in_ai_percent=("consumer_trust_in_ai_percent", "mean"),
            market_share_of_ai_companies_percent=("market_share_of_ai_companies_percent", "mean"),
        )
        .sort_values("net_impact_percent", ascending=False)
    )

    top_paises = pais_perf.head(10)
    fig_paises = px.bar(
        top_paises,
        x="net_impact_percent",
        y="country",
        orientation="h",
        color="ai_maturity_score",
        title="Top Paises por Impacto Liquido",
        labels={
            "net_impact_percent": "Impacto Liquido (p.p.)",
            "country": "Pais",
            "ai_maturity_score": "Indice de Maturidade",
        },
        color_continuous_scale=[[0, "#111111"], [0.5, "#7C4DFF"], [1, "#00F5FF"]],
    )
    fig_paises.update_layout(height=440, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(style_plot(fig_paises), use_container_width=True)

    c_left, c_right = st.columns([1.2, 1])
    with c_left:
        fig_scatter_pais = px.scatter(
            pais_perf,
            x="ai_adoption_rate_percent",
            y="consumer_trust_in_ai_percent",
            size="market_share_of_ai_companies_percent",
            color="net_impact_percent",
            text="country",
            title="Adocao vs Confianca por Pais",
            labels={
                "ai_adoption_rate_percent": "Adocao de IA (%)",
                "consumer_trust_in_ai_percent": "Confianca do Consumidor (%)",
                "net_impact_percent": "Impacto Liquido",
            },
            color_continuous_scale=[[0, "#111111"], [0.5, "#7C4DFF"], [1, "#00F5FF"]],
        )
        fig_scatter_pais.update_traces(textposition="top center")
        fig_scatter_pais.update_layout(height=420)
        st.plotly_chart(style_plot(fig_scatter_pais), use_container_width=True)

    with c_right:
        pais_long = top_paises[["country", "revenue_increase_due_to_ai_percent", "job_loss_due_to_ai_percent"]].melt(
            id_vars="country", var_name="metrica", value_name="valor"
        )
        pais_long["metrica"] = pais_long["metrica"].map(
            {
                "revenue_increase_due_to_ai_percent": "Aumento de Receita",
                "job_loss_due_to_ai_percent": "Perda de Empregos",
            }
        )
        fig_grupo_pais = px.bar(
            pais_long,
            x="country",
            y="valor",
            color="metrica",
            barmode="group",
            title="Receita vs Perda de Empregos (Top 10 Paises)",
            labels={"country": "Pais", "valor": "Percentual", "metrica": "Metrica"},
            color_discrete_map={"Aumento de Receita": "#00F5FF", "Perda de Empregos": "#FF2E88"},
        )
        fig_grupo_pais.update_layout(height=420, xaxis_tickangle=-25, legend_title_text="")
        st.plotly_chart(style_plot(fig_grupo_pais), use_container_width=True)

elif secao.endswith("Maturidade de IA"):
    st.markdown('<div class="section-title">Maturidade de IA</div>', unsafe_allow_html=True)

    mat_ano = visao_ano[["year", "ai_maturity_score"]].copy()
    fig_mat_ano = px.line(
        mat_ano,
        x="year",
        y="ai_maturity_score",
        markers=True,
        title="Evolucao do Indice de Maturidade",
        labels={"year": "Ano", "ai_maturity_score": "Indice de Maturidade"},
        color_discrete_sequence=["#00F5FF"],
    )
    fig_mat_ano.update_traces(line={"width": 3}, marker={"size": 8})
    fig_mat_ano.update_layout(height=410)
    st.plotly_chart(style_plot(fig_mat_ano), use_container_width=True)

    col1, col2 = st.columns([1.1, 1.1])
    with col1:
        fig_mat_pais = px.bar(
            comp_pais.head(10),
            x="country",
            y="ai_maturity_score",
            color="net_impact_percent",
            title="Top Paises por Maturidade",
            labels={
                "country": "Pais",
                "ai_maturity_score": "Indice de Maturidade",
                "net_impact_percent": "Impacto Liquido",
            },
            color_continuous_scale=[[0, "#111111"], [0.5, "#7C4DFF"], [1, "#00F5FF"]],
        )
        fig_mat_pais.update_layout(height=430, xaxis_tickangle=-25)
        st.plotly_chart(style_plot(fig_mat_pais), use_container_width=True)

    with col2:
        mat_setor = (
            df_filtrado.groupby("industry", as_index=False)
            .agg(ai_maturity_score=("ai_maturity_score", "mean"), net_impact_percent=("net_impact_percent", "mean"))
        )
        fig_mat_scatter = px.scatter(
            mat_setor,
            x="ai_maturity_score",
            y="net_impact_percent",
            color="ai_maturity_score",
            size="net_impact_percent",
            text="industry",
            title="Maturidade vs Impacto por Industria",
            labels={
                "ai_maturity_score": "Indice de Maturidade",
                "net_impact_percent": "Impacto Liquido (p.p.)",
            },
            color_continuous_scale=[[0, "#111111"], [0.5, "#7C4DFF"], [1, "#00F5FF"]],
        )
        fig_mat_scatter.update_traces(textposition="top center")
        fig_mat_scatter.update_layout(height=430)
        st.plotly_chart(style_plot(fig_mat_scatter), use_container_width=True)

else:
    st.markdown('<div class="section-title">Insights</div>', unsafe_allow_html=True)

    for item in narrativa_automatica(df_filtrado):
        st.markdown(f"<div class='insight-card'>- {item}</div>", unsafe_allow_html=True)

    for item in generate_insights(df_filtrado):
        st.markdown(f"<div class='insight-card'>- {item}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='insight-card'><b>{op_risk['opportunity']}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight-card'><b>{op_risk['risk']}</b></div>", unsafe_allow_html=True)

    matriz = comp_industria[["industry", "ai_adoption_rate_percent", "net_impact_percent", "ai_maturity_score"]].copy()
    q3 = matriz["net_impact_percent"].quantile(0.75)
    q1 = matriz["net_impact_percent"].quantile(0.25)
    matriz["prioridade"] = matriz["net_impact_percent"].apply(
        lambda x: "Escalar" if x >= q3 else ("Estabilizar" if x <= q1 else "Otimizar")
    )
    matriz = matriz.sort_values("net_impact_percent", ascending=False).rename(
        columns={
            "industry": "Industria",
            "ai_adoption_rate_percent": "Adocao de IA (%)",
            "net_impact_percent": "Impacto Liquido (p.p.)",
            "ai_maturity_score": "Indice de Maturidade",
            "prioridade": "Prioridade",
        }
    )

    st.markdown('<div class="section-title">Matriz Recomendada de Acoes</div>', unsafe_allow_html=True)
    st.dataframe(matriz, use_container_width=True)

with st.expander("Visualizar dados filtrados"):
    tabela = df_filtrado.rename(
        columns={
            "country": "Pais",
            "year": "Ano",
            "industry": "Industria",
            "ai_adoption_rate_percent": "Adocao de IA (%)",
            "ai_generated_content_volume_tbs_per_year": "Volume de Conteudo de IA (TB/ano)",
            "job_loss_due_to_ai_percent": "Perda de Empregos (%)",
            "revenue_increase_due_to_ai_percent": "Aumento de Receita (%)",
            "human_ai_collaboration_rate_percent": "Colaboracao Humano-IA (%)",
            "top_ai_tools_used": "Ferramenta de IA",
            "regulation_status": "Status Regulatorio",
            "consumer_trust_in_ai_percent": "Confianca do Consumidor (%)",
            "market_share_of_ai_companies_percent": "Participacao de Mercado (%)",
            "net_impact_percent": "Impacto Liquido (p.p.)",
            "ai_maturity_score": "Indice de Maturidade",
        }
    )
    st.dataframe(tabela, use_container_width=True)
