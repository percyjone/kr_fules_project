from dash import (
    callback,
    Input,
    Output,
    ctx,
)

from database.db import (
    acknowledge_all_alerts,
    resolve_all_alerts,
)


# ==========================================================
# QUICK ACTIONS
# ==========================================================

@callback(

    Output(
        "alerts-action-message",
        "children"
    ),

    Input(
        "acknowledge-all-btn",
        "n_clicks"
    ),

    Input(
        "resolve-all-btn",
        "n_clicks"
    ),

    prevent_initial_call=True,

)
def handle_alert_quick_actions(

    acknowledge_clicks,

    resolve_clicks

):

    trigger = ctx.triggered_id


    # ======================================================
    # ACKNOWLEDGE ALL
    # ======================================================

    if trigger == "acknowledge-all-btn":

        count = acknowledge_all_alerts()

        return (
            f"{count} alert(s) acknowledged."
        )


    # ======================================================
    # RESOLVE ALL
    # ======================================================

    if trigger == "resolve-all-btn":

        count = resolve_all_alerts()

        return (
            f"{count} alert(s) resolved."
        )


    return ""