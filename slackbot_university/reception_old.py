import os
import ssl
import json
import requests
import asyncio
import websockets

from .log import get_logger

config = dict(
    token = os.environ.get("SLACK_BOT_TOKEN"),
    url_rtm_connect="https://slack.com/api/rtm.connect",
    worker_plugins=[
        "lang_assistant",    
        "professor_knowall",
    ]
)
assert config["token"], "Add your token: export SLACK_BOT_TOKEN="
logger = get_logger("server")


def get_ws_url(url, token):
    url = url + "?token=" + token
    response = requests.get(url)
    return response.json()["url"]


message_id = 0


async def process_command(client_msg_id, channel, text):
    try:
        res = wikipedia.summary(text).splitlines()[0][:500]
    except Exception:
        import traceback
        res = traceback.format_exc()
    global message_id
    message_id += 1
    res = {
        "id": message_id,
        "type": "message",
        "channel": channel,
        "text": res
    }
    return json.dumps(res)


async def listen(url):
    ssl_context = ssl.SSLContext()
    async with websockets.connect(url, ssl=True) as ws:
        while True:
            res = json.loads(await ws.recv())
            if "type" in res and res["type"] == "message":
                try:
                    res = await process_command(
                        res['client_msg_id'],
                        res['channel'],
                        res["text"]
                    )
                    print(res)
                    await ws.send(res)
                except Exception:
                    continue


async def main():
    url=get_ws_url(config["url_rtm_connect"], config["token"])
    cmd = await listen(url)
    await process_command(cmd)
    #asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
