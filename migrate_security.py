from sqlalchemy import inspect, text

from app import app

from extensions import db


with app.app_context():

    inspector = inspect(db.engine)

    table_name = "user"

    tables = inspector.get_table_names()

    if table_name not in tables:

        print(
            "User table does not exist yet."
        )

    else:

        columns = {
            column["name"]
            for column in inspector.get_columns(
                table_name
            )
        }


        # =====================================================
        # ROLE
        # =====================================================

        if "role" not in columns:

            db.session.execute(
                text(
                    """
                    ALTER TABLE user
                    ADD COLUMN role
                    VARCHAR(20)
                    NOT NULL
                    DEFAULT 'admin'
                    """
                )
            )

            print(
                "Added user.role"
            )

        else:

            print(
                "user.role already exists"
            )


        # =====================================================
        # ACTIVE
        # =====================================================

        if "active" not in columns:

            db.session.execute(
                text(
                    """
                    ALTER TABLE user
                    ADD COLUMN active
                    BOOLEAN
                    NOT NULL
                    DEFAULT 1
                    """
                )
            )

            print(
                "Added user.active"
            )

        else:

            print(
                "user.active already exists"
            )


        db.session.commit()


        print(
            "Security database migration completed."
        )