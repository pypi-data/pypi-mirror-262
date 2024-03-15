import re
from typing import ClassVar

from bs4 import BeautifulSoup
from pydantic import BaseModel

from google_suite.models import Service
from google_suite.utils import g_service


def extract_text_from_content(content: str):
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    cleaned_text = re.sub(
        r"[\U00010000-\U0010ffff]|\\u[0-9a-fA-F]{4}|\u200d♂️|\n", " ", text
    )
    return cleaned_text


class Blogger(BaseModel):
    """Blogger class that contains all the methods to interact with the Blogger API"""

    BLOG_ID: ClassVar[str] = "6382765553594944624"

    @staticmethod
    def list_blogs():
        return g_service(Service.blogger).blogs().listByUser(userId="self").execute()

    @staticmethod
    def list_posts():
        return g_service(Service.blogger).posts().list(blogId=Blogger.BLOG_ID).execute()

    @staticmethod
    def get_post_content(post_id: str):
        return (
            g_service(Service.blogger)
            .posts()
            .get(blogId=Blogger.BLOG_ID, postId=post_id)
            .execute()
        )

    @staticmethod
    def search_post(query: str):
        return (
            g_service(Service.blogger)
            .posts()
            .search(blogId=Blogger.BLOG_ID, q=query)
            .execute()
        )

    @staticmethod
    def insert_post(title: str, content: str):
        """Insert a new post in the blog. Content must be in HTML format starting and ending with the body."""
        return (
            g_service(Service.blogger)
            .posts()
            .insert(blogId=Blogger.BLOG_ID, body={"title": title, "content": content})
            .execute()
        )

    @staticmethod
    def delete_post_by_id(post_id: str):
        return (
            g_service(Service.blogger)
            .posts()
            .delete(blogId=Blogger.BLOG_ID, postId=post_id)
            .execute()
        )

    @staticmethod
    def delete_post_by_title(title: str):
        posts = Blogger.list_posts()
        for post in posts["items"]:
            if post["title"] == title:
                print("Deleting post with title:", title)
                return Blogger.delete_post_by_id(post["id"])

    @staticmethod
    def list_comments(post_id: str):
        return (
            g_service(Service.blogger)
            .comments()
            .list(blogId=Blogger.BLOG_ID, postId=post_id)
            .execute()
        )

    @staticmethod
    def get_comment_by_id(post_id: str, comment_id: str):
        return (
            g_service(Service.blogger)
            .comments()
            .get(blogId=Blogger.BLOG_ID, postId=post_id, commentId=comment_id)
            .execute()
        )

    @staticmethod
    def list_comments_by_blog():
        return (
            g_service(Service.blogger)
            .comments()
            .listByBlog(blogId=Blogger.BLOG_ID)
            .execute()
        )

    @staticmethod
    def mark_as_spam(post_id: str, comment_id: str):
        return (
            g_service(Service.blogger)
            .comments()
            .markAsSpam(blogId=Blogger.BLOG_ID, postId=post_id, commentId=comment_id)
            .execute()
        )

    @staticmethod
    def mark_as_not_spam(post_id: str, comment_id: str):
        return (
            g_service(Service.blogger)
            .comments()
            .approve(blogId=Blogger.BLOG_ID, postId=post_id, commentId=comment_id)
            .execute()
        )
