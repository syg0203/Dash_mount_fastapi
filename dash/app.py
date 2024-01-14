"""
app.py: 메인 Dash 애플리케이션 스크립트.

이 스크립트는 Dash 애플리케이션을 초기화하고, 위에서 정의된 plots.py 및 dashboard_layout.py 모듈을 사용하여
애플리케이션의 레이아웃과 기능을 구성합니다. 이 스크립트는 애플리케이션을 실행하는 데 사용됩니다.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from src import *

dashboard_li = ["example1"]

app = FastAPI()


@app.get("/health_check")
def get_status() -> dict:
    '''
        Health check를 하는 함수 endpoint : health_check

        Args:
            None

        Returns:
            dict
    '''
    return {"code": 200, "status":"running"}

@app.get("/")
def get_summary() -> dict:
    '''
        접속 메인 함수 endpoint : /

        Args:
            None

        Returns:
            dict
    '''
    links = [f"http://127.0.0.1:2030/{dashboard}" for dashboard in dashboard_li]
    return {"content":"학습파트 DashBoard 입니다. 목업 page로 교체될 예정입니다.",
            "link":links}

for dashboard in dashboard_li:
    dash_app = example1(requests_pathname_prefix=f"/{dashboard}/")
    app.mount(f"/{dashboard}", WSGIMiddleware(dash_app.server))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2030)
