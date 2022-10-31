#Imports

import os
from fastapi import FastAPI,Query,Path, HTTPException, status,Body, Request, Response, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse, FileResponse
from pydantic import BaseModel, Field, AnyUrl
from typing import Optional, List, Dict

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


#models
class actor (BaseModel):

        first_name:Optional[str]
        last_name:Optional[str]
        born_day:Optional[int]
        born_month:Optional[str]
        awards:Optional[str]
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


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "title": "The martian web app",
                                       })


