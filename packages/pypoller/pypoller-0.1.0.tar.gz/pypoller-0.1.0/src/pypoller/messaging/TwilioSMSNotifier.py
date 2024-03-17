from typing import List
from twilio.rest import Client
from pypoller.util.decorators import non_null_args
from . import Notifier, Contact, Message
from .NotificationException import NotificationException


class TwilioSMSNotifier(Notifier):
    """
    Notifier class for sending SMS messages via Twilio.

    Uses Twilio's REST API to send SMS messages to contacts.
    """

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        phone_number: str,
        contacts: List[Contact] = [],
    ):
        """
        Initialize the TwilioSMSNotifier.

        Args:
            account_sid (str): Twilio account SID.
            auth_token (str): Twilio authentication token.
            phone_number (str): Twilio phone number used for sending messages.
            contacts (List[Contact], optional): List of contacts to be notified. Defaults to an empty list.
        """
        super().__init__(contacts)
        self.client = Client(account_sid, auth_token)
        self.phone_number = phone_number
        self.contacts = contacts

    @non_null_args
    def notify_inner(self, msg: Message):
        """
        Notify the contacts with the given message via SMS.

        Args:
            msg (Message): The message to be sent.
        """
        if len(msg.body) == 0:
            return

        for receiver in self.contacts:
            if not receiver.phone_number:
                print("Receiver phone number not provided, skipping")
                continue

            if msg.is_error and (not receiver.notify_error):
                print("Receiver not configured for errors, skipping")
                continue

            self.send_message(msg.body, receiver.phone_number)

    def send_message(self, message_body, phone_number):
        """
        Send an SMS message using Twilio's REST API.

        Args:
            message_body (str): The body of the message.
            phone_number (str): The phone number of the recipient.
        """
        try:
            self.client.messages.create(
                from_=self.phone_number, to=phone_number, body=message_body
            )
        except Exception as e:
            raise NotificationException("Exception when calling Twilio", e)
