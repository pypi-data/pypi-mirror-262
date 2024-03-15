import base64
import builtins
from typing import Optional
import requests

from .sdk import HttpRequestExecutor
from .custom_types import StradaError, StradaHttpResponse, StradaResponse
from .exception_handler import exception_handler
from .common import build_input_schema_from_strada_param_definitions, custom_print, hydrate_input_fields
from .debug_logger import with_debug_logs

# Initialize the print function to use the logger
builtins.print = custom_print

class IntercomCreateObjectResponse(StradaResponse):
    """
    Represents the response received when creating an object in Intercom.
    """

    data: Optional[dict]
    """data `Optional[dict]`\n---\nThe response data."""

    def __init__(self, http_response: requests.Response):
        super().__init__(
            success=False, error=None, data=None
        )  # Initialize parent class attributes

        if http_response.ok:
            raw_json: dict = http_response.json()
            self.data = raw_json
            self.success = True
        else:
            raw_json: dict = http_response.json()
            message = raw_json.get("message", http_response.text) 
            self.error = StradaError(
                errorCode=http_response.status_code,
                statusCode=http_response.status_code,
                message=message,
            )
            self.data = raw_json


class IntercomCustomHttpActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "IntercomAction"

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

    def build(self) -> 'IntercomCustomHttpAction':
        return self._get_instance()

    def _get_instance(self) -> 'IntercomCustomHttpAction':
        if self._instance is None:
            self._instance = IntercomCustomHttpAction()
        return self._instance


class IntercomCustomHttpAction:
    """
    Represents a custom HTTP action for Intercom.
    """
    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.method = None
        self.token = None
        self.path = "{}"
        self.headers = "{}"
        self.params = "{}"
        self.body = "{}"
        self.function_name = None

    @with_debug_logs(app_name="intercom")
    @exception_handler
    def execute(self, **kwargs) -> StradaHttpResponse:
        """Executes the custom HTTP action.\n---\nParameters should be passed as keyword arguments:\n```python\nres = MyAction.execute(name="Max")\n```"""
        return HttpRequestExecutor.execute(
            dynamic_parameter_json_schema=self.param_schema_definition,
            base_path_params=self.path,
            base_headers=self.headers,
            base_query_params=self.params,
            base_body=self.body,
            base_url=self.url,
            method=self.method,
            header_overrides={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            function_name=self.function_name,
            app_name="intercom",
            **kwargs,
        )

    @staticmethod
    def prepare(data) -> 'IntercomCustomHttpAction':
        """For Strada internal SDK use only."""
        builder = IntercomCustomHttpActionBuilder()
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
