import dash

from dash import (
    html,
    dcc,
    callback,
    Input,
    Output,
)

import dash_bootstrap_components as dbc

from datetime import (
    datetime,
    date,
    time,
    timedelta,
)

from database.db import (
    fetch_alerts,
    get_connection,
)

from components.alert_kpi_card import (
    alert_kpi_card
)

from components.alert_severity import (
    create_alert_severity_card
)

from components.alert_quick_actions import (
    create_alert_quick_actions
)

from components.alert_rules import (
    create_alert_rules_card
)


# ==========================================================
# REGISTER ALERTS PAGE
# ==========================================================

dash.register_page(
    __name__,
    path="/alerts",
    name="Alerts"
)


# ==========================================================
# DATE + TIME HELPER
# ==========================================================

def get_alert_datetime(alert):

    created_at = alert.get("created_at")
    created_time = alert.get("time")

    # ======================================================
    # NO CREATED DATE
    # ======================================================

    if created_at is None:
        return None

    # ======================================================
    # IF created_at IS DATETIME
    # ======================================================

    if isinstance(
        created_at,
        datetime
    ):

        base_date = created_at.date()

    # ======================================================
    # IF created_at IS DATE
    # ======================================================

    elif isinstance(
        created_at,
        date
    ):

        base_date = created_at

    # ======================================================
    # IF created_at IS STRING
    # ======================================================

    elif isinstance(
        created_at,
        str
    ):

        created_at = created_at.strip()

        datetime_formats = [

            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",

            "%d-%m-%Y %H:%M:%S",
            "%d-%m-%Y %H:%M",

            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d %H:%M",

            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M",

        ]

        date_formats = [

            "%Y-%m-%d",
            "%d-%m-%Y",
            "%Y/%m/%d",
            "%d/%m/%Y",

        ]

        base_date = None

        # --------------------------------------------------
        # FIRST TRY FULL DATETIME
        # --------------------------------------------------

        for fmt in datetime_formats:

            try:

                parsed_datetime = datetime.strptime(
                    created_at,
                    fmt
                )

                base_date = parsed_datetime.date()

                # If created_at already contains time,
                # use that time directly.

                if created_time is None:

                    return parsed_datetime

                break

            except ValueError:

                continue

        # --------------------------------------------------
        # THEN TRY DATE ONLY
        # --------------------------------------------------

        if base_date is None:

            for fmt in date_formats:

                try:

                    base_date = datetime.strptime(
                        created_at,
                        fmt
                    ).date()

                    break

                except ValueError:

                    continue

        if base_date is None:
            return None

    else:

        return None

    # ======================================================
    # IF TIME IS NONE
    # ======================================================

    if created_time is None:

        return datetime.combine(
            base_date,
            datetime.min.time()
        )

    # ======================================================
    # IF TIME IS datetime.time
    # ======================================================

    if isinstance(
        created_time,
        time
    ):

        return datetime.combine(
            base_date,
            created_time
        )

    # ======================================================
    # IF TIME IS datetime
    # ======================================================

    if isinstance(
        created_time,
        datetime
    ):

        return datetime.combine(
            base_date,
            created_time.time()
        )

    # ======================================================
    # IF TIME IS STRING
    # ======================================================

    if isinstance(
        created_time,
        str
    ):

        created_time = created_time.strip()

        time_formats = [

            "%H:%M:%S",
            "%H:%M",

            "%I:%M:%S %p",
            "%I:%M %p",

        ]

        for fmt in time_formats:

            try:

                parsed_time = datetime.strptime(
                    created_time,
                    fmt
                ).time()

                return datetime.combine(
                    base_date,
                    parsed_time
                )

            except ValueError:

                continue

    # ======================================================
    # FALLBACK
    # ======================================================

    return datetime.combine(
        base_date,
        datetime.min.time()
    )


# ==========================================================
# FORMAT DATE FOR TABLE
# ==========================================================

