from dash import (
    callback,
    Input,
    Output,
    State,
    ALL,
    ctx,
    html,
)

from database.db import fetch_tank_history

from components.tank_details import (
    create_tank_detail_panel,
    create_tank_detail_content,
)


# ==========================================================
# SELECTED TANK
# ==========================================================

@callback(

    Output(
        "selected-tank",
        "data"
    ),

    Input(
        "tanks-table",
        "selected_rows"
    ),

    Input(

        {
            "type":
                "tank-select-btn",

            "outlet":
                ALL,

            "tank":
                ALL
        },

        "n_clicks"

    ),

    State(
        "tanks-table",
        "data"
    ),

    State(
        "selected-tank",
        "data"
    ),

    prevent_initial_call=True,

)
def update_selected_tank(

    selected_rows,

    clicks,

    table_data,

    current_selected

):

    trigger = ctx.triggered_id


    # ======================================================
    # TABLE SELECTION
    # ======================================================

    if trigger == "tanks-table":

        if (
            selected_rows
            and table_data
        ):

            row = table_data[
                selected_rows[0]
            ]

            return {

                "outlet_code":
                    row["outlet_code"],

                "tank_id":
                    row["tank_id"]

            }

        return current_selected


    # ======================================================
    # TANK BUTTON
    # ======================================================

    if isinstance(
        trigger,
        dict
    ):

        if (
            trigger.get("type")
            == "tank-select-btn"
        ):

            if clicks:

                for click_count in clicks:

                    if (

                        click_count
                        is not None

                        and

                        click_count > 0

                    ):

                        return {

                            "outlet_code":
                                trigger[
                                    "outlet"
                                ],

                            "tank_id":
                                trigger[
                                    "tank"
                                ]

                        }


    return current_selected


# ==========================================================
# CREATE TANK DETAIL PANEL
#
# This callback is ONLY responsible for creating the
# Tank Details structure when a tank is selected.
#
# IMPORTANT:
# The tank-time-filter dropdown is created here.
#
# The 5-second refresh does NOT call this callback.
# ==========================================================

@callback(

    Output(
        "tank-detail-panel",
        "children"
    ),

    Input(
        "selected-tank",
        "data"
    ),

    prevent_initial_call=True,

)
def create_selected_tank_panel(

    selected

):

    # ======================================================
    # NO TANK SELECTED
    # ======================================================

    if not selected:

        return html.Div()


    # ======================================================
    # CREATE TANK DETAIL PANEL
    #
    # Default period = day
    # ======================================================

    return create_tank_detail_panel(

        selected,

        "day"

    )


# ==========================================================
# UPDATE TANK DETAIL CONTENT
#
# This callback handles:
#
# 1. Day / Month / Year changes
# 2. 5-second automatic refresh
#
# IMPORTANT:
#
# It updates ONLY:
#
#     tank-detail-content
#
# It does NOT recreate:
#
#     tank-time-filter
#
# Therefore the dropdown stays selected.
# ==========================================================

@callback(

    Output(
        "tank-detail-content",
        "children"
    ),

    # ------------------------------------------------------
    # PERIOD DROPDOWN
    # ------------------------------------------------------

    Input(

        "tank-time-filter",

        "value",

        allow_optional=True

    ),

    # ------------------------------------------------------
    # SELECTED TANK
    # ------------------------------------------------------

    Input(

        "selected-tank",

        "data"

    ),

    # ------------------------------------------------------
    # AUTO REFRESH
    #
    # KEEPING THIS MEANS YOUR TANK DATA STILL REFRESHES
    # EVERY 5 SECONDS.
    # ------------------------------------------------------

    Input(

        "refresh-interval",

        "n_intervals"

    ),

)
def update_tank_detail_content(

    period,

    selected,

    _n

):

    # ======================================================
    # NO TANK SELECTED
    # ======================================================

    if not selected:

        return html.Div()


    # ======================================================
    # DEFAULT PERIOD
    # ======================================================

    if not period:

        period = "day"


    # ======================================================
    # GET TANK INFORMATION
    # ======================================================

    outlet_code = selected[

        "outlet_code"

    ]

    tank_id = selected[

        "tank_id"

    ]


    # ======================================================
    # FETCH HISTORY
    # ======================================================

    history = fetch_tank_history(

        outlet_code,

        tank_id,

        period=period

    )


    # ======================================================
    # CREATE ONLY THE REFRESHABLE CONTENT
    #
    # IMPORTANT:
    #
    # DO NOT call:
    #
    #     create_tank_detail_panel()
    #
    # here.
    #
    # That would recreate the dropdown.
    #
    # Instead call:
    #
    #     create_tank_detail_content()
    #
    # which only creates the graphs/data.
    # ======================================================

    return create_tank_detail_content(

        selected,

        history,

        period

    )