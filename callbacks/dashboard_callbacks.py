from datetime import datetime

from dash import (
    callback,
    Input,
    Output,
    html,
)

import dash_bootstrap_components as dbc


from database.db import (
    fetch_latest_readings,
    fetch_alerts,
)

from utils.helpers import row_status

from components.kpi_cards import (
    kpi_card
)


# ==========================================================
# OUTLET DROPDOWN OPTIONS
# ==========================================================

@callback(

    Output(
        "outlet-select",
        "options"
    ),

    Input(
        "refresh-interval",
        "n_intervals"
    ),

)

def update_outlet_options(_):

    rows = fetch_latest_readings(
        "all"
    )

    outlets = sorted(

        {
            r["outlet_code"]

            for r in rows

        }

    )

    return [

        {
            "label":
                "All Outlets",

            "value":
                "all"
        }

    ] + [

        {
            "label":
                outlet,

            "value":
                outlet
        }

        for outlet in outlets

    ]


# ==========================================================
# KPI CALLBACK
# ==========================================================

@callback(

    Output(
        "kpi-row",
        "children"
    ),

    Output(
        "last-updated",
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

)

def update_kpis(
    _,
    outlet_code
):

    # ======================================================
    # FETCH LATEST TANK READINGS
    # ======================================================

    rows = fetch_latest_readings(

        outlet_code

    )

    # ======================================================
    # LAST UPDATED
    # ======================================================

    timestamp = (

        

        f"{datetime.now().strftime('%I:%M:%S %p')}"

    )

    # ======================================================
    # NO TANK DATA
    # ======================================================

    if not rows:

        empty = dbc.Alert(

            "No readings yet — publish a message via MQTT to populate the dashboard.",

            color="warning"

        )

        return (

            empty,

            timestamp

        )

    # ======================================================
    # OUTLETS
    # ======================================================

    outlets = sorted(

        {

            r["outlet_code"]

            for r in rows

        }

    )

    # ======================================================
    # TOTAL TANKS
    # ======================================================

    n_tanks = len(rows)

    # ======================================================
    # TOTAL VOLUME
    # ======================================================

    total_volume = sum(

        float(r["volume"])

        for r in rows

        if r.get("volume") is not None

    )

    # ======================================================
    # FETCH ALL ALERTS
    #
    # IMPORTANT:
    #
    # We intentionally use:
    #
    # severity="all"
    # status="all"
    #
    # Therefore the Dashboard count represents ALL
    # alerts that are displayed in the Alerts table.
    # ======================================================

    alerts = (

        fetch_alerts(

            severity="all",

            status="all"

        )

        or []

    )

    # ======================================================
    # TOTAL ALERT COUNT
    #
    # Example:
    #
    # Alerts table = 7 alerts
    #
    # Dashboard = 7
    #
    # Alerts table = 6 alerts
    #
    # Dashboard = 6
    # ======================================================

    active_alerts = len(alerts)

    # ======================================================
    # ALERT SUBLABEL
    # ======================================================

    if active_alerts > 0:

        alert_sublabel = (
            "Requires Attention"
        )

    else:

        alert_sublabel = (
            "All Clear"
        )

    # ======================================================
    # KPI ROW
    # ======================================================

    cards = dbc.Row(

        [

            # ==================================================
            # TOTAL OUTLETS
            # ==================================================

            kpi_card(

                # "📍",
                html.I(
                className="fas fa-gas-pump",
                style={
                    "fontSize": "24px",
                    "color": "#0f8f5f"
                }
                ),

                "Total Outlets",

                str(
                    len(outlets)
                ),

                ", ".join(
                    outlets
                ),

                "blue"

            ),

            # ==================================================
            # TOTAL TANKS
            # ==================================================

            kpi_card(

                # "🛢️",
                html.I(
                    className="fas fa-layer-group",
                    style={
                        "fontSize": "24px",
                        "color": "#2563eb"
                    }
                ),

                "Total Tanks",

                str(
                    n_tanks
                ),

                "Across Outlets",

                "green"

            ),

            # ==================================================
            # TOTAL VOLUME
            # ==================================================

            kpi_card(

                # "💧",
                html.I(
                    className="fas fa-tint",
                    style={
                        "fontSize": "24px",
                        "color": "#3b82f6"
                    }
                ),

                "Total Volume",

                f"{total_volume:.1f} L",

                "Across All Tanks",

                "purple"

            ),

            # ==================================================
            # ACTIVE ALERTS
            #
            # SHOWS ALL ALERTS
            #
            # CLICK → /alerts
            # ==================================================

            kpi_card(

                # "🔔",
                html.I(
                    className="fas fa-bell",
                    style={
                        "fontSize": "24px",
                        "color": "#f59e0b"
                    }
                ),

                "Active Alerts",

                str(
                    active_alerts
                ),

                alert_sublabel,

                "red",

                href="/alerts"

            ),

        ],

        className="g-3 justify-content-center"

    )

    # ======================================================
    # RETURN
    # ======================================================

    return (

        cards,

        timestamp

    )


# ==========================================================
# TANK DATA TABLE
# ==========================================================

@callback(

    Output(
        "tanks-table",
        "data"
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
        "tank-search",
        "value"
    ),

)

def update_tanks_table(

    _,

    outlet_code,

    search_text

):

    # ======================================================
    # FETCH TANK DATA
    # ======================================================

    rows = fetch_latest_readings(

        outlet_code

    )

    # ======================================================
    # SEARCH
    # ======================================================

    if search_text:

        search_text = (

            str(search_text)

            .strip()

            .lower()

        )

        rows = [

            row

            for row in rows

            if (

                search_text

                in str(

                    row["outlet_code"]

                ).lower()

                or

                search_text

                in str(

                    row["tank_id"]

                ).lower()

            )

        ]

    # ======================================================
    # CREATE TABLE DATA
    # ======================================================

    table_data = []

    for row in rows:

        table_data.append(

            {

                "outlet_code":
                    row["outlet_code"],

                "tank_id":
                    row["tank_id"],

                "temp":
                    row["temp"],

                "volume":
                    row["volume"],

                "last_updated":
                    row["time"],

                "status":
                    row_status(row),

            }

        )

    # ======================================================
    # RETURN
    # ======================================================

    return table_data