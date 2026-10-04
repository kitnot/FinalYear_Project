import sqlite3

from pathlib import Path

from datetime import datetime


def backup_database(
    database_path
):

    database_path = Path(
        database_path
    )


    if not database_path.exists():

        return None


    backup_directory = (
        database_path.parent.parent
        / "backups"
    )


    backup_directory.mkdir(
        parents=True,
        exist_ok=True
    )


    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    backup_path = (
        backup_directory
        / f"smart_attendance_{timestamp}.db"
    )


    source = sqlite3.connect(
        database_path
    )

    destination = sqlite3.connect(
        backup_path
    )


    try:

        with destination:

            source.backup(
                destination
            )

    finally:

        destination.close()

        source.close()


    return backup_path