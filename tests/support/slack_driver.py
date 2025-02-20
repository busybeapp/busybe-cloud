from collections import deque

from mimicker.mimicker import mimicker, post


class SlackDriver:
    received_payloads = deque()

    def __init__(self):
        self.slack = mimicker(port=9090).routes(
            post("/webhook").
            response_func(self.webhook_handler)
        )

    def webhook_handler(self, **kwargs):
        entry = kwargs.get("payload").get('text')
        self.received_payloads.appendleft(entry)
        return 200, {"ok": True}

    def stop(self):
        self.slack.shutdown()

    def get_callback_msg(self):
        return self.received_payloads[0] if (
            self.received_payloads) else self.received_payloads
