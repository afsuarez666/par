#Imports
import o#Imports
import os
from fastapi import FastAPI,Query,Path, HTTPException, status,Body, Request, Response, File,
UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse, FileResponse
from pydantic import BaseModel, Field, AnyUrl
from typing import Optional, List, Dicts
from fastapi import FastAPI,Query,Path, HTTPException, status,Body, Request, Response, File,
UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse, FileResponse
from pydantic import BaseModel, Field, AnyUrl
from typing import Optional, List, Dict

#models
class actor (BaseModel):

        first_name:Optional[str]
        last_name:Optional[str]
        born_day:Optional[int]
        born_month:Optional[str]
        awardsoptional[str]
        movies:Optional[str]
        picture:Optional[str]
        web:Optional[str]
        instagram:Optional[str]

class character (BaseModel):
    name:Optional[str]
    last_name:Optional[str]
    profession:Optional[str]
    role:Optional[str]
    days_out_of_earth:Optional[str]

# Retunr all actor
@app.get(
    path="/actor",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,

    description="Return all actors from the database",
    tags=["Actors"]
)
def get_actor(request: Request, number: Optional[str] = Query("5", max_length=2)):
    response = []
    for id, actor in list(actors.items())[:int(number)]:
        response.append((id, actor))
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "actor": response,
                                       "title": "All actors"})

# All Cars
@app.get(
    path="/cars",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,

    description="Return all cars from the 'db'",
    tags=["Cars"]
)
def get_cars(request: Request, number: Optional[str] = Query("5", max_length=3)):
    response = []
    for id, car in list(actors.items())[:int(number)]:
        response.append((id, car))
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "cars": response,
                                       "title": "All cars"})
# All Character
@app.get(
    path="/characters",
    status_code=status.HTTP_20
    response_class=HTMLResponse,

    description="Return all characteers fromata the database",
    tags=["Cars"]
)
def get_characters(request: Request, number: Optional[str] = Query("5", max_length=2)):
    response = []
    for id, character in list(character.items())[:int(number)]:
        response.append((id, character))
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "characters": response,
                                       "title": "All characters"})


# search  a character
 @app.post(
    path="/search",
    response_class=RedirectResponse
)
def search_character(id: str = Form(...)):
    return RedirectResponse("/characters/" + id, status_code=status.HTTP_302_FOUND)

# Actor by ID
@app.get(
    path="/actors/{id}",
    response_model=actor,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["actors"],
    description="Return actor by the id indicated"
)
def get_actor_by_id(request: Request, id: int = Path(..., gt=0, lt=1000)):
    actor = actors.get(id)
    response = templates.TemplateResponse("search.html", {"request": request,
                                                          "actor": actor,
                                                          "id": id,
                                                          "title": "Search Actor"})
    if not actor:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response

           
