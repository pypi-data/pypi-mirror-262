import base64
from typing import Optional
from pydantic import BaseModel
import requests
import builtins
from .sdk import HttpRequestExecutor 
from .exception_handler import exception_handler
from .custom_types import StradaError, StradaHttpResponse, StradaResponse
from .common import (
    build_input_schema_from_strada_param_definitions,
    hydrate_input_str,
    validate_http_input,
    custom_print
)
from .debug_logger import with_debug_logs

# Initialize the print function to use the logger
builtins.print = custom_print


class MessageData(BaseModel):
    """
    Represents the data of a Slack message.

    """

    bot_id: str
    """bot_id `str`\n---\nThe ID of the bot that sent the message."""

    type: str
    """type `str`\n---\nThe type of the message."""

    text: str
    """text `str`\n---\nThe text content of the message."""

    user: str
    """user `str`\n---\nThe user who sent the message."""

    ts: str
    """ts `str`\n---\nThe timestamp of the message."""

    app_id: str
    """app_id `str`\n---\nThe ID of the Slack app associated with the message."""

    team: str
    """team `str`\n---\nThe team ID associated with the message."""

    def __getitem__(self, item):
        return getattr(self, item)


class SlackSendMessageData(BaseModel):
    """
    Represents the data sent to Slack.
    """

    channel: str
    """channel `str`\n---\nThe channel the message was to."""

    message: MessageData
    """message `MessageData`\n---\nThe message that was sent."""

    def __getitem__(self, item):
        return getattr(self, item)


class SlackSendMessageResponse(StradaResponse):
    """
    Represents the response of a Slack send message API call.
    """

    data: Optional[SlackSendMessageData]
    """data `Optional[SlackSendMessageData]`\n---\nThe data returned in the response."""

    def __init__(self, http_response: requests.Response):
        super().__init__(
            success=False, error=None, data=None
        )  # Initialize parent class attributes

        if http_response.ok:
            raw_json: dict = http_response.json()
            success = raw_json["ok"]
            if not success:
                self.error = StradaError(
                    errorCode=http_response.status_code,
                    statusCode=http_response.status_code,
                    message=raw_json.get("error", "Error executing HTTP Request."),
                )
                self.data = raw_json
            else:
                self.data = SlackSendMessageData(
                    channel=raw_json["channel"],
                    message=MessageData(
                        bot_id=raw_json["message"]["bot_id"],
                        type=raw_json["message"]["type"],
                        text=raw_json["message"]["text"],
                        user=raw_json["message"]["user"],
                        ts=raw_json["message"]["ts"],
                        app_id=raw_json["message"]["app_id"],
                        team=raw_json["message"]["team"],
                    ),
                )
                self.success = True
        else:
            self.error = StradaError(
                errorCode=http_response.status_code,
                statusCode=http_response.status_code,
                message=http_response.text,
            )


class SlackSendMessageActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "SendMessage"

    def set_param_schema(self, param_schema):
        self._get_instance().param_schema_definition = (
            build_input_schema_from_strada_param_definitions(param_schema)
        )
        return self

    def set_url(self, url):
        self._get_instance().url = url
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_channel(self, channel):
        decoded_channel = base64.b64decode(channel).decode('utf-8')
        self._get_instance().channel = decoded_channel 
        return self

    def set_text(self, text):
        decoded_text = base64.b64decode(text).decode('utf-8')
        self._get_instance().text = decoded_text
        return self

    def set_function_name(self, function_name):
        if function_name is None:
            self._instance.function_name = self.default_function_name
        else:
            self._instance.function_name = function_name
        return self

    def build(self) -> 'SlackSendMessageAction':
        return self._get_instance()

    def _get_instance(self) -> 'SlackSendMessageAction':
        if self._instance is None:
            self._instance = SlackSendMessageAction()
        return self._instance


