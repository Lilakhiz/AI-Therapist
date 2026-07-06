from twilio.rest import Client

from backend.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER,
)

from backend.database import get_user_by_id


def call_emergency(user_id):

    user = get_user_by_id(user_id)

    if not user:
        return

    emergency_contact = user["emergency_contact"]

    if not emergency_contact:
        return

    client = Client(
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN
    )

    client.calls.create(
        to=emergency_contact,
        from_=TWILIO_FROM_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"
    )