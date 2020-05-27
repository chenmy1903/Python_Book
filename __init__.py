# -*- encoding: UTF-8 -*-
from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
import os
import uvicorn

__version__ = '0.0.1'


app = FastAPI(title='Python入门', description='没有Bug的Python电子书')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount('/static', StaticFiles(directory=os.path.join(BASE_DIR,
                                                        'static')), name='static')
templates = Jinja2Templates(os.path.join(BASE_DIR, 'templates'))


@app.get('/', description='Python书主页')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

def run_server(app: FastAPI = app, port: int = 8887):
    uvicorn.run(app, port=port)


if __name__ == "__main__":
    run_server()
