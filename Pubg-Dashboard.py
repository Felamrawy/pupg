
# # Pubg Dashboard

# Dashboard Sections:


import pandas as pd
#import numpy as np

#import matplotlib.pyplot as plt

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio

import warnings
warnings.filterwarnings('ignore') 

pio.renderers.default = 'notebook_connected' #for html export

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# %%
df = pd.read_csv('pubg-clean.csv')  

# %%

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])


# APP LAYOUT
app.layout = html.Div([
    html.Div([
        html.H1("PUBG Weapon Analytics Dashboard", style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        # Filters Section
        html.Div([
            html.Label("Filter by Weapon Type:"),
            dcc.Dropdown(
                id='weapon-type-filter',
                options=[{'label': i, 'value': i} for i in sorted(df['Weapon Type'].unique())],
                value=df['Weapon Type'].unique().tolist(),
                multi=True
            ),
        ], style={'padding': '20px', 'backgroundColor': "#B9DADF", 'borderRadius': '5px', 'marginBottom': '20px', 'color': "#000000"}),
    ], className="container"),

    #Tabs for different sections
    dcc.Tabs([
        # Tab 1: Overview
        dcc.Tab(label='1. Overview & Ranking', children=[
            html.Div([
                html.H3("Weapon Power Ranking (DPS)"),
                dcc.Graph(id='weapon-ranking-bar')
            ], style={'padding': '20px'})
        ]),

        # Tab 2: Combat Analysis
        dcc.Tab(label='2. Combat Analysis', children=[
            html.Div([
                html.H3("Lethality: DPS vs Time-To-Kill"),
                dcc.Graph(id='dps-ttk-scatter')
            ], style={'padding': '20px'})
        ]),

        # Tab 3: Ballistics
        dcc.Tab(label='3. Ballistics', children=[
            html.Div([
                html.H3("Ballistic Performance: Speed vs Range"),
                dcc.Graph(id='ballistics-scatter')
            ], style={'padding': '20px'})
        ]),

        # Tab 4: Efficiency
        dcc.Tab(label='4. Efficiency', children=[
            html.Div([
                html.H3("Damage Potential per Magazine"),
                dcc.Graph(id='mag-efficiency-bar')
            ], style={'padding': '20px'})
        ]),

        # Tab 5: Armour Analysis
        dcc.Tab(label='5. Armour Analysis', children=[
            html.Div([
                html.H3("Damage Reduction across Armour Levels"),
                dcc.RadioItems(
                    id='armour-type-selector',
                    options=[{'label': 'Body Damage', 'value': 'BDMG'}, {'label': 'Head Damage', 'value': 'HDMG'}],
                    value='BDMG',
                    labelStyle={'display': 'inline-block', 'marginRight': '20px'}
                ),
                dcc.Graph(id='armour-analysis-graph')
            ], style={'padding': '20px'})
        ]),
    ])
])

# CALLBACKS
@app.callback(
    [Output('weapon-ranking-bar', 'figure'),
     Output('dps-ttk-scatter', 'figure'),
     Output('ballistics-scatter', 'figure'),
     Output('mag-efficiency-bar', 'figure'),
     Output('armour-analysis-graph', 'figure')],
    [Input('weapon-type-filter', 'value'),
     Input('armour-type-selector', 'value')]
)
def update_dashboard(selected_types, armour_type):
    filtered_df = df[df['Weapon Type'].isin(selected_types)].sort_values('Damage Per Second', ascending=False)
    firearms_df = filtered_df[filtered_df['Weapon Class'] == 'Firearm']

    # Figure 1: Ranking
    fig_ranking = px.bar(
        filtered_df, x='Weapon Name', y='Damage Per Second',
        color='Weapon Type', title="Weapons Ranked by DPS"
    )

    # Figure 2: Combat Analysis
    y_col = 'TTK_chest'
    fig_combat = px.scatter(
        filtered_df, x='Damage Per Second', y='TTK_chest' if 'TTK_chest' in df.columns else 'Damage',
        color='Weapon Type', hover_name='Weapon Name',
        title="DPS vs Time-To-Kill (Lower TTK is better)",
        labels={'TTK_chest': 'Time to Kill (Chest)'}
    )
    if not filtered_df.empty:
        mean_x = filtered_df['Damage Per Second'].mean()
        mean_y = filtered_df[y_col].mean()

        # Add Crosshair Lines
        fig_combat.add_vline(x=mean_x, line_dash="dash", line_color="gray", opacity=0.5)
        fig_combat.add_hline(y=mean_y, line_dash="dash", line_color="gray", opacity=0.5)

        # Annotations (Positioned at corners relative to the data)
            # Bottom Right: High DPS, Low TTK
        fig_combat.add_annotation(x=filtered_df['Damage Per Second'].max(), y=filtered_df[y_col].min(),
                            text="<b>META MELTERS</b><br>High Power, Fast Kills", showarrow=False, 
                            yshift=15, xanchor='right', font=dict(color="green", size=10))

            # Bottom Left: Low DPS, Low TTK
        fig_combat.add_annotation(x=filtered_df['Damage Per Second'].min(), y=filtered_df[y_col].min(),
                            text="<b>PRECISION TOOLS</b><br>Efficient/Snipers", showarrow=False, 
                            yshift=15, xanchor='left', font=dict(color="blue", size=10))

            # Top Right: High DPS, High TTK
        fig_combat.add_annotation(x=filtered_df['Damage Per Second'].max(), y=filtered_df[y_col].max(),
                            text="<b>BULLET HOSES</b><br>High Pressure, Low Finish", showarrow=False, 
                            yshift=-15, xanchor='right', font=dict(color="orange", size=10))

            # Top Left: Low DPS, High TTK
        fig_combat.add_annotation(x=filtered_df['Damage Per Second'].min(), y=filtered_df[y_col].max(),
                            text="<b>HARASSERS</b><br>Low Lethality", showarrow=False, 
                            yshift=-15, xanchor='left', font=dict(color="red", size=10))
        


    # Figure 3: Ballistics
    fig_ballistics = px.scatter(
        firearms_df, x='Bullet Speed', y='Range',
        size='Damage', color='Weapon Type', hover_name='Weapon Name',
        title="Bullet Speed vs Effective Range"
    )

    # Figure 4: Efficiency
    fig_mag = px.bar(
        filtered_df.sort_values('Damage_per_mag', ascending=False),
        x='Weapon Name', y='Damage_per_mag', color='Bullet Type',
        title="Total Damage Output per Magazine"
    )

    # Figure 5: Armour Analysis (Subplots for Levels 0-3)
    fig_armour = make_subplots(rows=2, cols=2, subplot_titles=("Level 0", "Level 1", "Level 2", "Level 3"))
    for i in range(4):
        col_name = f'{armour_type}_{i}'
        r, c = (i // 2) + 1, (i % 2) + 1
        fig_armour.add_trace(
            go.Bar(x=filtered_df['Weapon Name'], y=firearms_df[col_name], name=f"Lvl {i}"),
            row=r, col=c
        )
    fig_armour.update_layout(height=700, title_text=f"{armour_type} Comparison by Protection Level", showlegend=False)

    return fig_ranking, fig_combat, fig_ballistics, fig_mag, fig_armour

# 4. RUN SERVER
if __name__ == '__main__':
    app.run(debug=True, port=8052)

# %% [markdown]
# dashboard link (local): http://127.0.0.1:8052
# 