def format_alert_date(alert):

    alert_datetime = get_alert_datetime(
        alert
    )

    if alert_datetime is None:
        return ""

    return alert_datetime.strftime(
        "%d-%m-%Y"
    )


# ==========================================================
# FORMAT TIME FOR TABLE
# ==========================================================

def format_alert_time(alert):

    # ======================================================
    # USE EXISTING time FIELD
    # ======================================================

    created_time = alert.get(
        "time"
    )

    if created_time is not None:

        # --------------------------------------------------
        # datetime.time
        # --------------------------------------------------

        if isinstance(
            created_time,
            time
        ):

            return created_time.strftime(
                "%H:%M:%S"
            )

        # --------------------------------------------------
        # datetime
        # --------------------------------------------------

        if isinstance(
            created_time,
            datetime
        ):

            return created_time.strftime(
                "%H:%M:%S"
            )

        # --------------------------------------------------
        # STRING
        # --------------------------------------------------

        if isinstance(
            created_time,
            str
        ):

            created_time = created_time.strip()

            time_formats = [

                "%H:%M:%S",
                "%H:%M",

                "%I:%M:%S %p",
                "%I:%M %p",

            ]

            for fmt in time_formats:

                try:

                    parsed_time = datetime.strptime(
                        created_time,
                        fmt
                    )

                    return parsed_time.strftime(
                        "%H:%M:%S"
                    )

                except ValueError:

                    continue

            # If the value is already in a readable
            # format, return it unchanged.

            return created_time

    # ======================================================
    # FALLBACK TO created_at TIME
    # ======================================================

    alert_datetime = get_alert_datetime(
        alert
    )

    if alert_datetime is None:
        return ""

    return alert_datetime.strftime(
        "%H:%M:%S"
    )


# ==========================================================
# FORMAT COMPARISON TEXT
# ==========================================================

def comparison_text(
    current,
    previous,
    previous_label
):

    difference = (
        current
        -
        previous
    )

    if difference > 0:

        return (
            f"+{difference} "
            f"vs {previous_label}"
        )

    if difference < 0:

        return (
            f"{difference} "
            f"vs {previous_label}"
        )

    return (
        f"No change "
        f"vs {previous_label}"
    )


# ==========================================================
# ALERT KPI DATA
# ==========================================================

