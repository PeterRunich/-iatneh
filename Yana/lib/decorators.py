from .sql_colorize import sql_color_set
from time import time

def query_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time()
            data, query = func(*args, **kwargs)

            query = sql_color_set(query)
            print(f"\033[92m|{round(time() - start_time, 5)} sec.|\033[0m {query}")

            return data

        return wrapper
