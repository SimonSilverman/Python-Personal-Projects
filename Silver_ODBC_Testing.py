# import Imports.Silver_ODBC as Sil_ODBC
from Imports.Silver_ODBC import SQL_server as Silver_ODBC_SQL_server
from Imports.Silver_ODBC import my_SQL

SQL_server = Silver_ODBC_SQL_server(server_name='LAPTOP-L46BVJII', database='sql_test')
my_SQL = my_SQL('root', 'test', '127.0.0.1', 'python_db')
def main():
    #------------SQL SERVER-----------------
    # SQL_server.test_con()
    # print(SQL_server.query("insert into simple_people Values(9,'Liam', 'Douglas',2022)"))
    # print(SQL_server.query_df("select * from simple_people"))
    # SQL_server.insert_one('simple_people',(3, 'Alex', 'Turro', 2022))
    # bulk_insert_list = [(4, 'Tristyn', 'Kahrs', 2022), (5, 'Robert', 'Brunney', 2022)]
    # SQL_server.insert_many('simple_people', bulk_insert_list, 4)
    # SQL_server.read('simple_people')
    # SQL_server.read('simple_people', ('Id', 'LastName'), 'Id')
    # SQL_server.update('simple_people', {'Id':1}, {'FirstName':"'Grayson'", 'LastName':"'Sudweeks'"})
    # SQL_server.delete('simple_people', {'FirstName':"'David'"})

    #-------------MYSQL------------------------------

    # my_SQL.test_con()
    # print(my_SQL.query("insert into simple_people Values(9,'Liam', 'Douglas',2022)"))
    # print(my_SQL.query_df("select * from simple_people"))
    # my_SQL.insert_one('simple_people',(3, 'Alex', 'Turro', 2022))
    # bulk_insert_list = [(4, 'Tristyn', 'Kahrs', 2022), (5, 'Robert', 'Brunney', 2022)]
    # my_SQL.insert_many('simple_people', bulk_insert_list, 4)
    # my_SQL.read('simple_people')
    # my_SQL.read('simple_people', ('Id', 'LastName'), 'Id')
    # my_SQL.update('simple_people', {'Id':1}, {'FirstName':"'Grayson'", 'LastName':"'Sudweeks'"})
    # my_SQL.delete('simple_people', {'FirstName':"'David'"})
    pass






if __name__ == '__main__':
    main()
    print('---------------------------------\nprogram is complete')