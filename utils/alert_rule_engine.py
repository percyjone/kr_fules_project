from config.settings import (
    HIGH_TEMPERATURE_THRESHOLD
)


# ==========================================================
# STOCK THRESHOLD PERCENTAGES
# ==========================================================

DEAD_STOCK_PERCENT = 0.07

MIN_STOCK_PERCENT = 0.15

MAX_STOCK_PERCENT = 0.80


# ==========================================================
# CHECK HIGH TEMPERATURE
# ==========================================================

def check_high_temperature(
    temperature
):

    # ------------------------------------------------------
    # No temperature value
    # ------------------------------------------------------

    if temperature is None:

        return False


    # ------------------------------------------------------
    # Compare temperature with threshold
    # ------------------------------------------------------

    return (

        float(temperature)

        >

        HIGH_TEMPERATURE_THRESHOLD

    )


# ==========================================================
# CALCULATE STOCK THRESHOLDS
# ==========================================================

def calculate_stock_thresholds(
    capacity
):

    # ------------------------------------------------------
    # No capacity
    # ------------------------------------------------------

    if capacity is None:

        return None


    capacity = float(
        capacity
    )


    # ------------------------------------------------------
    # Calculate thresholds
    # ------------------------------------------------------

    dead_stock = (

        capacity
        *
        DEAD_STOCK_PERCENT

    )


    min_stock = (

        capacity
        *
        MIN_STOCK_PERCENT

    )


    max_stock = (

        capacity
        *
        MAX_STOCK_PERCENT

    )


    return {

        "dead_stock":
            dead_stock,

        "min_stock":
            min_stock,

        "max_stock":
            max_stock

    }


# ==========================================================
# CHECK STOCK LEVEL
# ==========================================================

def check_stock_level(
    volume,
    capacity
):

    # ------------------------------------------------------
    # No volume or capacity
    # ------------------------------------------------------

    if (

        volume is None
        or
        capacity is None

    ):

        return None


    # ------------------------------------------------------
    # Calculate thresholds
    # ------------------------------------------------------

    thresholds = calculate_stock_thresholds(
        capacity
    )


    if thresholds is None:

        return None


    volume = float(
        volume
    )


    dead_stock = thresholds[
        "dead_stock"
    ]

    min_stock = thresholds[
        "min_stock"
    ]

    max_stock = thresholds[
        "max_stock"
    ]


    # ======================================================
    # DEAD STOCK
    # ======================================================

    if volume <= dead_stock:

        return {

            "status":
                "Dead Stock",

            "alert_type":
                "Dead Stock",

            "severity":
                "High",

            "indicator":
                "red_flicker",

            "threshold":
                dead_stock

        }


    # ======================================================
    # MINIMUM STOCK
    # ======================================================

    elif volume <= min_stock:

        return {

            "status":
                "Minimum Stock",

            "alert_type":
                "Minimum Stock",

            "severity":
                "Medium",

            "indicator":
                "yellow",

            "threshold":
                min_stock

        }


    # ======================================================
    # NORMAL STOCK
    # ======================================================

    elif volume <= max_stock:

        return {

            "status":
                "Normal",

            "alert_type":
                None,

            "severity":
                None,

            "indicator":
                "green",

            "threshold":
                None

        }


    # ======================================================
    # MAXIMUM STOCK
    # ======================================================

    else:

        return {

            "status":
                "Maximum Stock",

            "alert_type":
                "Maximum Stock",

            "severity":
                "Medium",

            "indicator":
                "yellow_flicker",

            "threshold":
                max_stock

        }