def get_alert_kpi_data():

    alerts = (
        fetch_alerts(
            severity="all",
            status="all"
        )
        or []
    )

    today = date.today()

    # ======================================================
    # CURRENT WEEK
    # ======================================================

    current_week_start = (
        today
        -
        timedelta(
            days=today.weekday()
        )
    )

    current_week_end = (
        current_week_start
        +
        timedelta(
            days=7
        )
    )

    # ======================================================
    # PREVIOUS WEEK
    # ======================================================

    previous_week_start = (
        current_week_start
        -
        timedelta(
            days=7
        )
    )

    previous_week_end = (
        current_week_start
    )

    # ======================================================
    # CURRENT MONTH
    # ======================================================

    current_month_start = date(
        today.year,
        today.month,
        1
    )

    # ======================================================
    # NEXT MONTH
    # ======================================================

    if today.month == 12:

        next_month_start = date(
            today.year + 1,
            1,
            1
        )

    else:

        next_month_start = date(
            today.year,
            today.month + 1,
            1
        )

    # ======================================================
    # PREVIOUS MONTH
    # ======================================================

    previous_month_end = (
        current_month_start
    )

    if today.month == 1:

        previous_month_start = date(
            today.year - 1,
            12,
            1
        )

    else:

        previous_month_start = date(
            today.year,
            today.month - 1,
            1
        )

    # ======================================================
    # YESTERDAY
    # ======================================================

    yesterday = (
        today
        -
        timedelta(
            days=1
        )
    )

    # ======================================================
    # COUNTERS
    # ======================================================

    active_count = 0

    today_count = 0

    yesterday_count = 0

    this_week_count = 0

    previous_week_count = 0

    this_month_count = 0

    previous_month_count = 0

    # ======================================================
    # PROCESS ALERTS
    # ======================================================

    for alert in alerts:

        # ==================================================
        # ACTIVE ALERTS
        # ==================================================

        status = str(
            alert.get(
                "status",
                ""
            )
        ).strip().lower()

        if status == "active":

            active_count += 1

        # ==================================================
        # GET ALERT DATETIME
        # ==================================================

        alert_datetime = (
            get_alert_datetime(
                alert
            )
        )

        if alert_datetime is None:

            continue

        alert_date = (
            alert_datetime.date()
        )

        # ==================================================
        # TODAY
        # ==================================================

        if alert_date == today:

            today_count += 1

        # ==================================================
        # YESTERDAY
        # ==================================================

        if alert_date == yesterday:

            yesterday_count += 1

        # ==================================================
        # CURRENT WEEK
        # ==================================================

        if (
            current_week_start
            <= alert_date
            <
            current_week_end
        ):

            this_week_count += 1

        # ==================================================
        # PREVIOUS WEEK
        # ==================================================

        if (
            previous_week_start
            <= alert_date
            <
            previous_week_end
        ):

            previous_week_count += 1

        # ==================================================
        # CURRENT MONTH
        # ==================================================

        if (
            current_month_start
            <= alert_date
            <
            next_month_start
        ):

            this_month_count += 1

        # ==================================================
        # PREVIOUS MONTH
        # ==================================================

        if (
            previous_month_start
            <= alert_date
            <
            previous_month_end
        ):

            previous_month_count += 1

    # ======================================================
    # COMPARISONS
    # ======================================================

    today_comparison = comparison_text(

        today_count,

        yesterday_count,

        "yesterday"

    )

    week_comparison = comparison_text(

        this_week_count,

        previous_week_count,

        "last week"

    )

    month_comparison = comparison_text(

        this_month_count,

        previous_month_count,

        "last month"

    )

    # ======================================================
    # RETURN
    # ======================================================

    return {

        "active":
            active_count,

        "today":
            today_count,

        "today_comparison":
            today_comparison,

        "week":
            this_week_count,

        "week_comparison":
            week_comparison,

        "month":
            this_month_count,

        "month_comparison":
            month_comparison,

    }


# ==========================================================
# ALERT KPI CARDS
# ==========================================================

def create_alert_kpi_cards():

    kpi = (
        get_alert_kpi_data()
    )

    return dbc.Row(

        [

            # ==================================================
            # ACTIVE ALERTS
            # ==================================================

            dbc.Col(

                alert_kpi_card(

                    # "🔔",
                    html.I(
                        className="fas fa-bell",
                        style={
                            "fontSize": "28px",
                            "color": "#15803D",
                        }
                    ),

                    "Active Alerts",

                    str(
                        kpi["active"]
                    ),

                    "Requires Attention",

                    "blue"

                ),

                width=12,
                sm=6,
                md=6,
                lg=6,
                xl=3

            ),

            # ==================================================
            # TODAY'S ALERTS
            # ==================================================

            dbc.Col(

                alert_kpi_card(

                    # "⚠️",
                    html.I(
                        className="fas fa-triangle-exclamation",
                        style={
                            "fontSize": "28px",
                            "color": "#15803D"
                        }
                    ),

                    "Today's Alerts",

                    str(
                        kpi["today"]
                    ),

                    kpi[
                        "today_comparison"
                    ],

                    "blue"

                ),

                width=12,
                sm=6,
                md=6,
                lg=6,
                xl=3

            ),

            # ==================================================
            # THIS WEEK
            # ==================================================

            dbc.Col(

                alert_kpi_card(

                    # "ℹ️",
                    html.I(
                        className="fas fa-circle-info",
                        style={
                            "fontSize": "28px",
                            "color": "#15803D"
                        }
                    ),

                    "This Week",

                    str(
                        kpi["week"]
                    ),

                    kpi[
                        "week_comparison"
                    ],

                    "blue"

                ),

                width=12,
                sm=6,
                md=6,
                lg=6,
                xl=3

            ),

            # ==================================================
            # THIS MONTH
            # ==================================================

            dbc.Col(

                alert_kpi_card(

                    # "✓",
                    html.I(
                        className="fas fa-circle-check",
                        style={
                            "fontSize": "28px",
                            "color": "#15803D"
                        }
                    ),

                    "This Month",

                    str(
                        kpi["month"]
                    ),

                    kpi[
                        "month_comparison"
                    ],

                    "green"

                ),

                width=12,
                sm=6,
                md=6,
                lg=6,
                xl=3

            ),

        ],

        className="g-3 mb-4"

    )


