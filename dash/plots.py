"""
plots.py: 데이터 시각화를 위한 플롯 생성 모듈.

이 모듈은 파이 차트, 막대 차트, 분포 플롯, 상관관계 히트맵 등 다양한 플롯을 생성하는 함수를 포함한 스크립트
각 함수는 Pandas DataFrame + a를 입력으로 받고, Plotly 그래프 객체를 반환
"""

import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs
import pandas as pd
import numpy as np

def create_pie_chart(df : pd.DataFrame) -> plotly.graph_objs:
    '''
        pie chart를 리턴하는 함수

        Args:
            df(pd.DataFrame) : 입력 DataFrame

        Returns:
            fig_pie(plotly.graph_objs)
    '''
    pie = df.groupby('target').count()['id'] / len(df)

    fig_pie = px.pie(pie.reset_index(),
                    values='id',
                    names='target',
                    hole=0.3,
                    color_discrete_sequence=['#bad6eb', '#2b7bba'],
                    )

    fig_pie.update_layout(
        autosize=True,
        margin=dict(l=30, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
        
    )
    return fig_pie

def create_bar_chart(df:pd.DataFrame, cat_pick:str) -> plotly.graph_objs:
    '''
        bar chart를 리턴하는 함수

        Args:
            df(pd.DataFrame) : 입력 DataFrame
            cat_pick(str) : x축 string
            
        Returns:
            fig_bar(plotly.graph_objs)
    '''
    fig_bar = px.bar(df,
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
    return fig_bar

def create_dist_plot(df:pd.DataFrame, cont_pick:str) -> plotly.graph_objs:
    '''
        dist chart를 리턴하는 함수

        Args:
            df(pd.DataFrame) : 입력 DataFrame
            cont_pick(str) : y값 string
            
        Returns:
            fig_dist(plotly.graph_objs)
    '''
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
    return fig_dist

def create_corr_heatmap(df:pd.DataFrame, corr_pick:list) -> plotly.graph_objs:
    '''
        corr chart를 리턴하는 함수

        Args:
            df(pd.DataFrame) : 입력 DataFrame
            corr_pick(list) : 선택한 변수값 list
            
        Returns:
            fig_corr(plotly.graph_objs)
    '''
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
