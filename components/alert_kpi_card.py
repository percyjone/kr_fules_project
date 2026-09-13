import dash_bootstrap_components as dbc

from dash import html

from config.settings import COLORS


# ==========================================================
# ALERT KPI CARD
# ==========================================================

def alert_kpi_card(
    icon,
    title,
    value,
    subtitle,
    color_key,
    value_id=None,
    subtitle_id=None
):

    # ======================================================
    # VALUE PROPERTIES
    # ======================================================

    value_props = {
        "className": "mb-1",
        "style": {
            "fontWeight": "700"
        }
    }

    # Only add id when an actual ID is supplied
    if value_id is not None:
        value_props["id"] = value_id

    # ======================================================
    # VALUE
    # ======================================================

    value_component = html.H4(
        value,
        **value_props
    )

    # ======================================================
    # SUBTITLE PROPERTIES
    # ======================================================

    subtitle_props = {
        "style": {
            "fontSize": "12px",
            "color": "#6b7280",
            "marginTop": "4px"
        }
    }

    # Only add id when an actual ID is supplied
    if subtitle_id is not None:
        subtitle_props["id"] = subtitle_id

    # ======================================================
    # SUBTITLE
    # ======================================================

    subtitle_component = html.Div(
        subtitle,
        **subtitle_props
    )

    # ======================================================
    # CARD
    # ======================================================

    return dbc.Card(

        dbc.CardBody(

            [

                # ==================================================
                # ICON
                # ==================================================

                html.Div(

                    icon,

                    style={

                        "width": "45px",

                        "height": "45px",

                        "backgroundColor":
                            COLORS[f"{color_key}_tint"],

                        "color":
                            COLORS[color_key],

                        "borderRadius":
                            "12px",

                        "display":
                            "flex",

                        "alignItems":
                            "center",

                        "justifyContent":
                            "center",

                        "fontSize":
                            "22px",

                        "marginBottom":
                            "10px"

                    }

                ),

                # ==================================================
                # VALUE
                # ==================================================

                value_component,

                # ==================================================
                # TITLE
                # ==================================================

                html.Div(

                    title,

                    style={

                        "fontSize":
                            "14px",

                        "color":
                            "#374151"

                    }

                ),

                # ==================================================
                # SUBTITLE
                # ==================================================

                subtitle_component,

            ],

            style={

                "padding":
                    "14px"

            }

        ),

        style={

            "borderRadius":
                "12px",

            "border":
                "1px solid #e5e7eb",

            "height":
                "100%"

        },

        className="shadow-sm"

    )