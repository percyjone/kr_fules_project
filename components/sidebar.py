from dash import html, dcc

from config.settings import COLORS


# ==========================================================
# NAV LINK
# ==========================================================

def nav_link(
    icon,
    label,
    href,
    active=False,
    id=None
):

    return dcc.Link(

        [

            html.Span(
                icon,
                className="me-2"
            ),

            html.Span(
                label
            )

        ],

        id=id,

        href=href,

        style={

            "display": "block",

            "textDecoration": "none",

            "padding": "10px 16px",

            "borderRadius": "8px",

            "color":
                "#ffffff"
                if active
                else COLORS["sidebar_text"],

            "backgroundColor":
                COLORS["sidebar_active"]
                if active
                else "transparent",

            "fontWeight":
                "500"
                if active
                else "400",

            "cursor": "pointer",

        },

        className="mb-1"

    )


# ==========================================================
# SIDEBAR
# ==========================================================

def create_sidebar():

    return html.Div(

        [
            # ==================================================
            # COMPANY LOGO
            # ==================================================

            html.Div(

                html.Img(

                    src="/assets/kr_logo.png",

                    style={
                        "width": "200px",
                        "height": "auto",
                        "display": "block",
                        "objectFit": "contain",
                    }

                ),

                style={
                    "width": "100%",
                    "padding": "20px 10px 10px 10px",
                    "boxSizing": "border-box",
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                }

            ),
            


            # ==================================================
            # NAVIGATION
            # ==================================================

            html.Div(

                [

                    # ------------------------------------------
                    # DASHBOARD
                    # ------------------------------------------

                    nav_link(

                        # "🏠︎",
                        html.I(className="fas fa-home"),

                        "Dashboard",

                        href="/",

                        active=True,

                        id="dashboard-nav"

                    ),


                    # ------------------------------------------
                    # OUTLETS
                    # ------------------------------------------

                    nav_link(

                        # "📍",
                        html.I(className="fas fa-map-marker-alt"),

                        "Outlets / Locations",

                        href="/outlets",

                        id="outlets-nav"

                    ),


                    # ------------------------------------------
                    # TANKS
                    # ------------------------------------------

                    nav_link(

                        # "🛢️",
                        html.I(className="fas fa-layer-group"),

                        "Tanks",

                        href="/tanks",

                        id="tanks-nav"

                    ),


                    # ------------------------------------------
                    # ALERTS
                    # ------------------------------------------

                    nav_link(

                        # "🔔",
                        html.I(className="fas fa-bell"),

                        "Alerts",

                        href="/alerts",

                        id="alerts-nav"

                    ),


                    # ------------------------------------------
                    # REPORTS
                    # ------------------------------------------

                    nav_link(

                        # "📄",
                        html.I(className="fas fa-file-alt"),
                        "Reports",

                        href="/reports",

                        id="reports-nav"

                    ),


                    # ------------------------------------------
                    # DEVICES
                    # ------------------------------------------

                    nav_link(

                        # "🖧",
                        html.I(className="fas fa-microchip"),
                        "Devices",

                        href="/devices",

                        id="devices-nav"

                    ),


                    # ------------------------------------------
                    # SETTINGS
                    # ------------------------------------------

                    nav_link(

                        # "⚙️",
                    html.I(className="fas fa-cog"),

                        "Settings",

                        href="/settings",

                        id="settings-nav"

                    ),

                ],

                style={

                    "padding": "0 12px"

                }

            ),


            # ==================================================
            # FOOTER
            # ==================================================

            html.Div(

                "© 2026 IoT Monitoring System",

                style={

                    "position": "absolute",

                    "bottom": "20px",

                    "left": "16px",

                    "color":
                        COLORS["sidebar_text"],

                    "fontSize": "12px"

                }

            ),

        ],

        id="sidebar",

        style={

            "position": "fixed",

            "top": 0,

            "left": 0,

            "bottom": 0,

            "width": "230px",

            "backgroundColor":
                COLORS["sidebar_bg"],

            "zIndex": 2000,
            "overflow": "hidden",

        }

    )