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
     dcc.Input(id='username', type='text', placeholder='Your (user)name'),
    html.Button(id='submit-button-score', n_clicks=0, children='Submit'),
     html.Ul(id='score-output')
])

def Finish():
    return body

app.layout = Finish()

def updateScoreboard(name, n_clicks):
    if(name is not None):
        if len(name)>0:
            if(n_clicks>0):
                score = (html.Li('1. Noa'), html.Li('2. Stan'), html.Li('3. {}'.format(name)))
                return(score)

if __name__ == '__main__':
    app.run_server(debug=True)
