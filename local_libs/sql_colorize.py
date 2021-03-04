from re import sub, I

def sql_color_set(query):
    sql_commands = ['select', 'from', 'DISTINCT', 'WHERE', 'or', 'not', 'ORDER BY', 'like', 'limit', 'offset', 'and', 'EXISTS']
    for command in sql_commands:
        query = sub(command, f"\033[94m{command}\033[0m", query, flags=I)

    return query
