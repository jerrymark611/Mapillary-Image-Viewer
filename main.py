# %%
import os

from fastapi import FastAPI, Request
import httpx
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, HTMLResponse

# %%
app = FastAPI()
templates = Jinja2Templates(directory=".")


def get_access_token(authorization_code: str, old_app_access_token: str = ""):
    """
    get a new access token
    :param authorization_code: code from authorization at https://www.mapillary.com/connect?client_id=4996748710342229
    :param refresh:
    :param old_app_access_token:
    :return: new_app_access_token
    """
    data = {"grant_type": "authorization_code", "client_id": "4996748710342229", 'code': authorization_code}

    header = {"Content-Type": "application/json", "Authorization": "OAuth MLY|4996748710342229"
                                                                   "|df37ea75c385590184f067f78962be3a"}
    r = httpx.post('https://graph.mapillary.com/token', data=data, headers=header)

    try:
        new_app_access_token = r.json()['access_token']
        return new_app_access_token
    except Exception:
        print("Get access token failed")
    return None

@app.get("/")
async def root(request: Request):
    # access_token = get_access_token(code)
    # print(access_token)
    # if not access_token:
    #     return RedirectResponse("https://www.mapillary.com/connect?client_id=4996748710342229")
    # print(request)
    return templates.TemplateResponse('index.html', context={"request": request})

    # return HTMLResponse(pkg_resources.resource_string(__name__, 'index.html'))

@app.get("/get_token")
async def get_token(code: str = None):
    access_token = get_access_token(code)
    return access_token


@app.get("/api")
def api(access_token: str = None, sequence_id: str = None):
    if not access_token:
        return RedirectResponse("https://www.mapillary.com/connect?client_id=4996748710342229")

    # print(access_token)

    header = {'Authorization': 'OAuth {}'.format(access_token)}
    url = 'https://graph.mapillary.com/image_ids?sequence_id={}'.format(sequence_id)
    r = httpx.get(url, headers=header)
    data = r.json()
    print(data)
    if not os.path.exists(os.path.join('data', sequence_id)):
        os.makedirs(os.path.join('data', sequence_id))
    for value in data['data']:
        request_image(access_token, sequence_id, value['id'])

    return "Sequence downloaded"


def request_image(access_token, sequence_id, image_id):
    header = {'Authorization': 'OAuth {}'.format(access_token)}
    url = 'https://graph.mapillary.com/{}?fields=thumb_2048_url'.format(image_id)
    r = httpx.get(url, headers=header)
    data = r.json()
    image_url = data['thumb_2048_url']
    # save each image with ID as filename to directory by sequence ID
    if os.path.isfile('{}/{}.jpg'.format(sequence_id, image_id)):
        return

    with open('data/{}/{}.jpg'.format(sequence_id, image_id), 'wb') as handler:
        image_data = httpx.get(image_url).content
        handler.write(image_data)
    return

# uvicorn main:app --reload
