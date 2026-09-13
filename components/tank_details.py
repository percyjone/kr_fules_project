from dash import html, dcc

import plotly.graph_objects as go

import dash_bootstrap_components as dbc

from config.settings import COLORS

from database.db import fetch_alerts





# ==========================================================
# TREND CHART
# ==========================================================

def make_trend_chart(
    history,
    field,
    label,
    color,
    period
):

    # ======================================================
    # NO DATA
    # ======================================================

    if not history:

        fig = go.Figure()

        if period == "day":

            x_title = "Time"

        elif period == "month":

            x_title = "Date / Time"

        elif period == "year":

            x_title = "Date"

        else:

            x_title = "Time"

        fig.update_layout(

            margin=dict(
                l=40,
                r=10,
                t=5,
                b=35
            ),

            height=210,

            showlegend=False,

            plot_bgcolor="white",

            paper_bgcolor="white",

            xaxis=dict(

                title=x_title,

                showgrid=False,

                showline=False,

                showticklabels=True,

            ),

            yaxis=dict(

                title=label,

                showgrid=True,

                gridcolor="#e6e8f0",

                showline=False,

                showticklabels=True,

                rangemode="tozero",

            ),

        )

        return html.Div(

            [

                html.Div(

                    [

                        html.I(

                            className=(

                                "fas fa-temperature-high"

                                if field == "temp"

                                else

                                "fas fa-tint"

                            ),

                            style={

                                "color": color,

                                "fontSize": "18px",

                                "marginRight": "8px"

                            }

                        ),

                        html.Span(

                            label,

                            style={

                                "fontSize": "15px",

                                "fontWeight": "600",

                                "color":
                                    COLORS["text_dark"]

                            }

                        )

                    ],

                    style={

                        "display": "flex",

                        "alignItems": "center",

                        "marginBottom": "2px"

                    }

                ),

                dcc.Graph(

                    figure=fig,

                    config={

                        "displayModeBar": False,

                        "responsive": True

                    },

                    style={

                        "height": "210px"

                    }

                )

            ]

        )


    # ======================================================
    # X DATA
    # ======================================================

    valid_rows = [

        r

        for r in history

        if r.get(field) is not None

    ]


    if period == "day":

        x = [

            f"{r['date']} {r['time']}"

            for r in valid_rows

        ]

    elif period == "month":

        x = [

            f"{r['date']} {int(r['hour']):02d}:00"

            for r in valid_rows

        ]

    elif period == "year":

        x = [

            str(r["date"])

            for r in valid_rows

        ]

    else:

        x = []


    # ======================================================
    # Y DATA
    # ======================================================

    y = [

        float(r[field])

        for r in valid_rows

    ]


    # ======================================================
    # GRAPH
    # ======================================================

    fig = go.Figure(

        go.Scatter(

            x=x,

            y=y,

            mode="lines+markers",

            line=dict(

                color=color,

                width=2.5

            ),

            marker=dict(

                size=6,

                color=color

            ),

            name=label

        )

    )


    fig.update_layout(

        margin=dict(

            l=40,

            r=10,

            t=5,

            b=30

        ),

        height=210,

        showlegend=False,

        plot_bgcolor="white",

        paper_bgcolor="white",

        hovermode="x unified",

        xaxis=dict(

            showgrid=False,

            showline=False,

            zeroline=False

        ),

        yaxis=dict(

            gridcolor="#e6e8f0",

            gridwidth=1,

            showline=False,

            zeroline=False,

            rangemode="tozero"

        ),

    )


    return html.Div(

        [

            # --------------------------------------------------
            # CHART TITLE
            # --------------------------------------------------

            html.Div(

                [

                    html.Div(

                        [

                            html.I(

                                className=(

                                    "fas fa-temperature-high"

                                    if field == "temp"

                                    else

                                    "fas fa-tint"

                                ),

                                style={

                                    "color": color,

                                    "fontSize": "18px",

                                    "marginRight": "8px"

                                }

                            ),

                            html.Span(

                                label,

                                style={

                                    "fontSize": "15px",

                                    "fontWeight": "600",

                                    "color":
                                        COLORS["text_dark"]

                                }

                            )

                        ],

                        style={

                            "display": "flex",

                            "alignItems": "center"

                        }

                    )

                ],

                style={

                    "marginBottom": "2px"

                }

            ),

            # --------------------------------------------------
            # GRAPH
            # --------------------------------------------------

            dcc.Graph(

                figure=fig,

                config={

                    "displayModeBar": False,

                    "responsive": True

                },

                style={

                    "height": "210px"

                }

            )

        ]

    )


