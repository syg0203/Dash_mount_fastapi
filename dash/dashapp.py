import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.figure_factory as ff

def create_dash_app(requests_pathname_prefix: str = '/') -> dash.Dash:
    df = pd.read_csv('data/data_sample.csv')
    vars_cat = [var for var in df.columns if var.startswith('cat')]
    vars_cont = [var for var in df.columns if var.startswith('cont')]

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # pie chart
    pie = df.groupby('target').count()['id'] / len(df)

    fig_pie = px.pie(pie.reset_index(),
                    values='id',
                    names='target',
                    hole=0.3,
                    color_discrete_sequence=['#bad6eb', '#2b7bba'],
                    )

    fig_pie.update_layout(
        width=320,
        height=250,
        margin=dict(l=30, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
        
    )

    # sidebar section 생성 (setting(1):(graph)10:(variables)9
    sidebar = html.Div(
        [
            dbc.Row(
                dbc.Col(html.H5('Settings', className='text-white font-italic', style={'margin-top': '12px'}), 
                        
                        width=12, 
                        className='bg-primary'),
                style={"height": "auto"}
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                    html.Img(src='https://avatars.githubusercontent.com/u/79491796?v=4',
                             style={'max-width': '90%', 'max-height': '45vh', 'height': 'auto', 'width': 'auto'}),
                    style={'text-align': 'center'}),
                    width=12
                ),
                style={"height": "auto"}
            ),
            dbc.Row(
                [
                    dbc.Col([
                        html.P('bar 변수', className='font-weight-bold'),
                        dcc.Dropdown(id='my-cat-picker', multi=False, value='cat0',
                                    options=[{'label': x, 'value': x} for x in vars_cat]),
                        html.P('line 변수', className='font-weight-bold', style={'margin-top': '16px'}),
                        dcc.Dropdown(id='my-cont-picker', multi=False, value='cont0',
                                    options=[{'label': x, 'value': x} for x in vars_cont]),
                        html.P('heatmap 변수', className='font-weight-bold', style={'margin-top': '16px'}),
                        dcc.Dropdown(id='my-corr-picker', multi=True, value=vars_cont + ['target'],
                                    options=[{'label': x, 'value': x} for x in vars_cont + ['target']]),
                        html.Button(id='my-button', n_clicks=0, children='적용하기',
                                    className='btn btn-dark mt-3'),
                        html.Hr()
                    ], width=12)
                ],
                style={'margin': '8px'}
            ),
            dbc.Row(
                [
                    dbc.Col([
                        html.P('선택 변수', className='font-weight-bold'),
                        dcc.Graph(figure=fig_pie, responsive=True)
                    ], width=12)
                ],
                style={"height": "45vh", 'margin': '8px'}
            )
        ]
    )

        # content section 생성
    content = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div([
                            html.P(id='bar-title', className='font-weight-bold'),
                            dcc.Graph(id="bar-chart", responsive=True)
                        ]),
                        md=6, lg=6  # 중간 및 큰 화면에서 6열 너비
                    ),
                    dbc.Col(
                        html.Div([
                            html.P(id='dist-title', className='font-weight-bold'),
                            dcc.Graph(id="dist-chart", responsive=True)
                        ]),
                        md=6, lg=6  # 중간 및 큰 화면에서 6열 너비
                    )
                ],
                style={'margin': '16px 8px'}
            ),
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.P('heatmap', className='font-weight-bold'),
                        dcc.Graph(id='corr-chart', responsive=True)
                    ]),
                    md=12  # 모든 화면 크기에서 12열 너비
                ),
                style={'margin': '8px'}
            )
        ]
    )

    app.layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(sidebar, md=12, lg=3, className='bg-light'),  # 중간 화면에서는 전체 너비, 큰 화면에서는 3열 너비
                    dbc.Col(content, md=12, lg=9)  # 중간 화면에서는 전체 너비, 큰 화면에서는 9열 너비
                ]
            ),
        ],
        fluid=True
    )


    @app.callback(Output('bar-chart', 'figure'),
                Output('bar-title', 'children'),
                Input('my-button', 'n_clicks'),
                State('my-cat-picker', 'value'))
    def update_bar(n_clicks, cat_pick):
        bar_df = df.groupby(['target', cat_pick]).count()['id'].reset_index()
        bar_df['target'] = bar_df['target'].replace({0: 'target=0', 1: 'target=1'})

        fig_bar = px.bar(bar_df,
                        x=cat_pick,
                        y="id",
                        color="target",
                        color_discrete_sequence=['#bad6eb', '#2b7bba'])

        fig_bar.update_layout(
            margin=dict(l=40, r=20, t=20, b=30),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend_title=None,
            yaxis_title=None,
            xaxis_title=None,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        title_bar = '선택 변수 : ' + cat_pick

        return fig_bar, title_bar


    @app.callback(Output('dist-chart', 'figure'),
                Output('dist-title', 'children'),
                Input('my-button', 'n_clicks'),
                State('my-cont-picker', 'value'))
    def update_dist(n_clicks, cont_pick):
        num0 = df[df['target'] == 0][cont_pick].values.tolist()
        num1 = df[df['target'] == 1][cont_pick].values.tolist()

        fig_dist = ff.create_distplot(hist_data=[num0, num1],
                                    group_labels=['target=0', 'target=1'],
                                    show_hist=False,
                                    colors=['#bad6eb', '#2b7bba'])

        fig_dist.update_layout(width=500,
                            height=340,
                            margin=dict(t=20, b=20, l=40, r=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            ))

        title_dist = '선택 변수 : ' + cont_pick

        return fig_dist, title_dist


    @app.callback(Output('corr-chart', 'figure'),
                Input('my-button', 'n_clicks'),
                State('my-corr-picker', 'value'))
    def update_corr(n_clicks, corr_pick):
        df_corr = df[corr_pick].corr()
        x = list(df_corr.columns)
        y = list(df_corr.index)
        z = df_corr.values

        fig_corr = ff.create_annotated_heatmap(
            z,
            x=x,
            y=y,
            annotation_text=np.around(z, decimals=2),
            hoverinfo='z',
            colorscale='Blues'
        )

        fig_corr.update_layout(width=1040,
                            height=300,
                            margin=dict(l=40, r=20, t=20, b=20),
                            paper_bgcolor='rgba(0,0,0,0)'
                            )

        return fig_corr
    return app

if __name__ == "__main__":
    app=create_dash_app()
    app.run_server() # 디버그 모드 추가
