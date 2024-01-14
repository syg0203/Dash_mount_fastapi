"""
dashboard_layout.py: 대시보드 레이아웃 구성 모듈.

이 모듈은 대시보드의 사이드바와 컨텐츠 영역을 구성하는 함수를 포함합니다.
각 함수는 필요한 인자를 받아 HTML 구성요소를 반환합니다.

TODO 1 : dbc.Col : 1개, 2개, 3개 별 스크립트(함수) 생성
TODO 2 : dbc.Row : 1개, 2개, 3개 별 스크립트(함수) 생성
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs

def create_sidebar(vars_cat:list, vars_cont:list, fig_pie:plotly.graph_objs) -> html:
    '''
        Sidebar 생성해주는 함수

        Args:
            vars_cat(list) : 그래프1 변수 선택 Dropbox list
            vars_cont(list) : 그래프2~3 변수 선택 Dropbox list

        Returns:
            sidebar(html)
    '''
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
    return sidebar

def create_content() -> html:
    '''
        Content 생성해주는 함수

        Returns:
            content(html)
    '''
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
    return content
