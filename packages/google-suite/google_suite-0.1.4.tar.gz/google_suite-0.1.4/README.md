# Google Suite

Python library to automate handling of various Google Suite APIs such as Gmail, Blogger, etc.

## Setup

- Make sure you have your Google token and credentials for your project from Google Cloud. You can follow the steps [here](https://developers.google.com/gmail/api/quickstart/python) to get started. You'll have to enable the Blogger api also.

## gmail.py

Quick overview of the methods:

| Name                 | Description                                                                                                                                                                | Arguments                                                                                                       |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| list_labels          | List of labels (returns a dict)                                                                                                                                            | None                                                                                                             |
| create_label         | Creates a label                                                                                                                                                            | label_name: str                                                                                                  |
| update_label         | Updates a label                                                                                                                                                            | label_name: str, new_label_name: str, label_visibility: LabelListVisibility, message_visibility: MessageListVisibility |
| delete_label         | Deletes a label                                                                                                                                                            | label_name: str                                                                                                  |
| label_by_id          | Gets a label by id                                                                                                                                                         | label_name: str                                                                                                  |
| label_by_name        | Gets a label by name                                                                                                                                                       | msg_label_list: list                                                                                             |
| mark_read            | Marks an email as read by id                                                                                                                                               | msg_id: str                                                                                                      |
| mark_all_read        | Marks all emails as read given a label or sender or both                                                                                                                   | label_id: str = None, sender: str = None                                                                         |
| mark_unread          | Marks an email as unread by id                                                                                                                                             | msg_id: str                                                                                                      |
| list_messages        | List of messages                                                                                                                                                           | None                                                                                                             |
| send_message         | Sends a message that can have with or without an attachment. If provided a threadId it will also reply within the email thread chain.                                      | from_sender: str, to: str, subject: str, message_text: str, file: str = None, thread_id: str = None            |
| download_attachment  | Downloads an attachment and puts it in the attachments directory. Returns the path of the attachment. Also marks the email as read                                         | label_name: str = None, sender: str = None                                                                      |
| download_attachments | Download attachments from a list of messages using a ThreadPool and puts it in the attachments directory. Returns the path of the attachment. Also marks the email as read | messages: list[Message]                                                                                          |
| list_filters         | List of filters                                                                                                                                                            | None                                                                                                             |
| get_filter           | Get a filter by id                                                                                                                                                         | filter_id: str                                                                                                  |
| create_filter        | Creates a filter                                                                                                                                                           | label_name: str = None, remove_from_inbox: bool = None, filter_from: str = None, subject: str = None, query: str = None, negatedQuery: str = None |
| update_filter        | Updates a filter                                                                                                                                                           | label_name: str, new_label_name: str = None, label_visibility: LabelListVisibility = None, message_visibility: MessageListVisibility = None |
| delete_filter        | Deletes a filter                                                                                                                                                           | filter_id: str                                                                                                  |

```python
from google_suite import Gmail

Gmail.list_labels()

# {'CHAT': 'CHAT',
#  'SENT': 'SENT',
#  'INBOX': 'INBOX',
#   etc...
#  'Unwanted': 'Label_9'}
```

## blogger.py

The `blogger.py` file contains methods to interact with the Blogger API:

| Method               | Description                                                                                           | Arguments                                                                                                       |
| -------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| list_blogs           | Lists all blogs by the user.                                                                          | None                                                                                                             |
| list_posts           | Lists all posts in a specific blog.                                                                   | None                                                                                                             |
| get_post_content     | Retrieves the content of a specific post.                                                             | post_id: str                                                                                                     |
| search_post          | Searches for posts based on a query.                                                                  | query: str                                                                                                       |
| insert_post          | Inserts a new post in the blog.                                                                       | title: str, content: str                                                                                        |
| delete_post_by_id    | Deletes a post by its ID.                                                                             | post_id: str                                                                                                     |
| delete_post_by_title | Deletes a post by its title.                                                                          | title: str                                                                                                      |
| list_comments        | Lists comments for a specific post.                                                                   | post_id: str                                                                                                     |
| get_comment_by_id    | Retrieves a comment by its ID.                                                                        | post_id: str, comment_id: str                                                                                    |
| list_comments_by_blog| Lists comments for the entire blog.                                                                   | None                                                                                                             |
| mark_as_spam         | Marks a comment as spam.                                                                              | post_id: str, comment_id: str                                                                                    |
| mark_as_not_spam     | Marks a comment as not spam.                                                                          | post_id: str, comment_id: str                                                                                    |

```python
from google_suite import Blogger
Blogger.list_blogs()
# {'kind': 'blogger#blogList',
#  'items': [{'kind': 'blogger#blog',
#    'id': '63.....',
#    'status': 'LIVE',
#    'name': 'The coolest blog ever',
#    'description': '',
#    'published': '2023-10-18T06:58:29-07:00',
#    'updated': '2024-03-12T10:20:35-07:00',
#    'url': 'http://tedfulk.blogspot.com/',
#    'selfLink': 'https://blogger.googleapis.com/v3/blogs/63.....',
#    'posts': {'totalItems': 2,
#     'selfLink': 'https://blogger.googleapis.com/v3/blogs/63...../posts'},
#    'pages': {'totalItems': 0,
#     'selfLink': 'https://blogger.googleapis.com/v3/blogs/63...../pages'},
#    'locale': {'language': 'en', 'country': '', 'variant': ''}}]}
```

## Utilizing the Service Object

The `util.py` file builds the service object to interact with the Google APIs. Ensure that the project is set up in the Google Cloud Platform, and the necessary permissions and correct access to the scopes for the APIs are granted.