# ==========================================================
# KPI REFRESH CALLBACK
# ==========================================================

@callback(

    Output(
        "alerts-kpi-cards",
        "children"
    ),

    Input(
        "alerts-refresh-interval",
        "n_intervals"
    )

)

def refresh_alert_kpi_cards(
    n_intervals
):

    return create_alert_kpi_cards()


# ==========================================================
# GET LATEST TANK STOCK
# ==========================================================

def get_latest_tank_stock(
    outlet_code,
    tank_id
):

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        sql = """

            SELECT

                outlet_code,

                tank_id,

                volume,

                capacity,

                dead_stock,

                min_stock,

                max_stock,

                temp,

                date,

                time

            FROM tank

            WHERE outlet_code = %s

            AND tank_id = %s

            ORDER BY

                rowid DESC

            LIMIT 1

        """

        cursor.execute(

            sql,

            (
                outlet_code,
                tank_id
            )

        )

        row = cursor.fetchone()

        return row

    except Exception as e:

        print(
            "Error fetching tank stock:",
            e
        )

        return None

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================================
# CREATE INDICATOR CIRCLE
# ==========================================================

def create_indicator(
    color,
    title,
    blinking=False
):

    animation = "none"

    if blinking:

        animation = (
            "stock-red-blink "
            "0.8s infinite"
        )

    return html.Span(

        "●",

        title=title,

        style={

            "fontSize":
                "24px",

            "display":
                "inline-block",

            "textAlign":
                "center",

            "width":
                "100%",

            "lineHeight":
                "1",

            "color":
                color,

            "textShadow":
                f"0 0 8px {color}",

            "animation":
                animation,

            "cursor":
                "default",

        }

    )


# ==========================================================
# STOCK / ALERT INDICATION
# ==========================================================