# ==========================================================
# RECENT ALERTS FOR SELECTED TANK
# ==========================================================

def create_tank_alerts(

    outlet_code,

    tank_id

):

    # ======================================================
    # FETCH ALL ALERTS
    # ======================================================

    alerts = fetch_alerts(

        severity="all",

        status="all"

    ) or []


    # ======================================================
    # FILTER ALERTS FOR THIS TANK
    # ======================================================

    tank_alerts = [

        alert

        for alert in alerts

        if (

            str(
                alert.get("outlet_code")
            ).strip()

            ==

            str(outlet_code).strip()

            and

            str(
                alert.get("tank_id")
            ).strip()

            ==

            str(tank_id).strip()

        )

    ]


    # ======================================================
    # NO ALERTS
    # ======================================================

    if not tank_alerts:

        return html.Div(

            [

                html.Span(

                    # "✅",
                    className="fas fa-check-circle",

                    style={
                        "color": "#087443",
                        "marginRight": "7px",

                        "fontSize": "14px"

                    }

                ),

                "No alerts — all systems normal"

            ],

            style={

                "color":
                    COLORS["text_muted"],

                "fontSize":
                    "14px"

            }

        )


    # ======================================================
    # ALERT ITEMS
    # ======================================================

    alert_items = []


    for alert in tank_alerts:

        severity = str(

            alert.get(

                "severity",

                ""

            )

        ).strip()


        status = str(

            alert.get(

                "status",

                ""

            )

        ).strip()


        message = str(

            alert.get(

                "message",

                ""

            )

        )


        alert_type = str(

            alert.get(

                "alert_type",

                ""

            )

        )


        alert_time = alert.get(

            "time",

            ""

        )


        # ==================================================
        # SEVERITY STYLE
        # ==================================================

        severity_style = {

            "High": {

                "color":
                    "#dc3545",

                "backgroundColor":
                    "#fff0f0"

            },

            "Medium": {

                "color":
                    "#fd7e14",

                "backgroundColor":
                    "#fff7ed"

            },

            "Low": {

                "color":
                    "#198754",

                "backgroundColor":
                    "#eaf8f0"

            }

        }.get(

            severity,

            {

                "color":
                    COLORS["text_muted"],

                "backgroundColor":
                    "#f8f9fa"

            }

        )


        # ==================================================
        # ALERT ITEM
        # ==================================================

        alert_items.append(

            html.Div(

                [

                    # --------------------------------------
                    # SEVERITY + TYPE
                    # --------------------------------------

                    html.Div(

                        [

                            html.Span(

                                severity,

                                style={

                                    **severity_style,

                                    "padding":
                                        "4px 9px",

                                    "borderRadius":
                                        "10px",

                                    "fontSize":
                                        "12px",

                                    "fontWeight":
                                        "600",

                                    "marginRight":
                                        "9px"

                                }

                            ),

                            html.Span(

                                alert_type,

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

                            )

                        ],

                        style={

                            "display": "flex",

                            "alignItems": "center",

                            "marginBottom": "5px"

                        }

                    ),

                    # --------------------------------------
                    # MESSAGE
                    # --------------------------------------

                    html.Div(

                        message,

                        style={

                            "fontSize":
                                "14px",

                            "lineHeight":
                                "1.4",

                            "color":
                                COLORS[
                                    "text_muted"
                                ]

                        }

                    ),

                    # --------------------------------------
                    # TIME + STATUS
                    # --------------------------------------

                    html.Div(

                        [

                            str(alert_time),

                            " • ",

                            status

                        ],

                        style={

                            "fontSize":
                                "12px",

                            "color":
                                COLORS[
                                    "text_muted"
                                ],

                            "marginTop":
                                "4px"

                        }

                    )

                ],

                style={

                    "padding":
                        "11px 0",

                    "borderBottom":
                        f"1px solid "
                        f"{COLORS['border']}"

                }

            )

        )


    return html.Div(

        alert_items

    )


