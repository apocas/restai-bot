import logging
import os
from tempfile import NamedTemporaryFile
from fastapi import FastAPI, HTTPException, Request, UploadFile

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/api")
async def createProject(request: Request):
    print(request.json())
    return {"message": "Hello World"}