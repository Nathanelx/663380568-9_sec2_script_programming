# agentic-comm-automator/src/sms_tasks.py
from .utils import setup_logging
from .email_tasks import EmailTasks  # Reuse EmailTasks for sending the actual email

logger = setup_logging(__name__)


class SMSTasks:
    """
    Sends SMS via email-to-SMS gateways (one email per phone number).
    """
    def __init__(self, email_tasks_instance):
        if not isinstance(email_tasks_instance, EmailTasks):
            raise TypeError("SMSTasks requires an instance of EmailTasks.")
        self.email_tasks = email_tasks_instance

        # Common US carrier email-to-SMS gateways (add more as needed)
        self.carrier_gateways = {
            "att": "@txt.att.net",
            "verizon": "@vtext.com",
            "tmobile": "@tmomail.net",
            "sprint": "@messaging.sprintpcs.com",
            "boost": "@sms.boostmobile.com",
            "cricket": "@mms.cricketwireless.net",
            "us_cellular": "@email.uscc.net",
        }
        logger.info("SMSTasks initialized.")

    def get_gateway_address(self, phone_number, carrier_name=None):
        """Builds '1234567890@txt.att.net', or returns phone_number if it is already a gateway address."""
        if carrier_name and carrier_name.lower() in self.carrier_gateways:
            return f"{phone_number}{self.carrier_gateways[carrier_name.lower()]}"
        if '@' in phone_number and '.' in phone_number:
            return phone_number
        return None

    def send_sms(self, phone_numbers, message, carrier_name=None):
        """
        Sends an SMS to every phone number in the list.
        :return: True if all messages were sent (email-wise), False otherwise.
        """
        if not phone_numbers:
            logger.warning("No phone numbers provided for SMS.")
            return False

        success_count = 0
        for phone_number in phone_numbers:
            gateway_address = self.get_gateway_address(phone_number, carrier_name)
            if not gateway_address:
                logger.warning(f"No known carrier for {phone_number} and it is not a gateway address. Cannot send SMS.")
                continue
            logger.info(f"Attempting to send SMS to {phone_number} via gateway: {gateway_address}")
            if self.email_tasks.send_email(recipients={'to': [gateway_address]}, subject="", body=message):
                success_count += 1

        logger.info(f"Attempted to send {len(phone_numbers)} SMS messages, {success_count} succeeded (email-wise).")
        return success_count == len(phone_numbers)
