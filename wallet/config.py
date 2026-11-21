from pathlib import Path


class DatabasePath:
    # The project folder (the one with run.py), found from where this file is.
    # This way the path works on any computer, from any folder.
    PROJECT_DIR = Path(__file__).resolve().parent.parent
    PATH = str(PROJECT_DIR / "database" / "wallet.db")
