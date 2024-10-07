import os
import logging
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse

from service.entries.model.entry import Entry
from service.entries.persistence.entries_store import EntriesStore
from service.slack.slack_content_messages import (SLACK_TEXT_PROVIDE_TASK_TITLE,
                                                  SLACK_TEXT_COMMAND_NOT_RECOGNIZED,
                                                  SLACK_TEXT_TOKEN_NOT_SET,
                                                  SLACK_TEXT_INVALID_TOKEN)

logger = logging.getLogger(__name__)

router = APIRouter()

persistence = EntriesStore()


@router.post("/")
async def slack_handler(
        command: str = Form(...), text: str = Form(...),
        token: str = Form(...)):
    await _validate_slack_token(token)

    logger.info(f"Received command: {command}, text: {text}")

    if command == "/busybe":
        task_title = text.strip()
        if not task_title:
            logger.error("Error: No task title provided")
            return JSONResponse(
                content={"text": SLACK_TEXT_PROVIDE_TASK_TITLE},
                status_code=200)

        created_entry = persistence.add_entry(Entry(title=task_title).dict())

        logger.info(f"Task created with ID: {created_entry.id},"
                    f" Title: {created_entry.title}")

        return JSONResponse(content={
            "text": f"Task created: {created_entry.title}",
            "id": created_entry.id
        }, status_code=200)

    logger.error("Error: Command not recognized")
    return JSONResponse(
        content={"text": SLACK_TEXT_COMMAND_NOT_RECOGNIZED},
        status_code=200)


async def _validate_slack_token(token):
    slack_token = os.getenv("SLACK_VERIFICATION_TOKEN")
    if not slack_token:
        logger.error("Error: Slack verification token not set")
        raise HTTPException(status_code=500, detail=SLACK_TEXT_TOKEN_NOT_SET)

    if token != slack_token:
        logger.error(f"Error: Invalid token: {token}")
        raise HTTPException(status_code=401, detail=SLACK_TEXT_INVALID_TOKEN)
