from ..local_libs.decorators import query_decorator
from ..local_libs.singleton import Singleton
import sqlite3
import asyncio

class Sqlite(metaclass=Singleton):
    def __init__(self):
        self.conn = sqlite3.connect("./iatneh/database/iatneh.db")
        self.cursor = self.conn.cursor()

    @query_decorator
    def get_genres(self, limit, offset):
        query = f"select id, name from genres limit {limit} offset {offset}"
        return self.cursor.execute(query).fetchall(), query

    @query_decorator
    def count_genres(self):
        query = f"select count(*) from genres"
        return self.cursor.execute(query).fetchone()[0], query

    @query_decorator
    def find_anime_by_name(self, name):
        query = f"select * from animes where name like '%{name}%'"
        return self.cursor.execute(query).fetchall(), query

    @query_decorator
    def find_anime_by_genre(self, genres):
        query = "select * from animes a where "
        for genre_id in genres:
            query += f"EXISTS (SELECT * FROM animes_genres ag WHERE a.id = ag.anime_id AND ag.genre_id = {genre_id}) and "
        query = query[:-4] # удаляет не нужный and в конце запроса, он появляется из-за предыдущий строки
        return self.cursor.execute(query).fetchall(), query
