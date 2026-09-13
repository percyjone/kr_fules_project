import mysql.connector as mysql

from config.settings import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
)


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    return mysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# ==========================================================
# FETCH LATEST READING FOR EACH TANK
# ==========================================================

def fetch_latest_readings(
    outlet_code="all"
):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    sql = """

        SELECT
            t1.outlet_code,
            t1.tank_id,
            t1.date,
            t1.time,
            t1.temp,
            t1.volume,
            t1.height,
            t1.capacity,
            t1.dead_stock,
            t1.min_stock,
            t1.max_stock

        FROM tank t1

        INNER JOIN (

            SELECT
                outlet_code,
                tank_id,

                MAX(
                    CONCAT(date, ' ', time)
                ) AS latest_ts

            FROM tank

            GROUP BY
                outlet_code,
                tank_id

        ) t2

        ON t1.outlet_code = t2.outlet_code

        AND t1.tank_id = t2.tank_id

        AND CONCAT(
            t1.date,
            ' ',
            t1.time
        ) = t2.latest_ts

    """

    params = ()


    # ======================================================
    # OUTLET FILTER
    # ======================================================

    if (
        outlet_code
        and
        outlet_code != "all"
    ):

        sql += """

            WHERE
                t1.outlet_code = %s

        """

        params = (
            outlet_code,
        )


    # ======================================================
    # ORDER
    # ======================================================

    sql += """

        ORDER BY
            t1.outlet_code,
            t1.tank_id

    """


    # ======================================================
    # EXECUTE
    # ======================================================

    cursor.execute(
        sql,
        params
    )

    rows = cursor.fetchall()


    cursor.close()
    conn.close()


    return rows


# ==========================================================
# FETCH TANK HISTORY
# ==========================================================

def fetch_tank_history(

    outlet_code,

    tank_id,

    period="day"

):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )


    # ======================================================
    # DAY
    # ======================================================

    if period == "day":

        sql = """

            SELECT

                date,

                time,

                temp,

                volume,

                height,

                capacity

            FROM tank

            WHERE

                outlet_code = %s

                AND tank_id = %s

                AND date = CURDATE()

            ORDER BY

                date ASC,

                time ASC

        """

        params = (

            outlet_code,

            tank_id

        )


    # ======================================================
    # MONTH
    # ======================================================

    elif period == "month":

        sql = """

            SELECT

                DATE(date) AS date,

                HOUR(time) AS hour,

                AVG(temp) AS temp,

                AVG(volume) AS volume,

                AVG(height) AS height,

                
                MAX(capacity) AS capacity

            FROM tank

            WHERE

                outlet_code = %s

                AND tank_id = %s

                AND YEAR(date) = YEAR(CURDATE())

                AND MONTH(date) = MONTH(CURDATE())

            GROUP BY

                DATE(date),

                HOUR(time)

            ORDER BY

                date ASC,

                hour ASC

        """

        params = (

            outlet_code,

            tank_id

        )


    # ======================================================
    # YEAR
    # ======================================================

    elif period == "year":

        sql = """

            SELECT

                date,

                AVG(temp) AS temp,

                AVG(volume) AS volume,

                AVG(height) AS height,

                MAX(capacity) AS capacity

            FROM tank

            WHERE

                outlet_code = %s

                AND tank_id = %s

                AND YEAR(date) = YEAR(CURDATE())

            GROUP BY

                date

            ORDER BY

                date ASC

        """

        params = (

            outlet_code,

            tank_id

        )


    # ======================================================
    # INVALID PERIOD
    # ======================================================

    else:

        cursor.close()

        conn.close()

        raise ValueError(
            "Invalid period. Use day, month, or year."
        )


    # ======================================================
    # EXECUTE
    # ======================================================

    cursor.execute(
        sql,
        params
    )

    rows = cursor.fetchall()


    cursor.close()
    conn.close()


    return rows


# ==========================================================
# FETCH ALERTS
# ==========================================================

def fetch_alerts(

    severity="all",

    status="all"

):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )


    try:

        # ==================================================
        # BASE QUERY
        # ==================================================

        sql = """

            SELECT

                id,

                outlet_code,

                tank_id,

                alert_type,

                message,

                severity,

                status,

                created_at,

                created_time AS time,

                resolved_at

            FROM alert_table

            WHERE 1=1

        """

        params = []


        # ==================================================
        # SEVERITY FILTER
        # ==================================================

        if (
            severity
            and
            severity != "all"
        ):

            sql += """

                AND severity = %s

            """

            params.append(
                severity
            )


        # ==================================================
        # STATUS FILTER
        # ==================================================

        if (
            status
            and
            status != "all"
        ):

            sql += """

                AND status = %s

            """

            params.append(
                status
            )


        # ==================================================
        # ORDER
        # ==================================================

        sql += """

            ORDER BY
                id DESC

        """


        # ==================================================
        # EXECUTE
        # ==================================================

        cursor.execute(
            sql,
            tuple(params)
        )

        rows = cursor.fetchall()


        return rows or []


    finally:

        cursor.close()
        conn.close()


