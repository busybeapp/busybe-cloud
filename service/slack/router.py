import json
import logging
import os

import httpx
from fastapi import APIRouter, Request, BackgroundTasks, HTTPException

from service.entries.model.entry import Entry
from service.entries.persistence.entries_store import EntriesStore
from service.slack.slack_content_messages import (SLACK_TEXT_INVALID_TOKEN,
                                                  SLACK_TEXT_TOKEN_NOT_SET)

logger = logging.getLogger(__name__)

router = APIRouter()

persistence = EntriesStore()


def send_followup_message(response_url: str, entry: Entry):
    message = {"text": f"{entry.title} was added to your busybe inbox"}
    with httpx.Client() as client:
        response = client.post(response_url, json=message)
        logger.info(f"Follow-up response status: {response.status_code}")


@router.post("/")
async def handle_message_shortcut(request: Request, background_tasks: BackgroundTasks):
    form_data = await request.form()
    payload = json.loads(form_data.get("payload", "{}"))
    await _validate_slack_token(payload.get('token'))

    response_url = payload.get("response_url")
    text = payload.get('message', {}).get('text', {})
    created_entry = persistence.add_entry(Entry(title=text).model_dump())
    if response_url:
        background_tasks.add_task(send_followup_message, response_url, created_entry)

    logger.info(f"Received payload: {payload}")
    return {"isBase64Encoded": True, "statusCode": 200, "body": "{}"}


async def _validate_slack_token(token):
    slack_token = os.getenv("SLACK_VERIFICATION_TOKEN")
    if not slack_token:
        logger.error("Error: Slack verification token not set")
        raise HTTPException(status_code=500, detail=SLACK_TEXT_TOKEN_NOT_SET)

    if token != slack_token:
        logger.error(f"Error: Invalid token: {token}")
        raise HTTPException(status_code=401, detail=SLACK_TEXT_INVALID_TOKEN)
