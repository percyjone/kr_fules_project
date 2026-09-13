from dash import html
import dash_bootstrap_components as dbc

from config.settings import COLORS


# ==========================================================
# QUICK ACTIONS
# ==========================================================

def create_alert_quick_actions():

    return dbc.Card(

        dbc.CardBody(

            [

                html.H6(

                    "Quick Actions",

                    style={
                        "fontWeight": "600",
                        "fontSize": "18px",
                        "marginBottom": "15px"
                    }
                ),

                # ------------------------------------------
                # ACKNOWLEDGE ALL
                # ------------------------------------------

                dbc.Button(

                    [

                        html.Span(
                            "✓",
                            className="me-2"
                        ),

                        "Acknowledge All"

                    ],

                    id="acknowledge-all-btn",

                    color="light",

                    className="w-100 text-start mb-2",

                    style={
                        "color": COLORS["blue"],
                        "border":
                            f"1px solid {COLORS['border']}",
                        "backgroundColor": "#fff"
                    }
                ),

                # ------------------------------------------
                # MARK ALL RESOLVED
                # ------------------------------------------

                dbc.Button(

                    [

                        html.Span(
                            "✓",
                            className="me-2"
                        ),

                        "Mark All as Resolved"

                    ],

                    id="resolve-all-btn",

                    color="light",

                    className="w-100 text-start mb-2",

                    style={
                        "border":
                            f"1px solid {COLORS['border']}",
                        "backgroundColor": "#fff"
                    }
                ),

                # ------------------------------------------
                # ALERT SETTINGS
                # ------------------------------------------

                dbc.Button(

                    [

                        html.Span(
                            "⚙",
                            className="me-2"
                        ),

                        "Alert Settings"

                    ],

                    id="alert-settings-btn",

                    color="light",

                    className="w-100 text-start mb-2",

                    style={
                        "border":
                            f"1px solid {COLORS['border']}",
                        "backgroundColor": "#fff"
                    }
                ),

                # ------------------------------------------
                # NOTIFICATION LOG
                # ------------------------------------------

                dbc.Button(

                    [

                        html.Span(
                            "♧",
                            className="me-2"
                        ),

                        "Notification Log"

                    ],

                    id="notification-log-btn",

                    color="light",

                    className="w-100 text-start",

                    style={
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