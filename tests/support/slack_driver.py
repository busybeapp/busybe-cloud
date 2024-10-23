import logging
import threading
from collections import deque

import uvicorn
from fastapi import FastAPI

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SlackDriver:

    def __init__(self):
        self._server_thread = None
        self._app = None
        self._received_payloads = deque()

    def start(self):
        self._start_app()

    def _start_app(self):
        app = FastAPI()
        self._app = app
        self._received_payloads = deque()

        @app.post("/webhook")
        async def webhook(payload: dict):
            self._received_payloads.appendleft(payload.get('text'))
            logger.info(f"Got a slack msg: {payload}")
            return {"ok": True}

        self._server_thread = threading.Thread(
            target=uvicorn.run,
            args=(app,),
            kwargs={"host": "localhost", "port": 9090},
            daemon=True
        )
        self._server_thread.start()

    def stop(self):
        if self._server_thread is not None:
            self._server_thread.join(timeout=1)

    def get_callback_msg(self):
        return self._received_payloads[0] if (
            self._received_payloads) else self._received_payloads
