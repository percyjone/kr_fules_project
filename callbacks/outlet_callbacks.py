from dash import (
    callback,
    Input,
    Output,
    State,
    ALL,
    ctx,
    no_update,
)

from dash import html

import dash_bootstrap_components as dbc

from database.db import fetch_latest_readings
from utils.helpers import row_status

from config.settings import COLORS


# ==========================================================
# OUTLET HEALTH PANEL
# ==========================================================

@callback(

    Output(
        "outlets-panel",
        "children"
    ),

    Input(
        "refresh-interval",
        "n_intervals"
    ),

    Input(
        "outlet-select",
        "value"
    ),

    Input(
        "outlet-search",
        "value"
    ),

)
def update_outlets_panel(

    _,
    outlet_code,
    search_text

):

    # ======================================================
    # FETCH ALL OUTLETS
    # ======================================================

    rows = fetch_latest_readings(
        "all"
    )

    grouped = {}

    for r in rows:

        outlet = r["outlet_code"]

        grouped.setdefault(
            outlet,
            []
        ).append(r)

    # ======================================================
    # SEARCH OUTLETS
    # ======================================================

    search_text = (

        str(search_text or "")
        .strip()
        .lower()

    )

    if search_text:

        grouped = {

            outlet: tanks

            for outlet, tanks
            in grouped.items()

            if search_text
            in str(outlet).lower()

        }

    # ======================================================
    # CREATE OUTLET CARDS
    # ======================================================

    items = []

    for outlet, tanks in sorted(
        grouped.items()
    ):

        # --------------------------------------------------
        # ONLINE COUNT
        # --------------------------------------------------

        online_count = sum(

            1

            for tank in tanks

            if row_status(tank)
            == "Online"

        )

        # --------------------------------------------------
        # OFFLINE COUNT
        # --------------------------------------------------

        offline_count = (

            len(tanks)
            - online_count

        )

        # --------------------------------------------------
        # SELECTED OUTLET
        # --------------------------------------------------

        is_selected = (

            outlet_code != "all"

            and outlet_code == outlet

        )

        # --------------------------------------------------
        # CARD STYLE
        # --------------------------------------------------

        card_style = {

            "padding":
                "14px",

            "marginBottom":
                "10px",

           "border": (
                "2px solid #209849"
                if is_selected
                else f"1px solid {COLORS['border']}"
            ),

            "borderRadius":
                "12px",

            "backgroundColor":

                (

                     "#eaf7ee"

                    if is_selected

                    else "#ffffff"

                ),

            "cursor":
                "pointer",

            "transition":
                "all 0.2s ease",

        }

        # ==================================================
        # OUTLET CARD
        # ==================================================

        items.append(

            html.Div(

                [

                    # ======================================
                    # OUTLET NAME + TANK COUNT
                    # ======================================

                    dbc.Row(

                        [

                            # --------------------------------
                            # OUTLET NAME
                            # --------------------------------

                            dbc.Col(

                                html.Div(

                                    [

                                        html.Span(

                                            # "📍",
                                            html.I(className="fas fa-map-marker-alt"),
                                           


                                            style={
                                                "color": "#FF3B4A",
                                                "fontSize": "18px",
                                                "fontSize":
                                                    "15px",

                                                "marginRight":
                                                    "8px"

                                            }

                                        ),

                                        html.Span(

                                            outlet,

                                            style={

                                                "fontWeight":
                                                    "600",

                                                "fontSize":
                                                    "15px",

                                                "color":
                                                    COLORS[
                                                        "text_dark"
                                                    ]

                                            }

                                        ),

                                    ]

                                ),

                                width=8

                            ),

                            # --------------------------------
                            # TANK COUNT
                            # --------------------------------

                            dbc.Col(

                                dbc.Badge(
                                f"{len(tanks)} Tank" + ("s" if len(tanks) != 1 else ""),
                                style={
                                    "fontWeight": "600",
                                    "fontSize": "12px",
                                    "padding": "7px 10px",
                                    "borderRadius": "16px",
                                },
                            ),

                                width=4,

                                className=
                                    "text-end"

                            ),

                        ],

                        className=
                            "align-items-center"

                    ),

                    # ======================================
                    # ONLINE / OFFLINE
                    # ======================================

                    html.Div(

                        [

                            # --------------------------------
                            # ONLINE
                            # --------------------------------

                            html.Span(

                                [

                                    html.Span(

                                        "●",

                                        style={

                                            "fontSize":
                                                "17px",

                                            "marginRight":
                                                "6px",

                                            "color":
                                                COLORS[
                                                    "green"
                                                ]

                                        }

                                    ),

                                    f"{online_count} Online"

                                ],

                                style={

                                    "color":
                                        COLORS["green"],

                                    "fontSize":
                                        "13px",

                                    "marginRight":
                                        "18px"

                                }

                            ),

                            # --------------------------------
                            # OFFLINE
                            # --------------------------------

                            html.Span(

                                [

                                    html.Span(

                                        "●",

                                        style={

                                            "fontSize":
                                                "17px",

                                            "marginRight":
                                                "6px",

                                            "color":
                                                COLORS[
                                                    "red"
                                                ]

                                        }

                                    ),

                                    f"{offline_count} Offline"

                                ],

                                style={

                                    "color":
                                        COLORS["red"],

                                    "fontSize":
                                        "13px"

                                }

                            ),

                        ],

                        style={

                            "marginTop":
                                "10px"

                        }

                    ),

                ],

                # ==========================================
                # CLICKABLE OUTLET
                # ==========================================

                id={

                    "type":
                        "outlet-select-btn",

                    "outlet":
                        outlet

                },

                n_clicks=0,

                style=card_style

            )

        )

    # ======================================================
    # NO OUTLETS
    # ======================================================

    if not items:

        if search_text:

            return html.Div(

                "No outlets found.",

                style={

                    "color":
                        COLORS["text_muted"],

                    "fontSize":
                        "13px",

                    "padding":
                        "15px 5px"

                }

            )

        return html.Div(

            "No outlets yet.",

            style={

                "color":
                    COLORS["text_muted"],

                "fontSize":
                    "13px",

                "padding":
                    "15px 5px"

            }

        )

    # ======================================================
    # RETURN OUTLETS
    # ======================================================

    return items


