import base64
import io
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

avocado = pd.read_csv('avocado-updated-2020.csv')

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select CSV Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id="output-data-upload"),
    html.H1(children='Avocado Prices Dashboard'),
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label': i, 'value': i}
                          for i in avocado['geography'].unique()],
                 value='New York'),
    # dcc.Graph(id='price-graph')

])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, filename):
    if contents is not None:
        for content, name in zip(contents, filename):
            save_file(content, name)
        return html.Div(['File(s) uploaded successfully.'])


def save_file(contents, filename):
    # Decode and read the contents of the uploaded file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Use pandas to read the CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            # Save the file to the server
            df.to_csv('uploaded_files/' + filename, index=False)
            print('File saved: ', filename)
        else:
            print('Invalid file format')
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])


# @app.callback(
#     Output(component_id='price-graph', component_property='figure'),
#     Input(component_id='geo-dropdown', component_property='value'))
# def update_graph(selected_geography):
#     filtered_avocado = avocado[avocado['geography'] == selected_geography]
#     line_fig = px.line(filtered_avocado,
#                        x='date', y='average_price',
#                        color='type',
#                        title=f'Avocado Prices in {selected_geography}')
#     return line_fig


if __name__ == '__main__':
    app.run(debug=True, host="localhost")
