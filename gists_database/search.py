from .models import Gist

def search_gists(db_connection, **kwargs):
    query = "SELECT * FROM gists WHERE 1=1"
    params = {}

    # Simple filters
    if 'github_id' in kwargs:
        query += " AND github_id = :github_id"
        params['github_id'] = kwargs['github_id']

    if 'created_at' in kwargs:
        query += " AND datetime(created_at) = datetime(:created_at)"
        params['created_at'] = kwargs['created_at']

    # Advanced datetime filters
    operators = {
        'gt': '>',
        'gte': '>=',
        'lt': '<',
        'lte': '<='
    }

    for key, value in kwargs.items():
        for op_key, sql_op in operators.items():
            if key.startswith(f'created_at__{op_key}'):
                query += f" AND datetime(created_at) {sql_op} datetime(:{key})"
                params[key] = value
            if key.startswith(f'updated_at__{op_key}'):
                query += f" AND datetime(updated_at) {sql_op} datetime(:{key})"
                params[key] = value

    # Execute query
    cursor = db_connection.execute(query, params)
    rows = cursor.fetchall()

    return [Gist(row) for row in rows]
