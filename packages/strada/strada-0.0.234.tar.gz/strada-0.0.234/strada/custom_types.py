from enum import Enum
from typing import Any, BinaryIO, Optional, Union
from pydantic import BaseModel

class HttpObjectType(Enum):
    REQUEST = 'REQUEST'
    RESPONSE = 'RESPONSE'
    
class LogType(Enum):
    FUNCTION_CALL = 'FUNCTION_CALL'
    HTTP_OBJECT = 'HTTP_OBJECT'

class StradaError(BaseModel):
    """
    Represents an error response returned by a Strada action.
    """

    errorCode: int
    """errorCode `int`\n---\nThe Strada error code associated with the error."""

    statusCode: int
    """statusCode `int`\n---\nThe end application action status code (usually HTTP status code) associated with the error."""

    message: str
    """message `str`\n---\nThe error message."""

    def __getitem__(self, item):
        return getattr(self, item)

class StradaResponse(BaseModel):
    """
    Represents a response returned by a Strada action. 
    """

    error: Optional[StradaError] = None
    """error `Optional[StradaError]`\n---\nAn optional error object if the response indicates an error."""
        
    success: bool
    """success `bool`\n---\nIndicates whether the execution was successful or not."""

    data: Optional[Any] = None
    """data `Optional[Any]`\n---\nAn optional data object containing the response data."""

    def __getitem__(self, item):
        return getattr(self, item)

class StradaHttpResponse(StradaResponse):
    """
    Represents an HTTP response returned by a Strada action. 
    """

    status_code: int
    """status_code `int`\n---\nThe HTTP status code of the response."""

    headers: dict
    """headers `dict`\n--\nThe HTTP headers of the response."""

class StradaFunction():
    def __init__(self, function_name: str):
        self.function_name = function_name

    def execute(self, **kwargs):
        raise NotImplementedError


FileContent = Union[bytes, BinaryIO]
FileTuple = tuple[str, FileContent, Union[str, None]]
FilesDict = dict[str, FileTuple]