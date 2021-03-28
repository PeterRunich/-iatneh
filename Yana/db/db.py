from ..lib.decorators import query_decorator
from ..lib.singleton import Singleton
from os import path
import sqlite3

class Sqlite(metaclass=Singleton):
    def __init__(self):
        self.conn = sqlite3.connect(path.dirname(__file__) + '/iatneh.db')
        self.cursor = self.conn.cursor()

        self.cache = {}
        self.__cache_all_genres()
        self.__cache_count_genres()

    @query_decorator
    def get_genres(self, limit, offset):
        query = f"select id, name from genres limit {limit} offset {offset}"

        if 'all_genres' in self.cache:
            return self.cache['all_genres'][offset:offset+limit], 'cached | ' + query
        else:
            return self.cursor.execute(query).fetchall(), query

    @query_decorator
    def get_genres_by_ids(self, ids):
        ids = ','.join(ids)
        query = f"select id, name from genres where id in ({ids})"

        return self.cursor.execute(query).fetchall(), query

    @query_decorator
    def find_genre_by_name(self, name):
        query = f"select * from genres where name like '%{name}%'"

        return self.cursor.execute(query).fetchall(), query

    @query_decorator
    def count_genres(self):
        query = f"select count(*) from genres"
        if 'count_genres' in self.cache:
            return self.cache['count_genres'], 'cached | ' + query
        else:
            return self.cursor.execute(query).fetchone()[0], query


    @query_decorator
    def find_anime_by_name(self, name, limit=0, offset=0):
        query = f"select * from animes where name like '%{name}%'"
        if limit != 0: query += f' limit {limit} offset {offset}'
        return self.cursor.execute(query).fetchall(), query

    @query_decorator
    def find_anime_by_genre(self, genres, limit=0, offset=0):
        query = "select * from animes a"

        for i, _ in enumerate(genres):
            query += f" join animes_genres ag{i} on a.id = ag{i}.anime_id"

        query += ' where'

        for i, genre_id in enumerate(genres):
            query += f" ag{i}.genre_id = {genre_id} and"


        query = query[:-4] # удаляет не нужный and в конце запроса, он появляется из-за предыдущий строки

        query += ' group by a.id'

        if limit != 0: query += f' limit {limit} offset {offset}'

        print(query)

        return self.cursor.execute(query).fetchall(), query

    def __cache_all_genres(self):
        self.cache['all_genres'] = self.get_genres(limit=10000, offset=0)

    def __cache_count_genres(self):
        self.cache['count_genres'] = self.count_genres()
