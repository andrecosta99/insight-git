import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, html
from dash.exceptions import PreventUpdate

from .plugin_loader import load_plugins
from .utils import clone_remote_repo

# Mapping of plugin identifiers to their display titles
PLUGIN_TITLES = {
    "git_statistics": "Git Statistics",
    "commit_graph": "Commit Graph",
    "branch_information": "Branch Information",
    "commit_type": "Commit Type",
    "contributors": "Project Contributors",
    "code_quality": "Python Code Quality",
}


@callback(
    Output("url-error-message", "children"),
    Output("plugin-error-message", "children"),
    Input("load-repo-button", "n_clicks"),
    State("repo-input", "value"),
    State("plugin-selector", "value"),
    prevent_initial_call=True,
)
def validate_input(n_clicks, url, selected_plugins):
    """
    Validates the input fields. Checks if the repository URL is entered
    and at least one plugin is selected. Returns error messages accordingly.

    Args:
        n_clicks (int): The number of times the load repository button was clicked.
        url (str): The URL of the Git repository.
        selected_plugins (list): The selected plugins.

    Returns:
        tuple: Tuple containing URL error message and plugin error message.
    """
    url_error = ""
    plugin_error = ""
    if not url:
        url_error = "Please enter a repository URL."
    if not selected_plugins:
        plugin_error = "Please select at least one plugin."
    return url_error, plugin_error


def register_callbacks(app):
    """
    Registers callbacks in the application. Handles the interactions in the application,
    including validating inputs and updating the plugin output area based on the
    selected plugins and repository URL.

    Args:
        app (Dash app): The Dash application instance where callbacks will be registered.
    """

    @app.callback(
        Output("plugin-output-area", "children"),
        [Input("load-repo-button", "n_clicks")],
        [State("repo-input", "value"), State("plugin-selector", "value")],
    )
    def update_plugin_output(n_clicks, repo_url, selected_plugins):
        """
        Updates the plugin output based on user interactions. Clones the repository,
        loads the selected plugins, and updates the output area with the results
        from each plugin.

        Args:
            n_clicks (int): The number of times the load repository button was clicked.
            repo_url (str): The URL of the Git repository to analyze.
            selected_plugins (list): The selected plugins for analysis.

        Returns:
            list: A list of Dash components representing the output from each selected plugin.
        """
        if n_clicks is None or n_clicks < 1 or not repo_url or not selected_plugins:
            raise PreventUpdate

        loading_message = html.Div(
            "Data is updated",
            style={"textAlign": "center", "marginTop": "14px", "marginBottom": "20px"},
        )

        repo_path = clone_remote_repo(repo_url)
        if repo_path is None:
            return [html.Div("Failed to clone the repository.")]

        plugins = load_plugins()
        plugin_outputs = [loading_message]

        for plugin_name in selected_plugins:
            plugin_function = plugins.get(plugin_name)
            if plugin_function:
                try:
                    plugin_output = plugin_function(repo_path)
                    card_title = PLUGIN_TITLES.get(
                        plugin_name, plugin_name.replace("_", " ").title()
                    )
                    card = dbc.Card(
                        [dbc.CardHeader(card_title), dbc.CardBody([plugin_output])],
                        className="mb-4",
                    )
                    plugin_outputs.append(card)
                except Exception as e:
                    plugin_outputs.append(html.Div(f"Error loading {plugin_name}: {e}"))

        return plugin_outputs