def create_stock_indication(
    outlet_code,
    tank_id,
    alert_type=None
):

    tank = get_latest_tank_stock(

        outlet_code,

        tank_id

    )

    # ======================================================
    # NO TANK DATA
    # ======================================================

    if not tank:

        return html.Span(

            "⚪",

            title="No tank data",

            style={

                "fontSize":
                    "20px",

                "display":
                    "inline-block",

                "textAlign":
                    "center",

                "width":
                    "100%"

            }

        )

    # ======================================================
    # VALUES
    # ======================================================

    volume = tank.get(
        "volume"
    )

    capacity = tank.get(
        "capacity"
    )

    dead_stock = tank.get(
        "dead_stock"
    )

    min_stock = tank.get(
        "min_stock"
    )

    max_stock = tank.get(
        "max_stock"
    )

    temperature = tank.get(
        "temp"
    )

    # ======================================================
    # HIGH TEMPERATURE
    # ======================================================

    if str(
        alert_type or ""
    ).strip().lower() == "high temperature":

        temp_text = (

            f"{temperature}°C"

            if temperature is not None

            else "High temperature"

        )

        return create_indicator(

            "#dc3545",

            (
                "High Temperature Alert — "
                f"{temp_text}"
            ),

            blinking=True

        )

    # ======================================================
    # VALIDATION
    # ======================================================

    if (

        volume is None

        or dead_stock is None

        or min_stock is None

        or max_stock is None

    ):

        return html.Span(

            "⚪",

            title=(
                "Stock thresholds unavailable"
            ),

            style={

                "fontSize":
                    "20px",

                "display":
                    "inline-block",

                "textAlign":
                    "center",

                "width":
                    "100%"

            }

        )

    # ======================================================
    # FLOAT CONVERSION
    # ======================================================

    try:

        volume = float(
            volume
        )

        dead_stock = float(
            dead_stock
        )

        min_stock = float(
            min_stock
        )

        max_stock = float(
            max_stock
        )

        if capacity is not None:

            capacity = float(
                capacity
            )

    except (
        TypeError,
        ValueError
    ):

        return html.Span(

            "⚪",

            title="Invalid stock values",

            style={

                "fontSize":
                    "20px",

                "display":
                    "inline-block",

                "textAlign":
                    "center",

                "width":
                    "100%"

            }

        )

    # ======================================================
    # DEAD STOCK
    # ======================================================

    if volume <= dead_stock:

        return create_indicator(

            "#dc3545",

            (

                "Dead Stock — "

                f"{volume:.2f} L "

                f"≤ {dead_stock:.2f} L"

            ),

            blinking=True

        )

    # ======================================================
    # MINIMUM STOCK
    # ======================================================

    elif volume <= min_stock:

        return html.Span(

            "●",

            title=(

                "Minimum Stock — "

                f"{volume:.2f} L "

                f"≤ {min_stock:.2f} L"

            ),

            style={

                "fontSize":
                    "24px",

                "display":
                    "inline-block",

                "textAlign":
                    "center",

                "width":
                    "100%",

                "lineHeight":
                    "1",

                "color":
                    "#ffc107",

                "textShadow":
                    "0 0 8px #ffc107",

                "cursor":
                    "default",

            }

        )

    # ======================================================
    # MAXIMUM STOCK
    # ======================================================

    elif volume > max_stock:

        return html.Span(

            "●",

            title=(

                "Above Maximum Stock — "

                f"{volume:.2f} L "

                f"> {max_stock:.2f} L"

            ),

            style={

                "fontSize":
                    "24px",

                "display":
                    "inline-block",

                "textAlign":
                    "center",

                "width":
                    "100%",

                "lineHeight":
                    "1",

                "color":
                    "#ffc107",

                "textShadow":
                    "0 0 8px #ffc107",

                "animation":
                    (
                        "stock-yellow-blink "
                        "0.8s infinite"
                    ),

                "cursor":
                    "default",

            }

        )

    # ======================================================
    # NORMAL STOCK
    # ======================================================

    else:

        return html.Span(

            "●",

            title=(

                "Normal Stock — "

                f"{volume:.2f} L "

                f"(Min: {min_stock:.2f} L, "

                f"Max: {max_stock:.2f} L)"

            ),

            style={

                "fontSize":
                    "24px",

                "display":
                    "inline-block",

                "textAlign":
                    "center",

                "width":
                    "100%",

                "lineHeight":
                    "1",

                "color":
                    "#198754",

                "textShadow":
                    "0 0 8px #198754",

                "cursor":
                    "default",

            }

        )


# ==========================================================
# FILTER ALERTS
# ==========================================================

