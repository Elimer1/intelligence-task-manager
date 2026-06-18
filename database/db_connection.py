import mysql.connector
from mysql.connector import errorcode

class DB_connection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            user="root",
            password="1234",
            host='localhost',
            port=3306,
            database="Intelligence_db"
        )

        #self.get_connection()
        try:
            self.create_database()
            self.create_tables()
        except Exception as e:
            return{"Error with creating database or table": e}


    def get_connection(self):
        try:
            if not self.connection.is_connected():
                self.connection.reconnect()
            return self.connection
        
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return {"ERROR": "Something is wrong with username or password"}
            
            if e.errno == errorcode.ER_BAD_DB_ERROR:
                return {"ERROR": "Database does not exist"}
            
            return {"ERROR": e}


    def create_database(self):
        with self.connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")


    def create_tables(self):
        agents_sql = """CREATE TABLE IF NOT EXISTS agents (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        specialty VARCHAR(50) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        completed_missions INT DEFAULT 0,
        failed_missions INT DEFAULT 0,
        agent_rank ENUM("Junior", "Senior", "Commander")
        )"""
        with self.connection.cursor() as cursor:
            cursor.execute(agents_sql)


        missions_sql = """CREATE TABLE IF NOT EXISTS missions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(50) NOT NULL,
        description TEXT NOT NULL,
        location VARCHAR(50) NOT NULL,
        difficulty INT CHECK (1 <= difficulty <= 10),
        importance INT CHECK (1 <= importance <= 10),
        status ENUM("NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED") DEFAULT "NEW",
        risk_level VARCHAR(50) NOT NULL,
        assigned_agent_id INT DEFAULT NULL
        )"""
        with self.connection.cursor() as cursor:
            cursor.execute(missions_sql)



if __name__ == "__main__":
    db = DB_connection()
    print("success")
#create an instance of db or somehting or jsut call the methods with self?
#when creating tw tablesin one mehod jsutamke sql and excute and then do it again?
#not null for all if not explicit?
#enum for numbers?
#do i have to "use" database and where
#what to do in except when connecting?
#other erros i have to check in db_connection?
#self.getconnection in init?

