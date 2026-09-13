import threading

from dash import Dash, html, page_container,dcc
import dash_bootstrap_components as dbc

from components.sidebar import create_sidebar
from config.settings import COLORS


# ==========================================================
# CREATE APP
# ==========================================================

app = Dash(

    __name__,

    use_pages=True,

    # ======================================================
    # STYLESHEETS
    # ======================================================

    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],

    suppress_callback_exceptions=True,

)


# ==========================================================
# MAIN APPLICATION LAYOUT
# ==========================================================

app.layout = html.Div(

    [

        # ==================================================
        # SIDEBAR
        # ==================================================

        create_sidebar(),
        
        # --------------------------------------------------
        # Current browser URL
        # --------------------------------------------------

        dcc.Location(
            id="url",
            refresh=True
        ),
        # ==================================================
        # STORE LOGGED-IN USER INFORMATION
        # ==================================================

        dcc.Store(
            id="user-session",
            storage_type="session"
        ),

       

        # ==================================================
        # PAGE CONTENT
        # ==================================================

        html.Div(

            page_container,

            id="page-content",

            style={

                "marginLeft": "0px",

                "padding": "28px",

                "backgroundColor":
                    COLORS["page_bg"],

                "minHeight": "100vh",
                "boxSizing": "border-box",

            }

        ),

    ]

)


# ==========================================================
# CALLBACKS
# ==========================================================

from callbacks import sidebar_callbacks
from callbacks import dashboard_callbacks
from callbacks import outlet_callbacks
from callbacks import tank_callbacks
from callbacks import alerts_callbacks
from callbacks import auth_callbacks

# ==========================================================
# MQTT
# ==========================================================

def start_mqtt_service():

    from mqtt_to_sql import start_mqtt

    start_mqtt()


mqtt_thread = threading.Thread(

    target=start_mqtt_service,

    daemon=True

)

mqtt_thread.start()


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        use_reloader=False

    )