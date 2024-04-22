from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os

class SlackPlugin:

    def __init__(self, agent : 'ReActAgent'):
        self.app = App(
            token=os.environ.get("SLACK_BOT_TOKEN"),
        )
        self.agent = agent
        self.app.message()(self.reply)
        self.handler = SocketModeHandler(self.app)

    def reply(self, message, say):
        user_query = message.get("text")
        response = self.agent.chat(user_query).response
        say(str(response))


