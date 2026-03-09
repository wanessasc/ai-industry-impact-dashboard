import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns


def plot_corr_heatmap(df: pd.DataFrame) -> plt.Figure:
    """Create seaborn correlation heatmap for numeric columns."""
    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr, cmap="YlGnBu", annot=True, fmt=".2f", ax=ax)
    ax.set_title("Correlation Matrix")
    fig.tight_layout()
    return fig


def plot_yearly_adoption(df_yearly: pd.DataFrame):
    """Interactive trend chart for AI adoption."""
    return px.line(
        df_yearly,
        x="year",
        y="ai_adoption_rate_percent",
        markers=True,
        title="AI Adoption Trend",
        labels={"ai_adoption_rate_percent": "AI Adoption (%)", "year": "Year"},
        template="plotly_white",
    )


def plot_country_scatter(df: pd.DataFrame):
    """Interactive bubble chart for country comparison."""
    return px.scatter(
        df,
        x="ai_adoption_rate_percent",
        y="consumer_trust_in_ai_percent",
        size="revenue_increase_due_to_ai_percent",
        color="regulation_status",
        hover_name="country",
        title="Adoption vs Trust (Bubble = Revenue Gain)",
        labels={
            "ai_adoption_rate_percent": "AI Adoption (%)",
            "consumer_trust_in_ai_percent": "Consumer Trust (%)",
            "revenue_increase_due_to_ai_percent": "Revenue Increase (%)",
        },
        template="plotly_white",
    )
