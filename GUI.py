import dash
import dash_core_components as dcc
import dash_html_components as html

class Gui:

    @staticmethod
    def getMarkup():
        color = ['#292d3e', '#c3e88d']
        return html.Div(style = { 'color' : color[0]},
            children = html.Div(style = {'display' : 'block', 'margin' : '0 auto',
            'padding' : '30px 0px', 'width' : '100%', 'max-width' : '1300px',},
            children = [
                html.H1(style = {'text-align' : 'center', 'margin' : '0'}, children = "Yandex zen parser"),
                html.H6(style = {'text-align' : 'center', 'margin-bottom' : '50px'}, children = "By GTX1060"),
                html.H5(children = "Enter link to the Zen channel and articles limit:"),
                html.Div(style = {'display' : 'inline-block', 'margin' : '15px 0px'}, children = [
                dcc.Input(style = {'margin-right' : '15px'}, id='url-input', value='', type='text'),
                dcc.Input(style = {'margin-right' : '15px', 'width' : '40px'}, id='limit-input', value='', type='text'),
                html.Button(id='url-button', children='Go', n_clicks=0)]),
                dcc.Loading(
                    id="load-indicator",
                    type="graph",
                    style= {'padding-bottom' : '30px'}
                ),
                dcc.Graph(id='stats-graph', style= {'margin-top' : '70px', 'height' : '1000px'})
        ]))
    