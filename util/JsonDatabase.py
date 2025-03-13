import os
import re
from pysondb import db


def _create_db_file(file_path):
    if not os.path.exists(file_path):
        if os.path.dirname(file_path) != '':
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        db.create_db(os.path.basename(file_path), create_file=True)
        print(f"Created new database file at {file_path}")


class JsonDatabase:
    def __init__(self, db_file):
        _create_db_file(db_file)
        self.db = db.getDb(db_file)

    def add(self, data):
        return self.db.add(data)

    def get_all(self):
        return self.db.getAll()

    def search_by_key(self, key, value):
        return self.db.reSearch(key, re.escape(value))


if __name__ == "__main__":
    db = JsonDatabase('/home/walter/Videos/Eiga/fortuna/imdb_cache.json')
    print(db.search_by_key('genre', 'Comedy'))
