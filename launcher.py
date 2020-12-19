import matplotlib.pyplot as plt
import channel as c
import export
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as exp
from dash.dependencies import Input, Output, State
import GUI
import webbrowser
import time

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = GUI.Gui.getMarkup()
isLoading = False
articleCounter = 0

def limitStr(s : str):
    global articleCounter
    articleCounter += 1
    min = len(s) if len(s) < 20 else 20
    return "{0}. {1}...".format(articleCounter, s[0:min])

@app.callback(
    Output('stats-graph', 'figure'),
    [Input('url-button', 'n_clicks')],
    [State('url-input', 'value'), State('limit-input', 'value')])
def onBtnClick(n_clicks, url, limit):
    if (url != ""):
        channel = c.Channel(url)
        app.title = channel.channelName
        global isLoading
        isLoading = True
        data = channel.getArticlesStats(int(limit)) if (limit != "" and limit.isdigit()) else channel.getArticlesStats()
        isLoading = False
        #titles = list(map(limitStr, data["names"]))
        global articleCounter
        articleCounter = 0
        fig = go.Figure(data=[go.Scatter(y=data["views"], x=data["names"],
            mode="lines+markers", name = "Views")])
        fig.add_trace(go.Scatter(y=data["readings"], x=data["names"],
            mode="lines+markers", name = "Readings"))
        fig.update_layout(transition_duration=500)
        return fig
    return go.Figure(data=[go.Scatter()])

@app.callback(Output("load-indicator", "children"),[Input('url-button', 'n_clicks')])
def input_triggers_nested(n_clicks):
    time.sleep(1)
    while isLoading:
        time.sleep(1)

if ( __name__ == "__main__"):
    webbrowser.open("http://127.0.0.1:8050/", new=1)
app.run_server(debug=False)

    

