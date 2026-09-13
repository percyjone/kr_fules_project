import dash

from dash import Dash, html,dcc

import dash_bootstrap_components as dbc


dash.register_page(
    __name__,
    path="/register",
    name="Register"
)

layout = html.Div([
    dbc.Container(
        [
        dbc.Row(
            [
                dbc.Col
                    (
                        dbc.Card(
                            dbc.CardBody([
                                html.Div(
                                    [
                                        html.H2(
                                            "Register",
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
                                                      "Name:",
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
                                                        type="text",
                                                        placeholder="Enter your name",
                                                        style={
                                                            "width": "100%",
                                                            "maxWidth": "300px",
                                                         },
                                                  )
                                              ),
                                            ]
                                            
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
                                                        type="email",
                                                        placeholder="Enter your email",
                                                        style={
                                                            "width": "100%",
                                                            "maxWidth": "300px",
                                                         },
                                                  )
                                              ),
                                            ]
                                            
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
                                                        type="password",
                                                        placeholder="Enter your password",
                                                        style={
                                                            "width": "100%",
                                                            "maxWidth": "300px",
                                                         },
                                                  )
                                              ),
                                            ]
                                            
                                        ),
                                        
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(
                                                        "Confirm Password:",
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
                                                        type="password",
                                                        placeholder="Confirm your password",
                                                        style={
                                                            "width": "100%",
                                                            "maxWidth": "300px",
                                                         },
                                                    ),
                                                     
                                                ),
                                                
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Register",
                                                        color="primary",
                                                        className=" mx-auto d-block w-10",
                                                        style={
                                                            "marginTop": "20px"
                                                        }
                                                    ),
                                                    width="auto",
                                                    className="mx-auto d-block text-center "
                                                )
                                            ]
                                        ),
                                        
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        "Already have an account? ",
                                                        className="text-center",
                                                        style={
                                                            "marginTop": "10px"
                                                        }
                                                    ),
                                                    width="auto",
                                                    className="text-center"
                                                ),
                                                dbc.Col(
                                                    dcc.Link(
                                                        "Login here",
                                                        href="/login",
                                                        
                                                        style={
                                                            "marginTop": "10px",
                                                            "color": "#209849",
                                                            "fontWeight": "500",
                                                            
                                                            
                                                        }
                                                    ),
                                                    width="auto",
                                                    className=" d-block mt-2"
                                                )
                                            ]
                                        )
                                        
                                        
                                    ]

                                )
                            ])
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