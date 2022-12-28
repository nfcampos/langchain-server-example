"""
Adapted from https://fastapi.tiangolo.com/advanced/websockets/#await-for-messages-and-send-messages

Obviously this is not production-ready.
"""

import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from .patch_langchain import patch
from .agent import create_agent
from .context import Context

patch()

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8001/ws");
            function showMessage(content, color) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                message.style.color = color
                var content = document.createTextNode(content)
                message.appendChild(content)
                messages.appendChild(message)
            }

            ws.onmessage = function(event) {
                showMessage(event.data, 'green')
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                showMessage(input.value, 'blue')
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    loop = asyncio.get_event_loop()
    # This is called from a separate thread, and runs back in the main thread
    handle_message_sync = lambda msg: asyncio.run_coroutine_threadsafe(
        websocket.send_text(msg), loop
    )
    executor = create_agent(ctx=Context(handle_message_sync))

    while True:
        data = await websocket.receive_text()
        # This runs in a separate thread
        await asyncio.get_event_loop().run_in_executor(None, executor.run, data)
