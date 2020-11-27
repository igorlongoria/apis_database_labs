'''

All of the following exercises should be done using sqlalchemy.

Using the provided database schema, write the necessary code to print information about the film and category table.

'''
import sqlalchemy
from pprint import pprint

engine = sqlalchemy.create_engine('mysql+pymysql://root:Vetealaverga04?@localhost/sakila')
connection = engine.connect()
metadata = sqlalchemy.MetaData()
film = sqlalchemy.Table('film', metadata, autoload=True, autoload_with=engine)
category = sqlalchemy.Table('category', metadata, autoload=True, autoload_with=engine)

#print(film.columns.keys())
#print(repr(metadata.tables['film']))

query = sqlalchemy.select([film])
query_2 = sqlalchemy.select([category])
result_proxy = connection.execute(query)
result_proxy2 = connection.execute(query_2)

result_set = result_proxy.fetchmany(100)
result_set2 = result_proxy2.fetchall()
pprint(result_set)
pprint(result_set2)