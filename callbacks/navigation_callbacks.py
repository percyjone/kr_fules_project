from dash import (
    callback,
    Input,
    Output,
    ctx,
    html,
)

from pages.dashboard import (
    create_dashboard_page
)

from pages.alerts import (
    create_alerts_page
)


# ==========================================================
# PAGE NAVIGATION
# ==========================================================

@callback(

    Output(
        "page-content",
        "children"
    ),

    Input(
        "dashboard-nav",
        "n_clicks"
    ),

    Input(
        "outlets-nav",
        "n_clicks"
    ),

    Input(
        "tanks-nav",
        "n_clicks"
    ),

    Input(
        "alerts-nav",
        "n_clicks"
    ),

    Input(
        "reports-nav",
        "n_clicks"
    ),

    Input(
        "devices-nav",
        "n_clicks"
    ),

    Input(
        "settings-nav",
        "n_clicks"
    ),

)
def navigate_pages(

    dashboard_clicks,

    outlets_clicks,

    tanks_clicks,

    alerts_clicks,

    reports_clicks,

    devices_clicks,

    settings_clicks

):

    trigger = ctx.triggered_id




    # ======================================================
    # DASHBOARD
    # ======================================================

    if trigger == "dashboard-nav":

        return create_dashboard_page()


    # ======================================================
    # OUTLETS
    # ======================================================

    if trigger == "outlets-nav":

        return html.Div(

            [

                html.H3(
                    "Outlets / Locations"
                )

            ]

        )


    # ======================================================
    # TANKS
    # ======================================================

    if trigger == "tanks-nav":

        return html.Div(

            [

                html.H3(
                    "Tanks"
                )

            ]

        )


    # ======================================================
    # ALERTS
    # ======================================================

    if trigger == "alerts-nav":

        return create_alerts_page()


    # ======================================================
    # REPORTS
    # ======================================================

    if trigger == "reports-nav":

        return html.Div(

            [

                html.H3(
                    "Reports"
                )

            ]

        )


    # ======================================================
    # DEVICES
    # ======================================================

    if trigger == "devices-nav":

        return html.Div(

            [

                html.H3(
                    "Devices"
                )

            ]

        )


    # ======================================================
    # SETTINGS
    # ======================================================

    if trigger == "settings-nav":

        return html.Div(

            [

                html.H3(
                    "Settings"
                )

            ]

        )


    # ======================================================
    # DEFAULT
    # ======================================================

    return create_dashboard_page()