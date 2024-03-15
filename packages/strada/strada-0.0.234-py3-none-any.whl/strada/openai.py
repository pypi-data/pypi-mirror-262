"""Strada SDK for OpenAI."""

from io import BytesIO
import builtins
import base64
import json
from typing import Any, Optional
import requests

from pydantic import BaseModel, Field, ValidationError, validator
from .custom_types import StradaError, StradaHttpResponse, StradaResponse 
from .error_codes import PublicErrorCodes
from .exception import StradaValidationException
from .sdk import HttpRequestExecutor 
from .exception_handler import exception_handler
import time
import requests
from .common import (
    build_input_schema_from_strada_param_definitions,
    hydrate_input_fields,
    hydrate_input_str,
    validate_http_input,
    custom_print
)
from .debug_logger import with_debug_logs
from pydantic import BaseModel, Field

# Initialize the print function to use the logger
builtins.print = custom_print

class PromptResponse(BaseModel):
    """
    Represents a response to a prompt.

    Attributes:
        id (str): The ID of the response.
        response (str): The response text.
        response_json (Optional[Any]): The response in JSON format (if available).
        is_json (bool): Indicates whether the response is in JSON format.
    """
    id: str
    """id `str`\n---\nThe ID of the response."""
    response: str
    """response `str`\n---\nThe OpenAI response text."""
    response_json: Optional[Any]
    """response_json `Optional[Any]`\n---\nThe OpenAI response in JSON format (if `is_json` is `True`)."""
    is_json: bool 
    """is_json `bool`\n---\nIndicates whether the response is JSON. If `True`, the `response_json` field will contain the parsed JSON response."""
    
    def __getitem__(self, item):
        return getattr(self, item)

class SendPromptResponse(StradaResponse):
    """
    Represents the response received from sending a prompt to OpenAI API.

    """
    data: Optional[PromptResponse]
    """data `Optional[PromptResponse]`\n---\nThe response data."""

    def __init__(self, http_response: requests.Response):
        super().__init__(
            success=False, error=None, data=None
        )  # Initialize parent class attributes

        if http_response.ok:
            raw_json: dict = http_response.json()

            if "choices" in raw_json:
                if len(raw_json["choices"]) > 0:
                    text_content = raw_json["choices"][0]["message"]["content"]
                    is_json = False
                    parsed_content = None
                    try:
                        parsed_content = json.loads(text_content) 
                        is_json = True
                    except:
                        pass

                    self.data = PromptResponse(
                        id=raw_json["id"],
                        response=text_content,
                        response_json=parsed_content,
                        is_json=is_json,
                    )
                    self.success = True
                    
                    # Early return, as the rest is error handling
                    return

            self.error = StradaError( 
                errorCode=PublicErrorCodes.Http.NOT_FOUND,
                statusCode=http_response.status_code,
                message="Request to OpenAI Successful, but no response was returned. See the 'data' field for the full response from OpenAI."
            )
            self.data = raw_json
        else:
            debug_data = None
            try:
                debug_data = http_response.json()
            except:
                pass

            self.error = StradaError(
                errorCode=http_response.status_code,
                statusCode=http_response.status_code,
                message=http_response.text,
            )
            self.data = debug_data

class SendPromptRequestPayload(BaseModel):
    """
    Represents a payload for sending a prompt request.
    """
    prompt: str = Field(..., title="Prompt")
    """prompt `str`\n---\nThe prompt text."""

    instructions: Optional[str] = Field(None, title="Instructions")
    """instructions `Optional[str]`\n---\nAdditional instructions for the prompt. Defaults to None."""

    use_json: Optional[bool] = Field(None, title="Use JSON")
    """use_json `Optional[bool]`\n---\nFlag indicating whether to use JSON format. Defaults to None."""

    model: str = Field(..., title="Model")
    """model `str`\n---\nThe model to use for generating the response."""

    temperature: float = Field(..., ge=0.0, le=2.0, title="Temperature")
    """temperature `float`\n---\nThe temperature parameter for generating the response. Must be between 0.0 and 2.0."""

    def __getitem__(self, item):
        return getattr(self, item)   

    @validator('prompt')
    def check_not_empty(cls, v: str):
        if not v.strip():
            raise ValueError('Prompt is a required field.')
        return v

class OpenAISendPromptActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "OpenAISendPrompt"

    def set_param_schema(self, param_schema):
        self._get_instance().param_schema_definition = (
            build_input_schema_from_strada_param_definitions(param_schema)
        )
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_organization_id(self, organization_id):
        self._get_instance().organization_id = organization_id
        return self
    
    def set_payload(self, payload: str):
        decoded = base64.b64decode(payload).decode('utf-8')
        self._get_instance().payload = decoded 
        return self
    
    def set_function_name(self, function_name):
        if function_name is None:
            self._instance.function_name = self.default_function_name
        else:
            self._instance.function_name = function_name
        return self

    def build(self) -> 'OpenAISendPromptAction':
        return self._get_instance()

    def _get_instance(self) -> 'OpenAISendPromptAction':
        if self._instance is None:
            self._instance = OpenAISendPromptAction()
        return self._instance

class OpenAISendPromptAction:
    """
    Represents an action to send a prompt to OpenAI for chat completions.
    """

    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.token = None
        self.organization_id = None
        self.function_name = None
        self.payload = "{}" 

    def _parse_if_valid(raw_payload):
        # Now validate the payload against the SendPromptRequestPayload schema
        try:
            return SendPromptRequestPayload(**raw_payload)
        except ValidationError as e:
            raise StradaValidationException(str(e), schema=SendPromptRequestPayload.schema(), data=raw_payload)
    
    @with_debug_logs(app_name="openai-chatgpt")
    @exception_handler
    def execute(self, **kwargs) -> SendPromptResponse:
        """Executes the OpenAI Send Prompt action.\n---\nParameters should be passed as keyword arguments:\n```python\nres = MyAction.execute(name="Max")\n```"""
        validate_http_input(self.param_schema_definition, **kwargs)
        
        raw_payload = hydrate_input_fields(self.param_schema_definition, self.payload, **kwargs)


        headers ={} 
        headers["Authorization"] = f"Bearer {self.token}"
        headers["Content-Type"] = "application/json"
        headers["OpenAI-Beta"] = "assistants=v1"
        if self.organization_id:
            headers["OpenAI-Organization"] = self.organization_id
        
        parsed_payload = OpenAISendPromptAction._parse_if_valid(raw_payload)

        body = {}
        messages = []
        if parsed_payload.use_json:
            body["response_format"] = {"type": "json_object"}
            messages.append({"role": "system", "content": "Return response as JSON."})

        if parsed_payload.instructions: 
            messages.append({"role": "system", "content": parsed_payload.instructions})
        messages.append({"role": "user", "content": parsed_payload.prompt})
        body["messages"] = messages
        body["model"] = parsed_payload.model
        body["temperature"] = parsed_payload.temperature 

        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=body,
        )

        return SendPromptResponse(response) 
    
    @staticmethod
    def prepare(data) -> 'OpenAISendPromptAction':
        """For Strada internal SDK use only."""
        builder = OpenAISendPromptActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_token(data["access_token"])
            .set_payload(data["payload"])
            .set_function_name(data.get("function_name", None))
            .build()
        )
class OpenAICustomHttpActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "OpenAIAction"

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

    def set_path_params(self, path_params):
        self._instance.path = path_params
        return self

    def set_query_params(self, params):
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

    def build(self) -> 'OpenAICustomHttpAction':
        return self._get_instance()

    def _get_instance(self) -> 'OpenAICustomHttpAction':
        if self._instance is None:
            self._instance = OpenAICustomHttpAction()
        return self._instance


