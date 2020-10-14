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

def limitStr(s : str):
    min = len(s) if len(s) < 20 else 20
    return s[0:min]+"..."

@app.callback(
    Output('stats-graph', 'figure'),
    [Input('url-button', 'n_clicks')],
    [State('url-input', 'value'), State('limit-input', 'value')])
def onBtnClick(n_clicks, url, limit):
    if (url != ""):
        channel = c.Channel(url)
        global isLoading
        isLoading = True
        data = channel.getArticlesStats(int(limit)) if (limit != "" and limit.isdigit()) else channel.getArticlesStats()
        isLoading = False
        titles = list(map(limitStr, data["names"]))
        fig = go.Figure(data=[go.Scatter(y=data["views"], x=titles,
            mode="lines+markers", name = "Views")])
        fig.add_trace(go.Scatter(y=data["readings"], x=titles,
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

    

#https://zen.yandex.ru/id/5eba7f439f339d116671be06

# class GUI:

#     app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

#     def __init__(self):
#         color = ['#292d3e', '#c3e88d']
#         self.app.layout = html.Div(style = { 'color' : color[0]},
#             children = html.Div(style = {'display' : 'block', 'margin' : '0 auto',
#             'padding' : '30px 0px', 'width' : '100%', 'max-width' : '1300px',},
#             children = [
#                 html.H1(style = {'text-align' : 'center', 'margin' : '0'}, children = "Yandex zen parser"),
#                 html.H6(style = {'text-align' : 'center', 'margin-bottom' : '50px'}, children = "By GTX1060"),
#                 html.H5(children = "Enter link to the Zen channel:"),
#                 html.Div(style = {'display' : 'inline-block', 'margin' : '15px 0px'}, children = [
#                 dcc.Input(style = {'margin-right' : '15px'}, id='url-input', value='URL', type='text'),
#                 html.Button(id='url-button', children='Go', n_clicks=0)]),
#                 dcc.Graph(id='stats-graph')
#         ]))
    
#     @classmethod
#     @app.callback(
#         Output('stats-graph', 'figure'),
#         [Input('url-button', 'n_clicks')],
#         [State('url-input', 'value')])
#     def onBtnClick(n_clicks, url):
#         fig = go.Figure(data=[go.Scatter(x=[1, 2, 3],  y=[4, 1, 2])])
#         fig.update_layout(transition_duration=500)
#         return fig

#     def runGUI(self):
#         self.app.run_server(debug=True)

# g = GUI()
# g.runGUI()

#table = export.Table(''.join([a for a in channel.channelName if a.isalpha()]))
#table.addColumn(data["names"], "Names")
#table.addColumn(data["views"], "Views")
#table.addColumn(data["readings"], "Readings")
#table.addColumn(data["comments"], "Comments")
#table.addColumn(data["viewTime"], "Time")
#table.addChart("views", [],[],{"B1" : f"B{len(data['views'])}"})
#table.close()