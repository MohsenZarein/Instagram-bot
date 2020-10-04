from .create_connection import Create_Connection
from sqlite3 import Error
from time import sleep

def Delete_from_followings(data):

    delete_from_followings_sql = """DELETE FROM followings
                                     WHERE user_id=?"""

    connection = Create_Connection(data[1])

    if connection:
        try:
            cursor = connection.cursor()

            # Delete from followings
            cursor.execute(delete_from_followings_sql,(data[3],))
            connection.commit()

            result = {
                "status":"ok"
            }
            return result

        except Error:
            try:
                """ Perform a second try """
                cursor = connection.cursor()

                # Delete from followings
                cursor.execute(delete_from_followings_sql,(data[3],))
                connection.commit()

                result = {
                    "status":"ok"
                }
                return result

            except Error as err:
                print(err)
                result = {
                    "status":"db_error"
                }
                return result
        
        finally:
            connection.close()

    else:
        result = {
            "status":"db_error"
        }
