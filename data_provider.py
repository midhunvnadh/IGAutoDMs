

def add_user_as_messaged(username):
    with open("data/messaged_users.txt", "a") as f:
        f.write(f"{username}\n")
        f.close()


def already_messaged(username):
    with open("data/messaged_users.txt", "r") as f:
        string = f.read()
        lines = string.splitlines()
        return username in lines
