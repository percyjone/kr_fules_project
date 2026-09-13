from dash import (
    html,
    dcc,
    callback,
    Input,
    Output,
)

import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from database.db import fetch_alert_severity_counts
from config.settings import COLORS


# ==========================================================
# CREATE DONUT FIGURE
# ==========================================================

def create_severity_figure(
    high,
    medium,
    low
):

    fig = go.Figure(

        data=[

            go.Pie(

                labels=[
                    "High",
                    "Medium",
                    "Low"
                ],

                values=[
                    high,
                    medium,
                    low
                ],

                hole=0.70,

                textinfo="none",

                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "%{value} alerts"
                    "<extra></extra>"
                ),

                marker=dict(

                    colors=[
                        "#ef4444",
                        "#f59e0b",
                        "#3b82f6"
                    ],

                    line=dict(
                        color="#ffffff",
                        width=2
                    )

                )

            )

        ]

    )

    fig.update_layout(

        height=120,

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),

        showlegend=False,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"

    )

    return fig


# ==========================================================
# GET CURRENT SEVERITY COUNTS
# ==========================================================

def get_current_severity_counts():

    counts = (
        fetch_alert_severity_counts()
        or {}
    )

    high = int(
        counts.get(
            "High",
            0
        )
    )

    medium = int(
        counts.get(
            "Medium",
            0
        )
    )

    low = int(
        counts.get(
            "Low",
            0
        )
    )

    total = (
        high
        + medium
        + low
    )

    return (
        high,
        medium,
        low,
        total
    )


# ==========================================================
# ALERTS BY SEVERITY
# ==========================================================

def create_alert_severity_card():

    # ======================================================
    # INITIAL DATABASE VALUES
    # ======================================================

    (
        high,
        medium,
        low,
        total
    ) = get_current_severity_counts()


    # ======================================================
    # INITIAL DONUT
    # ======================================================

    fig = create_severity_figure(

        high,
        medium,
        low

    )


    # ======================================================
    # CHART
    # ======================================================

    chart = html.Div(

        [

            dcc.Graph(

                id="alert-severity-chart",

                figure=fig,

                config={
                    "displayModeBar": False
                },

                style={
                    "height": "105px",
                    "width": "105px"
                }

            ),


            # ==================================================
            # CENTER TOTAL
            # ==================================================

            html.Div(

                [

                    html.Div(

                        str(total),

                        id="alert-severity-total",

                        style={
                            "fontSize": "18px",
                            "fontWeight": "700",
                            "color": COLORS["text_dark"]
                        }

                    ),

                    html.Div(

                        "Active",

                        style={
                            "fontSize": "11px",
                            "color": COLORS["text_muted"]
                        }

                    )

                ],

                style={

                    "position": "absolute",

                    "top": "50%",

                    "left": "50%",

                    "transform":
                        "translate(-50%, -50%)",

                    "textAlign": "center"

                }

            )

        ],

        style={

            "position": "relative",

            "width": "105px",

            "height": "105px",

            "flexShrink": "0"

        }

    )


    # ======================================================
    # LEGEND
    # ======================================================

    legend = html.Div(

        [

            _severity_row(

                "#ef4444",

                "High",

                high,

                "alert-severity-high"

            ),

            _severity_row(

                "#f59e0b",

                "Medium",

                medium,

                "alert-severity-medium"

            ),

            _severity_row(

                "#3b82f6",

                "Low",

                low,

                "alert-severity-low"

            )

        ],

        style={

            "flex": "1",

            "minWidth": "120px",

            "paddingLeft": "8px"

        }

    )


    # ======================================================
    # REFRESH TIMER
    # ======================================================

    refresh_interval = dcc.Interval(

        id="alert-severity-refresh",

        interval=5000,

        n_intervals=0

    )


    # ======================================================
    # CARD
    # ======================================================

    return dbc.Card(

        dbc.CardBody(

            [

                # ------------------------------------------
                # REFRESH TIMER
                # ------------------------------------------

                refresh_interval,


                # ------------------------------------------
                # TITLE
                # ------------------------------------------

                html.H6(

                    "Alerts by Severity",

                    style={

                        "fontWeight": "600",

                        "fontSize": "16px",

                        "marginBottom": "15px"

                    }

                ),


                # ------------------------------------------
                # CHART + LEGEND
                # ------------------------------------------

                html.Div(

                    [

                        chart,

                        legend

                    ],

                    style={

                        "display": "flex",

                        "alignItems": "center",

                        "justifyContent":
                            "space-between",

                        "width": "100%"

                    }

                )

            ]

        ),

        style={

            "border":
                f"1px solid {COLORS['border']}",

            "borderRadius":
                "10px",

            "overflow":
                "hidden"

        },

        className="shadow-sm"

    )


# ==========================================================
# SEVERITY ROW
# ==========================================================

def _severity_row(

    color,

    label,

    value,

    component_id

):

    return html.Div(

        [

            # ==================================================
            # LABEL + DOT
            # ==================================================

            html.Div(

                [

                    html.Span(

                        style={

                            "display":
                                "inline-block",

                            "width":
                                "10px",

                            "height":
                                "10px",

                            "borderRadius":
                                "50%",

                            "backgroundColor":
                                color

                        }

                    ),

                    html.Span(

                        label,

                        style={

                            "fontSize":
                                "14px",

                            "whiteSpace":
                                "nowrap"

                        }

                    )

                ],

                style={

                    "display":
                        "flex",

                    "alignItems":
                        "center",

                    "gap":
                        "8px"

                }

            ),


            # ==================================================
            # COUNT
            # ==================================================

            html.Span(

                str(value),

                id=component_id,

                style={

                    "fontWeight":
                        "600",

                    "fontSize":
                        "14px",

                    "minWidth":
                        "16px",

                    "textAlign":
                        "right"

                }

            )

        ],

        style={

            "display":
                "flex",

            "justifyContent":
                "space-between",

            "alignItems":
                "center",

            "marginBottom":
                "12px",

            "width":
                "100%"

        }

    )


# ==========================================================
# REFRESH ALERT SEVERITY
# ==========================================================

@callback(

    Output(
        "alert-severity-chart",
        "figure"
    ),

    Output(
        "alert-severity-total",
        "children"
    ),

    Output(
        "alert-severity-high",
        "children"
    ),

    Output(
        "alert-severity-medium",
        "children"
    ),

    Output(
        "alert-severity-low",
        "children"
    ),

    Input(
        "alert-severity-refresh",
        "n_intervals"
    )

)
def refresh_alert_severity(

    n_intervals

):

    # ======================================================
    # GET LATEST DATABASE COUNTS
    # ======================================================

    (
        high,
        medium,
        low,
        total
    ) = get_current_severity_counts()


    # ======================================================
    # CREATE UPDATED DONUT
    # ======================================================

    figure = create_severity_figure(

        high,

        medium,

        low

    )


    # ======================================================
    # RETURN UPDATED DATA
    # ======================================================

    return (

        figure,

        str(total),

        str(high),

        str(medium),

        str(low)

    )