import sqlite3
from sqlite3 import Error
import os
from pathlib import Path
from time import sleep

def Create_Connection(owner_username):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    
    cwd = os.getcwd()
    try:
        Path(cwd + '/LOGS/{0}'.format(owner_username)).mkdir(parents=True, exist_ok=False)
        db_file = cwd + '/LOGS/{0}/instagram.db'.format(owner_username)
    except FileExistsError:
        db_file = cwd + '/LOGS/{0}/instagram.db'.format(owner_username)


    connection = None

    try:
        connection = sqlite3.connect(db_file)
        status = Create_Tables(connection)
        if status == True:
            return connection
        else:
            print("Sorry! Connection was stablished to the db but couldn't create or check for tables . try again ...")
            return None
    except Error:
        try:
            """ Perform a second try """
            sleep(2)
            connection = sqlite3.connect(db_file)
            status = Create_Tables(connection)
            if status == True:
                return connection
            else:
                print("Sorry! Connection was stablished to the db but couldn't create or check for tables . try again ...")
                return None
        except Error as err:
            print(err)

    return connection



def Create_Tables(connection):
    """ Create db tables if not exists yet """

    sql_create_followings_table = """ CREATE TABLE IF NOT EXISTS followings (
                                        owner_id text,
                                        owner_username text ,
                                        username text,
                                        user_id text,
                                        date text
                                    ); """

    sql_create_unfollowed_table = """ CREATE TABLE IF NOT EXISTS unfollowed (
                                        owner_id text,
                                        owner_username text ,
                                        username text,
                                        user_id text,
                                        date text
                                    ); """

    
    try:
        cursor = connection.cursor()
        cursor.execute(sql_create_followings_table)
        cursor.execute(sql_create_unfollowed_table)
        return True
    except Error as err:
        print(err)
        return False

