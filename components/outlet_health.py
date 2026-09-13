from dash import html

import dash_bootstrap_components as dbc

from config.settings import COLORS


# ==========================================================
# OUTLET HEALTH CARD
# ==========================================================

def create_outlet_health_card():

    return dbc.Card(

        dbc.CardBody(

            [

                # ==================================================
                # HEADER
                # ==================================================

                dbc.Row(

                    [

                        # ==========================================
                        # OUTLETS TITLE
                        # ==========================================

                        dbc.Col(

                            html.Div(

                                "Outlets",

                                style={

                                    "backgroundColor": "#087443",

                                    "color": "#ffffff",

                                    "padding": "10px 16px",

                                    "borderRadius": "12px",

                                    "fontSize": "18px",

                                    "fontWeight": "600",

                                    "display": "inline-block"

                                }

                            ),

                            width="auto"

                        ),


                        # ==========================================
                        # SEARCH + ALL OUTLETS
                        # ==========================================

                        dbc.Col(

                            [

                                # ==================================
                                # SEARCH BAR
                                # ==================================

                                html.Div(

                                    [

                                        # Search icon
                                        html.I(

                                            className="fas fa-search",

                                            style={

                                                "fontSize": "13px",

                                                "color": "#58758A",

                                                "position": "absolute",

                                                "left": "12px",

                                                "top": "50%",

                                                "transform":
                                                    "translateY(-50%)",

                                                "zIndex": "2",

                                            }

                                        ),


                                        # Search input
                                        dbc.Input(

                                            id="outlet-search",

                                            type="text",

                                            placeholder="Search outlet...",

                                            debounce=False,

                                            value="",

                                            style={

                                                "height": "40px",

                                                "border":
                                                    f"1px solid {COLORS['border']}",

                                                "borderRadius": "10px",

                                                "fontSize": "13px",

                                                # Space for search icon
                                                "padding":
                                                    "6px 10px 6px 34px",

                                                "width": "100%",

                                            }

                                        ),

                                    ],

                                    # Required for icon positioning
                                    style={

                                        "position": "relative",

                                        "width": "100%",

                                    }

                                ),


                                # ==================================
                                # ALL OUTLETS BUTTON
                                # ==================================

                                dbc.Button(

                                    "All Outlets",

                                    id="all-outlets-btn",

                                    color="link",

                                    size="sm",

                                    className="p-0 mt-2",

                                    style={

                                        "color": "#087443",

                                        "fontSize": "13px",

                                        "fontWeight": "600",

                                        "textDecoration": "none",

                                        "marginLeft": "70px"

                                    }

                                )

                            ],

                            width=True,

                            style={

                                "maxWidth": "220px"

                            },

                        ),

                    ],

                    className="align-items-start mb-3"

                ),


                # ==================================================
                # OUTLET LIST
                # ==================================================

                html.Div(

                    html.Div(

                        id="outlets-panel"

                    ),

                   className="outlet-health-scroll",

                    style={

                        # ------------------------------------------
                        # HEIGHT
                        # ------------------------------------------

                        "maxHeight":
                            "280px",

                        "minHeight":
                            "280px",

                        # ------------------------------------------
                        # VERTICAL SCROLL
                        # ------------------------------------------

                        "overflowY":
                            "auto",

                        # ------------------------------------------
                        # NO HORIZONTAL SCROLL
                        # ------------------------------------------

                        "overflowX":
                            "hidden",

                        # ------------------------------------------
                        # SPACE BEFORE SCROLLBAR
                        # ------------------------------------------

                        "paddingRight":
                            "4px",

                    }

                ),

            ]

        ),

        style={

            "border":
                f"1px solid {COLORS['border']}",

            "borderRadius":
                "12px",

            "overflow":
                "hidden"

        },

        className=
            "h-100 shadow-sm"

    )