from .create_connection import Create_Connection
from sqlite3 import Error
from time import sleep


def Follow_tags_query(data):

    follow_tags_sql = """INSERT INTO tags(owner_id,owner_username,tag,date)
                         VALUES(?,?,?,?)"""
    
    delete_from_Unfollowedtags_sql = """DELETE FROM Unfollowedtags
                                        WHERE tag=?"""

    fetch_Unfollowedtags_sql = """SELECT * FROM Unfollowedtags"""

                    
    result = {
        "status":"ok"
    }

    connection = Create_Connection(data[1])

    if connection:

        try:
            cursor = connection.cursor()

            # Check if you have unfollowed this tag before
            cursor.execute(fetch_Unfollowedtags_sql)
            res = cursor.fetchall()
            for row in res:
                if row[2] == data[2]:
                    # Delete from Unfollowedtags
                    cursor.execute(delete_from_Unfollowedtags_sql,(data[2],))
                    connection.commit()
                    break
                    
            # Insert into followed tags
            cursor.execute(follow_tags_sql,data)
            connection.commit()

            return result
        except Error:
            try:
                """ Perform a second try """
                sleep(2)

                cursor = connection.cursor()

                # Check if you have unfollowed this tag before
                cursor.execute(fetch_Unfollowedtags_sql)
                res = cursor.fetchall()
                for row in res:
                    if row[2] == data[2]:
                        # Delete from Unfollowedtags
                        cursor.execute(delete_from_Unfollowedtags_sql,(data[2],))
                        connection.commit()
                        break
                        
                # Insert into followed tags
                cursor.execute(follow_tags_sql,data)
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




    