# ==========================================================
# TANK DETAIL CONTENT
#
# This part is refreshed by tank_callbacks.py.
#
# The dropdown is NOT inside this function.
# ==========================================================

def create_tank_detail_content(

    selected,

    history,

    period="day"

):

    # ======================================================
    # NO SELECTED TANK
    # ======================================================

    if not selected:

        return html.Div()


    # ======================================================
    # TANK INFORMATION
    # ======================================================

    outlet_code = selected["outlet_code"]

    tank_id = selected["tank_id"]


    # ======================================================
    # DATA
    # ======================================================

    if history:

        latest = history[-1]

        temperature = latest.get(

            "temp",

            "-"

        )

        volume = latest.get(

            "volume",

            "-"

        )


        # --------------------------------------------------
        # LAST UPDATED
        # --------------------------------------------------

        if "time" in latest:

            last_updated = (

                f'{latest["date"]} '

                f'{latest["time"]}'

            )

        elif "hour" in latest:

            last_updated = (

                f'{latest["date"]} '

                f'{int(latest["hour"]):02d}:00'

            )

        else:

            last_updated = str(

                latest.get(

                    "date",

                    "-"

                )

            )

    else:

        latest = None

        temperature = "-"

        volume = "-"

        last_updated = "-"


  # ======================================================