# ==========================================================
# OUTLET SELECTION FROM PANEL
# ==========================================================

@callback(

    Output(
        "outlet-select",
        "value",
        allow_duplicate=True
    ),

    Input(

        {
            "type":
                "outlet-select-btn",

            "outlet":
                ALL

        },

        "n_clicks"

    ),

    State(

        {
            "type":
                "outlet-select-btn",

            "outlet":
                ALL

        },

        "id"

    ),

    prevent_initial_call=True,

)
def select_outlet_from_panel(

    clicks,
    outlet_ids

):

    trigger = ctx.triggered_id

    # ======================================================
    # CHECK TRIGGER
    # ======================================================

    if not isinstance(

        trigger,
        dict

    ):

        return no_update

    if (

        trigger.get("type")
        != "outlet-select-btn"

    ):

        return no_update

    # ======================================================
    # FIND SELECTED OUTLET
    # ======================================================

    for i, outlet_id in enumerate(

        outlet_ids or []

    ):

        if (

            outlet_id == trigger

            and i < len(
                clicks or []
            )

            and clicks[i] is not None

            and clicks[i] > 0

        ):

            return outlet_id[
                "outlet"
            ]

    return no_update


# ==========================================================
# ALL OUTLETS BUTTON
# ==========================================================

@callback(

    Output(
        "outlet-select",
        "value",
        allow_duplicate=True
    ),

    Input(
        "all-outlets-btn",
        "n_clicks"
    ),

    prevent_initial_call=True,

)
def select_all_outlets(

    n_clicks

):

    if n_clicks:

        return "all"

    return no_update