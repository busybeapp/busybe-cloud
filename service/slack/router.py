import os
import logging
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse

from service.entries.model.entry import Entry
from service.entries.persistence.entries_store import EntriesStore

logger = logging.getLogger(__name__)

router = APIRouter()

persistence = EntriesStore()


@router.post("/")
async def slack_handler(
        command: str = Form(...), text: str = Form(...), token: str = Form(...)
        ):
    slack_token = os.getenv("SLACK_VERIFICATION_TOKEN")
    if not slack_token:
        logger.error("Error: Slack verification token not set")
        raise HTTPException(status_code=500, detail="Slack verification token not set")

    logger.info(f"Received command: {command}, text: {text}, token: {token}")

    if token != slack_token:
        logger.error("Error: Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")

    if command == "/busybe":
        task_title = text.strip()
        if not task_title:
            logger.error("Error: No task title provided")
            return JSONResponse(
                content={"text": "Please provide a task title."},
                status_code=200)

        created_entry = persistence.add_entry(Entry(title=task_title).dict())

        logger.info(f"Task created with ID: {created_entry.id},"
                    f" Title: {created_entry.title}")

        return JSONResponse(content={
            "text": f"Task created: {created_entry.title}",
            "id": created_entry.id
        }, status_code=200)

    elif command == "/listentries":
        all_entries = persistence.get_entries()

        if not all_entries:
            logger.info("No entries found.")
            return JSONResponse(content={"text": "No tasks found."}, status_code=200)

        entry_list = "\n".join([f"{entry['title']}" for entry in all_entries])
        logger.info(f"Returning {len(all_entries)} entries.")

        return JSONResponse(content={
            "text": f"Here are your tasks:\n{entry_list}"
        }, status_code=200)

    logger.error("Error: Command not recognized")
    return JSONResponse(content={"text": "Command not recognized."}, status_code=200)
