import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# Sample Data
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 11, 12, 13, 14]
})

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout with scatter plot and hidden questionnaire modal
app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        figure=px.scatter(df, x='x', y='y')
    ),
    dbc.Modal(
        [
            dbc.ModalHeader("Questionnaire"),
            dbc.ModalBody([
                dbc.Label("Question 1"),
                dbc.Input(type="text", placeholder="Your answer here", id="answer1"),
                # Add more questions here
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="ml-auto")
            ),
        ],
        id="questionnaire-modal",
        is_open=False,
    )
])

# Callback to open questionnaire on scatter plot click
@app.callback(
    Output("questionnaire-modal", "is_open"),
    [Input("scatter-plot", "clickData"), Input("close-modal", "n_clicks")],
    [State("questionnaire-modal", "is_open")]
)
def toggle_modal(clickData, close_click, is_open):
    if clickData or close_click:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run_server(debug=True)
