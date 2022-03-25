from instagrapi import Client
from time import sleep
import random
import json
import os


try:
    user_name = os.environ['USERNAME']
    password = os.environ['PASSWORD']
except:
    print("Issue with env!!!")
    sleep(60)
    exit()


def create_if_not_file_exists(name):
    if not os.path.exists(name):
        with open(name, "w") as f:
            f.write("")
            f.close()


def create_folder_if_not_exists(name):
    if not os.path.exists(name):
        os.mkdir(name)


def get_random_line():
    file_path = "data/message.txt"
    with open(file_path) as f:
        lines = f.readlines()
        return random.choice(lines)


def login():
    cl = Client()
    print("Logging in...")
    cl.login(user_name, password)
    print("Logged in...")
    return cl


def get_media_ids(cl):
    feed = cl.get_timeline_feed()["feed_items"]
    medias = []
    for post in feed:
        try:
            media = post["media_or_ad"]["pk"]
            medias.append(cl.media_id(media))
        except:
            pass
    return medias


def add_user_as_messaged(username):
    with open("data/messaged_users.txt", "a") as f:
        f.write(f"{username}\n")
        f.close()


def already_messaged(username):
    with open("data/messaged_users.txt") as f:
        lines = f.readlines()
        return username in lines


def message(cl, username):
    message = get_random_line()
    user_id = cl.user_id_from_username(username)
    cl.direct_send(message, user_ids=[user_id])
    add_user_as_messaged(username)
    print(f"Messaged {username}!")


def message_commentors(cl, media_ids):
    for media_id in media_ids:
        comments = cl.media_comments(media_id)
        for comment in comments:
            comment = comment.dict()
            username = comment["user"]["username"]
            if not already_messaged(username):
                try:
                    message(cl, username)
                except:
                    print(f"Couldn't message {username}")


def main():
    create_folder_if_not_exists("data")
    create_if_not_file_exists("data/message.txt")
    create_if_not_file_exists("data/messaged_users.txt")
    cl = login()

    while True:
        print("Getting medias...")
        media_ids = get_media_ids(cl)
        print("Messaging commentors...")
        message_commentors(cl, media_ids)
        sleep(60)


if __name__ == "__main__":
    main()
