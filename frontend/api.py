import requests
BASE_URL='http://127.0.0.1:8000'
def request(method,path,**kwargs):
    kwargs.setdefault('timeout',10); r=requests.request(method,f'{BASE_URL}{path}',**kwargs); r.raise_for_status(); return r.json()
