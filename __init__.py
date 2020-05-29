# -*- encoding: UTF-8 -*-
from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
import os
import uvicorn
from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.lexers import get_lexer_for_filename
from pygments.formatters.html import HtmlFormatter

__version__ = '0.0.1'


app = FastAPI(title='Python入门', description='没有Bug的Python电子书',
              version=__version__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount('/static', StaticFiles(directory=os.path.join(BASE_DIR,
                                                        'static')), name='static')
templates = Jinja2Templates(os.path.join(BASE_DIR, 'templates'))
code_temp_templates = Jinja2Templates(
    os.path.join(BASE_DIR, 'templates', 'document', 'temp'))
document_templates = Jinja2Templates(
    os.path.join(BASE_DIR, 'templates', 'document'))
docs = {
    '首页': 'index.html',
    '安装Python': 'install_python.html',
    'print语句': 'print_function.html',
    'input语句': 'input_function.html',
    'range函数': 'range_function.html',
    'if语句': 'if_statements.html',
    'for语句': 'for_statements.html'
}


@app.get('/', description='Python书主页')
def index(request: Request):
    clear_temp()
    return templates.TemplateResponse('index.html', {'request': request, 'docs': docs})


@app.get('/document/{doc_html_name}', description='文档缓存')
def document(request: Request, doc_html_name: str = 'index.html'):
    return document_templates.TemplateResponse(doc_html_name, {'request': request})


@app.get('/open_html/')
def open_html(request: Request, url: str = None):
    return templates.TemplateResponse('open_html.html', {"request": request, 'url': url})


@app.get('/get_code_color/{code_color_file_name}')
def code_color(request: Request, code_color_file_name: str = None, css_name: str = 'default'):
    if not code_color_file_name:
        return templates.TemplateResponse('open_html.html', {'request': request, 'url': ''})
    with open(os.path.join(BASE_DIR, 'static', code_color_file_name), encoding='utf-8') as f:
        code = f.read()
    return_data = f'<title>{code_color_file_name}</title>' + '<style type="text/css">\n' + \
        HtmlFormatter(style=css_name).get_style_defs('.highlight') + "</style>" + \
        highlight(code, get_lexer_for_filename(code_color_file_name),
                  HtmlFormatter(
            linenos=True))
    out_file_name = os.path.join(
        BASE_DIR, 'static', code_color_file_name).replace('\\', '/')
    if out_file_name != "":
        with open(os.path.join(BASE_DIR, 'templates', 'document', 'temp', out_file_name.split('/')[-1]
                               .replace('.' + out_file_name.split('.')[-1], '.html')), 'w', encoding='utf-8') as f:
            f.write(return_data)
    return code_temp_templates.TemplateResponse(out_file_name.split('/')[-1].
                                                replace('.' + out_file_name.split('.')[-1], '.html'), {'request': request})

def clear_temp():
    for file_name in os.listdir(os.path.join(BASE_DIR, 'templates', 'document', 'temp')):
        os.remove(os.path.join(BASE_DIR, 'templates', 'document', 'temp', file_name))


def run_server(app: FastAPI = app, port: int = 8887):
    clear_temp()
    uvicorn.run(app, port=port)


if __name__ == "__main__":
    run_server()
