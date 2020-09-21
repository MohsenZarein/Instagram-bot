from .create_connection import Create_Connection
from sqlite3 import Error
from time import sleep

def Follow_Query(data):

    follow_sql = """INSERT INTO followings(owner_id,owner_username,username,user_id,date)
                     VALUES(?,?,?,?,?)"""
    

    result = {
        "status":"ok"
    }

    connection = Create_Connection(data[1])

    if connection:

        try:
            cursor = connection.cursor()
            cursor.execute(follow_sql,data)
            connection.commit()
            return result
        except Error:
            try:
                """ Perform a second try """
                sleep(2)
                cursor = connection.cursor()
                cursor.execute(follow_sql,data)
                connection.commit()
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

            
            

            
    
    




            