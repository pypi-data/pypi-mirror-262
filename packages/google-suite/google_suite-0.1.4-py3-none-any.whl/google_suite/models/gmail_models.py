from typing import Union
from pydantic import BaseModel
from enum import Enum


class Header(BaseModel):
    name: str | None
    value: str | None


class MessagePartBody(BaseModel):
    attachmentId: str | None
    size: int | None
    data: str | None


class MessagePart(BaseModel):
    partId: str | None
    mimeType: str | None
    filename: str | None
    headers: list[Header] | None
    body: MessagePartBody | None
    parts: list[dict] | None


class Message(BaseModel):
    msg_id: str
    threadId: str
    labelIds: list[str] | None
    snippet: str | None
    historyId: str | None
    internalDate: str | None
    payload: MessagePart | None
    sizeEstimate: int | None
    raw: str | None


class UserMessageList(BaseModel):
    messages: list[Message] | None
    nextPageToken: str | None
    resultSizeEstimate: int | None


class MessageListVisibility(str, Enum):
    SHOW = "show"
    HIDE = "hide"


class LabelListVisibility(str, Enum):
    LABEL_SHOW = "labelShow"
    LABEL_HIDE = "labelHide"
    SHOW_IF_UNREAD = "labelShowIfUnread"


class Label(BaseModel):
    label_id: str
    name: str
    messageListVisibility: MessageListVisibility
    labelListVisibility: LabelListVisibility
    type: str | None
    messagesTotal: int | None
    messagesUnread: int | None
    threadsTotal: int | None
    threadsUnread: int | None
    color: dict | None


class SizeComparison(str, Enum):
    LARGE = "larger"
    SMALL = "smaller"


class Filter(BaseModel):
    id: str
    criteria: dict[str, Union[str, bool, int, SizeComparison]]
    action: dict[str, Union[list[str], str]]
