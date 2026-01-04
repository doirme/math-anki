import os
from pathlib import Path

from db.models import Base
from db.session import engine


def reset_database():
    print("⚠️  Resetting Database...")

    # 1. Close all connections (optional, but good practice)
    engine.dispose()

    # 2. Drop all tables if they exist
    print("Dropping all tables...")
    Base.metadata.drop_all(engine)

    # 3. Recreate all tables
    print("Recreating tables...")
    Base.metadata.create_all(engine)

    print("✅ Database reset successfully! You can now regenerate your blocks.")


if __name__ == "__main__":
    # Ensure we are in the right directory to find the db file if relative
    reset_database()
