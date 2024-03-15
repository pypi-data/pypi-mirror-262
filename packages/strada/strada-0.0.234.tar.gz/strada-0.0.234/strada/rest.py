import base64
import json
import builtins
import requests
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field, ValidationError, validator 

from .sdk import HttpRequestExecutor
from .custom_types import FilesDict, StradaHttpResponse
from .exception import StradaValidationException
from .exception_handler import exception_handler
from .common import (
    basic_auth_str,
    build_input_schema_from_strada_param_definitions,
    hydrate_input_fields,
    hydrate_input_str,
    custom_print,
)
from .debug_logger import with_debug_logs

# Initialize the print function to use the logger
builtins.print = custom_print


class CustomHttpActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "CustomHTTPAction"

    def set_param_schema(self, param_schema):
        decoded = base64.b64decode(param_schema).decode("utf-8")
        self._get_instance().param_schema_definition = (
            build_input_schema_from_strada_param_definitions(decoded)
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

    def set_api_key(self, api_key):
        self._get_instance().api_key = api_key
        return self

    def set_basic_auth(self, basic_auth):
        self._get_instance().basic_auth = basic_auth
        return self

    def set_headers(self, headers):
        self._instance.headers = headers
        return self

    def set_params(self, params):
        self._instance.params = params
        return self

    def set_body(self, body):
        decoded = base64.b64decode(body).decode("utf-8")
        self._instance.body = decoded 
        return self
    
    def set_function_name(self, function_name):
        if function_name is None:
            self._instance.function_name = self.default_function_name
        else:
            self._instance.function_name = function_name
        return self

    def build(self) -> 'CustomHttpAction':
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = CustomHttpAction()
        return self._instance


class FileUploadData(BaseModel):
    form_key: str = Field(..., title='Form key')
    name: str = Field(..., title='File name')
    file_url: Optional[str] = Field(None, title='File URL')
    file_content: Optional[str] = Field(None, title='File content')
    type: str = Field(..., title='File type')

    @validator('file_content')
    def check_file_url_or_content(cls, v, values, **kwargs):
        if not v and not values.get('file_url'):
            raise ValueError('Either "File URL" or "File content" must be provided.')
        return v

class HttpBodyFormSchema(BaseModel):
    type: Union[Literal['JSON'], Literal['Form'], Literal['File']] = Field(..., title='Type of data')
    Form: Optional[list[tuple[str, str]]] = Field(None, title='Form data')
    JSON: Optional[Any] = Field(None, title='JSON data')
    File: Optional[FileUploadData] = Field(None, title='File upload data')

def convert_to_set(key_value_tuples: list[tuple[str, str]]) -> dict[str, str]:
    result = {}
    for key, value in key_value_tuples:
        result[key] = value
    return result

class CustomHttpAction:
    """
    Represents a custom HTTP action that can be executed.

    Attributes:
        param_schema_definition (str): The schema definition for the parameters.
        url (str): The URL to send the HTTP request to.
        method (str): The HTTP method to use for the request.
        token (str): The authentication token to include in the request header.
        api_key (str): The API key to include in the request header.
        basic_auth (str): The basic authentication credentials in JSON format.
        headers (str): The additional headers to include in the request.
        params (str): The query parameters to include in the request.
        body (str): The request body.
        function_name (str): The name of the function associated with the action.
    """
    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.method = None
        self.token = None
        self.api_key = None
        self.basic_auth = "{}"
        self.headers = "{}"
        self.params = "{}"
        self.body = "{}"
        self.function_name = None

    def _get_authorization_header(self):
        if self.api_key:
            return f"{self.api_key}"
        elif self.basic_auth:
            parsed_basic_auth = json.loads(self.basic_auth)
            return basic_auth_str(
                username=parsed_basic_auth.get("username", ""),
                password=parsed_basic_auth.get("password", ""),
            )
        elif self.token:
            return f"Bearer {self.token}"
    
    def _parse_if_valid(self, raw_payload):
        # Now validate the payload against the SendPromptRequestPayload schema
        try:
            return HttpBodyFormSchema(**raw_payload)
        except ValidationError as e:
            raise StradaValidationException(
                str(e), schema=HttpBodyFormSchema.schema(), data=raw_payload
            )



    @with_debug_logs(app_name="custom-http")
    @exception_handler
    def execute(self, **kwargs) -> StradaHttpResponse:
        """Executes the custom HTTP action.\n---\nParameters should be passed as keyword arguments:\n```python\nres = MyAction.execute(name="Max")\n```"""
        # For custom http, the path parameters can be provided as part of the URL itself
        hydratedUrl = hydrate_input_str(
            self.url, self.param_schema_definition, **kwargs
        )

        raw_payload = hydrate_input_fields(
            self.param_schema_definition, self.body, **kwargs
        )

        header_overrides = {"Authorization": self._get_authorization_header()}

        parsed_payload = self._parse_if_valid(raw_payload) 
        body = None
        files : FilesDict = None
        if parsed_payload.type == 'JSON':
            body = parsed_payload.JSON
            header_overrides['content-type'] = 'application/json'
        elif parsed_payload.type == 'Form':
            body = convert_to_set(parsed_payload.Form)
        elif parsed_payload.type == 'File':        
            # For a file the body must be set and cannot be None
            body = {}
            if parsed_payload.Form:
                # Check if the file also has info in the 'Form' field
                body = convert_to_set(parsed_payload.Form)

            if parsed_payload.File.file_url:
                response = requests.get(parsed_payload.File.file_url)
                if response.status_code == 200:
                    file_content = response.content
                    files = {
                        parsed_payload.File.form_key: (
                            parsed_payload.File.name,
                            file_content,
                            parsed_payload.File.type
                        )
                    }
                else:
                    raise StradaValidationException(f"Failed to download file from {parsed_payload.File.file_url}")
            elif parsed_payload.File.file_content: 
                decoded = base64.b64decode(parsed_payload.File.file_content)
                files = {
                    parsed_payload.File.form_key: (
                        parsed_payload.File.name,
                        decoded,
                        parsed_payload.File.type
                    )
                }

        return HttpRequestExecutor.execute(
            dynamic_parameter_json_schema=self.param_schema_definition,
            base_path_params="{}",
            base_headers=self.headers,
            base_query_params=self.params,
            base_body=body,
            base_url=hydratedUrl,
            method=self.method,
            body_overrides=body,
            files=files,
            header_overrides=header_overrides,
            function_name=self.function_name,
            app_name="custom-http",
            **kwargs,
        )

    @staticmethod
    def prepare(data) -> 'CustomHttpAction':
        """For Strada internal SDK use only."""
        builder = CustomHttpActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_method(data["method"])
            .set_token(data["token"])
            .set_api_key(data["api_key"])
            .set_basic_auth(data["basic_auth"])
            .set_headers(data.get("headers", "{}"))
            .set_params(data.get("query", "{}"))
            .set_body(data.get("body", "{}"))
            .set_function_name(data.get("function_name", None))
            .build()
        )

