import json
import logging

import httpx
from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse

from service.entries.persistence.entries_store import EntriesStore

logger = logging.getLogger(__name__)
router = APIRouter()
persistence = EntriesStore()


# Function to send follow-up message
def send_followup_message(response_url: str):
    message = {"text": "Great!"}
    with httpx.Client() as client:
        response = client.post(response_url, json=message)
        logger.info(f"Follow-up response status: {response.status_code}")


@router.post("/slack/message-shortcut")
async def handle_message_shortcut(request: Request, background_tasks: BackgroundTasks):
    form_data = await request.form()  # Await the form data correctly
    payload = json.loads(form_data.get("payload", "{}"))  # Retrieve the payload

    # Log the entire payload for debugging
    logger.info(f"Received payload: {payload}")

    # Extract response_url from the payload
    response_url = payload.get("response_url")

    # If response_url exists, send the follow-up message
    if response_url:
        background_tasks.add_task(send_followup_message, response_url)

    # Immediately respond to Slack to avoid the timeout error
    return JSONResponse(content={"text": "Message received"}, status_code=200)


# @router.post("/slack/message-shortcut")
# async def handle_message_shortcut(request: Request):
#     form_data = await request.form()
#     payload = json.loads(form_data.get("payload", "{}"))
#
#     # Log the entire payload for debugging
#     logger.info(f"Received payload: {payload}")
#
#     # Extract response_url from the payload
#     response_url = payload.get("response_url")
#
#     # If response_url exists, send the follow-up message
#     if response_url:
#         message = {
#             "text": "Great!"  # Message that will pop up in Slack
#         }
#         async with httpx.AsyncClient() as client:
#             await client.post(response_url, json=message)
#
#     return JSONResponse(content={"text": "Message received"})


#     try:
#         # Parse form data
#         form_data = await request.form()
#         payload = json.loads(form_data.get("payload", "{}"))
#
#         # Log the entire payload for debugging
#         logger.debug(f"Received payload: {payload}")
#
#         # Extract message text
#         message = payload.get("message", {})
#         message_text = message.get("text", "")
#
#         # Create the entry
#         created_entry = persistence.add_entry(Entry(title=message_text).dict())
#         logger.info(f"Created entry with ID: {created_entry.id}")
#
#         # Return a very simple response
#         return {"text": "Great! We saved that for you! 📝"}
#
#     except Exception as e:
#         logger.exception("Error handling message shortcut")
#         return {"text": "Sorry, something went wrong. Please try again."}
