"""This module provides classes and utilities for interacting with Outlook email,
including sending and retrieving messages, managing folders, and handling exceptions."""
import base64
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List

from O365 import Message, Account
from O365.message import MessageAttachment
from O365.utils import Query

from t_office_365.endpoints import OutlookEndpoints
from t_office_365.exceptions import AssetNotFoundError


@dataclass
class QueryMap:
    def __init__(self, key: str, value: str or bool, method: str) -> None:
        """
        Initialize QueryMap with key, value, and method.

        :param key: Key to map to in query.
        :param value: Value to filter on.
        :param method: Method to apply for filtering.
        """
        self.key = key
        self.value = value
        self.method = method


class Outlook:
    """A class for interacting with Outlook email."""

    def __init__(self, account: Account) -> None:
        """
        Initialize the Outlook interface with the specified account.

        Parameters:
            account (Account): The account used to authenticate with Outlook.
        """
        self.endpoints = OutlookEndpoints(account)

    def get_emails(
        self,
        folder_name: str = "Inbox",
        subject: str = "",
        from_email: str = "",
        to: str = "",
        after: datetime = None,
        before: datetime = None,
        unread: bool = None,
        has_attachments: bool = None,
        pattern_by_subject: re.Pattern = None,
        pattern_by_attachment: re.Pattern = None,
    ) -> List[Message]:
        """
        Retrieve emails.

        :param:
            folder_name: Name of the folder from which to retrieve emails.
            subject: Subject filter for emails.
            from_email: Sender email filter for emails.
            to: Recipient email filter for emails.
            after: Filter for emails received after this datetime.
            before: Filter for emails received before this datetime.
            unread: Filter for unread emails.
            has_attachments: Filter for emails with attachments.
            pattern_by_subject: Filter for emails matching a pattern in subject.
            pattern_by_attachment: Filter for emails matching a pattern in attachments.

        :return: List of messages retrieved.
        """
        q_args = []
        if unread is not None:
            q_args.append(QueryMap(key="isRead", value=not unread, method="equals"))
        if has_attachments is not None:
            q_args.append(QueryMap(key="has_attachments", value=has_attachments, method="equals"))
        if subject:
            q_args.append(QueryMap(key="subject", value=subject, method="equals"))
        if pattern_by_subject is not None:
            q_args.append(QueryMap(key="subject", value=pattern_by_subject, method="contains"))
        if from_email:
            q_args.append(QueryMap(key="from", value=from_email, method="equals"))
        if to:
            q_args.append(QueryMap(key="to", value=to, method="equals"))
        if after:
            q_args.append(
                QueryMap(key="receivedDateTime", value=after.strftime("%Y-%m-%dT%H:%M:%SZ"), method="greater_equal")
            )
            q_args.pop()
        if before:
            q_args.append(
                QueryMap(key="receivedDateTime", value=before.strftime("%Y-%m-%dT%H:%M:%SZ"), method="less_equal")
            )
            q_args.pop()

        mailbox = self.endpoints.mailbox
        query = self.__query_map(mailbox.new_query(), q_args)

        email_folder = mailbox.get_folder(folder_name=folder_name)
        if not email_folder:
            raise AssetNotFoundError(f'No such folder: "{folder_name}"')

        messages = mailbox.get_messages(query=query)

        if pattern_by_attachment:
            # Filter messages based on attachment filenames
            filtered_messages = []
            for message in messages:
                attachments = message.attachments
                for attachment in attachments:
                    if re.match(pattern_by_attachment, attachment.name):
                        filtered_messages.append(message)
                        # No need to check other attachments if one matches
                        break
            return filtered_messages
        else:
            return messages

    def send_message(
        self,
        to: List = [],
        cc: List = [],
        subject: str = "",
        body: str = "",
        attachments: List = [],
        html: bool = False,
    ) -> None:
        """
        Send an email message.

        :param:
            to (list): List of email addresses to send the message to.
            cc (list): List of email addresses to include in the CC field.
            subject (str): Subject of the email message.
            body (str): Body of the email message.
            attachments (list): List of file paths or attachments to include in the email.
            html (bool): Indicates whether the body of the email is HTML formatted.

        :return:
            None
        """

        m = self.endpoints.new_message

        # Add recipients (To and CC)
        list(map(lambda _to: m.to.add(_to), to))
        list(map(lambda _cc: m.cc.add(_cc), cc))

        # Set subject and body
        m.subject = subject
        m.body = body

        # Save the message
        m.save_message()

        # Add attachments
        list(map(lambda attachment: m.attachment.add(attachment), attachments))

        # Set email body format (HTML or plain text)
        if html:
            m.body_format = "HTML"

        # Send the message
        m.send()

    def get_attachment_by_subject(self, subject: str, pattern: re.Pattern, folder_name: str) -> str:
        """
        Gets attachment from email by subject.

        :param:
            subject (str): Subject of the email to search for.
            pattern (str): Regular expression pattern to match for attachment file name.
            folder_name (str): Name of the folder to retrieve

        :return:
            str: File path of the saved attachment.
        """
        query = self.__query_map(
            self.endpoints.mailbox.new_query(), [QueryMap(key="subject", value=subject, method="equals")]
        )
        calendar_folder = self.endpoints.mailbox.get_folder(folder_name=folder_name)
        return self.__download_attachments(calendar_folder, query, pattern)

    def __get_by_date_emails(self, query=None) -> Message or None:
        """
        Retrieve emails by date.

        :param:
            query: Query for filtering emails.

        :return:
            Message: Email message object or None if no email is found.
        """
        all_messages = list(self.endpoints.inbox_folder.get_messages(query=query, download_attachments=False))
        for message in all_messages:
            if self.__check_date(message.created):
                message.mark_as_read()
                message.move(self.endpoints.archive_folder)
                return message
        return None

    def get_two_factor_code_email(
        self, subject_pattern: re.Pattern, otp_code_pattern: re.Pattern = r"\b\d{6}\b"
    ) -> str:
        """
        Retrieve two-factor authentication code from email.

        :param:
            subject_pattern (re.Pattern)
            otp_code_pattern (re.Pattern)

        :return:
            str: Two-factor authentication code extracted from the email.

        :raise:
            ValueError: If no email is found.
        """
        query = self.endpoints.mailbox.new_query().on_attribute("subject").contains(subject_pattern)
        retry_count = 0
        while retry_count < 12:
            if result := self.__get_by_date_emails(query):
                match = re.search(otp_code_pattern, result.body.split("<body>")[1].split("<br><br>")[0].strip())
                if match:
                    return match.group()
            retry_count += 1
            time.sleep(5)
        else:
            raise ValueError("No email found")

    def __query_map(self, query_obj: Query, query_args: List[QueryMap]) -> Query:
        """
        Method that Maps attributes and values to a query object.

        :param:
            query (Query):  Query object to which attributes and values will be mapped.

        :return:
            Query: Modified query object.
        """
        for q in query_args:
            query_obj = getattr(query_obj.on_attribute(q.key), q.method)(q.value)
        return query_obj

    @staticmethod
    def __download_attachments(folder, query, pattern: re.Pattern = ""):
        """
        Downloads attachments from messages in a folder that match a specified pattern.

        :param:
            folder (Folder): folder from which to retrieve messages.
            query (Query): query object to filter messages.
            pattern (str): regular expression pattern to match attachment filenames.

        :return:
            str: File path of downloaded attachment.

        :raise:
            AttachmentNotFoundError: if no attachment found
        """
        messages = list(folder.get_messages(query=query, download_attachments=True))
        messages = list(filter(lambda x: any(re.match(pattern, f.name) for f in list(x.attachments)), messages))
        messages = sorted(messages, key=lambda x: x.received, reverse=True)

        for message in messages:
            for file in message.attachments:
                if re.match(pattern, file.name):
                    file_path = os.path.join(os.getcwd(), file.name)
                    with open(file_path, "wb") as w:
                        decoded_content = base64.b64decode(file.content)
                        w.write(decoded_content)
                    return file_path
        else:
            raise AssetNotFoundError("No attachment found")

    @staticmethod
    def __check_date(mail_date):
        """Check if the mail date is within 2 minutes of the current time."""
        time_now = datetime.now()
        return (
            time_now.date() == mail_date.date()
            and time_now.hour == mail_date.hour
            and time_now.minute - mail_date.minute <= 2
        )

    @staticmethod
    def download_attachment(file: MessageAttachment, download_dir: str = None) -> str:
        """
        Download an attachment from an email message and save it to the specified directory.

        :param:
            file (MessageAttachment): The attachment file object to download.
            download_dir (str): The directory where the attachment will be saved.

        :return:
            str: The file path of the downloaded attachment.
        """
        if not download_dir:
            download_dir = f"{os.getcwd()}/{file.name}"
        file_path = os.path.join(download_dir)
        with open(file_path, "wb") as w:
            decoded_content = base64.b64decode(file.content)
            w.write(decoded_content)
        return file_path
