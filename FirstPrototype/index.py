import os
import glob
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import flask

from calculate_bias import CalculateBias
from ResumeClassifier import ResumeeClassifier
from app import Game, display_bias, classify_resumee 
from finish import Finish, updateScoreboard
from homepage import Home

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

server = app.server

calculator = CalculateBias()
classifier = ResumeeClassifier()

layout1 = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id='page-content')
])

def serve_layout():
    if flask.has_request_context():
        return layout1
    return html.Div([
        layout1,
        Home(),
        Game()
    ])


app.layout = serve_layout

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

def display_page(pathname):
    if pathname=='/app.py':
        return Game()
    elif pathname=='/finish.py':
        return Finish()
    else:
        return Home()


@app.callback(Output('display-bias', 'children'), 
                [Input('dropdown', 'value')])

def update_jobVacancy(value):
    bias = display_bias(value)
    return bias



@app.callback([Output('output-state', 'style'),
                Output('output-text', 'children'),
                 Output('output-button', 'children')],
              [Input('dropdown', 'value'),
              Input('submit-button-state', 'n_clicks')],
              [State('resume-name', 'value'),
               State('resume-skills', 'value'),
               State('resume-experience', 'value'),
               State('resume-education', 'value'),
               State('resume-qualities', 'value')])

def update_resumee(dropdown, n_clicks, input1, input2, input3, input4, input5):
    classification = classify_resumee(dropdown, n_clicks, input1, input2, input3, input4, input5)
    return classification


@app.callback(Output('score-output', 'children'), 
                [Input('username', 'value'),
                Input('submit-button-score', 'n_clicks')])

def update_scoreboard(value, n_clicks):
    score = updateScoreboard(value, n_clicks)
    return score

if __name__ == '__main__':
    app.run_server(debug=True)