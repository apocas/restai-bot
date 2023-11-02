import logging
import os
from tempfile import NamedTemporaryFile
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request, UploadFile
import requests

from dotenv import load_dotenv
from fastapi import Form

from app.models import ChallengeModel

load_dotenv()

app = FastAPI()


def ingest(response_url: str, message: str):
    url = os.environ["RESTAI_URL"] + '/projects/' + os.environ["RESTAI_PROJECT"] + '/ingest/url'
    data = {"url": message}
    response = requests.post(url, json=data)

    data = {"response_type": "in_channel", 'text': response.json()}
    requests.post(response_url, json=data)


@app.post("/challenge")
def challenge(challenge: ChallengeModel):
    return challenge.challenge


@app.post("/slash")
def slash(channel_name: str = Form(...), user_name: str = Form(...), command: str = Form(...), text: str = Form(...), response_url: str = Form(...)):
    words = text.split()
    operation = words[0] if words else None
    message = ' '.join(words[1:]) if len(words) > 1 else ''

    if operation == 'ingest':
        BackgroundTasks.add_task(ingest, response_url, message)
        return {"response_type": "in_channel", 'text': 'Processing...'}
    elif operation == 'question':
        url = os.environ["RESTAI_URL"] + '/projects/' + \
            os.environ["RESTAI_PROJECT"] + '/question'
        data = {"question": message}
        response = requests.post(url, json=data)
        answer = response.json().get('answer', '')
        return {"response_type": "in_channel", 'text': answer}
    elif operation == 'chat':
        pass
    else:
        return {"response_type": "in_channel", 'text': 'Please rewrite you statement.'}
