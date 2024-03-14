import ipih


def start() -> None:
    from ws735Service.service import start

    start(True)


if __name__ == "__main__":
    start()
