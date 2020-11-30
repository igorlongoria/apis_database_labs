'''

Please create a new Python application that interfaces with a brand new database.
This application must demonstrate the ability to:

    - create at least 3 tables
    - insert data to each table
    - update data in each table
    - select data from each table
    - delete data from each table
    - use at least one join in a select query

BONUS: Make this application something that a user can interact with from the CLI. Have options
to let the user decide what tables are going to be created, or what data is going to be inserted.
The more dynamic the application, the better!


'''
import sqlalchemy
from sqlalchemy import func
from pprint import pprint

engine = sqlalchemy.create_engine('mysql+pymysql://root:Password?@localhost/Baseball_Players')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# Create 3 tables.
baseball_player = sqlalchemy.Table('baseball_player', metadata,
                                   sqlalchemy.Column('player_id', sqlalchemy.Integer(), nullable=False, primary_key=True),
                                   sqlalchemy.Column('first_name', sqlalchemy.String(255), nullable=False),
                                   sqlalchemy.Column('last_name', sqlalchemy.String(255), nullable=False),
                                   sqlalchemy.Column('last_update', sqlalchemy.DateTime(timezone=True), nullable=False, server_default=func.now()))

stat_names = sqlalchemy.Table('stat_names', metadata,
                                sqlalchemy.Column('stat_id', sqlalchemy.Integer(), primary_key=True, nullable=False),
                                sqlalchemy.Column('stat_name', sqlalchemy.String(255), nullable=False),
                                sqlalchemy.Column('last_update', sqlalchemy.DateTime(timezone=True), nullable=False, server_default=func.now()))

player_stats = sqlalchemy.Table('player_stats', metadata,
                                sqlalchemy.Column('player_id', sqlalchemy.Integer(), sqlalchemy.ForeignKey('baseball_player.player_id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True, nullable=False),
                                sqlalchemy.Column('stat_id', sqlalchemy.Integer(), sqlalchemy.ForeignKey('stat_names.stat_id', onupdate='CASCADE', ondelete= 'CASCADE'), primary_key=True, nullable=False,),
                                sqlalchemy.Column('amount', sqlalchemy.Integer(), nullable=False),
                                sqlalchemy.Column('last_updated', sqlalchemy.DateTime(timezone=True), nullable=False, server_default=func.now()))

metadata.create_all(engine)

baseball_player = sqlalchemy.Table('baseball_player', metadata, autoload=True, autoload_with=engine)
stat_names = sqlalchemy.Table('stat_names', metadata, autoload=True, autoload_with=engine)
player_stats = sqlalchemy.Table('player_stats', metadata, autoload=True, autoload_with=engine)

# Insert Players into Table 1.

query_player = sqlalchemy.insert(baseball_player)
player_query = [{'first_name':'Juan', 'last_name':'Soto'},
                {'first_name':'Freddie', 'last_name':'Freeman'},
                {'first_name':'Marcel', 'last_name':'Ozuna'},
                {'first_name':'DJ', 'last_name':'LeMahieu'},
                {'first_name':'Jose', 'last_name':'Ramirez'},
                {'first_name':'Mike', 'last_name':'Trout'},
                {'first_name':'Dominic', 'last_name':'Smith'},
                {'first_name':'Nelson', 'last_name':'Cruz'},
                {'first_name':'Ronald', 'last_name':'Acuna'},
                {'first_name':'Jose', 'last_name':'Abreu'}]


inserted_player = connection.execute(query_player, player_query)

# Insert Stat Name into Table 2.

query = sqlalchemy.insert(stat_names)
stat_query = [{'stat_name':'Games'},
              {'stat_name':'At Bats'},
              {'stat_name':'Runs'},
              {'stat_name':'Hits'},
              {'stat_name':'2B'},
              {'stat_name':'3B'},
              {'stat_name':'HR'},
              {'stat_name':'RBI'},
              {'stat_name':'BB'},
              {'stat_name':'SO'},
              {'stat_name':'CS'}]

inserted_stat_name = connection.execute(query, stat_query)

#Insert Player Stats and amounts.

query_player_stat = sqlalchemy.insert(player_stats)
player_stat_query = [{'player_id':1, 'stat_id':1, 'amount':47},
                     {'player_id':2, 'stat_id':1, 'amount':60},
                     {'player_id':3, 'stat_id':1, 'amount':60},
                     {'player_id':4, 'stat_id':1, 'amount':50},
                     {'player_id':5, 'stat_id':1, 'amount':58},
                     {'player_id':6, 'stat_id':1, 'amount':53},
                     {'player_id':7, 'stat_id':1, 'amount':50},
                     {'player_id':8, 'stat_id':1, 'amount':53},
                     {'player_id':9, 'stat_id':1, 'amount':46},
                     {'player_id':10, 'stat_id':1, 'amount':60}]

inserted_player_stat = connection.execute(query_player_stat, player_stat_query)

# Update data in each Table

query_update_player = sqlalchemy.update(baseball_player).values(first_name='Juanito').where(baseball_player.columns.first_name == 'Juan')
player_update = connection.execute(query_update_player)

query_update_stat_name = sqlalchemy.update(stat_names).values(stat_name= 'Triples').where(stat_names.columns.stat_name == 'CS')
stat_update = connection.execute(query_update_stat_name)

query_update_player_stat = sqlalchemy.update(player_stats).values(amount= 50).where(sqlalchemy.and_(player_stats.columns.player_id == 1, player_stats.columns.stat_id == 1))
player_stats_update = connection.execute(query_update_player_stat)

# Select Data from each table.

query_select_player = sqlalchemy.select([baseball_player])
query_select_stats = sqlalchemy.select([stat_names])
query_select_player_stats = sqlalchemy.select([player_stats])
result_proxy = connection.execute(query_select_player)
result_proxy_2 = connection.execute(query_select_stats)
result_proxy_3 = connection.execute(query_select_player_stats)

result_set = result_proxy.fetchall()
result_set_2 = result_proxy_2.fetchall()
result_set_3 = result_proxy_3.fetchall()

# Printing the data from the tables.

pprint(result_set)
print()
pprint((result_set_2))
print()
pprint((result_set_3))

# Delete data from each table.

query_to_delete_player = sqlalchemy.delete(baseball_player).where(sqlalchemy.and_(baseball_player.columns.first_name == 'Jose', baseball_player.columns.last_name == 'Abreu'))
delete_player = connection.execute(query_to_delete_player)

query_to_delete_stat_name = sqlalchemy.delete(stat_names).where(stat_names.columns.stat_name == 'CS')
delete_stat_name = connection.execute(query_to_delete_stat_name)

query_to_delete_player_stats = sqlalchemy.delete(player_stats).where(sqlalchemy.and_(player_stats.columns.player_id == 10, player_stats.columns.stat_id == 1))
delete_player_stats = connection.execute(query_to_delete_player_stats)

# Use at least one join statement.

join_statement = baseball_player.join(player_stats, player_stats.columns.player_id == baseball_player.columns.player_id).join(stat_names, stat_names.columns.stat_id == player_stats.columns.stat_id)
query_to_print = sqlalchemy.select([baseball_player.columns.first_name, baseball_player.columns.last_name, stat_names.columns.stat_name, player_stats.columns.amount]).order_by(sqlalchemy.asc(player_stats.columns.amount)).select_from(join_statement)

join_result = connection.execute(query_to_print)
join_result_set = join_result.fetchall()
pprint(join_result_set)
