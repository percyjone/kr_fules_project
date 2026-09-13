from dash import (
    callback,
    Input,
    Output,
)

from config.settings import COLORS


# ==========================================================
# ACTIVE SIDEBAR PAGE
# ==========================================================

@callback(

    Output(
        "dashboard-nav",
        "style"
    ),

    Output(
        "outlets-nav",
        "style"
    ),

    Output(
        "tanks-nav",
        "style"
    ),

    Output(
        "alerts-nav",
        "style"
    ),

    Output(
        "reports-nav",
        "style"
    ),

    Output(
        "devices-nav",
        "style"
    ),

    Output(
        "settings-nav",
        "style"
    ),

    Input(
        "_pages_location",
        "pathname"
    )

)
def update_active_sidebar(pathname):

    # ======================================================
    # NAVIGATION DATA
    # ======================================================

    nav_items = [

        (
            "/",
            "dashboard"
        ),

        (
            "/outlets",
            "outlets"
        ),

        (
            "/tanks",
            "tanks"
        ),

        (
            "/alerts",
            "alerts"
        ),

        (
            "/reports",
            "reports"
        ),

        (
            "/devices",
            "devices"
        ),

        (
            "/settings",
            "settings"
        ),

    ]


    # ======================================================
    # DEFAULT STYLE
    # ======================================================

    def normal_style():

        return {

            "display": "block",

            "textDecoration": "none",

            "padding": "10px 16px",

            "borderRadius": "8px",

            "color":
                COLORS["sidebar_text"],

            "backgroundColor":
                "transparent",

            "fontWeight":
                "400",

            "cursor":
                "pointer",

        }


    # ======================================================
    # ACTIVE STYLE
    # ======================================================

    def active_style():

        return {

            "display": "block",

            "textDecoration": "none",

            "padding": "10px 16px",

            "borderRadius": "8px",

            "color":
                "#ffffff",

            "backgroundColor":
                COLORS["sidebar_active"],

            "fontWeight":
                "500",

            "cursor":
                "pointer",

        }


    # ======================================================
    # CREATE STYLES
    # ======================================================

    styles = {

        "dashboard":
            normal_style(),

        "outlets":
            normal_style(),

        "tanks":
            normal_style(),

        "alerts":
            normal_style(),

        "reports":
            normal_style(),

        "devices":
            normal_style(),

        "settings":
            normal_style(),

    }


    # ======================================================
    # FIND ACTIVE PAGE
    # ======================================================

    for href, name in nav_items:

        if pathname == href:

            styles[name] = active_style()

            break


    # ======================================================
    # RETURN IN SAME ORDER AS OUTPUTS
    # ======================================================

    return (

        styles["dashboard"],

        styles["outlets"],

        styles["tanks"],

        styles["alerts"],

        styles["reports"],

        styles["devices"],

        styles["settings"],

    )