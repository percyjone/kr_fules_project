from dash import callback, Input, Output, State

from database.auth import authenticate_user


@callback(
    # Store logged-in user information
    Output("user-session", "data"),

    # Redirect browser
    Output("url", "pathname"),

    # Display login message
    Output("login-message", "children"),

    # Login button
    Input("login-btn", "n_clicks"),

    # Email and password
    State("input-email", "value"),
    State("input-password", "value"),

    prevent_initial_call=True,
)
def login_user(n_clicks, email, password):

    # ======================================================
    # CHECK EMPTY FIELDS
    # ======================================================

    if not email or not password:
        return (
            None,
            "/login",
            "Please enter both email and password."
        )

    # ======================================================
    # AUTHENTICATE USER
    # ======================================================

    user = authenticate_user(
        email,
        password
    )

    # ======================================================
    # LOGIN FAILED
    # ======================================================

    if user is None:
        return (
            None,
            "/login",
            "Invalid email or password. Please try again."
        )

    # ======================================================
    # LOGIN SUCCESSFUL
    # ======================================================

    session_data = {
        "logged_in": True,
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }

    # ======================================================
    # REDIRECT TO DASHBOARD
    # ======================================================

    return (
        session_data,
        "/",
        "Login successful! Welcome, " + user["name"] + "."
    )