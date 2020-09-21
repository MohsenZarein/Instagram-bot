from .create_connection import Create_Connection
from sqlite3 import Error
from time import sleep

def Get_followings_query(owner_id,owner_username):

    fetch_from_followings_sql = """SELECT * FROM followings
                                    WHERE owner_id = {0}""".format(owner_id)

    connection = Create_Connection(owner_username)
    
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(fetch_from_followings_sql)
            followings = cursor.fetchall()
            result = {
                "status":"ok",
                "followings":followings
            }
            return result
        except Error:
            try:
                """ Perform a second try """
                sleep(2)
                cursor = connection.cursor()
                cursor.execute(fetch_from_followings_sql)
                followings = cursor.fetchall()
                result = {
                    "status":"ok",
                    "followings":followings
                }
                return result
            except Error as err:
                print(err)
                result = {
                    "status":"db_error",
                    "followings":[]
                }
                return result
        finally:
            connection.close()

    else:
        result = {
            "status":"error",
            "followings":[]
        }
        return result

    
