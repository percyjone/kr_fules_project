import dash

from dash import Dash, html,dcc

import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/login",
    name="Login"
)

layout =html.Div([
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                html.Div(
                                    [
                                        html.H2(
                                            "Login",
                                            className="text-center mb-4",
                                            style={
                                                "fontWeight": "600",
                                                "color":"#209849"
                                            },
                                        ),
                                        dbc.Row(
                                            [
                                                    dbc.Col(
                                                        dbc.Label(
                                                            "Email:",
                                                            style={
                                                                "fontWeight": "500",
                                                                "color": "#374151",
                                                                "marginBottom": "0",
                                                                "width": "80px",
                                                                
                                                                
                                                            },
                                                    ),
                                                        width="auto",
                                                        className="pe-1",
                                                    ),
                                                    dbc.Col(
                                                            dbc.Input(
                                                                id="input-email",
                                                                type="email",
                                                                placeholder="Enter your email",
                                                                style={
                                                                    "width": "100%",
                                                                    "maxWidth": "300px",
                                                               },
                                                            ),
                                                            width="auto",
                                                            className="ps-1",
                                                            
                                                    ),
                                                    
                                            
                                            ],className="align-items-center justify-content-center mb-3"
                                            
                                        ),
                                        dbc.Row(
                                            [
                                                    dbc.Col(
                                                        dbc.Label(
                                                            "Password:",
                                                            style={
                                                                "fontWeight": "500",
                                                                "color": "#374151",
                                                                "marginBottom": "0",
                                                                 "width": "80px",
                                                                
                                                                
                                                            },
                                                    ),
                                                        width="auto",
                                                        className="pe-1",
                                                    ),
                                                    dbc.Col(
                                                            dbc.Input(
                                                                id="input-password",
                                                                type="password",
                                                                placeholder="Enter your password",
                                                                style={
                                                                    "width": "100%",
                                                                    "maxWidth": "300px",
                                                               },
                                                            ),
                                                            width="auto",
                                                            className="ps-1",
                                                            
                                                    ),
                                                    
                                            
                                            ],className="align-items-center justify-content-center mb-3"
                                            
                                        ),
                                        
                                        
                                        dbc.Button(
                                            "Login",
                                            color="primary",
                                            id="login-btn",
                                            n_clicks=0,
                                            className=" mx-auto d-block w-10",
                                            
                                        ),
                                        html.Div(
                                                id="login-message",
                                                className="mt-3 text-center",
                                        ),
                                                                                
                                        html.Hr(
                                            style={"marginTop": "25px"}
                                        ),
                                        
                                         html.Div(
                                            [
                                                html.Span(
                                                    "Don't have an account? "
                                                ),
                                                dcc.Link(
                                                    "Register",
                                                    href="/register",
                                                    style={
                                                        "textDecoration": "none",
                                                        "fontWeight": "500",
                                                    },
                                                ),
                                            ],
                                            className="text-center",
                                        ),
                                    ]
                                )
                                ]
                             )
                    ),
                    width=4,
                    className="mx-auto my-5"
                    )
                ]
            )

        ],
        fluid=True
    )
])

