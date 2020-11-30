'''
Consider each of the tasks below as a separate database query. Using SQLAlchemy, which is the necessary code to:

- Select all the actors with the first name of your choice

- Select all the actors and the films they have been in

- Select all the actors that have appeared in a category of a comedy of your choice

- Select all the comedic films and sort them by rental rate

- Using one of the statements above, add a GROUP BY statement of your choice

- Using one of the statements above, add a ORDER BY statement of your choice

'''
import sqlalchemy
from pprint import pprint

engine = sqlalchemy.create_engine('mysql+pymysql://root:Password?@localhost/sakila')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

actor = sqlalchemy.Table('actor', metadata, autoload=True, autoload_with=engine)
film = sqlalchemy.Table('film', metadata, autoload=True, autoload_with=engine)
film_actor = sqlalchemy.Table('film_actor', metadata, autoload=True, autoload_with=engine)
film_category = sqlalchemy.Table('film_category', metadata, autoload=True, autoload_with=engine)
category = sqlalchemy.Table ('category', metadata, autoload=True, autoload_with=engine)

#select all the actors with the first name of your choice

query = sqlalchemy.select([actor]).where(actor.columns.first_name == 'PENELOPE')
result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
pprint(result_set)

# Select all the actors and the films they have been in

join_statement = actor.join(film_actor, film_actor.columns.actor_id == actor.columns.actor_id).join(film, film.columns.film_id == film_actor.columns.film_id)
query = sqlalchemy.select([actor.columns.first_name, actor.columns.last_name, film.columns.title]).select_from(join_statement)

result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
pprint(result_set)

# Select all the actors that have appeared in a category of of your choice

join_statement = actor.join(film_actor, film_actor.columns.actor_id == actor.columns.actor_id).join(film, film.columns.film_id == film_actor.columns.film_id).join(film_category, film_category.columns.film_id == film.columns.film_id).join(category, category.columns.category_id == category.columns.category_id )
query = sqlalchemy.select([actor.columns.first_name, actor.columns.last_name, category.columns.name]).where(category.columns.name == "Action").select_from(join_statement)

result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
pprint(result_set)

# Select all the comedic films and sort them by rental rate

join_statement = film.join(film_category, film_category.columns.film_id == film.columns.film_id).join(category, category.columns.category_id == film_category.columns.category_id)
query = sqlalchemy.select([film.columns.title, category.columns.name, film.columns.rental_rate]).where(category.columns.name == "Comedy").order_by(sqlalchemy.asc(film.columns.rental_rate)).select_from(join_statement)
result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
pprint(result_set)

# Using one of the statements above, add a GROUP BY statement of your choice

join_statement = film.join(film_category, film_category.columns.film_id == film.columns.film_id).join(category, category.columns.category_id == film_category.columns.category_id)
query = sqlalchemy.select([sqlalchemy.func.count(film.columns.film_id), category.columns.name]).group_by(category.columns.name).select_from(join_statement)
result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
pprint(result_set)

# Using one fo the statements above, add a ORDER BY statement of your choice

join_statement = actor.join(film_actor, film_actor.columns.actor_id == actor.columns.actor_id).join(film, film.columns.film_id == film_actor.columns.film_id).join(film_category, film_category.columns.film_id == film.columns.film_id).join(category, category.columns.category_id == film_category.columns.category_id )
query = sqlalchemy.select([actor.columns.last_name, actor.columns.first_name, film.columns.title, category.columns.name]).where(category.columns.name == "Action").order_by(sqlalchemy.asc(actor.columns.last_name)).select_from(join_statement)

result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
pprint(result_set)