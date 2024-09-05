from dash import Dash, html, dcc, Output, Input, State
import pandas as pd
import plotly.express as px
app = Dash(__name__)

server = app.server


# Load your data
xls = pd.ExcelFile('LCT.xlsx')
pangsa = pd.read_excel(xls, 'Pangsa Transaksi')
nasabah = pd.read_excel(xls, 'Total Pelaku Looker')
avgNasabah = pd.read_excel(xls, 'Rerata Nasabah LCT Bulanan')
transaksi = pd.read_excel(xls, 'Total Transaksi Looker')
avgTransaksi = pd.read_excel(xls, 'Rerata Transaksi LCT Bulanan')



def visualize_line(data_sheet, xaxis, yaxis, title):
    data_sheet.columns = data_sheet.iloc[0].astype(str)
    data_sheet = data_sheet.iloc[1:]
    data_sheet = data_sheet.dropna(subset=['Negara'])

    # Melt the DataFrame to long format
    tabel = pd.melt(data_sheet, id_vars=['Negara'], var_name='Year', value_name='Value')

    # Rename columns
    tabel.rename(columns={'Negara': 'Country'}, inplace=True)

    # Filter out "Grand Total" values in the 'Year' column
    tabel = tabel[tabel['Year'] != 'Grand Total']
    tabel = tabel[tabel['Country'] != 'Grand Total']

    # Change 'Year' column to datetime
    tabel['Year'] = tabel['Year'].astype(float).astype(int)  # Convert to integer
    tabel['Year'] = pd.to_datetime(tabel['Year'], format='%Y')  # Convert to datetime

    fig = px.line(tabel, x='Year', y='Value', title=title, color='Country', width=1000, height=600, markers=True)

    # Center title and customize axis names
    fig.update_layout(
        title_x=0.5,
        xaxis_title=xaxis,
        yaxis_title=yaxis
    )

    return fig

def visualize_bar(data_sheet, xaxis, yaxis, title):
    data_sheet.columns = data_sheet.iloc[0].astype(str)
    data_sheet = data_sheet.iloc[1:]
    data_sheet = data_sheet.dropna(subset=['Negara'])

    # Melt the DataFrame to long format
    tabel = pd.melt(data_sheet, id_vars=['Negara'], var_name='Year', value_name='Value')

    # Rename columns
    tabel.rename(columns={'Negara': 'Country'}, inplace=True)

    # Filter out "Grand Total" values in the 'Year' column
    tabel = tabel[tabel['Year'] != 'Grand Total']
    tabel = tabel[tabel['Country'] != 'Grand Total']

    # Change 'Year' column to datetime
    tabel['Year'] = tabel['Year'].astype(float).astype(int)  # Convert to integer
    tabel['Year'] = pd.to_datetime(tabel['Year'], format='%Y')  # Convert to datetime

    fig = px.bar(tabel, x='Year', y='Value', title=title, color='Country', width=1000, height=600, barmode='group')

    # Center title and customize axis names
    fig.update_layout(
        title_x=0.5,
        xaxis_title=xaxis,
        yaxis_title=yaxis,
        legend=dict(
            title=None,
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Align the legend to the bottom
            y=-0.2,  # Position the legend below the chart
            xanchor="center",  # Center the legend horizontally
            x=0.5  
        )
    )

    return fig


# Define the app layout with a closeable sidebar and main content
app.layout = html.Div(style={'display': 'flex'}, children=[
    # Sidebar container
    html.Div(id='sidebar', style={'width': '20%', 'padding': '20px', 'background-color': '#f4f4f4', 'display': 'block'}, children=[
        html.Img(src='assets/BI_Logo.png', style={'width': '100%', 'height': 'auto'}),
        html.Button('Close Sidebar', id='close-sidebar-button', n_clicks=0),
        html.H2('Sidebar'),
        html.Hr(),
        html.Label('Negara'),
        dcc.Dropdown(['Jepang', 'Malaysia', 'Thailand', 'Tiongkok'], multi=True,placeholder='Pilih Negara'),
        html.Br(),
        html.Label('Tahun'),
        dcc.Dropdown(['2018', '2019', '2020', '2021', '2022', '2023', '2024'],multi=True,placeholder='Pilih Tahun'),
        


    ]),

    # Main content container
    html.Div(style={'width': '80%', 'padding': '20px'}, children=[
        html.Button('Open Sidebar', id='open-sidebar-button', n_clicks=0, style={'display': 'none'}),
        html.H1(children='LCT Overview',style={'margin-left': '50px'}),

        # Div container with flexbox to align graphs side by side
        html.Div([
            dcc.Graph(
                id='example-graph',
                figure=visualize_bar(transaksi, 'Year', 'Total Transaksi', 'Total Transaksi')
            ),
            dcc.Graph(
                id='example-graph2',
                figure=visualize_bar(nasabah, 'Year', 'Total Nasabah', 'Total Nasabah')
            )
        ], style={'display': 'flex', 'flex-direction': 'row'}),  # Flexbox style to align side by side

        # New row for additional graphs
        html.Div([
            dcc.Graph(
                id='example-graph3',
                figure=visualize_bar(avgNasabah, 'Year', 'Average Nasabah', 'Average Nasabah')
            ),
            dcc.Graph(
                id='example-graph4',
                figure=visualize_bar(avgTransaksi, 'Year', 'Average Transaksi', 'Average Transaksi')
            )
        ], style={'display': 'flex', 'flex-direction': 'row'})  # Flexbox style to align the new graphs side by side
    ])
])

# Callbacks for toggling sidebar
@app.callback(
    Output('sidebar', 'style'),
    Output('open-sidebar-button', 'style'),
    Input('close-sidebar-button', 'n_clicks'),
    Input('open-sidebar-button', 'n_clicks'),
    State('sidebar', 'style')
)
def toggle_sidebar(n_clicks_close, n_clicks_open, sidebar_style):
    # Determine which button was clicked
    if n_clicks_close > n_clicks_open:
        return {'width': '20%', 'padding': '20px', 'background-color': '#f4f4f4', 'display': 'none'}, {'display': 'block'}
    elif n_clicks_open > n_clicks_close:
        return {'width': '20%', 'padding': '20px', 'background-color': '#f4f4f4', 'display': 'block'}, {'display': 'none'}
    return sidebar_style, {'display': 'none' if sidebar_style['display'] == 'block' else 'block'}

if __name__ == '__main__':
    app.run(debug=True)
