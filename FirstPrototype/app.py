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

calculator = CalculateBias()
classifier = ResumeeClassifier()

def getVacancies():    
    x = []
    for file in glob.glob("./job_vacancies/*.txt"):
        res = str(file).split('/')[-1]
        x.append(res)
    return x


body = html.Div([
    html.Div([
        html.Div( [
                html.H2('Select a job advertisement'),
                dcc.Dropdown(
                    id='dropdown',
                    options=[{'label': i, 'value': i} for i in getVacancies()],
                    value=''
                ),
                html.Div(id='display-bias'),
            ], className="job_selector"),
            html.Div( [
                html.H2('The resumee'),
            dcc.Input(id='resume-name', type='text', placeholder='name'),
            dcc.Textarea(id='resume-skills', placeholder="skills"),
            dcc.Textarea(id='resume-experience', placeholder="experience"),
            dcc.Textarea(id='resume-education', placeholder="education"),
            dcc.Textarea(id='resume-qualities', placeholder="personal qualities"),
            html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
            html.Div(id='output-state', className="result"),
            html.Div(id='output-text', className="error_text"),
            html.Div(id='output-button'),
            ], className="job_resumee"),
           
    ], className="wrapper")
    
    # html.Div([
    #     html.Div([
    #         html.H2('Masculine-biased words', className="bias__title"),
    #         html.Ul(id='output-male')
    #     ], className="bias__male"),
    #     html.Div([
    #         html.H2('Feminine-biased words', className="bias__title"),
    #         html.Ul(id='output-female')
    #     ], className="bias__female"),
    # ], className="bias"),
])

def display_bias(value):
    bias = calculator.returnBias(value)
    print(bias)
    if bias:
        classification = bias
        return (classification)
    else: 
        return None

def classify_resumee(dropdown, n_clicks, input1, input2, input3, input4, input5):
    classification = classifier.classify(input1, input2, input3, input4, input5)
    if(dropdown is not None):
        if len(dropdown)>0:
            bias = calculator.returnBias(dropdown)
            print(bias, classification)
            if(classification is None):
                return ({'background-color': 'white'}, 'Please fill in a resumee', '')
                # return u'''
                #     The Button has been pressed {} times,
                #     Input 1 is "{}",
                #     and Input 2 is "{}",
                #     and Input 3 is "{}",
                #     and Input 4 is "{}",
                #     and Input 5 is "{}"
                # '''.format(n_clicks, input1, input2, input3, input4, input5,
            else:
                if(bias == 'feminine-biased' and classification == 'female'):
                    return ({'background-color': 'green'}, 'yay1', dcc.Link('got it!', href='/finish.py') )
                elif(bias == 'masculine-biased' and classification == 'male'):
                    return ({'background-color': 'red'}, 'Try again.', dcc.Link('got it!', href='/finish.py') )
                else:
                    return ({'background-color': 'red'}, 'nope1', '')    
        else:
            if(n_clicks is 1):
                return ({'background-color': 'white'},'Try improving, this was your first try', '')
            else:
                return ({'background-color': 'white'}, 'Please fill in a job vacancy & a resumee', '')
    else:
        return ({'background-color': 'red'}, 'You did not select a job vacancy','')


def Game():
    return body

app.layout = Game()

if __name__ == '__main__':
    app.run_server(debug=True)
