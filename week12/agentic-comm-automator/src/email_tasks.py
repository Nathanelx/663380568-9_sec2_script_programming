# agentic-comm-automator/src/email_tasks.py
import email
import imaplib
import os
import smtplib
from email.header import decode_header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


class EmailTasks:
    """
    Handles sending (SMTP) and receiving (IMAP) emails.
    """
    def __init__(self, smtp_server, smtp_port, imap_server, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.imap_server = imap_server
        self.sender_email = sender_email
        self.sender_password = sender_password
        self._smtp = None  # Internal SMTP connection
        self._imap = None  # Internal IMAP connection
        logger.info(f"EmailTasks initialized for {sender_email}.")

    # --- SMTP (Sending) Methods ---
    def _connect_smtp(self):
        """Establishes and logs into the SMTP server."""
        if self._smtp:
            return True
        try:
            self._smtp = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30)
            self._smtp.starttls()  # Secure the connection
            self._smtp.login(self.sender_email, self.sender_password)
            logger.info("Successfully connected and logged into SMTP server.")
            return True
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed. Check email and app password. Error: {e}")
        except smtplib.SMTPConnectError as e:
            logger.error(f"SMTP connection failed. Check server address and port. Error: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during SMTP connect/login: {e}")
        self._smtp = None
        return False

    def _disconnect_smtp(self):
        """Disconnects from the SMTP server."""
        if self._smtp:
            try:
                self._smtp.quit()
                logger.info("Disconnected from SMTP server.")
            except Exception as e:
                logger.warning(f"Error during SMTP disconnection: {e}")
            finally:
                self._smtp = None

    def send_email(self, recipients, subject, body, attachments=None, is_html=False):
        """
        Sends an email with optional multiple attachments.
        :param recipients: dict with lists for 'to', 'cc', 'bcc'.
        :param attachments: list of file paths (missing files are skipped).
        :return: True if email sent successfully, False otherwise.
        """
        to_recipients = recipients.get('to', [])
        cc_recipients = recipients.get('cc', [])
        bcc_recipients = recipients.get('bcc', [])  # BCC ไม่ใส่ใน header
        all_recipients = to_recipients + cc_recipients + bcc_recipients
        if not all_recipients:
            logger.error("No recipients specified for email.")
            return False

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = ", ".join(to_recipients)
        if cc_recipients:
            msg['Cc'] = ", ".join(cc_recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html' if is_html else 'plain', 'utf-8'))

        for attachment_path in attachments or []:
            if not os.path.exists(attachment_path):
                logger.warning(f"Attachment file not found: {attachment_path}. Skipping.")
                continue
            try:
                filename = os.path.basename(attachment_path)
                with open(attachment_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=filename)
                part['Content-Disposition'] = f'attachment; filename="{filename}"'
                msg.attach(part)
                logger.info(f"Attached file: {attachment_path}")
            except Exception as e:
                logger.error(f"Error attaching file {attachment_path}: {e}")

        if not self._connect_smtp():
            return False
        try:
            self._smtp.send_message(msg, from_addr=self.sender_email, to_addrs=all_recipients)
            cc_text = f" (CC: {', '.join(cc_recipients)})" if cc_recipients else ""
            logger.info(f"Email sent successfully to {', '.join(to_recipients)}{cc_text}. Subject: '{subject}'.")
            return True
        except Exception as e:
            logger.error(f"Failed to send email. Error: {e}")
            return False
        finally:
            self._disconnect_smtp()

    # --- IMAP (Receiving) Methods ---
    def _connect_imap(self):
        """Establishes and logs into the IMAP server."""
        if self._imap:
            return True
        try:
            self._imap = imaplib.IMAP4_SSL(self.imap_server)
            self._imap.login(self.sender_email, self.sender_password)
            logger.info("Successfully connected and logged into IMAP server.")
            return True
        except imaplib.IMAP4.error as e:
            logger.error(f"IMAP authentication failed. Check email and app password. Error: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during IMAP connect/login: {e}")
        self._imap = None
        return False

    def _disconnect_imap(self):
        """Disconnects from the IMAP server."""
        if self._imap:
            try:
                self._imap.logout()
                logger.info("Disconnected from IMAP server.")
            except Exception as e:
                logger.warning(f"Error during IMAP disconnection: {e}")
            finally:
                self._imap = None

    def search_emails(self, mailbox='INBOX', criteria='UNSEEN', from_sender=None, subject_contains=None):
        """
        Searches for emails based on criteria (UNSEEN/SEEN/ALL + FROM + SUBJECT).
        :return: A list of email IDs (bytes).
        """
        if not self._connect_imap():
            return []
        try:
            self._imap.select(mailbox)
            search_query = [criteria]
            if from_sender:
                search_query.extend(['FROM', f'"{from_sender}"'])
            if subject_contains:
                search_query.extend(['SUBJECT', f'"{subject_contains}"'])

            status, email_ids = self._imap.search(None, *search_query)
            if status != 'OK':
                logger.error(f"IMAP search failed. Status: {status}")
                return []

            uids = email_ids[0].split() if email_ids and email_ids[0] else []
            logger.info(f"Found {len(uids)} emails matching criteria in '{mailbox}'.")
            return uids
        except Exception as e:
            logger.error(f"Error searching emails: {e}")
            return []
        finally:
            self._disconnect_imap()

    def parse_message(self, raw_email, download_attachments_dir=None):
        """Parses a raw RFC822 email into sender, subject, text/html body, and attachments."""
        msg = email.message_from_bytes(raw_email)
        text_body, html_body, attachments_meta = "", "", []

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            filename = part.get_filename()

            if "attachment" in content_disposition or filename:
                if not filename:
                    continue
                filename = os.path.basename(self._decode_header_part(filename))  # กันชื่อไฟล์มี path
                filepath = None
                if download_attachments_dir:
                    ensure_directory_exists(download_attachments_dir)
                    filepath = os.path.join(download_attachments_dir, filename)
                    try:
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        logger.info(f"Downloaded attachment: {filepath}")
                    except Exception as e:
                        logger.error(f"Error downloading attachment {filename}: {e}")
                        filepath = None
                attachments_meta.append({'filename': filename, 'filepath': filepath})
            elif content_type in ("text/plain", "text/html"):
                charset = part.get_content_charset() or 'utf-8'
                text = part.get_payload(decode=True).decode(charset, errors='replace')
                if content_type == "text/plain":
                    text_body += text
                else:
                    html_body += text

        return {
            "sender": self._decode_header_part(msg['From']),
            "subject": self._decode_header_part(msg['Subject']),
            "text_body": text_body,
            "html_body": html_body,
            "has_attachments": bool(attachments_meta),
            "attachments_meta": attachments_meta,
        }

    def fetch_email_content(self, uid, mark_as_read=True, download_attachments_dir=None):
        """
        Fetches and parses a specific email by ID. Optionally marks as read and downloads attachments.
        :return: dict with uid, sender, subject, text_body, html_body, has_attachments, attachments_meta; or None.
        """
        if not self._connect_imap():
            return None
        try:
            self._imap.select('INBOX')
            status, msg_data = self._imap.fetch(uid, '(RFC822)')
            if status != 'OK' or not msg_data or not msg_data[0]:
                logger.error(f"Failed to fetch email UID {uid}. Status: {status}")
                return None

            info = self.parse_message(msg_data[0][1], download_attachments_dir)
            info["uid"] = uid.decode('utf-8')

            if mark_as_read:
                self._imap.store(uid, '+FLAGS', '\\Seen')
                logger.info(f"Marked email UID {info['uid']} as read.")
            return info
        except Exception as e:
            logger.error(f"Error fetching/parsing email UID {uid}: {e}")
            return None
        finally:
            self._disconnect_imap()

    def _decode_header_part(self, header_value):
        """Decodes header parts that might be encoded (e.g., '=?UTF-8?B?U3ViamVjdA==?=')."""
        if header_value is None:
            return ""
        decoded_string = ""
        for part, charset in decode_header(header_value):
            if isinstance(part, bytes):
                try:
                    decoded_string += part.decode(charset if charset else 'utf-8')
                except (LookupError, UnicodeDecodeError):
                    decoded_string += part.decode('latin-1', errors='replace')
            else:
                decoded_string += part
        return decoded_string.strip()
