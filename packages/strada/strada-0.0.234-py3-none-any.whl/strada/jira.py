import base64
import builtins
from typing import Optional

from pydantic import BaseModel, Field, ValidationError
import requests
from .custom_types import StradaError, StradaHttpResponse, StradaResponse
from .exception import StradaValidationException
from .sdk import HttpRequestExecutor
from .exception_handler import exception_handler
from .common import (
    build_input_schema_from_strada_param_definitions,
    custom_print,
    hydrate_input_fields,
    validate_http_input,
)
from .debug_logger import with_debug_logs

# Initialize the print function to use the logger
builtins.print = custom_print


class SearchIssueRequestPayload(BaseModel):
    """
    Represents a payload for searching Jira issues.
    """

    issue_key: Optional[str] = Field(None, title="Issue Key")
    """issue_key `Optional[str]`\n---\nThe issue key."""

    summary: Optional[str] = Field(None, title="Summary")
    """summary `Optional[str]`\n---\nThe summary of the issue."""
    
    def __getitem__(self, item):
        return getattr(self, item)   

class CreateIssueRequestPayload(BaseModel):
    """
    Represents a payload for creating a Jira issue.
    """

    project: str = Field(..., title="Project")
    """project `str`\n---\nThe project of the issue."""

    issue_type: str = Field(..., title="Issue Type")
    """issue_type `str`\n---\nThe type of the issue."""

    summary: str = Field(..., title="Summary")
    """summary `str`\n---\nThe summary of the issue."""

    description: Optional[str] = Field(None, title="Description")
    """description `Optional[str]`\n---\nThe description of the issue."""

    reporter_id: Optional[str] = Field(None, title="Reporter ID")
    """reporter_id `Optional[str]`\n---\nThe ID of the reporter."""

    assignee_id: Optional[str] = Field(None, title="Assignee ID")
    """assignee_id `Optional[str]`\n---\nThe ID of the assignee."""

    parent_id: Optional[str] = Field(None, title="Parent ID")
    """parent_id `Optional[str]`\n---\nThe ID of the parent issue."""

    def __getitem__(self, item):
        return getattr(self, item)   

class JiraIssueData(BaseModel):
    """
    Represents the data of a Jira issue or subtask.

    Attributes:
        id (str): The ID of the created issue or subtask.
        key (str): The key of the created issue or subtask.
        self (str): The URL of the created issue or subtask.
    """

    id: str = Field(
        ..., title="ID", description="The ID of the created issue or subtask."
    )
    """id `str`\n---\nThe ID of the created issue or subtask."""

    key: str = Field(
        ..., title="Key", description="The key of the created issue or subtask."
    )
    """key `str`\n---\nThe key of the created issue or subtask."""

    self: str = Field(
        ..., title="Self", description="The URL of the created issue or subtask."
    )
    """self `str`\n---\nThe URL of the created issue or subtask."""

    def __getitem__(self, item):
        return getattr(self, item)   

