from enum import Enum
from ccdefundamentals.env import ADMIN_CHAT_ID, MAILTO_LINK, MAILTO_USER
import requests


class TooterType(Enum):
    INFO = "info"
    GRAPHQL_ERROR = "graphql error"
    MONGODB_ERROR = "mongodb error"
    REQUESTS_ERROR = "requests error"
    BOT_MAIN_LOOP_ERROR = "bot_main_loop_error"


class TooterChannel(Enum):
    BOT = "bot"
    NOTIFIER = "notifier"
    SMART = "smart"


class Tooter:
    def __init__(
        self,
        environment: str,
        branch: str,
        NOTIFIER_API_TOKEN: str,
        BOT_API_TOKEN: str,
        FASTMAIL_TOKEN: str,
    ) -> None:
        self.environment = environment
        self.branch = branch
        self.NOTIFIER_API_TOKEN = NOTIFIER_API_TOKEN
        self.BOT_API_TOKEN = BOT_API_TOKEN
        self.FASTMAIL_TOKEN = FASTMAIL_TOKEN
        self.url = "https://tooter.concordium-explorer.nl/notify/"
        self.email_part_1 = MAILTO_LINK
        self.email_part_2 = f"""&user={MAILTO_USER}&pass={FASTMAIL_TOKEN}&from=Concordium Explorer Bot<bot@concordium-explorer.nl>"""

    def email(self, title: str, body: str, email_address: str, value=None, error=None):
        body_signature = """
Please visit your <a href='https://concordium-explorer.nl/settings/user/overview'>account</a> to adjust notification settings.

        """
        payload = {
            "urls": f"{self.email_part_1}{email_address}{self.email_part_2 }",
            "title": title,
            "body": body + body_signature,
            "format": "html",
        }
        _ = requests.post(self.url, json=payload)

    def relay(
        self,
        channel: TooterChannel,
        body: str,
        notifier_type: TooterType,
        title: str,
        chat_id: int = None,
        value=None,
        error=None,
        bcc=False,
    ):
        API_TO_USE = (
            self.BOT_API_TOKEN
            if channel == TooterChannel.BOT
            else self.NOTIFIER_API_TOKEN
        )
        chat_id = ADMIN_CHAT_ID if channel == TooterChannel.NOTIFIER else chat_id

        payload = {
            "urls": f"tgram://{API_TO_USE}/{chat_id}",
            "title": f"{title}<br/>",
            "body": body,
            "format": "html",
        }
        _ = requests.post(self.url, json=payload)

    def send(
        self,
        channel: TooterChannel,
        message: str,
        notifier_type: TooterType,
        chat_id: int = None,
        value=None,
        error=None,
    ):
        API_TO_USE = (
            self.BOT_API_TOKEN
            if channel == TooterChannel.BOT
            else self.NOTIFIER_API_TOKEN
        )
        chat_id = ADMIN_CHAT_ID if channel == TooterChannel.NOTIFIER else chat_id

        title = f"t: {notifier_type.value} | e: {self.environment} | b: {self.branch}"
        body = message
        if value:
            body += "| value: {value} "
        if error:
            body += "| error: {error}."

        payload = {
            "urls": f"tgram://{API_TO_USE}/{chat_id}",
            "title": title,
            "body": body,
            "format": "html",
        }
        _ = requests.post(self.url, json=payload)
