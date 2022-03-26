from instagrapi import Client
from time import sleep
from data_provider import add_user_as_messaged, already_messaged
import random
import json
import os


try:
    user_name = os.environ['IG_USERNAME']
    password = os.environ['IG_PASSWORD']
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
    session_file_path = f'data/session_{user_name}.json'
    cl = Client()
    print("Logging in...")
    try:
        cl.load_settings(session_file_path)
        print("Session file found!!!")
    except:
        pass
    cl.login(user_name, password)
    cl.dump_settings(session_file_path)
    print("Done")
    return cl


def get_media_ids(cl):
    following = cl.user_following(cl.user_id, 0)
    media_ids = []
    for user in following:
        user_name = cl.username_from_user_id(user)
        print("Searching for media from ", user_name)
        medias = cl.user_medias(user, 5)
        for media in medias:
            media_ids.append(media.id)
    return media_ids


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
                except Exception as e:
                    print(f"Couldn't message {username}", e)


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