class JiraSearchIssuesResponse(StradaResponse):
    """
    Represents a response from a Jira search issues API call.

    Attributes:
        success (bool): Indicates whether the API call was successful.
        error (StradaError): An error object containing details if the API call failed.
        data (dict): The raw JSON data returned by the API call.
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
            error_messages = raw_json.get("errorMessages", [])
            if len(error_messages) > 0:
                message = " ".join(error_messages)
            else:
                message = http_response.text
            self.error = StradaError(
                errorCode=http_response.status_code,
                statusCode=http_response.status_code,
                message=message,
            )
            self.data = raw_json


class JiraSearchIssuesAction:
    """
    Represents an action to search for issues in Jira.

    Attributes:
        param_schema_definition (Any): The parameter schema definition.
        token (str): The access token.
        base_url (str): The base URL of the Jira instance.
        cloud_id (str): The cloud ID of the Jira instance.
        function_name (str): The name of the function.
        payload (str): The payload for the action.
    """

    def __init__(self):
        self.param_schema_definition = None
        self.token = None
        self.base_url = None
        self.cloud_id = None
        self.function_name = None
        self.payload = "{}"

    def _parse_if_valid(self, raw_payload):
        # Now validate the payload against the SendPromptRequestPayload schema
        try:
            return SearchIssueRequestPayload(**raw_payload)
        except ValidationError as e:
            raise StradaValidationException(
                str(e), schema=SearchIssueRequestPayload.schema(), data=raw_payload
            )

    @with_debug_logs(app_name="jira")
    @exception_handler
    def execute(self, **kwargs) -> JiraSearchIssuesResponse:
        """Executes the Jira Search Issues action.\n---\nParameters should be passed as keyword arguments:\n```python\nres = MyAction.execute(name="Max")\n```"""
        validate_http_input(self.param_schema_definition, **kwargs)

        raw_payload = hydrate_input_fields(
            self.param_schema_definition, self.payload, **kwargs
        )

        parsed_payload = self._parse_if_valid(raw_payload)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        if parsed_payload.issue_key and parsed_payload.summary:
            jql = f"key = {parsed_payload.issue_key} AND summary ~ '{parsed_payload.summary}'"
        elif parsed_payload.issue_key:
            jql = f"key = {parsed_payload.issue_key}"
        elif parsed_payload.summary:
            jql = f"summary ~ '{parsed_payload.summary}'"

        create_search_payload = {
            "expand": ["names", "schema"],
            "fields": ["*all"],
            "fieldsByKeys": False,
            "jql": jql,
            "maxResults": 50,
            "startAt": 0,
        }
        response = requests.post(
            f"https://api.atlassian.com/ex/jira/{self.cloud_id}/rest/api/3/search",
            headers=headers,
            json=create_search_payload,
        )

        return JiraSearchIssuesResponse(response)

    @staticmethod
    def prepare(data) -> 'JiraSearchIssuesAction':
        """For Strada internal SDK use only."""
        builder = JiraSearchIssuesActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_token(data["access_token"])
            .set_base_url(data["base_url"])
            .set_cloud_id(data["cloud_id"])
            .set_payload(data["payload"])
            .set_function_name(data.get("function_name", None))
            .build()
        )


class JiraCreateIssueResponse(StradaResponse):
    """
    Represents the response received when creating an issue in Jira.
    """

    data: Optional[JiraIssueData]
    """data `Optional[JiraIssueData]`\n---\nThe response data."""

    def __init__(self, http_response: requests.Response):
        super().__init__(
            success=False, error=None, data=None
        )  # Initialize parent class attributes

        if http_response.ok:
            raw_json: dict = http_response.json()
            self.data = JiraIssueData(
                id=raw_json["id"], key=raw_json["key"], self=raw_json["self"]
            )
            self.success = True
        else:
            raw_json: dict = http_response.json()
            error_messages = raw_json.get("errorMessages", [])
            if len(error_messages) > 0:
                message = " ".join(error_messages)
            else:
                message = http_response.text
            self.error = StradaError(
                errorCode=http_response.status_code,
                statusCode=http_response.status_code,
                message=message,
            )
            self.data = raw_json


class JiraSearchIssuesActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "JiraSearchIssueAction"

    def set_param_schema(self, param_schema):
        decoded = base64.b64decode(param_schema).decode("utf-8")
        self._get_instance().param_schema_definition = (
            build_input_schema_from_strada_param_definitions(decoded)
        )
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_base_url(self, base_url):
        self._get_instance().base_url = base_url
        return self

    def set_cloud_id(self, cloud_id):
        self._get_instance().cloud_id = cloud_id
        return self

    def set_payload(self, row_data_json: str):
        decoded = base64.b64decode(row_data_json).decode("utf-8")
        self._get_instance().payload = decoded
        return self

    def set_function_name(self, function_name):
        if function_name is None:
            self._instance.function_name = self.default_function_name
        else:
            self._instance.function_name = function_name
        return self

    def build(self) -> 'JiraSearchIssuesAction':
        return self._get_instance()

    def _get_instance(self) -> 'JiraSearchIssuesAction':
        if self._instance is None:
            self._instance = JiraSearchIssuesAction()
        return self._instance


class JiraCreateIssueActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "JiraCreateIssueAction"

    def set_param_schema(self, param_schema):
        decoded = base64.b64decode(param_schema).decode("utf-8")
        self._get_instance().param_schema_definition = (
            build_input_schema_from_strada_param_definitions(decoded)
        )
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_base_url(self, base_url):
        self._get_instance().base_url = base_url
        return self

    def set_cloud_id(self, cloud_id):
        self._get_instance().cloud_id = cloud_id
        return self

    def set_payload(self, row_data_json: str):
        decoded = base64.b64decode(row_data_json).decode("utf-8")
        self._get_instance().payload = decoded
        return self

    def set_function_name(self, function_name):
        if function_name is None:
            self._instance.function_name = self.default_function_name
        else:
            self._instance.function_name = function_name
        return self

    def build(self) -> 'JiraCreateIssueAction':
        return self._get_instance()

    def _get_instance(self) -> 'JiraCreateIssueAction':
        if self._instance is None:
            self._instance = JiraCreateIssueAction()
        return self._instance


class JiraCreateIssueAction:
    """
    Represents an action to create an issue in Jira.
    """
    def __init__(self):
        self.param_schema_definition = None
        self.token = None
        self.base_url = None
        self.cloud_id = None
        self.function_name = None
        self.payload = "{}"

    def _parse_if_valid(raw_payload):
        # Now validate the payload against the SendPromptRequestPayload schema
        try:
            return CreateIssueRequestPayload(**raw_payload)
        except ValidationError as e:
            raise StradaValidationException(
                str(e), schema=CreateIssueRequestPayload.schema(), data=raw_payload
            )

    @with_debug_logs(app_name="jira")
    @exception_handler
    def execute(self, **kwargs) -> JiraCreateIssueResponse:
        """Executes the Jira Create Issue action.\n---\nParameters should be passed as keyword arguments:\n```python\nres = MyAction.execute(name="Max")\n```"""
        validate_http_input(self.param_schema_definition, **kwargs)

        raw_payload = hydrate_input_fields(
            self.param_schema_definition, self.payload, **kwargs
        )

        parsed_payload = JiraCreateIssueAction._parse_if_valid(raw_payload)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        create_issue_payload = {
            "fields": {
                "project": {"id": parsed_payload.project},
                "issuetype": {"id": parsed_payload.issue_type},
                "summary": parsed_payload.summary,
            }
        }
        if parsed_payload.description:
            create_issue_payload["fields"]["description"] = {
                "content": [
                    {
                        "content": [
                            {
                                "text": parsed_payload.description,
                                "type": "text",
                            }
                        ],
                        "type": "paragraph",
                    }
                ],
                "type": "doc",
                "version": 1,
            }
        if parsed_payload.reporter_id:
            create_issue_payload["fields"]["reporter"] = {
                "id": parsed_payload.reporter_id
            }

        if parsed_payload.assignee_id:
            create_issue_payload["fields"]["assignee"] = {
                "id": parsed_payload.assignee_id
            }

        if parsed_payload.parent_id:
            create_issue_payload["fields"]["parent"] = {"id": parsed_payload.parent_id}

        response = requests.post(
            f"https://api.atlassian.com/ex/jira/{self.cloud_id}/rest/api/3/issue",
            headers=headers,
            json=create_issue_payload,
        )

        return JiraCreateIssueResponse(response)

    @staticmethod
    def prepare(data) -> 'JiraCreateIssueAction':
        """For Strada internal SDK use only."""
        builder = JiraCreateIssueActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_token(data["access_token"])
            .set_base_url(data["base_url"])
            .set_cloud_id(data["cloud_id"])
            .set_payload(data["payload"])
            .set_function_name(data.get("function_name", None))
            .build()
        )


class JiraCustomHttpActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "JiraAction"

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

    def build(self) -> 'JiraCustomHttpAction':
        return self._get_instance()

    def _get_instance(self) -> 'JiraCustomHttpAction':
        if self._instance is None:
            self._instance = JiraCustomHttpAction()
        return self._instance


class JiraCustomHttpAction:
    """
    Represents a custom HTTP action for Jira.

    Attributes:
        param_schema_definition (str): The JSON schema definition for the dynamic parameters.
        url (str): The URL for the HTTP request.
        method (str): The HTTP method for the request.
        token (str): The access token for authentication.
        headers (str): The headers for the request in JSON format.
        path (str): The path parameters for the request in JSON format.
        params (str): The query parameters for the request in JSON format.
        body (str): The body of the request in JSON format.
        function_name (str): The name of the function associated with the action.
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

    @with_debug_logs(app_name="jira")
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
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            function_name=self.function_name,
            app_name="jira",
            **kwargs,
        )

    @staticmethod
    def prepare(data) -> 'JiraCustomHttpAction':
        """For Strada internal SDK use only."""
        builder = JiraCustomHttpActionBuilder()
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