from database.db import (
    create_alert,
    active_alert_exists,
    resolve_active_alert,
)

from utils.alert_rule_engine import (
    check_high_temperature,
    check_stock_level,
)


# ==========================================================
# PROCESS TANK READING
# ==========================================================

def process_tank_reading(
    outlet_code,
    tank_id,
    temperature,
    volume,
    capacity
):

    # ======================================================
    # PROCESS TEMPERATURE ALERT
    # ======================================================

    temperature_alert_id = None

    temperature_alert_type = (
        "High Temperature"
    )


    # ======================================================
    # NO TEMPERATURE ALERT
    # ======================================================

    if temperature is not None:

        # --------------------------------------------------
        # HIGH TEMPERATURE
        # --------------------------------------------------

        if check_high_temperature(
            temperature
        ):

            if not active_alert_exists(

                outlet_code,

                tank_id,

                temperature_alert_type

            ):

                message = (

                    "Temperature above "
                    f"threshold ({temperature}°C)"

                )


                temperature_alert_id = create_alert(

                    outlet_code,

                    tank_id,

                    temperature_alert_type,

                    message,

                    "High"

                )


        # --------------------------------------------------
        # TEMPERATURE NORMAL
        # --------------------------------------------------

        else:

            if active_alert_exists(

                outlet_code,

                tank_id,

                temperature_alert_type

            ):

                resolve_active_alert(

                    outlet_code,

                    tank_id,

                    temperature_alert_type

                )


    # ======================================================
    # PROCESS STOCK LEVEL
    # ======================================================

    stock_alert_id = None


    # ------------------------------------------------------
    # Check stock level
    # ------------------------------------------------------

    stock_result = check_stock_level(

        volume,

        capacity

    )


    # ======================================================
    # NO STOCK RESULT
    # ======================================================

    if stock_result is None:

        return temperature_alert_id


    stock_status = stock_result[
        "status"
    ]

    alert_type = stock_result[
        "alert_type"
    ]

    severity = stock_result[
        "severity"
    ]

    threshold = stock_result[
        "threshold"
    ]


    # ======================================================
    # DEAD STOCK
    # ======================================================

    if stock_status == "Dead Stock":

        message = (

            f"Tank volume ({volume} L) "
            f"has reached dead stock level "
            f"({threshold:.0f} L)"

        )


        # --------------------------------------------------
        # CREATE ALERT
        # --------------------------------------------------

        if not active_alert_exists(

            outlet_code,

            tank_id,

            alert_type

        ):

            stock_alert_id = create_alert(

                outlet_code,

                tank_id,

                alert_type,

                message,

                severity

            )


        # --------------------------------------------------
        # RESOLVE OTHER STOCK ALERTS
        # --------------------------------------------------

        resolve_if_active(

            outlet_code,

            tank_id,

            "Minimum Stock"

        )

        resolve_if_active(

            outlet_code,

            tank_id,

            "Maximum Stock"

        )


    # ======================================================
    # MINIMUM STOCK
    # ======================================================

    elif stock_status == "Minimum Stock":

        message = (

            f"Tank volume ({volume} L) "
            f"has reached minimum stock level "
            f"({threshold:.0f} L)"

        )


        # --------------------------------------------------
        # CREATE ALERT
        # --------------------------------------------------

        if not active_alert_exists(

            outlet_code,

            tank_id,

            alert_type

        ):

            stock_alert_id = create_alert(

                outlet_code,

                tank_id,

                alert_type,

                message,

                severity

            )


        # --------------------------------------------------
        # RESOLVE OTHER STOCK ALERTS
        # --------------------------------------------------

        resolve_if_active(

            outlet_code,

            tank_id,

            "Dead Stock"

        )

        resolve_if_active(

            outlet_code,

            tank_id,

            "Maximum Stock"

        )


    # ======================================================
    # NORMAL STOCK
    # ======================================================

    elif stock_status == "Normal":

        # --------------------------------------------------
        # Resolve all stock alerts
        # --------------------------------------------------

        resolve_if_active(

            outlet_code,

            tank_id,

            "Dead Stock"

        )

        resolve_if_active(

            outlet_code,

            tank_id,

            "Minimum Stock"

        )

        resolve_if_active(

            outlet_code,

            tank_id,

            "Maximum Stock"

        )


    # ======================================================
    # MAXIMUM STOCK
    # ======================================================

    elif stock_status == "Maximum Stock":

        message = (

            f"Tank volume ({volume} L) "
            f"has exceeded maximum stock level "
            f"({threshold:.0f} L)"

        )


        # --------------------------------------------------
        # CREATE ALERT
        # --------------------------------------------------

        if not active_alert_exists(

            outlet_code,

            tank_id,

            alert_type

        ):

            stock_alert_id = create_alert(

                outlet_code,

                tank_id,

                alert_type,

                message,

                severity

            )


        # --------------------------------------------------
        # RESOLVE OTHER STOCK ALERTS
        # --------------------------------------------------

        resolve_if_active(

            outlet_code,

            tank_id,

            "Dead Stock"

        )

        resolve_if_active(

            outlet_code,

            tank_id,

            "Minimum Stock"

        )


    # ======================================================
    # RETURN RESULT
    # ======================================================

    if temperature_alert_id is not None:

        return temperature_alert_id


    if stock_alert_id is not None:

        return stock_alert_id


    return None


# ==========================================================
# RESOLVE ACTIVE ALERT IF EXISTS
# ==========================================================

def resolve_if_active(
    outlet_code,
    tank_id,
    alert_type
):

    if active_alert_exists(

        outlet_code,

        tank_id,

        alert_type

    ):

        return resolve_active_alert(

            outlet_code,

            tank_id,

            alert_type

        )


    return None