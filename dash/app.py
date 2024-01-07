import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from dashapp import create_dash_app

app = FastAPI()

@app.get("/status")
def get_status():
    return {"routes": [{"method": "GET", "path": "/", "summary": "Sub-mounted Dash application"},
                       {"method": "GET", "path": "/status", "summary": "App status"}]}

dash_app = create_dash_app(requests_pathname_prefix="/")
app.mount("/", WSGIMiddleware(dash_app.server))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2030)
