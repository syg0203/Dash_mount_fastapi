"""
example1.py: 메인 Dash 애플리케이션 스크립트.

이 스크립트는 Dash 애플리케이션을 초기화하고, 위에서 정의된 plots.py 및 dashboard_layout.py 모듈을 사용하여
애플리케이션의 레이아웃과 기능을 구성합니다. 이 스크립트는 애플리케이션을 실행하는 데 사용됩니다.

TODO 1 : read_csv가 아닌 쿼리 형식으로 변경
"""

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs

import pandas as pd

from plots import create_bar_chart, create_corr_heatmap, create_dist_plot, create_pie_chart
from dashboard_layout import create_sidebar, create_content

def create_dash_app(requests_pathname_prefix: str = '/') -> dash.Dash:
    '''
        Dash app 생성 함수

        Args:
            requests_pathname_prefix(str) : Dash prefix 경로

        Returns:
            app(dash.Dash) : 구성된 Dash return
    '''
    # 쿼리로 대체
    df = pd.read_csv('data/data_sample.csv')
    vars_cat = [var for var in df.columns if var.startswith('cat')]
    vars_cont = [var for var in df.columns if var.startswith('cont')]

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],requests_pathname_prefix=requests_pathname_prefix)

    # pie chart
    fig_pie = create_pie_chart(df)
    # sidebar section 생성 (setting(1):(graph)10:(variables)9
    sidebar = create_sidebar(vars_cat=vars_cat,vars_cont=vars_cont,fig_pie=fig_pie)
    # content section 생성
    content = create_content()

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
                Input('my-cat-picker', 'value'))
    def update_bar(cat_pick:str) -> (plotly.graph_objs,str):
        '''
            bar chart 생성 함수

            Args:
                cat_pick(str) : Dropbox를 통해 선택한 변수

            Returns:
                fig_bar(graph_objs) : 구성된 bar return
                title_bar(str) : 선택한 변수 기반 barchart title
        '''
        bar_df = df.groupby(['target', cat_pick]).count()['id'].reset_index()
        bar_df['target'] = bar_df['target'].replace({0: 'target=0', 1: 'target=1'})

        fig_bar = create_bar_chart(bar_df, cat_pick)

        title_bar = '선택 변수 : ' + cat_pick

        return fig_bar, title_bar


    @app.callback(Output('dist-chart', 'figure'),
                Output('dist-title', 'children'),
                Input('my-cont-picker', 'value'))
    def update_dist(cont_pick:str) -> (plotly.graph_objs,str):
        '''
            dist chart 생성 함수

            Args:
                cont_pick(str) : Dropbox를 통해 선택한 변수

            Returns:
                fig_dist(graph_objs) : 구성된 disk return
                title_dist(str) : 선택한 변수 기반 distchart title
        '''
        fig_dist=create_dist_plot(df, cont_pick)

        title_dist = '선택 변수 : ' + cont_pick

        return fig_dist, title_dist


    @app.callback(Output('corr-chart', 'figure'),
                Input('my-corr-picker', 'value'))
    def update_corr(corr_pick : list) -> plotly.graph_objs:
        '''
            corr chart 생성 함수

            Args:
                corr_pick(list) : 선택한 변수 배열

            Returns:
                fig_corr(graph_objs) : 구성된 corr return
        '''
        fig_corr=create_corr_heatmap(df,corr_pick)

        return fig_corr
    return app

if __name__ == "__main__":
    '''
        디버그 모드
    '''
    app=create_dash_app('/')
    app.run_server() # 디버그 모드 추가
