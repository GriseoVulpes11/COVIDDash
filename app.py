from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import requests
import plotly.express as px

response = requests.get("https://api.covid19api.com/live/country/united-states")
DATA = response.json()

fig = px.line(DATA, x="Date", y="Confirmed", title="New Confirmed Cases by Country",
              color="Province")

state_name_list = []
for state_data in DATA:
    state_name_list.append(state_data['Province'])

app = Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    dcc.Markdown(
        id="title",
        children="COVID Dashboard"

    ),

    dcc.Dropdown(
        id="country_select_dropdown",
        options=state_name_list,
        value=['Colorado'],
        multi=True
    ),

    dcc.Graph(
        id="country_bar_graph",
        figure=fig
    ),
    dcc.RadioItems(
        id="radio_data_select",
        options=['Confirmed', 'Deaths', 'Recovered', 'Active'],
        value="Confirmed"
    )
])


@app.callback(
    Output("country_bar_graph", "figure"),
    Input("country_select_dropdown", "value"),
    Input("radio_data_select", "value")
)
def update_country_graph(state_name,data_select):
    records_to_display = []
    for curr_country in DATA:
        if curr_country['Province'] in state_name:
            records_to_display.append(curr_country)
    return px.line(records_to_display, x="Date", y=data_select, title=f"COVID-19 {data_select} by State",
                   color="Province")


if __name__ == '__main__':
    app.run_server(debug=True)