def filter_alerts(
    alert_data,
    severity="all",
    alert_type="all"
):

    filtered = []

    severity_filter = str(
        severity or "all"
    ).strip().lower()

    alert_type_filter = str(
        alert_type or "all"
    ).strip().lower()

    # ======================================================
    # STOCK ALERT TYPES
    # ======================================================

    stock_alert_types = {

        "minimum stock",

        "maximum stock",

        "dead stock",

    }

    # ======================================================
    # TEMPERATURE ALERT TYPES
    # ======================================================

    temperature_alert_types = {

        "high temperature",

    }

    # ======================================================
    # PROCESS ALERTS
    # ======================================================

    for alert in alert_data:

        alert_severity = str(

            alert.get(
                "severity",
                ""
            )

        ).strip().lower()

        current_alert_type = str(

            alert.get(
                "alert_type",
                ""
            )

        ).strip().lower()

        # ==================================================
        # SEVERITY FILTER
        # ==================================================

        if (

            severity_filter != "all"

            and

            alert_severity != severity_filter

        ):

            continue

        # ==================================================
        # ALERT TYPE FILTER
        # ==================================================

        if alert_type_filter == "stock":

            if (
                current_alert_type
                not in stock_alert_types
            ):

                continue

        elif alert_type_filter == "temperature":

            if (
                current_alert_type
                not in temperature_alert_types
            ):

                continue

        filtered.append(
            alert
        )

    return filtered


# ==========================================================
# CREATE ALERT TABLE ROWS
# ==========================================================

def create_alert_table_rows(
    alert_data
):

    rows = []

    for index, alert in enumerate(
        alert_data
    ):

        # ==================================================
        # SEVERITY
        # ==================================================

        severity = str(

            alert.get(
                "severity",
                ""
            )

        ).strip()

        severity_style = {

            "High": {

                "color":
                    "#dc3545",

                "backgroundColor":
                    "#fff0f0",

            },

            "Medium": {

                "color":
                    "#f59e0b",

                "backgroundColor":
                    "#fff8e8",

            },

            "Low": {

                "color":
                    "#2563eb",

                "backgroundColor":
                    "#eef5ff",

            },

        }.get(

            severity,

            {}

        )

        # ==================================================
        # OUTLET
        # ==================================================

        outlet_code = alert.get(
            "outlet_code",
            ""
        )

        # ==================================================
        # TANK
        # ==================================================

        tank_id = alert.get(
            "tank_id",
            ""
        )

        # ==================================================
        # ALERT TYPE
        # ==================================================

        alert_type = str(

            alert.get(
                "alert_type",
                ""
            )

        ).strip()

        # ==================================================
        # DATE
        # ==================================================

        alert_date = format_alert_date(
            alert
        )

        # ==================================================
        # TIME
        # ==================================================

        alert_time = format_alert_time(
            alert
        )

        # ==================================================
        # ACTION INDICATOR
        # ==================================================

        stock_indicator = (
            create_stock_indication(

                outlet_code,

                tank_id,

                alert_type

            )
        )

        # ==================================================
        # CREATE ROW
        # ==================================================

        rows.append(

            html.Tr(

                [

                    # ======================================
                    # DATE
                    # ======================================

                    html.Td(

                        alert_date

                    ),

                    # ======================================
                    # TIME
                    # ======================================

                    html.Td(

                        alert_time

                    ),

                    # ======================================
                    # OUTLET
                    # ======================================

                    html.Td(

                        outlet_code

                    ),

                    # ======================================
                    # TANK
                    # ======================================

                    html.Td(

                        tank_id

                    ),

                    # ======================================
                    # ALERT TYPE
                    # ======================================

                    html.Td(

                        alert_type

                    ),

                    # ======================================
                    # MESSAGE
                    # ======================================

                    html.Td(

                        alert.get(
                            "message",
                            ""
                        )

                    ),

                    # ======================================
                    # SEVERITY
                    # ======================================

                    html.Td(

                        html.Span(

                            severity,

                            style={

                                **severity_style,

                                "padding":
                                    "5px 10px",

                                "borderRadius":
                                    "15px",

                                "fontSize":
                                    "12px",

                                "fontWeight":
                                    "500",

                            }

                        )

                    ),

                    # ======================================
                    # ACTION
                    # ======================================

                    html.Td(

                        stock_indicator,

                        style={

                            "textAlign":
                                "center",

                            "verticalAlign":
                                "middle",

                            "width":
                                "80px",

                        }

                    ),

                ]

            )

        )

    return rows