# VOLUME / CAPACITY
# ======================================================

    # ======================================================
    # VOLUME / CAPACITY
    # ======================================================

    if latest:

        volume_value = float(
            latest.get("volume", 0) or 0
        )

        tank_capacity = float(
            latest.get("capacity", 0) or 0
        )

    else:

        volume_value = 0

        tank_capacity = 0


    if tank_capacity > 0:

        capacity_percentage = (

            volume_value
            /
            tank_capacity

        ) * 100

    else:

        capacity_percentage = 0


    capacity_percentage = max(

        0,

        min(

            capacity_percentage,

            100

        )

    )
    # ======================================================
    # TANK GAUGE
    # ======================================================

    if latest:

        gauge_text = (

            f"{volume_value:.0f} L"

        )

        gauge_percentage_text = (

            f"{capacity_percentage:.0f}% Capacity"

        )

        gauge_background = (

            "linear-gradient("

            "to top, "

            f"{COLORS['blue']} "

            f"{capacity_percentage}%, "

            "#dce8fb "

            f"{capacity_percentage}%"

            ")"

        )

        gauge_text_color = "#ffffff"

    else:

        gauge_text = "-"

        gauge_percentage_text = (

            "0% Capacity"

        )

        gauge_background = (

            "linear-gradient("

            "to top, "

            "#dce8fb 0%, "

            "#dce8fb 100%"

            ")"

        )

        gauge_text_color = COLORS["text_muted"]


    # ======================================================
    # TANK GAUGE
    # ======================================================

    gauge = html.Div(

        [

            html.Div(

                gauge_text,

                style={

                    "position":
                        "absolute",

                    "bottom":
                        "15px",

                    "left":
                        "0",

                    "width":
                        "100%",

                    "textAlign":
                        "center",

                    "color":
                        gauge_text_color,

                    "fontWeight":
                        "700",

                    "fontSize":
                        "22px",

                    "zIndex":
                        "2"

                }

            )

        ],

        style={

            "position":
                "relative",

            "width":
                "100%",

            "maxWidth":
                "145px",

            "height":
                "220px",

            "margin":
                "0 auto",

            "border":
                "3px solid #d9e1ef",

            "borderRadius":
                "18px",

            "background":
                gauge_background,

            "overflow":
                "hidden",

            "boxShadow":
                "0 2px 8px rgba(0,0,0,0.04)"

        }

    )


    # ======================================================
    # CAPACITY PILL
    # ======================================================

    capacity_pill = html.Div(

        [

            html.I(

                className="fas fa-tint",

                style={

                    "color":
                        "#087443",

                    "fontSize":
                        "16px",

                    "marginRight":
                        "7px"

                }

            ),

            html.Span(

                gauge_percentage_text,

                style={

                    "color":
                        "#087443",

                    "fontWeight":
                        "600",

                    "fontSize":
                        "14px"

                }

            )

        ],

        style={

            "display":
                "flex",

            "alignItems":
                "center",

            "justifyContent":
                "center",

            "backgroundColor":
                "#eaf7f0",

            "borderRadius":
                "25px",

            "padding":
                "7px 14px",

            "margin":
                "10px auto 0",

            "width":
                "fit-content",

            "minWidth":
                "150px"

        }

    )


    # ======================================================
    # STAT CARD HELPER
    # ======================================================

    def stat_card(

        icon_class,

        icon_color,

        value,

        label

    ):

        return html.Div(

            [

                # ------------------------------------------
                # ICON
                # ------------------------------------------

                html.Div(

                    html.I(

                        className=icon_class,

                        style={

                            "color":
                                icon_color,

                            "fontSize":
                                "22px"

                        }

                    ),

                    style={

                        "width":
                            "40px",

                        "height":
                            "40px",

                        "borderRadius":
                            "50%",

                        "backgroundColor":
                            "#eef7f3",

                        "display":
                            "flex",

                        "alignItems":
                            "center",

                        "justifyContent":
                            "center",

                        "flexShrink":
                            "0"

                    }

                ),

                # ------------------------------------------
                # TEXT
                # ------------------------------------------

                html.Div(

                    [

                        html.Div(

                            value,

                            style={

                                "fontSize":
                                    "16px",

                                "fontWeight":
                                    "700",

                                "color":
                                    COLORS[
                                        "text_dark"
                                    ],

                                "lineHeight":
                                    "1.2",

                                "marginBottom":
                                    "3px"

                            }

                        ),

                        html.Div(

                            label,

                            style={

                                "fontSize":
                                    "12px",

                                "color":
                                    COLORS[
                                        "text_muted"
                                    ]

                            }

                        )

                    ],

                    style={

                        "marginLeft":
                            "12px"

                    }

                )

            ],

            style={

                "display":
                    "flex",

                "alignItems":
                    "center",

                "backgroundColor":
                    "#ffffff",

                "border":
                    f"1px solid "
                    f"{COLORS['border']}",

                "borderLeft":
                    "3px solid #209849",

                "borderRadius":
                    "12px",

                "padding":
                    "12px 14px",

                "minHeight":
                    "64px",

                "boxShadow":
                    "0 3px 12px rgba(0,0,0,0.035)",

                "marginBottom":
                    "10px"

            }

        )


    # ======================================================
    # TEMPERATURE VALUE
    # ======================================================

    if temperature != "-":

        temperature_text = (

            f"{float(temperature):g} °C"

        )

    else:

        temperature_text = "-"


    # ======================================================
    # VOLUME VALUE
    # ======================================================

    if volume != "-":

        volume_text = (

            f"{float(volume):g} L"

        )

    else:

        volume_text = "-"


    # ======================================================
    # LAST UPDATED CARD
    # ======================================================

    last_updated_card = html.Div(

        [

            html.Div(

                html.I(

                    className="far fa-clock",

                    style={

                        "color":
                            "#087443",

                        "fontSize":
                            "22px"

                    }

                ),

                style={

                    "width":
                        "40px",

                    "height":
                        "40px",

                    "borderRadius":
                        "50%",

                    "backgroundColor":
                        "#eef7f3",

                    "display":
                        "flex",

                    "alignItems":
                        "center",

                    "justifyContent":
                        "center",

                    "flexShrink":
                        "0"

                }

            ),

            html.Div(

                [

                    html.Div(

                        last_updated,

                        style={

                            "fontSize":
                                "15px",

                            "fontWeight":
                                "700",

                            "color":
                                COLORS[
                                    "text_dark"
                                ],

                            "lineHeight":
                                "1.2",

                            "marginBottom":
                                "5px"

                        }

                    ),

                    html.Div(

                        "Last Updated",

                        style={

                            "fontSize":
                                "12px",

                            "color":
                                COLORS[
                                    "text_muted"
                                ]

                        }

                    )

                ],

                style={

                    "marginLeft":
                        "12px"

                }

            )

        ],

        style={

            "display":
                "flex",

            "alignItems":
                "center",

            "backgroundColor":
                "#ffffff",

            "border":
                f"1px solid "
                f"{COLORS['border']}",

            "borderLeft":
                "3px solid #209849",

            "borderRadius":
                "12px",

            "padding":
                "12px 14px",

            "minHeight":
                "64px",

            "boxShadow":
                "0 3px 12px rgba(0,0,0,0.035)"

        }

    )


    # ======================================================
    # STATS COLUMN
    # ======================================================

    stats = html.Div(

        [

            stat_card(

                "fas fa-temperature-high",

                "#087443",

                temperature_text,

                "Temperature"

            ),

            stat_card(

                "fas fa-tint",

                "#2F80ED",

                volume_text,

                "Volume"

            ),

            last_updated_card

        ],

        style={

            "width":
                "100%"

        }

    )


    # ======================================================
    # TEMPERATURE CHART CARD
    # ======================================================

    temperature_chart = dbc.Card(

        dbc.CardBody(

            make_trend_chart(

                history,

                "temp",

                "Temperature (°C)",

                COLORS["green"],

                period

            ),

            style={

                "padding":
                    "12px 12px 5px"

            }

        ),

        style={

            "border":
                f"1px solid "
                f"{COLORS['border']}",

            "borderRadius":
                "16px",

            "height":
                "100%",

            "boxShadow":
                "0 3px 12px rgba(0,0,0,0.035)"

        }

    )


    # ======================================================
    # VOLUME CHART CARD
    # ======================================================

    volume_chart = dbc.Card(

        dbc.CardBody(

            make_trend_chart(

                history,

                "volume",

                "Volume (L)",

                COLORS["blue"],

                period

            ),

            style={

                "padding":
                    "12px 12px 5px"

            }

        ),

        style={

            "border":
                f"1px solid "
                f"{COLORS['border']}",

            "borderRadius":
                "16px",

            "height":
                "100%",

            "boxShadow":
                "0 3px 12px rgba(0,0,0,0.035)"

        }

    )


    # ======================================================
    # MAIN TANK DETAIL ROW
    # ======================================================

    main_row = dbc.Row(

        [

            # --------------------------------------------------
            # GAUGE
            # --------------------------------------------------

            dbc.Col(

                html.Div(

                    [

                        gauge,

                        capacity_pill

                    ],

                    style={

                        "padding":
                            "3px 0"

                    }

                ),

                xs=12,

                sm=6,

                lg=2,

                className="mb-2 mb-lg-0"

            ),

            # --------------------------------------------------
            # STATS
            # --------------------------------------------------

            dbc.Col(

                stats,

                xs=12,

                sm=6,

                lg=2,

                className="mb-2 mb-lg-0"

            ),

            # --------------------------------------------------
            # TEMPERATURE
            # --------------------------------------------------

            dbc.Col(

                temperature_chart,

                xs=12,

                lg=4,

                className="mb-2 mb-lg-0"

            ),

            # --------------------------------------------------
            # VOLUME
            # --------------------------------------------------

            dbc.Col(

                volume_chart,

                xs=12,

                lg=4,

                className="mb-2 mb-lg-0"

            )

        ],

        className="g-2"

    )


    return main_row


