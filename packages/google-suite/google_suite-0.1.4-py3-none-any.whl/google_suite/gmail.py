import base64
import mimetypes
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.message import EmailMessage

from googleapiclient.errors import HttpError
from pydantic import BaseModel

from google_suite.models import (
    Filter,
    Label,
    LabelListVisibility,
    Message,
    MessageListVisibility,
    MessagePartBody,
    UserMessageList,
    Service,
)
from google_suite.utils import g_service


class Gmail(BaseModel):
    """Gmail class that contains all the methods to interact with the Gmail API"""

    @staticmethod
    def list_labels():
        """List all Labels of the user's labels

            Args:
                service (class): Gmail service object
            Returns:
                dict: {label_name: label_id}
                {
            "INBOX": "INBOX",
            "UNREAD": "UNREAD",
            "test": "Label_970233519473840444_example",
            etc...
        }
        """
        try:
            results = (
                g_service(Service.gmail).users().labels().list(userId="me").execute()
            )
            resp_labels = results.get("labels", {})
            if not resp_labels:
                print("No labels found.")
            else:
                print("Labels name: label id")
                return {label["name"]: label["id"] for label in resp_labels}
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def create_label(label_name: str):
        """Create a Label. To create a sub_label for a parent label, use the following format: 'parent_label/sub_label'.
        Args:
            label_name (str): 'test'
        Returns:
            Label
        """
        try:
            label = {
                "labelListVisibility": LabelListVisibility.SHOW_IF_UNREAD,
                "messageListVisibility": MessageListVisibility.SHOW,
                "name": label_name,
            }
            label = Label(
                **(
                    g_service(Service.gmail)
                    .users()
                    .labels()
                    .create(userId="me", body=label)
                    .execute()
                )
            )
            print("Label created successfully")
            return label
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def update_label(
        label_name: str,
        new_label_name: str = None,
        label_visibility: LabelListVisibility = None,
        message_visibility: MessageListVisibility = None,
    ):
        """Update a Label. To update a sub_label for a parent label, use the following format: 'parent_label/sub_label'.
        Args:
            label_name (str): 'test'
            new_label_name (str): 'test2'
        Returns:
            Label
        """
        try:
            label_id = Gmail.list_labels().get(label_name)
            label = {
                "labelListVisibility": label_visibility,
                "messageListVisibility": message_visibility,
                "name": new_label_name,
            }
            label = Label(
                **(
                    g_service(Service.gmail)
                    .users()
                    .labels()
                    .update(userId="me", id=label_id, body=label)
                    .execute()
                )
            )
            print("Label updated successfully")
            return label
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def delete_label(label_name: str):
        """Delete a Label. To delete a sub_label for a parent label, use the following format: 'parent_label/sub_label'.
        Args:
            label_name (str): 'test'
        Returns:
            None
        """
        try:
            label_id = Gmail.list_labels().get(label_name)
            g_service(Service.gmail).users().labels().delete(
                userId="me", id=label_id
            ).execute()
            print(
                f"Label name: {label_name}, Label with id: {label_id} deleted successfully"
            )
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def label_by_id(label_name: str):
        """Get a single label by id"""
        label_id: str = Gmail.list_labels().get(label_name)
        return label_id

    @staticmethod
    def label_by_name(msg_label_lsit: list):
        """Get a single label by name"""
        label_id: str = next(
            (label for label in msg_label_lsit if "Label" in label),
            None,
        )
        label_name: str = next(
            (key for key, value in Gmail.list_labels().items() if value == label_id),
            None,
        )
        return label_name

    @staticmethod
    def message_by_id(msg: Message):
        """Get a single message by id"""
        message = Message(
            **(
                g_service(Service.gmail)
                .users()
                .messages()
                .get(userId="me", id=msg["id"])
                .execute()
            )
        )
        return message

    @staticmethod
    def mark_read(msg_id: str):
        """Mark a single message as read"""
        message = Message(
            **(
                g_service(Service.gmail)
                .users()
                .messages()
                .modify(
                    userId="me",
                    id=msg_id,
                    body={"removeLabelIds": ["UNREAD"]},
                )
                .execute()
            )
        )
        return message

    @staticmethod
    def mark_unread(msg_id: str):
        """Mark a single message as unread"""
        message = Message(
            **(
                g_service(Service.gmail)
                .users()
                .messages()
                .modify(
                    userId="me",
                    id=msg_id,
                    body={"addLabelIds": ["UNREAD"]},
                )
                .execute()
            )
        )
        return message

    @staticmethod
    def list_unread_messages(label_id: str = None, sender: str = None):
        """Filtered unread messages from a label, or from a sender
        Args:
            label_id (str): 'Label_970233519473840444_example' = default(None)
            sender (str): 'example@gmail.com' = default(None)
        Returns:
            list[Message]"""
        try:
            if sender and label_id:
                unread_message_list = UserMessageList(
                    **(
                        g_service(Service.gmail)
                        .users()
                        .messages()
                        .list(
                            userId="me",
                            labelIds=[f"{label_id}"],
                            q=f"from:{sender}, is:unread",
                            maxResults=1000,
                        )
                        .execute()
                    )
                )
            elif sender and not label_id and "@" in sender:
                unread_message_list = UserMessageList(
                    **(
                        g_service(Service.gmail)
                        .users()
                        .messages()
                        .list(
                            userId="me",
                            q=f"from:{sender}, is:unread",
                            maxResults=1000,
                        )
                        .execute()
                    )
                )
            elif sender and not label_id:
                unread_message_list = UserMessageList(
                    **(
                        g_service(Service.gmail)
                        .users()
                        .messages()
                        .list(
                            userId="me",
                            q=f"{sender}, is:unread",
                            maxResults=1000,
                        )
                        .execute()
                    )
                )
            else:
                unread_message_list = UserMessageList(
                    **(
                        g_service(Service.gmail)
                        .users()
                        .messages()
                        .list(
                            userId="me",
                            labelIds=[f"{label_id}"],
                            q="is:unread",
                            maxResults=1000,
                        )
                        .execute()
                    )
                )
            messages = unread_message_list.model_dump().get("messages", [])
            messages_list: list[Message] = []
            if not messages:
                print(
                    f"No messages found. All messages must be read or no messages exist with the label. {label_id} or possibly no messages from {sender}"
                )
            else:
                print(f"Total unread Messages: {len(messages)}")
            for msg in messages:
                # get each message from the sender
                message = Gmail.message_by_id(msg)
                messages_list.append(message)
            return messages_list
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def mark_all_read(label_id: str = None, sender: str = None):
        """Mark all unread messages from a label from a sender as read"""
        try:
            # filtered unread messages from a label from a sender
            unread_messages = Gmail.list_unread_messages(label_id, sender)
            if not unread_messages:
                print()
                print("Messages might already be read.")
            else:
                print(f"You have {len(unread_messages)} Messages being marked as read:")
                for msg in unread_messages:
                    # get each message from the label from a sender
                    Gmail.mark_read(msg.id)
            print()
            print("All messages have been marked as read")
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def download_attachment(label_name: str = None, sender: str = None):
        """Get a single attachment by sender"""
        try:
            messages = []
            if label_name and not sender:
                label_id: str = Gmail.list_labels().get(label_name)
                messages = Gmail.list_unread_messages(label_id=label_id)
            elif sender and not label_name:
                messages = Gmail.list_unread_messages(sender=sender)
                for msg in messages:
                    for part in msg.payload.parts:
                        if "attachmentId" in part["body"]:
                            label_name = Gmail.label_by_name(msg.labelIds)
                            attachment = MessagePartBody(
                                **(
                                    g_service(Service.gmail)
                                    .users()
                                    .messages()
                                    .attachments()
                                    .get(
                                        userId="me",
                                        messageId=msg.id,
                                        id=part["body"]["attachmentId"],
                                    )
                                    .execute()
                                )
                            )
                            file_data = base64.urlsafe_b64decode(
                                attachment.data.encode("UTF-8")
                            )
                            if not os.path.exists("attachments"):
                                os.mkdir("attachments")
                            path = os.path.join(
                                os.getcwd(),
                                "attachments",
                                label_name + "_" + part["filename"].replace(" ", "_"),
                            )
                            with open(path, "wb") as f:
                                f.write(file_data)
                            print(
                                f"Attachment {label_name}_{part['filename']}  downloaded"
                            )
                            print()
                            Gmail.mark_read(msg.id)
                            return path
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def download_attachments(messages: list[Message]):
        """Download attachments from a list of messages using a ThreadPool"""
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_path = {
                executor.submit(Gmail.download_attachment_from_message, msg): msg
                for msg in messages
            }
            for future in as_completed(future_to_path):
                future.result()

    @staticmethod
    def download_attachment_from_message(msg: Message):
        """Download an attachment from a single message"""
        try:
            for part in msg.payload.parts:
                if "attachmentId" in part["body"]:
                    label_name = Gmail.label_by_name(msg.labelIds)
                    attachment = MessagePartBody(
                        **(
                            g_service(Service.gmail)
                            .users()
                            .messages()
                            .attachments()
                            .get(
                                userId="me",
                                messageId=msg.id,
                                id=part["body"]["attachmentId"],
                            )
                            .execute()
                        )
                    )
                    file_data = base64.urlsafe_b64decode(
                        attachment.data.encode("UTF-8")
                    )
                    if not os.path.exists("attachments"):
                        os.mkdir("attachments")
                    path = os.path.join(
                        os.getcwd(),
                        "attachments",
                        label_name + "_" + part["filename"].replace(" ", "_"),
                    )
                    with open(path, "wb") as f:
                        f.write(file_data)
                    print(f"Attachment {label_name}_{part['filename']}  downloaded")
                    print()
                    Gmail.mark_read(msg.id)
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def send_message(
        from_sender: str,
        to: str,
        subject: str,
        message_text: str,
        file: str = None,
        thread_id: str = None,
    ):
        """Send an new email message
        Args:
            from_sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.
            file: The filename of the attachment.
            thread_id: The id of the thread if you want to reply to it.
        Returns:
            Message
        """
        try:
            message = EmailMessage()
            message.set_content(message_text)
            message["to"] = to
            message["from"] = from_sender
            message["subject"] = subject
            if file:
                # guessing the MIME type
                type_subtype, _ = mimetypes.guess_type(file)
                maintype, subtype = type_subtype.split("/")
                with open(file, "rb") as fp:
                    attachment_data = fp.read()
                message.add_attachment(attachment_data, maintype, subtype)
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            created_message = {"raw": encoded_message}
            if thread_id:
                created_message["threadId"] = thread_id
            sent_message = Message(
                **(
                    g_service(Service.gmail)
                    .users()
                    .messages()
                    .send(userId="me", body=created_message)
                    .execute()
                )
            )
            return sent_message
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def list_filters():
        """List all filters
        Args:
            None
        Returns:
            list[Filter]
        """
        try:
            filters = (
                g_service(Service.gmail)
                .users()
                .settings()
                .filters()
                .list(userId="me")
                .execute()
                .get("filter", [])
            )
            list_of_filters: list[Filter] = []
            if not filters:
                print("No filters found.")
            else:
                for f in filters:
                    filt = Filter(**f)
                    list_of_filters.append(filt)
            return list_of_filters
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def get_filter(filter_id: str):
        """Get a filter
        Args:
            filter_id: The ID of the filter to get.
        Returns:
            Filter
        """
        try:
            filt = Filter(
                **(
                    g_service(Service.gmail)
                    .users()
                    .settings()
                    .filters()
                    .get(userId="me", id=filter_id)
                    .execute()
                )
            )
            return filt
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def create_filter(
        label_name: str = None,
        remove_from_inbox: bool = None,
        filter_from: str = None,
        subject: str = None,
        query: str = None,
        negatedQuery: str = None,
    ):
        """Create a filter
        Args:
            label_name: The name of the label to add to the filter.
            remove_from_inbox: boolean, whether to skip the  from the inbox.
            filter_from: The email address of the sender to add to the filter.
            subject: The subject of the email message to add to the filter.
            query: All emails that DO contain the string i.e. "secret knock"
            negatedQuery: All emails that do not contain the string i.e. "secret knock"
        Returns:
            Filter
        """
        try:
            labels = Gmail.list_labels()
            label_id = None
            if label_name in labels:
                label_id = labels[label_name]
            else:
                label = Gmail.create_label(label_name)
                label_id = label.id
            filter_content = {
                "criteria": {},
                "action": {},
            }
            if label_id:
                filter_content["action"]["addLabelIds"] = [f"{label_id}"]
            if remove_from_inbox:
                filter_content["action"]["removeLabelIds"] = ["INBOX"]
            if filter_from:
                filter_content["criteria"]["from"] = f"{filter_from}"
            if subject:
                filter_content["criteria"]["subject"] = f"{subject}"
            if query:
                filter_content["criteria"]["query"] = f"{query}"
            if negatedQuery:
                filter_content["criteria"]["negatedQuery"] = f"{negatedQuery}"
            created_filter = Filter(
                **(
                    g_service(Service.gmail)
                    .users()
                    .settings()
                    .filters()
                    .create(userId="me", body=filter_content)
                    .execute()
                )
            )
            return created_filter
        except HttpError as error:
            print("An error occurred:", error)

    @staticmethod
    def delete_filter(filter_id: str):
        """Delete a filter
        Args:
            filter_id: The ID of the filter to delete.
        Returns:
            None
        """
        try:
            g_service(Service.gmail).users().settings().filters().delete(
                userId="me", id=filter_id
            )
            print(f"Filter with id: {filter_id} deleted successfully")
        except HttpError as error:
            print("An error occurred:", error)
