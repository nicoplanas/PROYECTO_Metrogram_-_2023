from user import *

class Multimedia:
    def __init__(self, publisher, type, url, caption, date, tags, comments, likes, cont_likes, cont_comments, cont_interactions):
        self.publisher = publisher
        self.type = type
        self.url = url
        self.caption = caption
        self.date = date
        self.tags = tags
        self.multimedia = {"type": type, "url": url}
        self.comments = comments
        self.likes = likes
        self.cont_likes = cont_likes
        self.cont_comments = cont_comments
        self.cont_interactions = cont_interactions

    def show_attr(self, username):
        hashtags = ""
        for tag in self.tags:
            if len(hashtags) == 0:
                hashtags += f"#{tag}"
            else:
                hashtags += f" #{tag}"
        x = slice(0, 10)
        return f"""
PUBLISHED BY '@{username}' - TYPE: {self.type}
LIKES: {self.cont_likes}

CAPTION: {self.caption}
TAGS: {hashtags}

{self.cont_comments} COMMENTS
PUBLISHED: {self.date[x]}"""

    def give_like(self, logged_in_user, user):
       
        if logged_in_user.username in self.likes:
            remove_like = input("""\nYa usted le dio like a esta publicación, desea remover su like?
                
1. Si.
2. No.

>> """)
            if remove_like == "1":
                self.likes.remove(logged_in_user.username)
                self.cont_likes = len(self.likes)
                self.cont_interactions -= 1
                logged_in_user.cont_interactions -= 1
                user.cont_interactions -= 1
            else:
                return "FINALIZADO"
            
        elif logged_in_user.username not in self.likes:
            self.likes.append(logged_in_user.username)
            self.cont_likes = len(self.likes)
            self.cont_interactions += 1
            logged_in_user.cont_interactions += 1
            user.cont_interactions += 1

    def add_comment(self, logged_in_user, user, comment, date):

        self.comments.append({"commenter": logged_in_user.username.lower(), "comment": comment, "date": date})
        self.cont_comments = len(self.comments)
        self.cont_interactions += 1
        logged_in_user.cont_interactions += 1
        user.cont_interactions += 1