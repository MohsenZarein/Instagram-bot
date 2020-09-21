from .create_connection import Create_Connection
from sqlite3 import Error
from time import sleep


def Check_for_follow_query(data):
    
    fetch_from_unfollowed_sql = """ SELECT (user_id) FROM unfollowed 
                                    WHERE owner_id = {0} """.format(data[0])

    result = {
        "status":"ok"
    }

    connection = Create_Connection(data[1])

    if connection:

        try:
            cursor = connection.cursor()
            cursor.execute(fetch_from_unfollowed_sql)
            users = cursor.fetchall()
            for user in users:
                if user[0] == data[3]:
                    # You have already unfollowed this user once
                    result = {
                        "status":"error"
                    }
                    return result

            return result
        except Error:
            try:
                """ Perform a second try """
                sleep(2)
                cursor = connection.cursor()
                cursor.execute(fetch_from_unfollowed_sql)
                users = cursor.fetchall()
                for user in users:
                    if user[0] == data[3]:
                        # You have already unfollowed this user once
                        result = {
                            "status":"error"
                        }
                        return result

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
        return result