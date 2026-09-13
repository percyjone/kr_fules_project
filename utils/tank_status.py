# ==========================================================
# TANK STOCK STATUS
# ==========================================================

DEAD_STOCK_PERCENT = 0.07
MIN_STOCK_PERCENT = 0.15
MAX_STOCK_PERCENT = 0.80


def get_tank_stock_status(volume, capacity):
    """
    Determine tank stock condition based on
    current volume and tank capacity.
    """

    if volume is None or capacity is None:
        return {
            "status": "Unknown",
            "color": "#6b7280",
            "flicker": False
        }

    volume = float(volume)
    capacity = float(capacity)

    dead_stock = capacity * DEAD_STOCK_PERCENT
    min_stock = capacity * MIN_STOCK_PERCENT
    max_stock = capacity * MAX_STOCK_PERCENT

    # ------------------------------------------------------
    # DEAD STOCK
    # ------------------------------------------------------

    if volume <= dead_stock:

        return {
            "status": "Dead Stock",
            "color": "#ef4444",
            "flicker": True
        }

    # ------------------------------------------------------
    # MINIMUM STOCK
    # ------------------------------------------------------

    elif volume <= min_stock:

        return {
            "status": "Minimum Stock",
            "color": "#f59e0b",
            "flicker": False
        }

    # ------------------------------------------------------
    # NORMAL
    # ------------------------------------------------------

    elif volume <= max_stock:

        return {
            "status": "Normal",
            "color": "#16a34a",
            "flicker": False
        }

    # ------------------------------------------------------
    # MAXIMUM STOCK
    # ------------------------------------------------------

    else:

        return {
            "status": "Maximum Stock",
            "color": "#f59e0b",
            "flicker": True
        }