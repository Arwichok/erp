from contextlib import suppress
import os

with suppress(FileNotFoundError):
    os.remove("test.sqlite3")
os.environ["DB_URL"] = "sqlite+aiosqlite:///test.sqlite3"
