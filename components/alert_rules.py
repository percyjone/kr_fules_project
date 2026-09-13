from dash import html
import dash_bootstrap_components as dbc

from config.settings import COLORS


# ==========================================================
# ALERT RULES
# ==========================================================

def create_alert_rules_card():

    total_rules = 12
    enabled_rules = 10

    return dbc.Card(

        dbc.CardBody(

            [

                html.H6(

                    "Alert Rules",

                    style={
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "marginBottom": "18px"
                    }
                ),

                # ------------------------------------------
                # TOTAL RULES
                # ------------------------------------------

                dbc.Row(

                    [

                        dbc.Col(
                            "Total Rules",
                            className="text-muted"
                        ),

                        dbc.Col(

                            str(total_rules),

                            className="text-end",

                            style={
                                "fontWeight": "600"
                            }
                        )

                    ],

                    className="mb-3"
                ),

                # ------------------------------------------
                # ENABLED
                # ------------------------------------------

                dbc.Row(

                    [

                        dbc.Col(
                            "Enabled",
                            className="text-muted"
                        ),

                        dbc.Col(

                            str(enabled_rules),

                            className="text-end",

                            style={
                                "fontWeight": "600"
                            }
                        )

                    ],

                    className="mb-3"
                ),

                # ------------------------------------------
                # MANAGE RULES
                # ------------------------------------------

                dbc.Button(

                    [

                        "Manage Rules",

                        html.Span(
                            " →",
                            className="ms-1"
                        )

                    ],

                    id="manage-alert-rules-btn",

                    color="light",

                    className="w-100",

                    style={
                        "color": COLORS["blue"],
                        "border":
                            f"1px solid {COLORS['border']}",
                        "backgroundColor": "#fff"
                    }
                )

            ]

        ),

        style={
            "border":
                f"1px solid {COLORS['border']}",
            "borderRadius": "10px"
        },

        className="shadow-sm"
    )