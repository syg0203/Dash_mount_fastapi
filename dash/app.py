"""
app.py: 메인 Dash 애플리케이션 스크립트.

이 스크립트는 Dash 애플리케이션을 초기화하고, 위에서 정의된 plots.py 및 dashboard_layout.py 모듈을 사용하여
애플리케이션의 레이아웃과 기능을 구성합니다. 이 스크립트는 애플리케이션을 실행하는 데 사용됩니다.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from dash.src.dashapp import create_dash_app

app = FastAPI()

@app.get("/status")
def get_status():
    return {"routes": [{"method": "GET", "path": "/", "summary": "Sub-mounted Dash application"},
                       {"method": "GET", "path": "/status", "summary": "App status"}]}

dash_app = create_dash_app(requests_pathname_prefix="/")
app.mount("/", WSGIMiddleware(dash_app.server))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2030)
