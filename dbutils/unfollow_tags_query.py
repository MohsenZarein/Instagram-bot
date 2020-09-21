from .create_connection import Create_Connection
from sqlite3 import Error
from time import sleep


def Unfollow_tags_query(data):
    

    delete_from_tags_sql = """DELETE FROM tags
                                     WHERE tag=?"""

    insert_into_Unfollowedtags_sql = """INSERT INTO Unfollowedtags(owner_id,owner_username,tag,date)
                                        VALUES(?,?,?,?)"""

    fetch_Unfollowedtags_sql = """SELECT * FROM Unfollowedtags"""

    
    connection = Create_Connection(data[1])

    if connection:
        try:
            cursor = connection.cursor()

            # Check if you have already unfollowed this tag
            cursor.execute(fetch_Unfollowedtags_sql)
            res = cursor.fetchall()        
            for row in res:
                if row[2] == data[2]:
                    result = {
                        "status":"ok"
                    }
                    return result

            # Delete from followings
            cursor.execute(delete_from_tags_sql,(data[2],))
            connection.commit()

            # Insert into unfollowedtags
            cursor.execute(insert_into_Unfollowedtags_sql,data)
            connection.commit()

            result = {
                "status":"ok"
            }

            return result

        except Error:
            try:
                """ Perform a second try """
                sleep(2)

                cursor = connection.cursor()

                # Check if you have already unfollowed this tag
                cursor.execute(fetch_Unfollowedtags_sql)
                res = cursor.fetchall()        
                for row in res:
                    if row[2] == data[2]:
                        result = {
                            "status":"ok"
                        }
                        return result

                # Delete from followings
                cursor.execute(delete_from_tags_sql,(data[2],))
                connection.commit()

                # Insert into unfollowedtags
                cursor.execute(insert_into_Unfollowedtags_sql,data)
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
