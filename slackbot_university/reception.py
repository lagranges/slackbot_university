import os
from slack import RTMClient
from slack.errors import SlackApiError

from .log import get_logger
from .professor_representative import ProfessorRepresentative
logger = get_logger("server")

professor_repr = ProfessorRepresentative(
    ["language", "general"]        
)

@RTMClient.run_on(event='message')
def say_hello(**payload):
    global counter
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'text' in data and 'user' in data:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        text = data['text']

        try:
            response = web_client.chat_postMessage(
                channel=channel_id,
                text=professor_repr.answer_short(text),
                #thread_ts=thread_ts
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            #assert e.response["ok"] is False
            #assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

rtm_client = RTMClient(token=os.environ["SLACK_API_TOKEN"])
rtm_client.start()
