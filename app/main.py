from app.kafka_broker import KafkaBroker  # noqa: F401


def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    broker = KafkaBroker()
    broker.start()


if __name__ == "__main__":
    main()
