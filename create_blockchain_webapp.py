
def create_app():
    list_of_strings = []

    from dash import Dash, dcc, html, Input, Output, State, callback
    import dash_bootstrap_components as dbc
    from justblockchain import justblockchain
    import secrets
    import math

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

            html.H1(
                "Blockchain Explorer",
                className="text-center my-4"
            ),

            html.Hr(),

            # THEME SELECTOR
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

            html.Div(
                id="theme-output",
                style={"display": "none"}
            ),

            # INPUT CARD
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

            # BLOCKCHAIN RECORDS
            html.H3(
                "Blockchain Records",
                className="mb-3"
            ),

            # RECORD COUNT AND PAGE SIZE
            dbc.Row(
                [

                    dbc.Col(
                        [
                            dbc.Label("Records per page"),

                            dcc.Dropdown(
                                id="page-size",
                                options=[
                                    {"label": "5", "value": 5},
                                    {"label": "10", "value": 10},
                                    {"label": "20", "value": 20},
                                    {"label": "50", "value": 50}
                                ],
                                value=5,
                                clearable=False
                            )
                        ],
                        md=3
                    ),

                    dbc.Col(
                        html.Div(
                            id="record-count",
                            className="text-end mt-4"
                        ),
                        md=9
                    )

                ],
                className="mb-3"
            ),

            # BLOCKCHAIN RECORD OUTPUT
            html.Div(
                id="container-button-basic",
                children=dbc.Alert(
                    "Enter a value and press Add Block.",
                    color="info"
                )
            ),

            # PAGINATION
            html.Div(
                [

                    dbc.Pagination(
                        id="pagination",
                        active_page=1,
                        max_value=1,
                        fully_expanded=False,
                        first_last=True,
                        previous_next=True,
                        className="justify-content-center mt-4"
                    )

                ]
            ),

            html.Hr(),

            html.Div(
                id="page-information",
                className="text-center text-muted mb-3"
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
    # COMMON PAGINATION CALLBACK
    # --------------------------------------------------

    @callback(

        Output("container-button-basic", "children"),

        Output("pagination", "max_value"),

        Output("pagination", "active_page"),

        Output("record-count", "children"),

        Output("page-information", "children"),

        Input("pagination", "active_page"),

        Input("page-size", "value"),

        Input("submit-value", "n_clicks"),

        Input("submit-value2", "n_clicks"),

        State("input-on-submit", "value"),

        prevent_initial_call=True

    )

    def update_blockchain(
        active_page,
        page_size,
        add_clicks,
        delete_clicks,
        value
    ):

        from dash import ctx, no_update

        

        triggered = ctx.triggered_id

        # ----------------------------------------------
        # ADD BLOCK
        # ----------------------------------------------

        if triggered == "submit-value":
            


            if not value or not value.strip():

                return (
                    dbc.Alert(
                        "Please enter a valid value.",
                        color="warning"
                    ),
                    no_update,
                    no_update,
                    no_update,
                    no_update
                )

            list_of_strings.append(value.strip())

            active_page = 1

        # ----------------------------------------------
        # DELETE ALL BLOCKS
        # ----------------------------------------------

        elif triggered == "submit-value2":

            
            return (
                dbc.Alert(
                    "All blockchain records have been deleted.",
                    color="success"
                ),
                1,
                1,
                "Total Records: 0",
                "Page 1 of 1"
            )

        # ----------------------------------------------
        # GENERATE BLOCKCHAIN
        # ----------------------------------------------

        blockchains = create_blockchains(list_of_strings)

        total_records = len(blockchains)

        # ----------------------------------------------
        # CALCULATE TOTAL PAGES
        # ----------------------------------------------

        total_pages = max(
            1,
            math.ceil(total_records / page_size)
        )

        # Ensure current page is valid
        active_page = min(
            max(active_page or 1, 1),
            total_pages
        )

        # ----------------------------------------------
        # PAGINATION INDEX
        # ----------------------------------------------

        start_index = (active_page - 1) * page_size

        end_index = start_index + page_size

        paginated_blocks = blockchains[
            start_index:end_index
        ]

        # ----------------------------------------------
        # DISPLAY BLOCKCHAIN RECORDS
        # ----------------------------------------------

        components = []

        for index, block in enumerate(
            paginated_blocks,
            start=start_index + 1
        ):

            component = dbc.Card(

                dbc.CardBody(
                    [

                        html.H5(
                            f"Block #{index}",
                            className="card-title"
                        ),

                        *[
                            html.P(
                                f"{key}: {val}",
                                style={
                                    "wordBreak": "break-word"
                                }
                            )
                            for key, val in block.items()
                        ]

                    ]
                ),

                className="mb-3"

            )

            components.append(component)

        if not components:

            components = [
                dbc.Alert(
                    "No blockchain records available.",
                    color="info"
                )
            ]

        # ----------------------------------------------
        # RECORD COUNT
        # ----------------------------------------------

        record_count = html.H6(
            f"Total Records: {total_records}"
        )

        # ----------------------------------------------
        # PAGE INFORMATION
        # ----------------------------------------------

        page_information = (
            f"Showing records {start_index + 1} "
            f"to {min(end_index, total_records)} "
            f"of {total_records}"
            if total_records > 0
            else "No records available"
        )

        page_information += (
            f" | Page {active_page} of {total_pages}"
        )

        return (
            components,
            total_pages,
            active_page,
            record_count,
            page_information
        )

    return app


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app = create_app()

    app.run(debug=True)
