import uuid

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

from nameko.extensions import DependencyProvider

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    # add new user for register API
    def add_user(self, userAccount, userPassword):
        # check if user already exist
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM users 
        WHERE user_account = %s;
        """, (userAccount,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'userAccount': row['user_account']
            })
        # if user exist then close connection and return msg
        if result:
            cursor.close()
            return "User Already Exist"
        # else if user does not exist then add new user, close connection, commit and return msg
        else:
            cursor = self.connection.cursor(dictionary=True)
            generateUUID = str(uuid.uuid4())
            cursor.execute("""
            INSERT INTO users (id, user_account, user_password)
            VALUES (%s, %s, %s);
            """, (generateUUID, userAccount, userPassword))
            cursor.close()
            self.connection.commit()
            return "Add User Success"
    
    # get user for login
    def get_user(self, userAccount, userPassword):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM users 
        WHERE user_account = %s AND user_password = %s;
        """, (userAccount, userPassword))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'userAccount': row['user_account']
            })
        cursor.close()
        return result

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='user_database',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())