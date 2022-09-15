import psycopg2
from requests import request


class Request:
    def __init__(self, table: str, column1: str, column2: str, column3: str):
        self.table = table
        self.column1 = column1
        self.column2 = column2
        self.column3 = column3

        self.db = psycopg2.connect(
            dbname='kivano_db',
            user='kivano',
            password='12345',
            host='localhost',
            port=5432
        )
        self.cursor = self.db.cursor()
        query = f"SELECT * FROM information_schema.tables where table_name='{table}'"
        self.cursor.execute(query=query)
        if bool(self.cursor.rowcount) is True:
            pass
        else:
            query = f"""
            CREATE TABLE {table}(
            id serial primary key,
            {column1} varchar, 
            {column2} varchar, 
            {column3} varchar
            );"""
            self.cursor.execute(query=query)
            self.db.commit()
            print('Table created!')

    def write_values(self, value1, value2, value3):
        query = f"""
        INSERT INTO {self.table}(
            {self.column1},
            {self.column2},
            {self.column3})
        VALUES(
            '{value1}',
            '{value2}',
            '{value3}');"""
        self.cursor.execute(query=query)
        self.db.commit()
