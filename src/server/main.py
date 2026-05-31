import os

from server.db.database import init_db


def main() -> None:
    print("Status API server started.")
    db_url = os.getenv("DATABASE_URL")
    print(db_url)
    init_db(db_url)
    return 0


if __name__=="__main__":
    main()
