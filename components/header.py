from dash import html, dcc
import dash_bootstrap_components as dbc

from config.settings import COLORS


# ==========================================================
# HEADER
# ==========================================================

def create_header():

    # ======================================================
    # TOP HEADER / NAVIGATION
    # ======================================================

    return html.Div(

        [

            # ==================================================
            # MAIN NAVIGATION BAR
            # ==================================================

            html.Div(

                [

                    # ==========================================
                    # LEFT - BRAND
                    # ==========================================

                    html.Div(

                        [

                            html.Div(

                                "KR",

                                style={
                                    "width": "42px",
                                    "height": "42px",
                                    "borderRadius": "10px",
                                    "backgroundColor": "#087443",
                                    "color": "#ffffff",
                                    "fontSize": "21px",
                                    "fontWeight": "800",
                                    "display": "flex",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "letterSpacing": "-1px",
                                    "flexShrink": "0",
                                }

                            ),

                            html.Div(

                                [

                                    html.Div(

                                        "K.R Trans Fuels",

                                        style={
                                            "fontSize": "16px",
                                            "fontWeight": "700",
                                            "color": "#063d29",
                                            "lineHeight": "20px",
                                            "whiteSpace": "nowrap",
                                        }

                                    ),

                                    html.Div(

                                        "Private Limited",

                                        style={
                                            "fontSize": "11px",
                                            "color": "#668277",
                                            "lineHeight": "16px",
                                            "whiteSpace": "nowrap",
                                        }

                                    ),

                                ]

                            ),

                        ],

                        className="header-brand",

                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "10px",
                            "minWidth": "0",
                            "flex": "0 1 auto",
                        }

                    ),

                    # ==========================================
                    # NAVIGATION
                    # ==========================================

                    html.Div(

                        [

                            # ----------------------------------
                            # HOME
                            # ----------------------------------

                            dcc.Link(

                                html.Div(

                                    [

                                        html.Span(
                                            className="fas fa-home",
                                            style={
                                                "color": "#ffffff",
                                                "fontSize": "17px"
                                            }
                                        ),

                                        html.Span("Home"),

                                    ],

                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "7px",
                                    }

                                ),

                                href="/",

                                style={
                                    "textDecoration": "none",
                                    "color": "#ffffff",
                                    "backgroundColor": "#087443",
                                    "padding": "10px 17px",
                                    "borderRadius": "10px",
                                    "fontSize": "14px",
                                    "fontWeight": "600",
                                }

                            ),

                            # ----------------------------------
                            # ABOUT
                            # ----------------------------------

                            dcc.Link(

                                "About",

                                href="#",

                                style={
                                    "textDecoration": "none",
                                    "color": "#18352b",
                                    "fontSize": "14px",
                                    "fontWeight": "500",
                                    "padding": "10px 13px",
                                }

                            ),

                            # ----------------------------------
                            # CONTACT
                            # ----------------------------------

                            dcc.Link(

                                "Contact",

                                href="#",

                                style={
                                    "textDecoration": "none",
                                    "color": "#18352b",
                                    "fontSize": "14px",
                                    "fontWeight": "500",
                                    "padding": "10px 13px",
                                }

                            ),

                        ],

                        className="header-navigation",

                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "3px",
                            "flex": "1 1 auto",
                            "minWidth": "0",
                            "flexWrap": "wrap",
                        }

                    ),

                    # ==========================================
                    # RIGHT SIDE
                    # ==========================================

                    html.Div(

                        [

                            # ----------------------------------
                            # OUTLET DROPDOWN
                            # ----------------------------------

                            html.Div(

                                dbc.Select(

                                    id="outlet-select",

                                    options=[
                                        {
                                            "label": "All Outlets",
                                            "value": "all"
                                        }
                                    ],

                                    value="all",

                                    style={
                                        "height": "42px",
                                        "width": "170px",
                                        "minWidth": "140px",
                                        "maxWidth": "100%",
                                        "border": "1px solid #dce9e2",
                                        "borderRadius": "22px",
                                        "backgroundColor": "#ffffff",
                                        "color": "#17382c",
                                        "fontSize": "13px",
                                        "fontWeight": "500",
                                        "paddingLeft": "16px",
                                        "paddingRight": "32px",
                                        "boxShadow": "0 2px 8px rgba(0,0,0,0.04)",
                                        "boxSizing": "border-box",
                                    }

                                )

                            ),

                            # ----------------------------------
                            # ALERT BELL
                            # ----------------------------------

                            dcc.Link(

                                html.Div(

                                    className="fas fa-bell",

                                    style={
                                        "width": "42px",
                                        "height": "42px",
                                        "borderRadius": "50%",
                                        "backgroundColor": "#ffffff",
                                        "border": "1px solid #dce9e2",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "fontSize": "17px",
                                        "boxShadow": "0 2px 8px rgba(0,0,0,0.04)",
                                        "flexShrink": "0",
                                    }

                                ),

                                href="/alerts",

                                style={
                                    "textDecoration": "none"
                                }

                            ),

                            # ----------------------------------
                            # USER
                            # ----------------------------------

                            html.Div(

                                [

                                    html.Div(

                                        className="fas fa-user",

                                        style={
                                            "width": "34px",
                                            "height": "34px",
                                            "borderRadius": "50%",
                                            "backgroundColor": "#e8f5ee",
                                            "color": "#087443",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "fontSize": "18px",
                                            "flexShrink": "0",
                                        }

                                    ),

                                    html.Span(

                                        "K.R Trans Fuels",

                                        className="header-user-name",

                                        style={
                                            "fontSize": "13px",
                                            "fontWeight": "600",
                                            "color": "#18352b",
                                            "whiteSpace": "nowrap",
                                        }

                                    ),

                                    html.Span(

                                        "⌄",

                                        style={
                                            "fontSize": "15px",
                                            "color": "#668277",
                                        }

                                    ),

                                ],

                                className="header-user",

                                style={
                                    "height": "42px",
                                    "padding": "4px 12px 4px 7px",
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "8px",
                                    "border": "1px solid #dce9e2",
                                    "borderRadius": "22px",
                                    "backgroundColor": "#ffffff",
                                    "boxShadow": "0 2px 8px rgba(0,0,0,0.04)",
                                    "minWidth": "0",
                                }

                            ),

                        ],

                        className="header-right",

                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "10px",
                            "flex": "0 1 auto",
                            "minWidth": "0",
                            "flexWrap": "wrap",
                        }

                    ),

                ],

                className="header-main",

                style={
                    "width": "100%",
                    "minHeight": "76px",
                    "padding": "10px 5px",
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "20px",
                    "backgroundColor": "#ffffff",
                    "borderBottom": "none",
                    "boxSizing": "border-box",
                    "flexWrap": "wrap",
                }

            ),

            # ==================================================
            # ECO-FRIENDLY TEXT
            # ==================================================

            html.Div(

                [

                    html.Span(
                        "🍃",
                        style={
                            "fontSize": "14px"
                        }
                    ),

                    html.Span(
                        "Eco-friendly automotive fuel — since 2007",
                        style={
                            "fontSize": "12px",
                            "fontWeight": "600",
                        }
                    ),

                ],

                className="header-eco",

                style={
                    "width": "100%",
                    "height": "14px",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "flex-end",
                    "gap": "7px",
                    "padding": "0 5px",
                    "boxSizing": "border-box",
                    "backgroundColor": "#ffffff",
                    "color": "#087443",
                    "borderBottom": "none",
                }

            ),

            # ==================================================
            # DASHBOARD TITLE AREA
            # ==================================================

            html.Div(

                [

                    html.Div(

                        [

                            html.H3(

                                "Dashboard",

                                className="mb-0",

                                style={
                                    "color": "#092f25",
                                    "fontSize": "30px",
                                    "fontWeight": "700",
                                    "letterSpacing": "-0.5px",
                                    "margin": "0",
                                }

                            ),

                            html.P(

                                "Real-time overview of all tanks",

                                className="mb-0",

                                style={
                                    "color": "#647f73",
                                    "fontSize": "15px",
                                    "marginTop": "4px",
                                }

                            ),

                        ],

                        className="dashboard-title"

                    ),

                    # ------------------------------------------
                    # LAST UPDATED
                    # IMPORTANT: KEEP THIS ID
                    # ------------------------------------------

                    html.Div(

                        [

                            html.Span(

                                "Last updated: ",

                                style={
                                    "color": "#7a9187",
                                    "fontSize": "12px",
                                }

                            ),

                            html.Span(

                                id="last-updated",

                                style={
                                    "color": "#315c4c",
                                    "fontSize": "12px",
                                    "fontWeight": "600",
                                }

                            ),

                        ],

                        className="last-updated-wrapper",

                        style={
                            "marginLeft": "auto",
                            "alignSelf": "flex-end",
                            "paddingBottom": "4px",
                        }

                    ),

                ],

                className="dashboard-title-area",

                style={
                    "width": "100%",
                    "padding": "15px 5px 10px 5px",
                    "display": "flex",
                    "alignItems": "flex-end",
                    "boxSizing": "border-box",
                    "gap": "10px",
                    "flexWrap": "wrap",
                }

            ),

        ],

        className="header-wrapper",

        style={
            "width": "100%",
            "boxSizing": "border-box",
        }

    )