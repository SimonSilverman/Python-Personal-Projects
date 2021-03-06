try:
    import pandas as pd
except:
    raise ImportError('Missing pandas pip install!')



class SQL:
    def test_con(self):
        print(self.mydb)
    def query(self, query_str: str): #pass in a sql query, does not return
        self.mycursor.execute(query_str)
        self.mydb.commit()
    def query_return(self, query_str: str): #pass in a sql query, returns a value
        self.mycursor.execute(query_str)
        myresult = self.mycursor.fetchall()
        return myresult
    def query_df(self, query_str: str): #pass in a sql query, returns a pandas dataframe
        table = pd.read_sql_query(query_str, self.mydb)
        return table
    def insert_one(self, table: str, values: tuple): #hand in the table name and a tuple of values 
        sql_values = "("
        for value in values:
            sql_values+=str(value)+','
        sql_values = sql_values.removeprefix(',') + ')'
        query_str = f"INSERT INTO {table} VALUES {str(values)}"
        self.mycursor.execute(query_str)
        self.mydb.commit()
    def read(self, table: str, data_wanted: list='*', primary_key: str=None): #pass in the table to grab data from and can optionally pass in a list with the fields you want back, will default to all fields, can optionally pass in a primary key to index on
        values_wanted = str(data_wanted).removeprefix('[').removesuffix(']').replace('\'', '').replace('\"','')
        if primary_key is None:
            table = pd.read_sql_query(f"SELECT {values_wanted} FROM {table}", self.mydb)
        else:
            table = pd.read_sql_query(f"SELECT {values_wanted} FROM {table}", self.mydb, index_col=primary_key)
        print(table)
    def update(self, table: str, upd_on: dict, new_vals: dict): #upd_on = {field, where_val} #dict of new vals {field:val, field:val}
        where_field = list(upd_on.keys())[0]
        val_field = upd_on[where_field]
        query_str = f"UPDATE {table} SET"
        for field, val in new_vals.items():
            query_str += f" {field} = {val},"
        query_str = query_str.removesuffix(',')
        query_str += f" WHERE {where_field} = {val_field}"
        self.mycursor.execute(query_str)
        self.mydb.commit()
    def delete(self, table: str, del_on: dict): #del_on {field, delete val} (single key val!)
        where_field = list(del_on.keys())[0]
        val_field = del_on[where_field]
        query_str = f"DELETE FROM {table} WHERE {where_field} = {val_field}"
        self.mycursor.execute(query_str)
        self.mydb.commit()

class My_SQL(SQL):
    def __init__(self, username: str, password: str, host_ip: str, schema: str):  #pass in username, password, ip, and schema for the database
        try:
            import mysql.connector
        except:
            raise ImportError('Missing mysql pip install!')
        self.mydb = mysql.connector.connect(user=username, password=password, host=host_ip, database=schema)
        self.mycursor = self.mydb.cursor()
    def insert_many(self, table: str, values: list, num_fields: int): #pass in table name, the list of tuples of values [(values)] and the number of fields in the table (excluding auto incrementing fields)
        value_str = "("
        for i in range(num_fields):
            value_str+="%s,"
        value_str = value_str.removesuffix(',') + ')'
        query_str = f"INSERT INTO {table} VALUES {value_str}"
        self.mycursor.fast_executemany = True
        self.mycursor.executemany(query_str, values)
        self.mydb.commit()

class SQL_server(SQL):
    global pyodbc
    try:
        import pyodbc
    except:
        raise ImportError('Missing pyodbc pip install!')
    def __init__(self, server_name: str, database: str): #pass in the servername (SELECT @@SERVERNAME) and the database name
        self.mydb = pyodbc.connect('Driver={SQL Server};'
                    f'Server={server_name};'
                    f'Database={database};'
                    'Trusted_Connection=yes;')
        self.mycursor = self.mydb.cursor()
    def insert_many(self, table: str, values: list, num_fields: int): #pass in table name, the list of tuples of values [(values)] and the number of fields in the table (excluding auto incrementing fields)
        value_str = "("
        for i in range(num_fields):
            value_str+="?,"
        value_str = value_str.removesuffix(',') + ')'
        query_str = f"INSERT INTO {table} VALUES {value_str}"
        self.mycursor.fast_executemany = True
        self.mycursor.executemany(query_str, values)
        self.mydb.commit()

class MongoDB:
    def __init__(self, host: str, port: int, database: str):
        try:
            from pymongo import MongoClient
        except:
            raise ImportError('Missing pymongo pip install!')
        self.myclient = MongoClient(host, port)
        self.mydb = self.myclient[database]
    def test_con(self):
        print(self.mydb)
    def insert_one(self, collection: str, values: dict): #{key:val, key:val}
        mycol = self.mydb[collection]
        mycol.insert_one(values)
    def insert_many(self, collection: str, values: list): #pass a list of dicts [{entry},{entry}]
        mycol = self.mydb[collection]
        mycol.insert_many(values)
    def read(self, collection: str, where: dict={}): #pass in search arguments {key:val_wanted, key:val_wanted}
        mycol = self.mydb[collection]
        return mycol.find(where)
    def update(self, collection: str, upd_on: dict, new_vals: dict, upsert: bool=True,): #pass in a dict of what to update on {fieldname: value looking for}, new values {fieldname: new_value}, optional upsert (default true)
        mycol = self.mydb[collection]
        set_vals = {"$set":new_vals}
        mycol.update_many(upd_on, set_vals, upsert)
    def update_one(self, collection: str, upd_on: dict, new_vals: dict, upsert: bool=True): #pass in a dict of what to update on {fieldname: value looking for}, new values {fieldname: new_value}, optional upsert (default true)
        mycol = self.mydb[collection]
        set_vals = {"$set":new_vals}
        mycol.update_one(upd_on, set_vals, upsert)
    def delete(self, collection: str, del_on: dict): #pass in a dict on what to del on {fieldname: value} or an aggregate ex: {'$or': [{'name':'Tobie'}, {'name': 'Grayson'}]}
        mycol = self.mydb[collection]
        mycol.delete_many(del_on)

class Neo4j:
    def __init__(self, address: str, username: str, password:str):
        try:
            from py2neo import Graph, Node
        except:
            raise ImportError('Missing py2neo pip install!')
        self.graph = Graph(address, auth=(username, password))
    def test_con(self):
        print(self.graph)


class Redis:
    def __init__(self, host, port, db):
        try:
            import redis
        except:
            import_error_msg += 'missing redis pip install! \n'
            if len(import_error_msg) > 0:
                print(import_error_msg.strip())
                quit()
        self.connection = redis.StrictRedis(host=host, port=port, db=db)