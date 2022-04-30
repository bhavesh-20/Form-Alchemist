import os

log_file = os.path.join(os.getcwd(), "log.txt")


def write_log(message):
    """
    Write a message to a log file.
    """
    if not os.path.exists(log_file):
        open(log_file, "w").close()

    with open(log_file, "a") as f:
        print(message)
        f.write(message + "\n")
