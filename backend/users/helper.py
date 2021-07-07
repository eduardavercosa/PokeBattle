def is_email_valid(opponent):
    if "@" not in opponent or " " in opponent:
        return False
    if "." not in opponent.split("@")[1]:
        return False
    return True