class SlackSendMessageAction:
    """
    Represents an action to send a message to a specified channel in Slack.

    Attributes:
        param_schema_definition (dict): The parameter schema definition for the action.
        url (str): The URL for the Slack API.
        token (str): The authentication token for the Slack API.
        function_name (str): The name of the function associated with the action.
        channel (str): The channel to send the message to.
        text (str): The text of the message to send.
    """

    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.token = None
        self.function_name = None
        self.channel = None
        self.text = None
    
    def _retry_with_join(self, url: str, headers: dict, body: dict):
        response = requests.post(url, headers=headers, json=body)
        if response.ok:
            response_json = response.json()
            if response_json["ok"]:
                return response
            else:
                if response_json["error"] == "not_in_channel":
                    # Join the channel and retry
                    join_url = "https://slack.com/api/conversations.join"
                    join_response = requests.post(join_url, headers=headers, json=body)
                    if join_response.ok:
                        return requests.post(url, headers=headers, json=body)
                    else:
                        # Return the original response
                        return response 
                else:
                    # Return the original response
                    return response

    @with_debug_logs(app_name="slack")
    @exception_handler
    def execute(self, **kwargs) -> SlackSendMessageResponse:
        """Executes the Slack Send Message action.\n---\nParameters should be passed as keyword arguments:\n```python\nres = MyAction.execute(name="Max")\n```"""
        validate_http_input(self.param_schema_definition, **kwargs)

        text = hydrate_input_str(self.text, self.param_schema_definition, **kwargs)
        channel = hydrate_input_str(
            self.channel, self.param_schema_definition, **kwargs
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        body = {
            "channel": channel,
            "text": text,
            "unfurl_links": False,
            "mrkdwn": True,
        }

        response = self._retry_with_join(self.url, headers, body)

        return SlackSendMessageResponse(response)

    @staticmethod
    def prepare(data) -> 'SlackSendMessageAction':
        """For Strada internal SDK use only."""
        builder = SlackSendMessageActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_token(data["access_token"])
            .set_channel(data["channel"])
            .set_text(data["text"])
            .set_function_name(data.get("function_name", None))
            .build()
        )


class SlackCustomHttpActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "SlackAction"

    def set_param_schema(self, param_schema):
        self._get_instance().param_schema_definition = (
            build_input_schema_from_strada_param_definitions(param_schema)
        )
        return self

    def set_url(self, url):
        self._get_instance().url = url
        return self

    def set_method(self, method):
        self._get_instance().method = method
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_headers(self, headers):
        self._instance.headers = headers
        return self

    def set_params(self, params):
        self._instance.params = params
        return self

    def set_body(self, body):
        self._instance.body = body
        return self

    def set_function_name(self, function_name):
        if function_name is None:
            self._instance.function_name = self.default_function_name
        else:
            self._instance.function_name = function_name
        return self

    def build(self) -> 'SlackCustomHttpAction':
        return self._get_instance()

    def _get_instance(self) -> 'SlackCustomHttpAction':
        if self._instance is None:
            self._instance = SlackCustomHttpAction()
        return self._instance


class SlackCustomHttpAction:
    """
    Represents a custom HTTP action for Slack integration.
    """

    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.method = None
        self.token = None
        self.headers = "{}"
        self.params = "{}"
        self.body = "{}"
        self.function_name = None

    @with_debug_logs(app_name="slack")
    @exception_handler
    def execute(self, **kwargs) -> StradaHttpResponse:
        """Executes the custom HTTP action.\n---\nParameters should be passed as keyword arguments:\n```python\nres = MyAction.execute(name="Max")\n```"""
        return HttpRequestExecutor.execute(
            dynamic_parameter_json_schema=self.param_schema_definition,
            base_path_params="{}",
            base_headers=self.headers,
            base_query_params=self.params,
            base_body=self.body,
            base_url=self.url,
            method=self.method,
            header_overrides={
                "Authorization": f"Bearer {self.token}",
            },
            function_name=self.function_name,
            app_name="slack",
            **kwargs,
        )

    @staticmethod
    def prepare(data) -> 'SlackCustomHttpAction':
        """For Strada internal SDK use only."""
        builder = SlackCustomHttpActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_method(data["method"])
            .set_token(data["access_token"])
            .set_headers(data.get("headers", "{}"))
            .set_params(data.get("params", "{}"))
            .set_body(data.get("body", "{}"))
            .set_function_name(data.get("function_name", None))
            .build()
        )
