import json
from datetime import datetime

import paho.mqtt.client as mqtt
import mysql.connector as mysql

from utils.alert_processor import (
    process_tank_reading
)


# ==========================================================
# MYSQL CONNECTION
# ==========================================================

db = mysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="iot_device"
)

cursor = db.cursor()

db.autocommit = True

print("Connected to MySQL")


# ==========================================================
# MQTT CONNECT CALLBACK
# ==========================================================

def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties
):

    if reason_code == 0:

        print("Connected to Mosquitto")

        client.subscribe(
            "water/tank"
        )

        print(
            "Subscribed to water/tank"
        )

    else:

        print(
            "MQTT connection failed:",
            reason_code
        )


# ==========================================================
# MQTT MESSAGE CALLBACK
# ==========================================================

def on_message(
    client,
    userdata,
    message
):

    try:

        # ==================================================
        # MQTT PAYLOAD → TEXT
        # ==================================================

        payload = message.payload.decode(
            "utf-8"
        )

        print("\nReceived JSON:")
        print(payload)


        # ==================================================
        # JSON TEXT → PYTHON DICTIONARY
        # ==================================================

        data = json.loads(
            payload
        )


        # ==================================================
        # GET VALUES FROM JSON
        # ==================================================

        outlet_code = data[
            "outlet_code"
        ]

        tank_id = data[
            "tank_id"
        ]

        temperature = data[
            "temperature"
        ]

        volume = data[
            "volume"
        ]

        height = data[
            "height"
        ]

        capacity = data[
            "capacity"
        ]


        # ==================================================
        # CALCULATE STOCK THRESHOLDS
        #
        # Dead stock = 7%
        # Minimum stock = 15%
        # Maximum stock = 80%
        # ==================================================

        dead_stock = capacity * 0.07

        min_stock = capacity * 0.15

        max_stock = capacity * 0.80


        # ==================================================
        # PRINT CALCULATED VALUES
        # ==================================================

        print(
            "Capacity:",
            capacity
        )

        print(
            "Dead stock:",
            dead_stock
        )

        print(
            "Minimum stock:",
            min_stock
        )

        print(
            "Maximum stock:",
            max_stock
        )


        # ==================================================
        # GENERATE DATE AND TIME
        # ==================================================

        now = datetime.now()

        current_date = now.strftime(
            "%Y-%m-%d"
        )

        current_time = now.strftime(
            "%H:%M:%S"
        )


        # ==================================================
        # INSERT INTO MYSQL
        # ==================================================

        sql = """
            INSERT INTO tank
            (
                outlet_code,
                dead_stock,
                min_stock,
                max_stock,
                tank_id,
                date,
                time,
                temp,
                volume,
                capacity,
                height
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """


        values = (
            outlet_code,
            dead_stock,
            min_stock,
            max_stock,
            tank_id,
            current_date,
            current_time,
            temperature,
            volume,
            capacity,
            height
        )


        cursor.execute(
            sql,
            values
        )

        db.commit()


        # ==================================================
        # PROCESS ALERTS
        # ==================================================

        alert_id = process_tank_reading(

            outlet_code,

            tank_id,

            temperature,

            volume,

            capacity

        )


        if alert_id is not None:

            print(
                "Alert processed. Result:",
                alert_id
            )


        # ==================================================
        # SUCCESS MESSAGE
        # ==================================================

        print(
            "Data inserted successfully!"
        )

        print(
            "--------------------------------"
        )

        print(
            "Outlet:",
            outlet_code
        )

        print(
            "Tank:",
            tank_id
        )

        print(
            "Temperature:",
            temperature
        )

        print(
            "Volume:",
            volume
        )

        print(
            "Height:",
            height
        )

        print(
            "Capacity:",
            capacity
        )

        print(
            "Dead Stock:",
            dead_stock
        )

        print(
            "Min Stock:",
            min_stock
        )

        print(
            "Max Stock:",
            max_stock
        )

        print(
            "--------------------------------"
        )


    # ======================================================
    # ERROR HANDLING
    # ======================================================

    except json.JSONDecodeError:

        print(
            "Invalid JSON received"
        )


    except KeyError as e:

        print(
            "Missing JSON field:",
            e
        )


    except mysql.Error as e:

        print(
            "MySQL error:",
            e
        )


    except Exception as e:

        print(
            "Unexpected error:",
            e
        )


# ==========================================================
# START MQTT
# ==========================================================

def start_mqtt():

    print(
        "Starting MQTT → MySQL service..."
    )


    # ======================================================
    # CREATE MQTT CLIENT
    # ======================================================

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2
    )


    # ======================================================
    # REGISTER CALLBACKS
    # ======================================================

    client.on_connect = on_connect

    client.on_message = on_message


    # ======================================================
    # CONNECT TO MOSQUITTO
    # ======================================================

    print(
        "Connecting to Mosquitto..."
    )

    client.connect(
        "localhost",
        1883,
        60
    )


    # ======================================================
    # KEEP LISTENING
    # ======================================================

    print(
        "MQTT listener started."
    )

    client.loop_forever()