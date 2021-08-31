# %%
import requests
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from query import *

# %%
client_secret = "MLY|4996748710342229|df37ea75c385590184f067f78962be3a"
client_id = "4996748710342229"
radius = 100

app = FastAPI()
templates = Jinja2Templates(directory=".")

def get_access_token(authorization_code: str, old_access_token:str = None):
    header = {"Content-Type": "application/json", "Authorization": f"OAuth {client_secret}"}
    if not old_access_token:
        data = {"grant_type": "authorization_code", "client_id": client_id, 'code': authorization_code}
    else:
        data = {"grant_type": "authorization_code", "client_id": client_id, "refresh_token": old_access_token}
        

    r = requests.post('https://graph.mapillary.com/token', data=data, headers=header)

    try:
        new_app_access_token = r.json()['access_token']
        return new_app_access_token
    except Exception:
        print("Get access token failed")
    return None


# get access token for clinet with index.html
@app.get("/")
async def root(request: Request, code: str = None, old_access_token: str = None):
    if not code:
        return RedirectResponse("https://www.mapillary.com/connect?client_id=4996748710342229")
    access_token = get_access_token(code, old_access_token)
    if not access_token:
        return RedirectResponse("https://www.mapillary.com/connect?client_id=4996748710342229")

    # exchange access_token
    if old_access_token:
        return access_token
    return templates.TemplateResponse('index.html', context={"request": request, "access_token": access_token})

# 
@app.get("/api")
def api(lon: float, lat: float, access_token: str):
    return find_closest_point(access_token, lon, lat, radius)

# start the server
# `uvicorn server:app --reload --port 8080`