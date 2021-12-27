from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def index():
    return {"data":{"name":"Tomas Detko"}}


@app.get('/about')
def about():
    return {"data":{"about":"XXXXs"}}