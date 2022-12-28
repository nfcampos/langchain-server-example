from typing import Callable


HandleMessagesSync = Callable[[list[dict]], None]


class Context:
    def __init__(self, handle_message_sync: HandleMessagesSync):
        self.handle_message_sync = handle_message_sync

    def send_message_sync(self, content: str):
        self.handle_message_sync(content)
