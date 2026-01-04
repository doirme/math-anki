import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from db.models import Base
from db.session import DB_URL, init_db


def forced_reset():
    print(f"Database URL: {DB_URL}")

    # Path for SQLite
    if DB_URL.startswith("sqlite:///"):
        db_path = DB_URL.replace("sqlite:///", "")
        # Handle relative path starting with ./
        if db_path.startswith("./"):
            db_path = db_path[2:]

        path = Path(db_path)
        if path.exists():
            print(f"Deleting existing database file at {path}...")
            try:
                os.remove(path)
                print("File deleted.")
            except Exception as e:
                print(f"Error deleting file: {e}")
                print("Please make sure the Streamlit app is closed!")
                return
        else:
            print("Database file not found, creating new one.")

    print("Initializing database with new schema...")
    try:
        init_db()
        print("✅ Database initialized successfully with the 'meta_data' column.")
    except Exception as e:
        print(f"Error initializing DB: {e}")


if __name__ == "__main__":
    forced_reset()
