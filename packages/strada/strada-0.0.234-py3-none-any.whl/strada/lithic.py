"""Strada SDK for Lithic."""

import builtins

from .custom_types import StradaHttpResponse
from .sdk import HttpRequestExecutor
from .exception_handler import exception_handler
from .common import build_input_schema_from_strada_param_definitions, custom_print
from .debug_logger import with_debug_logs

# Initialize the print function to use the logger
builtins.print = custom_print


class LithicCustomHttpActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "LithicAction"

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

    def build(self) -> 'LithicCustomHttpAction':
        return self._get_instance()

    def _get_instance(self) -> 'LithicCustomHttpAction':
        if self._instance is None:
            self._instance = LithicCustomHttpAction()
        return self._instance


class LithicCustomHttpAction:
    """
    Represents a custom HTTP action for Lithic.
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

    @with_debug_logs(app_name="lithic")
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
                "Authorization": f"{self.token}",
                "Content-Type": "application/json",
            },
            function_name=self.function_name,
            app_name="lithic",
            **kwargs,
        )

    @staticmethod
    def prepare(data) -> 'LithicCustomHttpAction':
        """For Strada internal SDK use only."""
        builder = LithicCustomHttpActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_method(data["method"])
            .set_token(data["api_key"])
            .set_headers(data.get("headers", "{}"))
            .set_params(data.get("params", "{}"))
            .set_body(data.get("body", "{}"))
            .set_function_name(data.get("function_name", None))
            .build()
        )
