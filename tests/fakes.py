from time import sleep
from httpx import Client
from pprint import pprint
from faker import Faker


def main():
    fake = Faker()
    base_url = "http://localhost:8000/"

    with Client(base_url=base_url) as client:
        users = client.get("/users").json()
        clients = {}
        for user in users:
            new = Client(base_url=base_url)
            new.post(
                "/login",
                json={
                    "email": user["email"],
                    "password": "password",
                },
            ).json()
            clients[user["email"]] = new

        for email, client in clients.items():
            user = client.get("/user").json()
            print(f"{user['email'] == email} {email}")


if __name__ == "__main__":
    main()