# ==========================================================
# FILTER DROPDOWNS
# ==========================================================

def create_alert_filters():

    # ======================================================
    # SEVERITY DROPDOWN
    # ======================================================

    severity_dropdown = dbc.Col(

        [

            html.Label(

                "Severity",

                style={

                    "fontSize":
                        "13px",

                    "fontWeight":
                        "600",

                    "marginBottom":
                        "6px",

                    "color":
                        "#374151",

                }

            ),

            dcc.Dropdown(

                id="alert-severity-filter",

                options=[

                    {

                        "label":
                            "All Severities",

                        "value":
                            "all"

                    },

                    {

                        "label":
                            "High",

                        "value":
                            "High"

                    },

                    {

                        "label":
                            "Medium",

                        "value":
                            "Medium"

                    },

                    {

                        "label":
                            "Low",

                        "value":
                            "Low"

                    },

                ],

                value="all",

                clearable=False,

                searchable=False,

                style={

                    "fontSize":
                        "13px",

                }

            )

        ],

        width=12,

        sm=6,

        md=4,

        lg=3

    )

    # ======================================================
    # ALERT TYPE DROPDOWN
    # ======================================================

    alert_type_dropdown = dbc.Col(

        [

            html.Label(

                "Alert Type",

                style={

                    "fontSize":
                        "13px",

                    "fontWeight":
                        "600",

                    "marginBottom":
                        "6px",

                    "color":
                        "#374151",

                }

            ),

            dcc.Dropdown(

                id="alert-type-filter",

                options=[

                    {

                        "label":
                            "All Alerts",

                        "value":
                            "all"

                    },

                    {

                        "label":
                            "Stock Alerts",

                        "value":
                            "stock"

                    },

                    {

                        "label":
                            "Temperature Alerts",

                        "value":
                            "temperature"

                    },

                ],

                value="all",

                clearable=False,

                searchable=False,

                style={

                    "fontSize":
                        "13px",

                }

            )

        ],

        width=12,

        sm=6,

        md=4,

        lg=3

    )

    # ======================================================
    # FILTER ROW
    # ======================================================

    return dbc.Row(

        [

            severity_dropdown,

            alert_type_dropdown,

        ],

        className="g-3 mb-3"

    )


# ==========================================================
# RECENT ALERTS TABLE
# ==========================================================

def create_alerts_table():

    alert_data = (

        fetch_alerts()

        or []

    )

    # ======================================================
    # TABLE HEADER
    # ======================================================

    header = html.Thead(

        html.Tr(

            [

                # ==========================================
                # DATE
                # ==========================================

                html.Th(
                    "DATE"
                ),

                # ==========================================
                # TIME
                # ==========================================

                html.Th(
                    "TIME"
                ),

                # ==========================================
                # OUTLET CODE
                # ==========================================

                html.Th(
                    "OUTLET CODE"
                ),

                # ==========================================
                # TANK ID
                # ==========================================

                html.Th(
                    "TANK ID"
                ),

                # ==========================================
                # ALERT TYPE
                # ==========================================

                html.Th(
                    "ALERT TYPE"
                ),

                # ==========================================
                # MESSAGE
                # ==========================================

                html.Th(
                    "MESSAGE"
                ),

                # ==========================================
                # SEVERITY
                # ==========================================

                html.Th(
                    "SEVERITY"
                ),

                # ==========================================
                # ACTION
                # ==========================================

                html.Th(
                    "ACTION"
                ),

            ]

        )

    )

    # ======================================================
    # INITIAL ROWS
    # ======================================================

    rows = create_alert_table_rows(

        alert_data

    )

    # ======================================================
    # TABLE
    # ======================================================

    table = dbc.Table(

        [

            header,

            html.Tbody(

                rows,

                id="alerts-table-body"

            )

        ],

        bordered=False,

        hover=True,

        responsive=True,

        className="mb-0",

        style={

            "fontSize":
                "13px",

            "verticalAlign":
                "middle",

        }

    )

    # ======================================================
    # ALERT CARD
    # ======================================================

    return dbc.Card(

        dbc.CardBody(

            [

                html.H5(

                    "Recent Alerts",

                    className="mb-3"

                ),

                create_alert_filters(),

                table

            ]

        ),

        style={

            "border":
                "1px solid #e5e7eb",

            "borderRadius":
                "12px",

        },

        className="shadow-sm"

    )


