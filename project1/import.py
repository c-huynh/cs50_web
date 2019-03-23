import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader, None)
    for count, (isbn, title, author, year) in enumerate(reader):

        # Create author id if author not already in database
        if db.execute("SELECT * FROM authors WHERE name = :author_name", {"author_name": author}).rowcount == 0:
            db.execute("INSERT INTO authors (name) VALUES (:author_name)", {"author_name": author})

        # Insert book into database
        database_author = db.execute("SELECT id FROM authors WHERE name = :author_name", {"author_name": author}).fetchone()
        db.execute("INSERT INTO books (isbn, title, author_id, year) VALUES (:isbn, :title, :author_id, :year)",
                   {"isbn": isbn, "title": title, "author_id": database_author.id, "year": year})

        print(f"inserting {count}th book into database...")
    db.commit()

if __name__ == "__main__":
    main()
