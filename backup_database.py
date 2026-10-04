import sqlite3

from pathlib import Path

from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = (
    BASE_DIR / "instance"
)

BACKUP_DIR = (
    BASE_DIR / "backups"
)


DATABASE_DIR.mkdir(
    exist_ok=True
)

BACKUP_DIR.mkdir(
    exist_ok=True
)


SOURCE_DATABASE = (
    DATABASE_DIR /
    "smart_attendance.db"
)


if not SOURCE_DATABASE.exists():

    print(
        "Database not found:"
    )

    print(
        SOURCE_DATABASE
    )

    raise SystemExit(1)


timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)


BACKUP_DATABASE = (
    BACKUP_DIR /
    f"smart_attendance_{timestamp}.db"
)


source = sqlite3.connect(
    SOURCE_DATABASE
)

destination = sqlite3.connect(
    BACKUP_DATABASE
)


with destination:

    source.backup(
        destination
    )


destination.close()

source.close()


print(
    "Backup created successfully:"
)

print(
    BACKUP_DATABASE
)