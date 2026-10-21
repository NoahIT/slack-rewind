from enum import StrEnum
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

type Timestamp = Annotated[str, Field(pattern=r"^\d+\.\d+$")]


class _Model(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class UserProfile(_Model):
    """A person in the Slack workspace.

    Attributes:
        id: The Slack user ID, for example ``U012AB3CD``.
        name: The person's handle.
        real_name: Their full name, if set.
        display_name: The name they chose to be shown, if set.
        email: Their email address, when the token is allowed to read it.
        avatar_url: A link to their profile picture, if there is one.
    """

    id: str
    name: str
    real_name: str = ""
    display_name: str = ""
    email: str | None = None
    avatar_url: str | None = None

    @property
    def preferred_name(self) -> str:
        """The name Slack shows: the display name, then the real name, then the handle."""
        return self.display_name or self.real_name or self.name


class ConversationType(StrEnum):
    """The kinds of conversation, with the values Slack's API uses for them."""

    PUBLIC_CHANNEL = "public_channel"
    PRIVATE_CHANNEL = "private_channel"
    DIRECT_MESSAGE = "im"
    GROUP_MESSAGE = "mpim"


class Conversation(_Model):
    """A channel, direct message or group message the user is in.

    Attributes:
        id: The Slack conversation ID, for example ``C012AB3CD``.
        type: What kind of conversation it is.
        name: The conversation's name. Direct messages have none.
        user_id: For a direct message, the other person's user ID.
        topic: The channel's topic, if set.
    """

    id: str
    type: ConversationType
    name: str | None = None
    user_id: str | None = None
    topic: str = ""

    @model_validator(mode="after")
    def _check_identity(self) -> Self:
        if self.type is ConversationType.DIRECT_MESSAGE:
            if self.user_id is None:
                raise ValueError("a direct message needs the other person's user ID")
        elif self.name is None:
            raise ValueError(f"a conversation of type {self.type} needs a name")
        return self


class Reaction(_Model):
    """An emoji reaction on a message.

    Attributes:
        name: The emoji's name, for example ``thumbsup``.
        count: How many people reacted with it.
        users: Who reacted, by user ID.
    """

    name: str
    count: int
    users: tuple[str, ...] = ()


class Message(_Model):
    """A message in a conversation, or a reply in a thread.

    Attributes:
        channel_id: The conversation it was posted in.
        ts: Slack's timestamp for it, such as ``1712345678.000200``, which identifies the
            message within its conversation.
        text: The text as Slack stores it, with mentions written as ``<@U012AB3CD>``.
        user_id: Who posted it. Some bots and integrations post without a user.
        bot_id: The bot or integration that posted it, if one did.
        subtype: Slack's subtype for messages that aren't plain posts, such as
            ``channel_join``.
        thread_ts: The ``ts`` of the thread's first message, when the message is part of a
            thread.
        reply_count: How many replies the message has, when it starts a thread.
        reactions: The emoji reactions on it.
        permalink: A link that opens the message in Slack, once it is known.
    """

    channel_id: str
    ts: Timestamp
    text: str
    user_id: str | None = None
    bot_id: str | None = None
    subtype: str | None = None
    thread_ts: Timestamp | None = None
    reply_count: int = 0
    reactions: tuple[Reaction, ...] = ()
    permalink: str | None = None

    @property
    def is_thread_parent(self) -> bool:
        """Whether the message starts a thread that has replies."""
        return self.thread_ts == self.ts and self.reply_count > 0

    @property
    def is_thread_reply(self) -> bool:
        """Whether the message is a reply in another message's thread."""
        return self.thread_ts is not None and self.thread_ts != self.ts
