import sys
sys.path.append('../')
from login import Login
from login import ClientError
from get_info_by_username import Get_info_by_username

from dbutils.unfollow_tags_query import Unfollow_tags_query

from time import sleep
from re import search
from datetime import datetime
import os
import sys
import random
import argparse


def Unfollow_tags(api,file_name,amount):

    if os.path.isfile(file_name):
        path_for_tags_file = os.path.abspath(file_name)
    else:
        print("THERE IS NOT A FILE WITH '{0}' NAME IN CURRENT DIRECTORY".format(file_name))
        sys.exit()
    
    try:
        with open(path_for_tags_file , 'r') as fin:
            data = fin.readlines()
            if not data:
                print('TAGS FILE IS EMPTY !')
                sys.exit()
            else:
                tags = []
                for i in data:
                    tags.append(i.replace('\n',''))
        
    except FileNotFoundError:
        print("SUCH FILE DOES NOT EXIST !")
        sys.exit()
    except IOError:
        print("COULD NOT READ THE FILE !")
        sys.exit()
    

    print("\nStart unfollowing tags ...")

    me = Get_info_by_username(
                              api=api,
                              username=args.username
        )

    if not me:
        print('Encountered error while getting your info')
        return
    
    sleep(random.randrange(60,70))

    counter = 0
    for tag in tags:
        if counter >= amount:
            print("Reached maximun amount of unfollow tags .")
            break
        try:
            print("\n")
            print("Unfollowing  [[ #{0} ]] ...".format(tag))
            result = api.tag_unfollow(tag)
            if result['status'] == 'ok':
                print("UnFollowed !")
                counter = counter + 1

                data = (me['id'],me['username'],tag,str(datetime.now()))
                res = Unfollow_tags_query(data)

                if res["status"] == "ok":
                    print("saved to database !")
                    sleep(5)
                else:
                    print("could not save to database !")
                    sleep(5)

                sleep(random.randrange(60,70))
            else:
                print("Could not follow << #{0} >>".format(tag))
                print("\n")
                sleep(random.randrange(60,70))

                
        except ClientError as err:
            if err.code == 404:
                print("Could not find this tag ! skipping ...")
                sleep(random.randrange(60,70))
            elif err.code == 400:
                print("Bad Request: You have already unfollowed this hashtag . skipping ...")
                sleep(random.randrange(60,70))
            else:
                print(err)
        except Exception as err:
            print(err)
            print("sys.exit")
            sys.exit()


    print("Finished ! UnFollowed all tags in file")



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-l', '--list', dest='list', type=str, required=True)
    parser.add_argument('-a', '--amount', dest='amount', type=int , required=True)

    args = parser.parse_args()

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )

    Unfollow_tags(
                 api=api,
                 file_name=args.list,
                 amount=args.amount
    )