class OpenAICustomHttpAction:
    """
    Represents a custom HTTP action for OpenAI.

    """
    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.method = None
        self.token = None
        self.headers = "{}"
        self.path = "{}"
        self.params = "{}"
        self.body = "{}"
        self.function_name = None

    def _execute_with_file(self, **kwargs):
        validate_http_input(self.param_schema_definition, **kwargs)

        headers = hydrate_input_fields(
            self.param_schema_definition, self.headers, **kwargs
        )
        query_params = hydrate_input_fields(
            self.param_schema_definition, self.params, **kwargs
        )
        body = hydrate_input_fields(self.param_schema_definition, self.body, **kwargs)

        headers["Authorization"] = f"Bearer {self.token}"

        base_64_file_str = body.get("file", None)
        if base_64_file_str is None:
            return StradaResponse(
                success=False,
                error=StradaError(
                    errorCode=400,
                    statusCode=400,
                    message="No 'file' provided.'file' is required.",
                ),
            )
        MIME_type = body.get("MIME_type", None)
        if MIME_type is None:
            return StradaResponse(
                success=False,
                error=StradaError(
                    errorCode=400,
                    statusCode=400,
                    message="No 'MIME_type' provided. 'MIME_type' is required.",
                ),
            )

        base_64_decoded = base64.b64decode(base_64_file_str)
        del body["file"]
        del body["MIME_type"]

        response = requests.request(
            self.method,
            self.url,
            headers=headers,
            params=query_params,
            data=body,
            files={"file": ("input_file", BytesIO(base_64_decoded), MIME_type)},
        )

        response_data = response.json()
        if response.ok:  # HTTP status code 200-299
            return StradaResponse(success=True, data=response_data)
        else:
            # If the response contains structured error information, you can parse it here
            error_message = response_data.get("message", None)
            if error_message is None:
                error_message = response_data.get("error", None)
            if error_message is None:
                error_message = response.text
            if error_message is None:
                error_message = "Error executing HTTP Request."

            error = StradaError(
                errorCode=response.status_code,
                statusCode=response.status_code,
                message=error_message,
            )
            return StradaResponse(success=False, data=response_data, error=error)

    def _execute_custom_assistant_message(self, **kwargs):
        validate_http_input(self.param_schema_definition, **kwargs)

        headers = hydrate_input_fields(
            self.param_schema_definition, self.headers, **kwargs
        )
        path_params = hydrate_input_fields(
            self.param_schema_definition, self.path, **kwargs
        )
        body = hydrate_input_fields(self.param_schema_definition, self.body, **kwargs)

        headers["Authorization"] = f"Bearer {self.token}"
        headers["Content-Type"] = "application/json"
        headers["OpenAI-Beta"] = "assistants=v1"

        # Create the message and body to the
        threads_run_body = {
            "assistant_id": path_params["assistant_id"],
            "thread": {"messages": [{"role": "user", "content": body["message"]}]},
        }
        thread_run_resp = requests.post(
            "https://api.openai.com/v1/threads/runs",
            headers=headers,
            json=threads_run_body,
        )
        if thread_run_resp.ok:
            # Try 5 times to get the response
            parsed_resp = thread_run_resp.json()
            thread_id = parsed_resp["thread_id"]
            run_id = parsed_resp["id"]
            assistant_id = parsed_resp["assistant_id"]

            for index in range(20):
                time.sleep(1 + (index * 1))
                response = requests.get(
                    f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}",
                    headers=headers,
                )
                if response.ok:
                    run_response = response.json()
                    status = run_response.get("status")
                    if status in ["cancelled", "failed", "completed"]:
                        if status == "completed":
                            response = requests.get(
                                f"https://api.openai.com/v1/threads/{thread_id}/messages",
                                headers=headers,
                            )
                            if response.ok:
                                threads_messages_resp = response.json()
                                messages = threads_messages_resp.get("data", [])
                                for message in messages:
                                    if message.get("role") == "assistant":
                                        content = message.get("content")
                                        for content_message in content:
                                            if content_message.get("type") == "text":
                                                text = content_message.get("text")

                                                return StradaResponse(
                                                    success=True,
                                                    data={
                                                        "assistant_id": assistant_id,
                                                        "thread_id": thread_id,
                                                        "run_id": run_id,
                                                        "assistant_response": text,
                                                    },
                                                )
                                        # Could not find a text response.
                                        return StradaResponse(
                                            success=False,
                                            error=StradaError(
                                                errorCode=404,
                                                statusCode=404,
                                                message=f"Could not retrieve a 'text' assistant response for thread_id='{thread_id}' and run_id='{run_id}'. This implies that a file was returned instead of a text response.\n Full OpenAI message response is provided in the 'data' field.",
                                            ),
                                            data=messages,
                                        )

                                return StradaResponse(
                                    success=False,
                                    error=StradaError(
                                        errorCode=404,
                                        statusCode=404,
                                        message=f"Could not retrieve assistant response for thread_id='{thread_id}' and run_id='{run_id}'.",
                                    ),
                                    data=threads_messages_resp,
                                )
                            else:
                                return StradaResponse(
                                    success=False,
                                    error=StradaError(
                                        errorCode=response.status_code,
                                        statusCode=response.status_code,
                                        message=f"Error getting messages for thread_id='{thread_id}' and run_id='{run_id}'",
                                    ),
                                    data=run_response,
                                )
                        elif status == "cancelled":
                            return StradaResponse(
                                success=False,
                                error=StradaError(
                                    errorCode=response.status_code,
                                    statusCode=response.status_code,
                                    message=f"Run execution was cancelled by OpenAI for thread_id='{thread_id}' and run_id='{run_id}'. Please try again: {response.text}",
                                ),
                                data=run_response,
                            )
                        elif status == "failed":
                            return StradaResponse(
                                success=False,
                                error=StradaError(
                                    errorCode=response.status_code,
                                    statusCode=response.status_code,
                                    message=f"Run execution failed by OpenAI for thread_id='{thread_id}' and run_id='{run_id}'. Please try again: {response.text}",
                                ),
                                data=run_response,
                            )
                else:
                    return StradaResponse(
                        success=False,
                        error=StradaError(
                            errorCode=response.status_code,
                            statusCode=response.status_code,
                            message=f"Error getting run information for thread_id='{thread_id}' and run_id='{run_id}': {response.text}",
                        ),
                    )

            return StradaResponse(
                success=False,
                error=StradaError(
                    errorCode=404,
                    statusCode=404,
                    message=f"Could not retrieve assistant response for thread_id='{thread_id}' and run_id='{run_id}' after all retry attempts.",
                ),
            )
        else:
            return StradaResponse(
                success=False,
                error=StradaError(
                    errorCode=thread_run_resp.status_code,
                    statusCode=thread_run_resp.status_code,
                    message=f"Error creating and running thread: {thread_run_resp.text}",
                ),
            )

    @with_debug_logs(app_name="openai-chatgpt")
    @exception_handler
    def execute(self, **kwargs) -> StradaHttpResponse:
        """Executes the custom HTTP action.\n---\nParameters should be passed as keyword arguments:\n```python\nres = MyAction.execute(name="Max")\n```"""
        if "audio/transcriptions" in self.url or "audio/translations" in self.url:
            return self._execute_with_file(**kwargs)
        elif "/assistants/{assistant_id}/message" in self.url:
            return self._execute_custom_assistant_message(**kwargs)
        else:
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
                    "OpenAI-Beta": "assistants=v1",
                    "Content-Type": "application/json",
                },
                function_name=self.function_name,
                app_name="openai-chatgpt",
                **kwargs,
            )

    @staticmethod
    def prepare(data) -> 'OpenAICustomHttpAction':
        """For Strada internal SDK use only."""
        builder = OpenAICustomHttpActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_method(data["method"])
            .set_token(data["access_token"])
            .set_path_params(data.get("path", "{}"))
            .set_headers(data.get("headers", "{}"))
            .set_query_params(data.get("query", "{}"))
            .set_body(data.get("body", "{}"))
            .set_function_name(data.get("function_name", None))
            .build()
        )