# ==========================================================
# ALERT TABLE REFRESH + FILTER CALLBACK
# ==========================================================

@callback(

    Output(
        "alerts-table-body",
        "children"
    ),

    Input(
        "alerts-refresh-interval",
        "n_intervals"
    ),

    Input(
        "alert-severity-filter",
        "value"
    ),

    Input(
        "alert-type-filter",
        "value"
    ),

)

def refresh_alerts_table(

    n_intervals,

    severity,

    alert_type

):

    alert_data = (

        fetch_alerts()

        or []

    )

    # ======================================================
    # APPLY FILTERS
    # ======================================================

    filtered_alerts = filter_alerts(

        alert_data,

        severity,

        alert_type

    )

    # ======================================================
    # CREATE UPDATED ROWS
    # ======================================================

    return create_alert_table_rows(

        filtered_alerts

    )


# ==========================================================
# ALERT SEVERITY DATA
# ==========================================================

def get_alert_severity_data():

    alerts = (

        fetch_alerts(

            severity="all",

            status="all"

        )

        or []

    )

    high = 0

    medium = 0

    low = 0

    for alert in alerts:

        severity = str(

            alert.get(
                "severity",
                ""
            )

        ).strip().lower()

        if severity == "high":

            high += 1

        elif severity == "medium":

            medium += 1

        elif severity == "low":

            low += 1

    return {

        "high":
            high,

        "medium":
            medium,

        "low":
            low,

        "total":
            (
                high
                +
                medium
                +
                low
            )

    }


# ==========================================================
# RIGHT SIDE ALERT PANEL
# ==========================================================

def create_alert_side_panel():

    severity_card = (

        create_alert_severity_card()

    )

    return html.Div(

        [

            severity_card,

            html.Div(

                create_alert_quick_actions(),

                className="mt-3"

            ),

            html.Div(

                create_alert_rules_card(),

                className="mt-3"

            ),

        ]

    )


# ==========================================================
# COMPLETE ALERTS PAGE
# ==========================================================

def create_alerts_page():

    return html.Div(

        [

            # ==================================================
            # REFRESH TIMER
            # ==================================================

            dcc.Interval(

                id="alerts-refresh-interval",

                interval=5000,

                n_intervals=0

            ),

            # ==================================================
            # PAGE TITLE
            # ==================================================

            html.Div(

                [

                    html.H3(

                        "Alerts",

                        className="mb-1"

                    ),

                    html.P(

                        "Monitor and manage all system alerts",

                        className="text-muted mb-4"

                    ),

                ],

                style={

                    "marginLeft":
                        "5px"

                }

            ),

            # ==================================================
            # KPI CARDS
            # ==================================================

            html.Div(

                create_alert_kpi_cards(),

                id="alerts-kpi-cards"

            ),

            # ==================================================
            # MAIN CONTENT
            # ==================================================

            dbc.Row(

                [

                    # ==========================================
                    # LEFT
                    # ==========================================

                    dbc.Col(

                        create_alerts_table(),

                        width=12,

                        xl=9,

                        className="mb-4"

                    ),

                    # ==========================================
                    # RIGHT
                    # ==========================================

                    dbc.Col(

                        create_alert_side_panel(),

                        width=12,

                        xl=3,

                        className="mb-4"

                    ),

                ],

                className="g-3"

            ),

        ],

        style={

            "marginLeft":
                "30px"

        }

    )


# ==========================================================
# DASH PAGE LAYOUT
# ==========================================================

layout = create_alerts_page()