from time import sleep
from httpx import Client
from pprint import pprint
from faker import Faker


def main():
    fake = Faker()

    with Client() as client:
        # response = client.get("http://localhost:8000/api")
        # pprint(response.json())

        for _ in range(10):
            user = dict(name=fake.name(), email=fake.email(), password=fake.password())
            client.post(url="http://localhost:8000/api/signup", json=user)
            pprint(user)
            sleep(0.5)


if __name__ == "__main__":
    main()
