"""Chart-building helpers, kept separate so visualization code never mixes
with API or layout logic.
"""

import plotly.graph_objects as go

from config import get_class_meta


def probability_bar_chart(probabilities: dict) -> go.Figure:
    """Build a horizontal bar chart of class probabilities, sorted descending."""
    items = sorted(probabilities.items(), key=lambda kv: kv[1], reverse=True)

    labels = [get_class_meta(name)["label"] for name, _ in items]
    values = [value for _, value in items]
    colors = [get_class_meta(name)["color"] for name, _ in items]

    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker=dict(color=colors),
            text=[f"{v:.2f}%" for v in values],
            textposition="outside",
            cliponaxis=False,
        )
    )

    fig.update_layout(
        xaxis=dict(title="Probability (%)", range=[0, 105], gridcolor="#334155", color="#cbd5e1"),
        yaxis=dict(autorange="reversed", color="#e2e8f0"),
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font=dict(color="#e2e8f0"),
        margin=dict(l=10, r=40, t=10, b=10),
        height=240,
        showlegend=False,
    )

    return fig
