import time


def do_something():
    pass


def run():
    while True:
        time.sleep(60)
        do_something()


if __name__ == "__main__":
    run()
