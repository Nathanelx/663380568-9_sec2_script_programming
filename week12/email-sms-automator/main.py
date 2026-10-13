# email-sms-automator/main.py
import os
import sys
import time

# เรียกใช้โมดูลผ่านแพ็กเกจ src (ต้องรันจากโฟลเดอร์ email-sms-automator)
from src.email_sender import EmailSender
from src.email_receiver import EmailReceiver
from src.sms_gateway import SMSGateway
from src.utils import setup_logging, get_env_variable, ensure_directory_exists

logger = setup_logging(__name__)

RECEIVING_DEMO_SUBJECT = "Python Test: Email for Receiving Demo"


def main():
    """
    Main function to orchestrate email and SMS automation tasks.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    attachments_dir = os.path.join(data_dir, 'attachments')
    ensure_directory_exists(data_dir)
    ensure_directory_exists(attachments_dir)

    # --- Load Credentials from Environment Variables (.env) ---
    try:
        sender_email = get_env_variable("SENDER_EMAIL")
        sender_app_password = get_env_variable("SENDER_APP_PASSWORD")
        smtp_server = get_env_variable("SMTP_SERVER")
        smtp_port = int(get_env_variable("SMTP_PORT"))
        imap_server = get_env_variable("IMAP_SERVER")

        test_recipient_email = get_env_variable("TEST_RECIPIENT_EMAIL")
        test_sms_phone_number = get_env_variable("TEST_SMS_PHONE_NUMBER")
        test_sms_carrier = get_env_variable("TEST_SMS_CARRIER")
        student_info = get_env_variable("STUDENT_INFO", "ชื่อ-นามสกุล และรหัสนักศึกษา")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}. Please set all required environment variables in your .env file.")
        sys.exit(1)

    # --- Initialize Handlers ---
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_app_password)
    email_receiver = EmailReceiver(imap_server, sender_email, sender_app_password)
    sms_gateway = SMSGateway(email_sender)

    # --- Task 1: Send a simple plaintext email ---
    logger.info("--- Task 1: Sending a simple plaintext email ---")
    email_sender.send_email(
        recipient_email=test_recipient_email,
        subject="ทดสอบ Automated Python Test Email",
        body=f"{student_info}\n\nHello from your Python automation script! This is a plain text email."
    )
    time.sleep(2)  # Give a short delay

    # --- Task 2: Send an email with an attachment ---
    logger.info("--- Task 2: Sending an email with an attachment ---")
    attachment_file_path = os.path.join(data_dir, 'dummy_report.pdf')
    if os.path.exists(attachment_file_path):
        email_sender.send_email(
            recipient_email=test_recipient_email,
            subject="ทดสอบ Python Test Email with Attachment - Daily Report",
            body=f"{student_info}\n\nPlease find the daily report attached.",
            attachment_path=attachment_file_path
        )
    else:
        logger.warning(f"Attachment file not found at '{attachment_file_path}'. Skipping attachment email.")
    time.sleep(2)

    # --- Task 3: Send an SMS via email gateway ---
    logger.info("--- Task 3: Sending an SMS via email gateway ---")
    sms_gateway.send_sms(
        phone_number=test_sms_phone_number,
        message="Hello from Python! This is an automated SMS via email gateway.",
        carrier_name=test_sms_carrier
    )
    time.sleep(5)  # Give more time for SMS to arrive

    # --- Task 4: Receive and process emails ---
    logger.info("--- Task 4: Receiving and processing emails ---")
    # Send a new email to self to ensure there's an email to find for demo
    email_sender.send_email(
        recipient_email=sender_email,  # Send to self
        subject=f"ทดสอบ {RECEIVING_DEMO_SUBJECT}",
        body=f"{student_info}\n\nThis email is specifically for the receiving demo. It has an attachment!",
        attachment_path=attachment_file_path if os.path.exists(attachment_file_path) else None
    )
    logger.info("Sent a demo email to self for receiving task. Waiting a few seconds...")
    time.sleep(10)  # Give email server time to process and deliver

    # Search for unseen emails from self with a specific subject
    uids = email_receiver.search_emails(
        criteria='UNSEEN',
        from_sender=sender_email,
        subject_contains=RECEIVING_DEMO_SUBJECT
    )

    if uids:
        logger.info(f"Found {len(uids)} matching unread email(s) for receiving demo.")
        for uid in uids:
            logger.info(f"Processing email UID: {uid.decode('utf-8')}")
            email_details = email_receiver.fetch_email_content(
                uid=uid,
                mark_as_read=True,
                download_attachments_dir=attachments_dir
            )
            if email_details:
                logger.info(f"  Sender: {email_details['sender']}")
                logger.info(f"  Subject: {email_details['subject']}")
                logger.info(f"  Body Snippet: {email_details['body_snippet']}")
                if email_details['attachments_downloaded']:
                    logger.info(f"  Attachments downloaded: {', '.join(email_details['attachments_downloaded'])}")
                else:
                    logger.info("  No attachments downloaded for this email.")
            else:
                logger.error(f"Could not retrieve details for email UID: {uid.decode('utf-8')}")
    else:
        logger.info("No matching unread emails found for receiving demo.")

    logger.info("--- All communication automation tasks completed ---")


if __name__ == "__main__":
    main()
