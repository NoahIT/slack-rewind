import pytest
from pydantic import ValidationError

from slack_rewind.core.models import (
    Conversation,
    ConversationType,
    Message,
    Reaction,
    UserProfile,
)


def message(**fields: object) -> Message:
    return Message.model_validate(
        {"channel_id": "C1", "ts": "1712345678.000100", "text": "Hello", **fields}
    )


@pytest.mark.parametrize(
    ("display_name", "real_name", "expected"),
    [("Ali", "Alice Smith", "Ali"), ("", "Alice Smith", "Alice Smith"), ("", "", "alice")],
)
def test_preferred_name_follows_slacks_order(
    display_name: str, real_name: str, expected: str
) -> None:
    user = UserProfile(id="U1", name="alice", real_name=real_name, display_name=display_name)
    assert user.preferred_name == expected


def test_models_cant_be_changed() -> None:
    user = UserProfile(id="U1", name="alice")
    with pytest.raises(ValidationError):
        user.name = "bob"  # type: ignore[misc]


def test_models_reject_fields_they_dont_know() -> None:
    with pytest.raises(ValidationError):
        UserProfile.model_validate({"id": "U1", "name": "alice", "is_admin": True})


def test_a_direct_message_is_identified_by_the_other_person() -> None:
    conversation = Conversation(id="D1", type=ConversationType.DIRECT_MESSAGE, user_id="U2")
    assert conversation.name is None
    assert conversation.user_id == "U2"


def test_a_direct_message_needs_the_other_person() -> None:
    with pytest.raises(ValidationError, match="the other person's user ID"):
        Conversation(id="D1", type=ConversationType.DIRECT_MESSAGE)


@pytest.mark.parametrize(
    "kind",
    [
        ConversationType.PUBLIC_CHANNEL,
        ConversationType.PRIVATE_CHANNEL,
        ConversationType.GROUP_MESSAGE,
    ],
)
def test_other_conversations_need_a_name(kind: ConversationType) -> None:
    with pytest.raises(ValidationError, match="needs a name"):
        Conversation(id="C1", type=kind)
    assert Conversation(id="C1", type=kind, name="general").name == "general"


def test_conversation_types_use_slacks_values() -> None:
    assert [kind.value for kind in ConversationType] == [
        "public_channel",
        "private_channel",
        "im",
        "mpim",
    ]


def test_bots_can_post_without_a_user() -> None:
    posted = message(bot_id="B1", subtype="bot_message")
    assert posted.user_id is None
    assert posted.bot_id == "B1"


def test_messages_keep_their_reactions() -> None:
    posted = message(reactions=[{"name": "thumbsup", "count": 2, "users": ["U1", "U2"]}])
    assert posted.reactions == (Reaction(name="thumbsup", count=2, users=("U1", "U2")),)


@pytest.mark.parametrize(
    ("fields", "parent", "reply"),
    [
        ({}, False, False),
        ({"thread_ts": "1712345678.000100", "reply_count": 3}, True, False),
        ({"thread_ts": "1712345678.000100", "reply_count": 0}, False, False),
        ({"thread_ts": "1712345600.000100"}, False, True),
    ],
    ids=["on its own", "starts a thread", "replies were deleted", "reply"],
)
def test_messages_know_their_place_in_a_thread(
    fields: dict[str, object], parent: bool, reply: bool
) -> None:
    posted = message(**fields)
    assert posted.is_thread_parent is parent
    assert posted.is_thread_reply is reply


@pytest.mark.parametrize("ts", ["", "1712345678", "1712345678.", "1712345678.0001.2", "abc.def"])
def test_timestamps_must_look_like_slacks(ts: str) -> None:
    with pytest.raises(ValidationError):
        message(ts=ts)
    with pytest.raises(ValidationError):
        message(thread_ts=ts)