# ==========================================================
# CREATE TANK DETAIL PANEL
# ==========================================================

def create_tank_detail_panel(

    selected,

    period="day"

):

    # ======================================================
    # NO SELECTED TANK
    # ======================================================

    if not selected:

        return html.Div()


    # ======================================================
    # TANK INFORMATION
    # ======================================================

    outlet_code = selected["outlet_code"]

    tank_id = selected["tank_id"]


    # ======================================================
    # PERIOD DROPDOWN
    # ======================================================

    period_dropdown = dbc.Select(

        id="tank-time-filter",

        options=[

            {

                "label":
                    "Day",

                "value":
                    "day"

            },

            {

                "label":
                    "Month",

                "value":
                    "month"

            },

            {

                "label":
                    "Year",

                "value":
                    "year"

            }

        ],

        value=period,

        size="sm",

        style={

            "width":
                "125px",

            "height":
                "40px",

            "border":
                "1px solid #e2e7ef",

            "borderRadius":
                "10px",

            "fontSize":
                "15px",

            "fontWeight":
                "500",

            "color":
                COLORS["text_dark"],

            "backgroundColor":
                "#ffffff",

            "paddingLeft":
                "14px"

        }

    )


    # ======================================================
    # DETAIL CARD
    # ======================================================

    detail_card = dbc.Card(

        dbc.CardBody(

            [

                # ------------------------------------------------
                # HEADER
                # ------------------------------------------------

                dbc.Row(

                    [

                        dbc.Col(

                            html.H4(

                                f"Tank Details - "
                                f"{outlet_code} "
                                f"(Tank {tank_id})",

                                style={

                                    "fontSize":
                                        "22px",

                                    "fontWeight":
                                        "700",

                                    "color":
                                        COLORS[
                                            "text_dark"
                                        ],

                                    "margin":
                                        "0"

                                }

                            ),

                            xs=12,

                            md="auto"

                        ),

                        # ----------------------------------------
                        # PERIOD DROPDOWN
                        # ----------------------------------------

                        dbc.Col(

                            period_dropdown,

                            xs=12,

                            md="auto",

                            className="ms-md-auto mt-2 mt-md-0"

                        )

                    ],

                    className=(

                        "align-items-center "

                        "mb-3"

                    )

                ),

                # ------------------------------------------------
                # REFRESHABLE CONTENT
                # ------------------------------------------------

                html.Div(

                    id="tank-detail-content"

                )

            ],

            style={

                "padding":
                    "16px 18px 18px"

            }

        ),

        style={

            "border":
                "1px solid #edf0f5",

            "borderRadius":
                "18px",

            "backgroundColor":
                "#ffffff",

            "boxShadow":
                "0 3px 15px rgba(0,0,0,0.035)"

        },

        className="mb-3"

    )


    # ======================================================
    # OUTLET INFORMATION CARD
    # ======================================================

    info_card = dbc.Card(

        dbc.CardBody(

            [

                # ----------------------------------------------
                # TITLE
                # ----------------------------------------------

                html.Div(
                        [
                            html.I(
                                className="fas fa-shop",
                                style={
                                    "color": "#087443",
                                    "fontSize": "18px",
                                    "marginRight": "8px",
                                },
                            ),

                            html.Span(
                                "Outlet Information",
                                style={
                                     "fontSize": "19px",
                                        "fontWeight": "600",
                                        "color": COLORS["text_dark"],
                                },
                            ),
                        ],

                        className="mb-3",

                        style={
                            "display": "flex",
                            "alignItems": "center",
                        },
                    ),

                # ----------------------------------------------
                # OUTLET / LOCATION
                # ----------------------------------------------

                dbc.Row(

                    [

                        dbc.Col(
                                    html.Div(
                                        [
                                            html.I(
                                                className="fas fa-map-marker-alt",
                                                style={
                                                    "color": "#087443",
                                                    "fontSize": "16px",
                                                    "marginRight": "8px"
                                                }
                                            ),
                                            html.Span(
                                                "Outlet / Location"
                                            )
                                        ],
                                        style={
                                            "display": "flex",
                                            "alignItems": "center",
                                            "fontSize": "15px",
                                            "color": COLORS["text_muted"],
                                            "fontWeight": "500"
                                        }
                                    )
                                ),

                        dbc.Col(

                            outlet_code,

                            className="text-end",

                            style={

                                "fontSize":
                                    "16px",

                                "fontWeight":
                                    "600",

                                "color":
                                    COLORS["text_dark"]

                            }

                        )

                    ],

                    className="mb-3"

                ),

                # ----------------------------------------------
                # OUTLET CODE
                # ----------------------------------------------

                dbc.Row(

                    [

                        dbc.Col(
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-tag",
                                        style={
                                            "color": "#087443",
                                            "fontSize": "16px",
                                            "marginRight": "8px"
                                        }
                                    ),
                                    html.Span(
                                        "Outlet Code"
                                    )
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "fontSize": "15px",
                                    "color": COLORS["text_muted"],
                                    "fontWeight": "500"
                                }
                            )
                        ),

                        dbc.Col(

                            outlet_code,

                            className="text-end",

                            style={

                                "fontSize":
                                    "16px",

                                "fontWeight":
                                    "600",

                                "color":
                                    COLORS["text_dark"]

                            }

                        )

                    ],

                    className="mb-3"

                ),

                # ----------------------------------------------
                # TANK ID
                # ----------------------------------------------

                dbc.Row(

                    [

                        dbc.Col(
                                html.Div(
                                    [
                                        html.I(
                                            className="fas fa-layer-group",
                                            style={
                                                "color": "#087443",
                                                "fontSize": "16px",
                                                "marginRight": "8px"
                                            }
                                        ),
                                        html.Span(
                                            "Tank ID"
                                        )
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "fontSize": "15px",
                                        "color": COLORS["text_muted"],
                                        "fontWeight": "500"
                                    }
                                )
                            ),

                        dbc.Col(

                            str(tank_id),

                            className="text-end",

                            style={

                                "fontSize":
                                    "16px",

                                "fontWeight":
                                    "600",

                                "color":
                                    COLORS["text_dark"]

                            }

                        )

                    ]

                )

            ],

            style={

                "padding":
                    "24px"

            }

        ),

        style={

            "border":
                f"1px solid "
                f"{COLORS['border']}",

            "borderRadius":
                "12px",

            "height":
                "fit-content"

        },

        className="shadow-sm"

    )


    # ======================================================
    # RECENT ALERTS
    # ======================================================

    alerts_content = create_tank_alerts(

        outlet_code,

        tank_id

    )


    # ======================================================
    # ALERT CARD
    # ======================================================

    alerts_card = dbc.Card(

        dbc.CardBody(

            [

                # ----------------------------------------------
                # ALERT HEADER
                # ----------------------------------------------

                dbc.Row(

                    [

                        dbc.Col(
                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className="fas fa-bell",
                                            style={
                                                "color": "#087443",
                                                "fontSize": "18px",
                                                "marginRight": "8px",
                                            },
                                        ),
                                        style={
                                             "fontSize": "19px",
                                            "fontWeight": "600",
                                            "color": COLORS["text_dark"],
                                        },
                                    ),

                                    html.H6(
                                        "Recent Alerts",
                                        className="mb-0",
                                        style={
                                            "fontSize": "19px",
                                            "fontWeight": "600",
                                            "color": COLORS["text_dark"],
                                            "marginLeft": "12px",
                                        },
                                    ),
                                ],

                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                },
                            ),

                            width="auto",
                        ),

                        dbc.Col(

                            dcc.Link(

                                "View all",

                                href="/alerts",

                                style={

                                    "color":
                                        COLORS["green"],

                                    "fontSize":
                                        "14px",

                                    "fontWeight":
                                        "500",

                                    "textDecoration":
                                        "none",

                                    "cursor":
                                        "pointer"

                                }

                            ),

                            width="auto",

                            className="ms-auto"

                        )

                    ],

                    className="align-items-center mb-3"

                ),

                # ----------------------------------------------
                # ALERT CONTENT
                # ----------------------------------------------

                html.Div(

                    alerts_content,

                    style={

                        "maxHeight":
                            "135px",

                        "overflowY":
                            "auto",

                        "paddingRight":
                            "8px"

                    }

                )

            ],

            style={

                "padding":
                    "24px"

            }

        ),

        style={

            "border":
                f"1px solid "
                f"{COLORS['border']}",

            "borderRadius":
                "12px"

        },

        className="shadow-sm"

    )


    # ======================================================
    # RETURN
    # ======================================================

    return html.Div(

        [

            # --------------------------------------------------
            # MAIN DETAIL CARD
            # --------------------------------------------------

            detail_card,

            # --------------------------------------------------
            # INFORMATION + ALERTS
            # --------------------------------------------------

            dbc.Row(

                [

                    dbc.Col(

                        info_card,

                        width=12,

                        lg=6,

                        className="mb-3"

                    ),

                    dbc.Col(

                        alerts_card,

                        width=12,

                        lg=6,

                        className="mb-3"

                    )

                ],

                className="g-2"

            )

        ]

    )