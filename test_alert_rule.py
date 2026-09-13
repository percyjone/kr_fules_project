from utils.alert_processor import (
    process_tank_reading
)


# ==========================================================
# TEST 1
# NORMAL TEMPERATURE
# ==========================================================

print(
    "TEST 1: Temperature = 30°C"
)

result = process_tank_reading(

    "OUT001",

    1,

    30.0

)

print(
    "Result:",
    result
)


# ==========================================================
# TEST 2
# HIGH TEMPERATURE
# ==========================================================

print(
    "\nTEST 2: Temperature = 36°C"
)

result = process_tank_reading(

    "OUT001",

    1,

    36.0

)

print(
    "Result:",
    result
)


# ==========================================================
# TEST 3
# STILL HIGH
# ==========================================================

print(
    "\nTEST 3: Temperature = 37°C"
)

result = process_tank_reading(

    "OUT001",

    1,

    37.0

)

print(
    "Result:",
    result
)


# ==========================================================
# TEST 4
# BACK TO NORMAL
# ==========================================================

print(
    "\nTEST 4: Temperature = 34°C"
)

result = process_tank_reading(

    "OUT001",

    1,

    34.0

)

print(
    "Result:",
    result
)