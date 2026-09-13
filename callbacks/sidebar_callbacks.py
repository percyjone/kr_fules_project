from dash import (
    callback,
    Input,
    Output,
)

from config.settings import COLORS


# ==========================================================
# SIDEBAR TOGGLE
# ==========================================================

@callback(

    Output(
        "sidebar",
        "style"
    ),

    Output(
        "page-content",
        "style"
    ),

    Input(
        "sidebar-toggle",
        "n_clicks"
    )

)
def toggle_sidebar(n_clicks):

    # ======================================================
    # SIDEBAR OPEN
    # ======================================================

    if n_clicks is None or n_clicks % 2 == 0:

        sidebar_style = {

            "position": "fixed",

            "top": 0,

            "left": 0,

            "bottom": 0,

            "width": "230px",

            "backgroundColor":
                COLORS["sidebar_bg"],

            "zIndex": 1000,

            "transition":
                "left 0.3s ease"

        }

        page_style = {

            "marginLeft":
                "230px",

            "padding":
                "28px",

            "backgroundColor":
                COLORS["page_bg"],

            "minHeight":
                "100vh",

            "transition":
                "margin-left 0.3s ease"

        }

        return (

            sidebar_style,

            page_style

        )


    # ======================================================
    # SIDEBAR CLOSED
    # ======================================================

    sidebar_style = {

        "position": "fixed",

        "top": 0,

        "left": "-230px",

        "bottom": 0,

        "width": "230px",

        "backgroundColor":
            COLORS["sidebar_bg"],

        "zIndex": 1000,

        "transition":
            "left 0.3s ease"

    }

    page_style = {

        "marginLeft":
            "0px",

        "padding":
            "28px",

        "backgroundColor":
            COLORS["page_bg"],

        "minHeight":
            "100vh",

        "transition":
            "margin-left 0.3s ease"

    }

    return (

        sidebar_style,

        page_style

    )


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