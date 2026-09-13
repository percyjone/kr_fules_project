from dash import html, dash_table

import dash_bootstrap_components as dbc

from config.settings import COLORS


# ==========================================================
# TANK TABLE
# ==========================================================

def create_tanks_table_card():

    # ======================================================
    # DATA TABLE
    # ======================================================

    table = dash_table.DataTable(

        id="tanks-table",

        columns=[

            {
                "name": "OUTLET CODE",
                "id": "outlet_code"
            },

            {
                "name": "TANK ID",
                "id": "tank_id"
            },

            {
                "name": "TEMPERATURE (°C)",
                "id": "temp"
            },

            {
                "name": "VOLUME (L)",
                "id": "volume"
            },

            {
                "name": "LAST UPDATED",
                "id": "last_updated"
            },

            {
                "name": "STATUS",
                "id": "status"
            },

        ],

        # ==================================================
        # DATA
        # ==================================================

        data=[],

        # ==================================================
        # ROW SELECTION
        # ==================================================

        row_selectable="single",

        selected_rows=[],

        # ==================================================
        # CSS
        # ==================================================

        css=[

            # ----------------------------------------------
            # SEARCH / FILTER INPUT
            # ----------------------------------------------

            {
                "selector":
                    ".dash-filter input",

                "rule": """
                    color: #1a2233 !important;
                    background-color: #ffffff !important;
                    font-size: 13px !important;
                    opacity: 1 !important;
                """
            },

            {
                "selector":
                    ".dash-filter input::placeholder",

                "rule": """
                    color: #6b7280 !important;
                    opacity: 1 !important;
                """
            },

        ],

        # ==================================================
        # TABLE WIDTH
        # ==================================================

        style_table={

            "width":
                "100%",

            "overflowX":
                "hidden",

            "overflowY":
                "hidden",

        },

        # ==================================================
        # HEADER
        # ==================================================

        style_header={

            "backgroundColor":
                COLORS["page_bg"],

            "color":
                "#209849",

            "fontSize":
                "11px",

            "fontWeight":
                "600",

            "border":
                "none",

            "borderBottom":
                f"1px solid {COLORS['border']}",

            "height":
                "44px",

            "textAlign":
                "center",

            "whiteSpace":
                "normal",

            "padding":
                "6px 4px",

        },

        # ==================================================
        # CELLS
        # ==================================================

        style_cell={

            "fontFamily":
                "inherit",

            "fontSize":
                "13px",

            "padding":
                "8px 4px",

            "height":
                "44px",

            "minHeight":
                "44px",

            "border":
                "none",

            "borderBottom":
                f"1px solid {COLORS['border']}",

            "color":
                COLORS["text_dark"],

            "textAlign":
                "center",

            "whiteSpace":
                "normal",

            "overflow":
                "hidden",

            "textOverflow":
                "ellipsis",

        },

        # ==================================================
        # COLUMN WIDTHS
        # ==================================================

        style_cell_conditional=[

            # ----------------------------------------------
            # OUTLET CODE
            # ----------------------------------------------

            {
                "if": {
                    "column_id":
                        "outlet_code"
                },

                "width":
                    "15%",

                "minWidth":
                    "15%",

                "maxWidth":
                    "15%",

            },

            # ----------------------------------------------
            # TANK ID
            # ----------------------------------------------

            {
                "if": {
                    "column_id":
                        "tank_id"
                },

                "width":
                    "10%",

                "minWidth":
                    "10%",

                "maxWidth":
                    "10%",

            },

            # ----------------------------------------------
            # TEMPERATURE
            # ----------------------------------------------

            {
                "if": {
                    "column_id":
                        "temp"
                },

                "width":
                    "17%",

                "minWidth":
                    "17%",

                "maxWidth":
                    "17%",

            },

            # ----------------------------------------------
            # VOLUME
            # ----------------------------------------------

            {
                "if": {
                    "column_id":
                        "volume"
                },

                "width":
                    "15%",

                "minWidth":
                    "15%",

                "maxWidth":
                    "15%",

            },

            # ----------------------------------------------
            # LAST UPDATED
            # ----------------------------------------------

            {
                "if": {
                    "column_id":
                        "last_updated"
                },

                "width":
                    "10%",

                "minWidth":
                    "10%",

                "maxWidth":
                    "10%",

            },

            # ----------------------------------------------
            # STATUS
            # ----------------------------------------------

            {
                "if": {
                    "column_id":
                        "status"
                },

                "width":
                    "20%",

                "minWidth":
                    "20%",

                "maxWidth":
                    "20%",

            },

        ],

        # ==================================================
        # STATUS COLORS
        # ==================================================

        style_data_conditional=[

            # ----------------------------------------------
            # ONLINE
            # ----------------------------------------------

            {
                "if": {

                    "filter_query":
                        "{status} = Online",

                    "column_id":
                        "status"

                },

                "color":
                    COLORS["green"],

                "fontWeight":
                    "600",

            },

            # ----------------------------------------------
            # OFFLINE
            # ----------------------------------------------

            {
                "if": {

                    "filter_query":
                        "{status} = Offline",

                    "column_id":
                        "status"

                },

                "color":
                    COLORS["red"],

                "fontWeight":
                    "600",

            },

        ],

    )


    # ======================================================
    # TABLE CONTAINER
    # ======================================================

    scrollable_table = html.Div(

        table,

        className="tank-table-scroll",

        style={

            "height":
                "352px",

            "maxHeight":
                "352px",

            "overflowY":
                "auto",

            "overflowX":
                "hidden",

            "width":
                "100%",

        }

    )


    # ======================================================
    # CARD
    # ======================================================

    return dbc.Card(

        dbc.CardBody(

            [

                # ==================================================
                # HEADER
                # ==================================================

                dbc.Row(

                    [

                        # ------------------------------------------
                        # TITLE
                        # ------------------------------------------

                        dbc.Col(

                            html.H6(

                                "Tanks Data",

                                className="mb-3"

                            ),

                            width=6

                        ),

                        # ------------------------------------------
                        # SEARCH
                        # ------------------------------------------

                        dbc.Col(

                            html.Div(

                                [

                                    # Search icon
                                    html.I(

                                        className="fas fa-search",

                                        style={

                                            "fontSize":
                                                "13px",

                                            "color":
                                                "#58758A",

                                            "position":
                                                "absolute",

                                            "left":
                                                "10px",

                                            "top":
                                                "50%",

                                            "transform":
                                                "translateY(-50%)",

                                            "zIndex":
                                                "2",

                                        },

                                    ),

                                    # Search input
                                    dbc.Input(

                                        id="tank-search",

                                        placeholder=
                                            "Search tank / outlet code...",

                                        size="sm",

                                        style={

                                            "paddingLeft":
                                                "30px",

                                        },

                                    ),

                                ],

                                style={

                                    "position":
                                        "relative",

                                    "width":
                                        "100%",

                                },

                            ),

                            width=6

                        ),

                    ],

                    className=
                        "align-items-center"

                ),

                # ==================================================
                # TABLE
                # ==================================================

                scrollable_table,

            ]

        ),

        style={

            "border":
                f"1px solid {COLORS['border']}",

            "borderRadius":
                "12px",

        },

        className=
            "h-100 shadow-sm"

    )