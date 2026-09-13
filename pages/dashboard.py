import dash

from dash import (
    html,
    dcc,
)

import dash_bootstrap_components as dbc

from config.settings import (
    REFRESH_INTERVAL_MS,
)

from components.header import (
    create_header
)

from components.outlet_health import (
    create_outlet_health_card
)

from components.tanks_table import (
    create_tanks_table_card
)


# ==========================================================
# REGISTER DASHBOARD PAGE
# ==========================================================

dash.register_page(

    __name__,

    path="/",

    name="Dashboard"

)


# ==========================================================
# DASHBOARD PAGE
# ==========================================================

def create_dashboard_page():

    return html.Div(

        [

            # ==================================================
            # HEADER
            #
            # Header stays exactly where it is.
            # ==================================================

            create_header(),


            # ==================================================
            # DASHBOARD CONTENT
            #
            # Everything below the header is moved slightly
            # to the right so it aligns with the
            # "Real-time overview of all tanks" text.
            # ==================================================

            html.Div(

                [

                    # ==========================================
                    # REFRESH TIMER
                    # ==========================================

                    dcc.Interval(

                        id="refresh-interval",

                        interval=REFRESH_INTERVAL_MS,

                        n_intervals=0

                    ),


                    # ==========================================
                    # SELECTED TANK STORE
                    # ==========================================

                    dcc.Store(

                        id="selected-tank"

                    ),


                    # ==========================================
                    # KPI ROW
                    # ==========================================

                    html.Div(

                        id="kpi-row",

                        className="mb-4"

                    ),


                    # ==========================================
                    # MAIN DASHBOARD CONTENT
                    #
                    # Large screen:
                    #
                    # Outlets      = 3 columns
                    # Tanks Data   = 6 columns
                    # Right Panel  = 3 columns
                    #
                    # Total = 12 columns
                    # ==========================================

                    dbc.Row(

                        [

                            # ==================================
                            # OUTLET HEALTH
                            # ==================================

                            dbc.Col(

                                create_outlet_health_card(),

                                width=12,

                                lg=3,

                                className="mb-4"

                            ),


                            # ==================================
                            # TANKS DATA
                            # ==================================

                            dbc.Col(

                                create_tanks_table_card(),

                                width=12,

                                lg=9,

                                className="mb-4"

                            ),


                           

                        ],

                        className="g-3"

                    ),


                    # ==========================================
                    # TANK DETAILS
                    # ==========================================

                    html.Div(

                        id="tank-detail-panel"

                    ),

                ],

                # ==================================================
                # ALIGNMENT
                #
                # Header text has margin-left: 20px.
                # Give the dashboard content the same left offset.
                # ==================================================

                style={

                    "marginLeft": "20px",

                }

            ),

        ]

    )


# ==========================================================
# DASH PAGE LAYOUT
# ==========================================================

layout = create_dashboard_page()