# ==========================================================
# FETCH ALL ALERT COUNTS BY SEVERITY
#
# Counts ALL alerts regardless of status.
# ==========================================================

def fetch_alert_severity_counts():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    try:

        sql = """

            SELECT

                severity,

                COUNT(*) AS alert_count

            FROM alert_table

            GROUP BY
                severity

        """

        cursor.execute(sql)

        rows = cursor.fetchall()


        counts = {

            "High": 0,

            "Medium": 0,

            "Low": 0

        }


        for row in rows:

            severity = str(
                row.get(
                    "severity",
                    ""
                )
            ).strip()


            alert_count = int(
                row.get(
                    "alert_count",
                    0
                )
            )


            if severity in counts:

                counts[severity] = alert_count


        return counts


    finally:

        cursor.close()
        conn.close()


# ==========================================================
# ACKNOWLEDGE ALL ACTIVE ALERTS
# ==========================================================

def acknowledge_all_alerts():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        sql = """

            UPDATE alert_table

            SET

                status = 'Acknowledged'

            WHERE

                status = 'Active'

        """

        cursor.execute(sql)

        conn.commit()

        affected_rows = cursor.rowcount

        return affected_rows


    finally:

        cursor.close()
        conn.close()


# ==========================================================
# RESOLVE ALL ACTIVE / ACKNOWLEDGED ALERTS
# ==========================================================

def resolve_all_alerts():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        from datetime import datetime


        resolved_at = datetime.now().strftime(
            "%d-%m-%Y"
        )


        sql = """

            UPDATE alert_table

            SET

                status = 'Resolved',

                resolved_at = %s

            WHERE status IN (

                'Active',

                'Acknowledged'

            )

        """


        cursor.execute(

            sql,

            (resolved_at,)

        )


        conn.commit()

        affected_rows = cursor.rowcount

        return affected_rows


    finally:

        cursor.close()
        conn.close()


# ==========================================================
# CREATE ALERT
# ==========================================================

def create_alert(

    outlet_code,

    tank_id,

    alert_type,

    message,

    severity

):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        # ==================================================
        # CURRENT DATE / TIME
        # ==================================================

        from datetime import datetime


        now = datetime.now()


        created_at = now.strftime(
            "%d-%m-%Y"
        )


        created_time = now.strftime(
            "%H:%M:%S"
        )


        # ==================================================
        # INSERT ALERT
        # ==================================================

        sql = """

            INSERT INTO alert_table

            (

                outlet_code,

                tank_id,

                alert_type,

                message,

                severity,

                status,

                created_at,

                created_time

            )

            VALUES

            (

                %s,

                %s,

                %s,

                %s,

                %s,

                'Active',

                %s,

                %s

            )

        """


        cursor.execute(

            sql,

            (

                outlet_code,

                tank_id,

                alert_type,

                message,

                severity,

                created_at,

                created_time

            )

        )


        conn.commit()


        # ==================================================
        # GET GENERATED ALERT ID
        # ==================================================

        alert_id = cursor.lastrowid

        return alert_id


    finally:

        cursor.close()
        conn.close()


# ==========================================================
# CHECK ACTIVE ALERT
# ==========================================================

def active_alert_exists(

    outlet_code,

    tank_id,

    alert_type

):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        sql = """

            SELECT

                id

            FROM alert_table

            WHERE

                outlet_code = %s

                AND tank_id = %s

                AND alert_type = %s

                AND status = 'Active'

            LIMIT 1

        """


        cursor.execute(

            sql,

            (

                outlet_code,

                tank_id,

                alert_type

            )

        )


        row = cursor.fetchone()


        return row is not None


    finally:

        cursor.close()
        conn.close()


# ==========================================================
# RESOLVE ACTIVE ALERT
# ==========================================================

def resolve_active_alert(

    outlet_code,

    tank_id,

    alert_type

):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        from datetime import datetime


        resolved_at = datetime.now().strftime(
            "%d-%m-%Y"
        )


        sql = """

            UPDATE alert_table

            SET

                status = 'Resolved',

                resolved_at = %s

            WHERE

                outlet_code = %s

                AND tank_id = %s

                AND alert_type = %s

                AND status = 'Active'

        """


        cursor.execute(

            sql,

            (

                resolved_at,

                outlet_code,

                tank_id,

                alert_type

            )

        )


        conn.commit()


        affected_rows = cursor.rowcount

        return affected_rows


    finally:

        cursor.close()
        conn.close()