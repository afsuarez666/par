#Imports

import os
from fastapi import FastAPI,Query,Path, HTTPException, status,Body, Request, Response, File, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse, FileResponse
from pydantic import BaseModel, Field, AnyUrl
from typing import Optional, List, Dict

import base64

from database import actors
from database import characters

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


#models
class actor (BaseModel):

        first_name:Optional[str]
        last_name:Optional[str]
        born_day:Optional[int]
        born_month:Optional[str]
        born_year:Optional[int]
        awards:Optional[List[str]]
        movies:Optional[List[str]]
        picture:Optional[str]
        web:Optional[str]
        instagram:Optional[str]

class character (BaseModel):
    name:Optional[str]
    last_name:Optional[str]
    profession:Optional[List[str]]
    role:Optional[str]
    days_out_of_earth:Optional[str]


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "title": "The martian web app",
                                       })


# All actor
@app.get(
    path="/actor",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,

    description="Return all actor from the 'db'",
    tags=["Actor"]
)
def get_Actor(request: Request):
    response = []
    for id, actor in list(actors.items()):
        response.append((id, actor))
    return templates.TemplateResponse("all_actors.html",
                                      {"request": request,
                                       "actors": response,
                                       "title": "All actor"})

#All characters
@app.get(
    path="/character",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,

    description="Return all characters from the 'database'",
    tags=["Character"]
)
def get_Character(request: Request):
    response = []
    for id, character in list(characters.items()):
        response.append((id, character))
    return templates.TemplateResponse("all_character.html",
                                      {"request": request,
                                       "characters": response,
                                       "title": "All character"})


@app.post(
    path="/search",
    response_class=RedirectResponse
)
def search_actor(id: str = Form(...)):
    return RedirectResponse("/actor/" + id, status_code=status.HTTP_302_FOUND)



# Actor by ID
@app.get(
    path="/actor/{id}",
    response_model=actor,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Actors"],
    description="Return a actor by the id indicated"
)
def get_actor_by_id(request: Request, id: int = Path(..., gt=0, lt=1000)):
    actor = actors.get(id)
    response = templates.TemplateResponse("search.html", {"request": request,
                                                          "actor": actor,
                                                          "id": id,
                                                          "title": "Search an actor"})
    if not actor:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response


    # Character by ID
@app.get(
    path="/characters/{id}",
    response_model=character,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Characters"],
    description="Return a character by the id indicated"
)
def get_character_by_id(request: Request, id: int = Path(..., gt=0, lt=1000)):
    car = characters.get(id)
    response = templates.TemplateResponse("search2.html", {"request": request,
                                                          "character": character,
                                                          "id": id,
                                                          "title": "Search an character"})
    if not character:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response











@app.get(
    path=("/upload"),
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    tags=["Upload"]
)
def upload(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request,
                                                      "title": "Upload"})


def is_directory_ready():
    os.makedirs(os.getcwd()+"/uploadimg", exist_ok=True)
    return os.getcwd()+"/uploadimg/"


@app.post(
    path="/upload/image",
    tags=["Upload"])
def upload(request: Request, file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        dir = is_directory_ready()
        with open(dir + file.filename, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "Hubo un error al subir la imagen"}
    finally:
        file.file.close()

    base64_encoded_image = base64.b64encode(contents).decode("utf-8")

    return templates.TemplateResponse("upload2.html", {"request": request,  "myImage": base64_encoded_image})



