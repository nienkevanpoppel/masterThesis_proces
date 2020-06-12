import os
import glob
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from calculate_bias import CalculateBias
from ResumeClassifier import ResumeeClassifier

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

server = app.server

body = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div("hello!", className="wrapper"),
    dcc.Link('got it!', href='/app.py'),
])

def Home():
    return body

app.layout = Home()

if __name__ == '__main__':
    app.run_server(debug=True)
