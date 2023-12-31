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
    print("Ingesting... " + message)
    url = os.environ["RESTAI_URL"] + '/projects/' + \
        os.environ["RESTAI_PROJECT"] + '/ingest/url'
    data = {"url": message}
    response = requests.post(url, json=data)
    responsej = response.json()
    data = {
        "response_type": "in_channel",
        "blocks": [
            {
                'type': 'section',
                'text': {
                    "type": "mrkdwn",
                    'text': "Ingested " + str(responsej.get("documents", 0)) + " documents and " + str(responsej.get("texts", 0)) + " texts from " + responsej.get("url", "")
                }
            }
        ]
    }
    requests.post(response_url, json=data)


def question(response_url: str, message: str):
    url = os.environ["RESTAI_URL"] + '/projects/' + \
        os.environ["RESTAI_PROJECT"] + '/question'
    data = {"question": message}
    response = requests.post(url, json=data)
    answer = response.json().get('answer', 'Error...')

    data = {
        "response_type": "in_channel",
        "blocks": [
            {
                'type': 'section',
                'text': {
                    "type": "mrkdwn",
                    'text': answer
                }
            }
        ]
    }
    requests.post(response_url, json=data)


@app.post("/challenge")
def challenge(challenge: ChallengeModel):
    return challenge.challenge


@app.post("/slash")
def slash(channel_name: str = Form(...), user_name: str = Form(...), command: str = Form(...), text: str = Form(...), response_url: str = Form(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    words = text.split()
    operation = words[0] if words else None
    message = ' '.join(words[1:]) if len(words) > 1 else ''

    if operation == 'ingest':
        background_tasks.add_task(ingest, response_url, message)
        return {"response_type": "in_channel", 'text': 'Ingesting...'}
    elif operation == 'question':
        background_tasks.add_task(question, response_url, message)
        return {"response_type": "in_channel", 'text': 'Processing...'}
    elif operation == 'chat':
        pass
    else:
        return {"response_type": "in_channel", 'text': 'Please rewrite you statement.'}
