import logging
import os
from tempfile import NamedTemporaryFile
from fastapi import FastAPI, HTTPException, Request, UploadFile

from dotenv import load_dotenv
from fastapi import  Form

from app.models import ChallengeModel

load_dotenv()

app = FastAPI()

@app.post("/challenge")
def challenge(challenge: ChallengeModel):
    return challenge.challenge

@app.post("/slash")
def slash(channel_name: str = Form(...), user_name: str = Form(...), command: str = Form(...), text: str = Form(...)):
    return {"channel_name": channel_name, "user_name": user_name, "command": command, "text": text}