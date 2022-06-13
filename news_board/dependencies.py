import uuid

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

from nameko.extensions import DependencyProvider

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    # create news
    def add_news(self, newsTitle, newsDetail, fileUrl, createdAt):
        # check if news already exist
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news 
        WHERE title = %s;
        """, (newsTitle,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'title': row['title'],
                'detail': row['detail'],
                'fileUrl': row['file_url'],
                'createdAt': row['created_at'],
                'updatedAt': row['updated_at']
            })
        # if news exist then close connection and return msg
        if result:
            cursor.close()
            return "News Already Exist"
        # else if news does not exist then add news, close connection, commit and return msg
        else:
            cursor = self.connection.cursor(dictionary=True)
            generateUUID = str(uuid.uuid4())
            cursor.execute("""
            INSERT INTO news (id, title, detail, file_url, created_at)
            VALUES (%s, %s, %s, %s, %s);
            """, (generateUUID, newsTitle, newsDetail, fileUrl, createdAt))
            cursor.close()
            self.connection.commit()
            return "Add News Success"
    
    # edit news
    def edit_news(self, newsId, newsTitle, newsDetail, fileUrl, updatedAt):
        # check if news already exist
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news 
        WHERE id = %s;
        """, (newsId,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'title': row['title'],
                'detail': row['detail'],
                'fileUrl': row['file_url'],
                'createdAt': row['created_at'],
                'updatedAt': row['updated_at']
            })
        # if news exist then edit news, close connection, commit and return msg
        if result:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
            UPDATE news SET title = %s, detail = %s, file_url = %s, updated_at = %s WHERE id = %s;
            """, (newsTitle, newsDetail, fileUrl, updatedAt, newsId))
            cursor.close()
            self.connection.commit()
            return "Edit News Success"
        # else if news does not exist then close connection, and return msg
        else:
            return "News Does Not Exist"

    # delete news
    def delete_news(self, newsId):
        # check if news already exist
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news 
        WHERE id = %s;
        """, (newsId,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'title': row['title'],
                'detail': row['detail'],
                'fileUrl': row['file_url'],
                'createdAt': row['created_at'],
                'updatedAt': row['updated_at']
            })
        # if news exist then delete news, close connection, commit and return msg
        if result:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
            DELETE FROM news WHERE id = %s;
            """, (newsId,))
            cursor.close()
            self.connection.commit()
            return "News Deleted"
        # else if news does not exist then close connection and return msg 
        else:
            cursor.close()
            return "News With Id " + newsId + " Does Not Exist"

    # get all news
    def get_all_news(self):
        # check if news already exist
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news;
        """)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'title': row['title'],
                'detail': row['detail'],
                'fileUrl': row['file_url'],
                'createdAt': row['created_at'],
                'updatedAt': row['updated_at']
            })
        # if news exist then close connection, and return all news
        if result:
            cursor.close()
            return result
        # else if news does not exist then close connection and return msg 
        else:
            cursor.close()
            return "No News Exist"

    # get news by id
    def get_news_by_id(self, newsId):
        # check if news already exist
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news 
        WHERE id = %s;
        """, (newsId,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'title': row['title'],
                'detail': row['detail'],
                'fileUrl': row['file_url'],
                'createdAt': row['created_at'],
                'updatedAt': row['updated_at']
            })
        # if news exist then close connection, and return news
        if result:
            cursor.close()
            return result
        # else if news does not exist then close connection and return msg 
        else:
            cursor.close()
            return "News With Id " + newsId + " Does Not Exist"

    # download file by id
    def download_file_by_id(self, newsId):
        # check if file from news already exist
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM news 
        WHERE id = %s AND file_url IS NOT NULL;
        """, (newsId,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'fileUrl': row['file_url']
            })
        # if file from news exist then close connection, and return file path
        if result:
            cursor.close()
            return result
        # else if file from news does not exist then close connection and return msg 
        else:
            cursor.close()
            return "File From News Id " + newsId + " Does Not Exist"
           
class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='news_database',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())