import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict[str, float]:
    """Compute top-level business KPIs."""
    return {
        "records": int(df.shape[0]),
        "countries": int(df["country"].nunique()),
        "industries": int(df["industry"].nunique()),
        "avg_ai_adoption_percent": float(df["ai_adoption_rate_percent"].mean()),
        "avg_revenue_gain_percent": float(df["revenue_increase_due_to_ai_percent"].mean()),
        "avg_job_loss_percent": float(df["job_loss_due_to_ai_percent"].mean()),
        "avg_net_impact_percent": float(df["net_impact_percent"].mean()),
        "avg_maturity_score": float(df["ai_maturity_score"].mean()),
    }


def yearly_overview(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate core metrics by year."""
    return (
        df.groupby("year", as_index=False)
        .agg(
            ai_adoption_rate_percent=("ai_adoption_rate_percent", "mean"),
            revenue_increase_due_to_ai_percent=(
                "revenue_increase_due_to_ai_percent",
                "mean",
            ),
            job_loss_due_to_ai_percent=("job_loss_due_to_ai_percent", "mean"),
            net_impact_percent=("net_impact_percent", "mean"),
            ai_maturity_score=("ai_maturity_score", "mean"),
            volume_tbs=("ai_generated_content_volume_tbs_per_year", "sum"),
        )
        .round(2)
    )


def country_benchmark(df: pd.DataFrame) -> pd.DataFrame:
    """Benchmark countries by adoption and net impact."""
    return (
        df.groupby("country", as_index=False)
        .agg(
            ai_adoption_rate_percent=("ai_adoption_rate_percent", "mean"),
            net_impact_percent=("net_impact_percent", "mean"),
            ai_maturity_score=("ai_maturity_score", "mean"),
            records=("country", "count"),
        )
        .sort_values("ai_maturity_score", ascending=False)
        .round(2)
    )


def industry_benchmark(df: pd.DataFrame) -> pd.DataFrame:
    """Benchmark industries by business impact."""
    return (
        df.groupby("industry", as_index=False)
        .agg(
            ai_adoption_rate_percent=("ai_adoption_rate_percent", "mean"),
            revenue_increase_due_to_ai_percent=(
                "revenue_increase_due_to_ai_percent",
                "mean",
            ),
            job_loss_due_to_ai_percent=("job_loss_due_to_ai_percent", "mean"),
            net_impact_percent=("net_impact_percent", "mean"),
            ai_maturity_score=("ai_maturity_score", "mean"),
        )
        .sort_values("net_impact_percent", ascending=False)
        .round(2)
    )


def generate_insights(df: pd.DataFrame) -> list[str]:
    """Generate short, business-facing insights from filtered data."""
    country_tbl = country_benchmark(df)
    industry_tbl = industry_benchmark(df)

    top_country = country_tbl.iloc[0]
    top_industry = industry_tbl.iloc[0]
    low_industry = industry_tbl.iloc[-1]
    best_tool = (
        df.groupby("top_ai_tools_used")["net_impact_percent"]
        .mean()
        .sort_values(ascending=False)
        .index[0]
    )

    return [
        (
            f"{top_country['country']} lidera maturidade de IA "
            f"({top_country['ai_maturity_score']:.2f})."
        ),
        (
            f"{top_industry['industry']} tem maior impacto liquido medio "
            f"({top_industry['net_impact_percent']:.2f} p.p.)."
        ),
        (
            f"{low_industry['industry']} exige atencao, com menor impacto liquido "
            f"({low_industry['net_impact_percent']:.2f} p.p.)."
        ),
        f"Ferramenta com melhor impacto medio no recorte atual: {best_tool}.",
    ]


def metric_delta_vs_previous_year(df: pd.DataFrame, metric: str) -> dict[str, float | int]:
    """Return latest year, previous year and delta for one metric."""
    yearly = yearly_overview(df).sort_values("year")
    if yearly.empty:
        return {"year": 0, "previous_year": 0, "value": 0.0, "delta": 0.0}
    if yearly.shape[0] == 1:
        row = yearly.iloc[-1]
        return {
            "year": int(row["year"]),
            "previous_year": int(row["year"]),
            "value": float(row[metric]),
            "delta": 0.0,
        }

    latest = yearly.iloc[-1]
    previous = yearly.iloc[-2]
    return {
        "year": int(latest["year"]),
        "previous_year": int(previous["year"]),
        "value": float(latest[metric]),
        "delta": float(latest[metric] - previous[metric]),
    }


def opportunity_and_risk(df: pd.DataFrame) -> dict[str, str]:
    """Summarize top opportunity and main risk for executive storytelling."""
    ind = industry_benchmark(df)
    if ind.empty:
        return {"opportunity": "Sem dados.", "risk": "Sem dados."}

    best = ind.iloc[0]
    worst = ind.iloc[-1]
    return {
        "opportunity": (
            f"Oportunidade: priorizar {best['industry']} "
            f"(impacto liquido medio de {best['net_impact_percent']:.2f} p.p.)."
        ),
        "risk": (
            f"Risco: revisar plano de adocao em {worst['industry']} "
            f"(impacto liquido de {worst['net_impact_percent']:.2f} p.p.)."
        ),
    }
