def create_app():
    from dash import Dash, dcc, html, Input, Output, State, callback
    import dash_bootstrap_components as dbc
    from justblockchain import justblockchain
    import secrets


    # --------------------------------------------------
    # ALL AVAILABLE THEMES
    # --------------------------------------------------

    THEMES = {
        "Bootstrap": dbc.themes.BOOTSTRAP,
        "Cerulean": dbc.themes.CERULEAN,
        "Cosmo": dbc.themes.COSMO,
        "Cyborg": dbc.themes.CYBORG,
        "Darkly": dbc.themes.DARKLY,
        "Flatly": dbc.themes.FLATLY,
        "Journal": dbc.themes.JOURNAL,
        "Litera": dbc.themes.LITERA,
        "Lumen": dbc.themes.LUMEN,
        "Lux": dbc.themes.LUX,
        "Materia": dbc.themes.MATERIA,
        "Minty": dbc.themes.MINTY,
        "Morph": dbc.themes.MORPH,
        "Pulse": dbc.themes.PULSE,
        "Quartz": dbc.themes.QUARTZ,
        "Sandstone": dbc.themes.SANDSTONE,
        "Simplex": dbc.themes.SIMPLEX,
        "Sketchy": dbc.themes.SKETCHY,
        "Slate": dbc.themes.SLATE,
        "Solar": dbc.themes.SOLAR,
        "Spacelab": dbc.themes.SPACELAB,
        "Superhero": dbc.themes.SUPERHERO,
        "United": dbc.themes.UNITED,
        "Vapor": dbc.themes.VAPOR,
        "Yeti": dbc.themes.YETI,
        "Zephyr": dbc.themes.ZEPHYR,
    }


    # --------------------------------------------------
    # INITIALIZE DASH APPLICATION
    # --------------------------------------------------

    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )


    # --------------------------------------------------
    # GLOBAL BLOCKCHAIN DATA
    # --------------------------------------------------

    list_of_strings = []


    def generate_random_hash():
        return secrets.token_hex(32)


    def create_blockchains(strings):

        unique_strings = sorted(set(strings))

        blockchain = justblockchain.Blockchain()

        for string in unique_strings:
            blockchain.add_block(string)

        blockchains = blockchain.chain[1:]

        if blockchains:
            blockchains[0]["previous_hash"] = generate_random_hash()

        return blockchains


    # --------------------------------------------------
    # APPLICATION LAYOUT
    # --------------------------------------------------

    app.layout = dbc.Container(
        [

            # Application heading
            html.H1(
                "Blockchain Explorer",
                className="text-center my-4"
            ),

            html.Hr(),

            # Theme selector
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Select Application Theme"),

                            dcc.Dropdown(
                                id="theme-selector",

                                options=[
                                    {
                                        "label": theme,
                                        "value": theme
                                    }
                                    for theme in THEMES
                                ],

                                value="Bootstrap",
                                clearable=False
                            )

                        ],
                        md=4
                    )
                ],
                className="mb-4"
            ),

            # Hidden output for theme callback
            html.Div(
                id="theme-output",
                style={"display": "none"}
            ),

            # Input card
            dbc.Card(
                dbc.CardBody(
                    [

                        html.H4("Add Blockchain Data"),

                        dbc.Label("Enter a value"),

                        dbc.Input(
                            id="input-on-submit",
                            type="text",
                            placeholder="Enter blockchain data..."
                        ),

                        html.Div(
                            [

                                dbc.Button(
                                    "Add Block",
                                    id="submit-value",
                                    color="primary",
                                    className="me-2"
                                ),

                                dbc.Button(
                                    "Delete All",
                                    id="submit-value2",
                                    color="danger"
                                )

                            ],
                            className="mt-3"
                        )

                    ]
                ),
                className="mb-4"
            ),

            # Blockchain records heading
            html.H3(
                "Blockchain Records",
                className="mb-3"
            ),

            # Blockchain output
            html.Div(
                id="container-button-basic",
                children=dbc.Alert(
                    "Enter a value and press Add Block.",
                    color="info"
                )
            )

        ],

        fluid=True,
        className="p-4"
    )


    # --------------------------------------------------
    # DYNAMIC THEME SWITCHING
    # --------------------------------------------------

    app.clientside_callback(

        """
        function(theme) {

            const themes = {
                "Bootstrap": "bootstrap",
                "Cerulean": "cerulean",
                "Cosmo": "cosmo",
                "Cyborg": "cyborg",
                "Darkly": "darkly",
                "Flatly": "flatly",
                "Journal": "journal",
                "Litera": "litera",
                "Lumen": "lumen",
                "Lux": "lux",
                "Materia": "materia",
                "Minty": "minty",
                "Morph": "morph",
                "Pulse": "pulse",
                "Quartz": "quartz",
                "Sandstone": "sandstone",
                "Simplex": "simplex",
                "Sketchy": "sketchy",
                "Slate": "slate",
                "Solar": "solar",
                "Spacelab": "spacelab",
                "Superhero": "superhero",
                "United": "united",
                "Vapor": "vapor",
                "Yeti": "yeti",
                "Zephyr": "zephyr"
            };

            const themeName = themes[theme] || "bootstrap";

            const stylesheet =
                "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/"
                + themeName
                + "/bootstrap.min.css";

            let link = document.getElementById("theme-stylesheet");

            if (!link) {

                link = document.createElement("link");

                link.id = "theme-stylesheet";

                link.rel = "stylesheet";

                document.head.appendChild(link);

            }

            link.href = stylesheet;

            return theme;

        }
        """,

        Output("theme-output", "children"),

        Input("theme-selector", "value")

    )


    # --------------------------------------------------
    # ADD BLOCK CALLBACK
    # --------------------------------------------------

    @callback(

        Output("container-button-basic", "children"),

        Input("submit-value", "n_clicks"),

        State("input-on-submit", "value"),

        prevent_initial_call=True

    )

    def submit_input(n_clicks, value):

        global list_of_strings

        # Validate input
        if not value or not value.strip():

            return dbc.Alert(
                "Please enter a valid value.",
                color="warning"
            )

        # Add input to blockchain data
        list_of_strings.append(value.strip())

        # Generate blockchain
        blockchains = create_blockchains(list_of_strings)

        components = []

        # Display blockchain records
        for index, block in enumerate(blockchains):

            component = dbc.Card(

                dbc.CardBody(
                    [

                        html.H5(
                            f"Block #{index + 1}",
                            className="card-title"
                        ),

                        *[
                            html.P(
                                f"{key}: {val}"
                            )
                            for key, val in block.items()
                        ]

                    ]
                ),

                className="mb-3"

            )

            components.append(component)

        return components


    # --------------------------------------------------
    # DELETE ALL BLOCKS CALLBACK
    # --------------------------------------------------

    @callback(

        Output(
            "container-button-basic",
            "children",
            allow_duplicate=True
        ),

        Input("submit-value2", "n_clicks"),

        prevent_initial_call=True

    )

    def delete_input(n_clicks):

        global list_of_strings

        # Clear blockchain data
        list_of_strings = []

        return dbc.Alert(
            "All blockchain records have been deleted.",
            color="success"
        )

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
