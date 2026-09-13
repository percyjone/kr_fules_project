from dash import (
    html,
    dcc,
)

import dash_bootstrap_components as dbc

from config.settings import COLORS


# ==========================================================
# KPI CARD
# ==========================================================

def kpi_card(
    icon,
    label,
    value,
    sublabel,
    color_key,
    href=None
):

    # ======================================================
    # CARD BODY
    # ======================================================

    card = dbc.Card(

        dbc.CardBody(

            dbc.Row(

                [

                    # ==================================================
                    # ICON
                    # ==================================================

                    dbc.Col(

                        html.Div(

                            icon,

                            style={

                                "backgroundColor":
                                    COLORS[
                                        f"{color_key}_tint"
                                    ],

                                "color":
                                    COLORS[
                                        color_key
                                    ],

                                "borderRadius":
                                    "10px",

                                "width":
                                    "44px",

                                "height":
                                    "44px",

                                "display":
                                    "flex",

                                "alignItems":
                                    "center",

                                "justifyContent":
                                    "center",

                                "fontSize":
                                    "20px",

                            }

                        ),

                        width="auto"

                    ),

                    # ==================================================
                    # KPI CONTENT
                    # ==================================================

                    dbc.Col(

                        [

                            # ------------------------------------------
                            # LABEL
                            # ------------------------------------------

                            html.Div(

                                label,

                                className="small",

                                style={

                                    "color":
                                        COLORS[
                                            "text_muted"
                                        ],

                                    "whiteSpace":
                                        "nowrap",

                                }

                            ),

                            # ------------------------------------------
                            # VALUE
                            # ------------------------------------------

                            html.H4(

                                value,

                                className="mb-0 mt-1",

                                style={

                                    "color":
                                        COLORS[
                                            "text_dark"
                                        ],

                                    "fontWeight":
                                        "500",

                                }

                            ),

                            # ------------------------------------------
                            # SUBLABEL
                            # ------------------------------------------

                            html.Div(

                                sublabel,

                                className="small",

                                style={

                                    "color":
                                        COLORS[
                                            "text_muted"
                                        ],

                                }

                            ),

                        ]

                    ),

                ],

                align="center",

                className="g-3"

            )

        ),

        style={

            "border":
                f"1px solid {COLORS['border']}",

            "borderRadius":
                "12px",

            "height":
                "100%",

            "minHeight":
                "150px",

            "transition":
                "all 0.2s ease",

        },

        className="shadow-sm"

    )

    # ==========================================================
    # IF HREF IS PROVIDED
    #
    # The complete card becomes clickable.
    # ==========================================================

    if href:

        card_content = dcc.Link(

            card,

            href=href,

            style={

                "textDecoration":
                    "none",

                "color":
                    "inherit",

                "display":
                    "block",

                "height":
                    "100%",

                "cursor":
                    "pointer",

            }

        )

    else:

        card_content = card

    # ==========================================================
    # RETURN ONE CONSISTENT COLUMN
    #
    # IMPORTANT:
    # Every KPI card returns exactly one dbc.Col.
    # ==========================================================

    return dbc.Col(

        card_content,

        width=12,

        sm=6,

        lg=True,

    )