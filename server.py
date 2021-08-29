# %%
import requests
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from query import *

# %%
app = FastAPI()
templates = Jinja2Templates(directory=".")

def get_access_token(authorization_code: str, old_access_token:str = None):
    
    header = {"Content-Type": "application/json", "Authorization": "OAuth MLY|4996748710342229|df37ea75c385590184f067f78962be3a"}
    if not old_access_token:
        data = {"grant_type": "authorization_code", "client_id": "4996748710342229", 'code': authorization_code}
    else:
        data = {"grant_type": "authorization_code", "client_id": "4996748710342229", "refresh_token": old_access_token}
        

    r = requests.post('https://graph.mapillary.com/token', data=data, headers=header)

    try:
        new_app_access_token = r.json()['access_token']
        return new_app_access_token
    except Exception:
        print("Get access token failed")
    return None


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



@app.get("/api")
def api(lon: float, lat: float, access_token: str):
    result = find_closest_point(access_token, lon, lat)
    if result:
        return result
    else:
        return 

# uvicorn server:app --reload --port 8080