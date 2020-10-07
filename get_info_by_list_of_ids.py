from login import Login
from login import ClientError
from instagram_private_api import (
                                   ClientChallengeRequiredError,
                                   ClientCheckpointRequiredError,
                                   ClientSentryBlockError,
                                   ClientThrottledError
                                )   
from get_info_by_username import Get_info_by_username
from follow_by_id import Follow_by_id
from like_by_id import Like_by_id

from dbutils.check_for_follow_query import Check_for_follow_query
from dbutils.get_followings_query import Get_followings_query
from dbutils.follow_query import Follow_Query


from time import sleep
from datetime import datetime
from pathlib import  Path
import argparse
import random
import os
import sys
import json


def path_handler():
    cwd = os.getcwd()
    try:
        Path(cwd + '/LOGS/{0}'.format(args.username)).mkdir(parents=True, exist_ok=False)
        dest_file_path = cwd + '/LOGS/{0}/info.json'.format(args.username)
        return dest_file_path
    except FileExistsError:
        dest_file_path = cwd + '/LOGS/{0}/info.json'.format(args.username)
        return dest_file_path


def get_data_by_id(api,list_of_ids):

    if os.path.isfile(list_of_ids):
        path_for_list = os.path.abspath(list_of_ids)
        previous_info = []
        last_id = None
        if os.path.isfile(os.getcwd() + '/LOGS/{0}/info.json'.format(args.username)):
            with open(os.getcwd() + '/LOGS/{0}/info.json'.format(args.username),"r") as f:
                previous_info = json.load(f)
                if previous_info:
                    last_id = previous_info[-1]["id"]
                    print("last_id :",last_id)
        else:
            print("No previous info ...")
            
    else:
        print("THERE IS NOT A FILE WITH '{0}' NAME IN CURRENT DIRECTORY".format(list_of_ids))
        sys.exit()

    with open(path_for_list,'r') as fin:
        data = fin.readlines()
        ids = []
        for i in data:
            x = i.replace('\n','')
            y = x.replace(' ','')
            ids.append(y)

        DATA = []
        counter = 0
        try:
            
            flag = False
            if not last_id:
                print("No last_id")
                flag = True
            for id in ids:
                if flag == False:
                    if str(id) == str(last_id):
                        flag = True
                        print("found last_id !!!")
                        continue
                    else:
                        continue
                try:
                    info = {}
                    res = api.user_info(id)
                    info = {
                        "id":res['user']['pk'],
                        "username":res['user']['username'],
                        "full_name":res['user']['full_name'],
                        "bio":res['user']['biography'],
                        "follower_count":res['user']['follower_count'],
                        "following_count":res['user']['following_count'],
                        "media_count":res['user']['media_count'],
                        "is_private":res['user']['is_private']
                    }
                    DATA.append(info)
                    counter = counter + 1
                    
                    sleep(1)

                    if counter % 100 == 0:
                        print("~15 min sleep ...")
                        sleep(random.randrange(890,900))

                except ClientChallengeRequiredError as err:
                    print("ClientChallengeRequiredError : ",err)
                    with open(path_handler(),'w',encoding='UTF-8') as fout:
                        FullDATA = previous_info + DATA
                        json.dump(FullDATA,fout,indent=4)
                    return
                except ClientCheckpointRequiredError as err:
                    print("ClientCheckpointRequiredError : ",err)
                    with open(path_handler(),'w',encoding='UTF-8') as fout:
                        FullDATA = previous_info + DATA
                        json.dump(FullDATA,fout,indent=4)
                    return
                except ClientSentryBlockError as err:
                    print("ClientSentryBlockError : ",err)
                    with open(path_handler(),'w',encoding='UTF-8') as fout:
                        FullDATA = previous_info + DATA
                        json.dump(FullDATA,fout,indent=4)
                    return
                except ClientThrottledError as err:
                    print("ClientThrottledError : ",err)
                    with open(path_handler(),'w',encoding='UTF-8') as fout:
                        FullDATA = previous_info + DATA
                        json.dump(FullDATA,fout,indent=4)
                    sleep(120)
                except ClientError as err:
                    print(err)
                    with open(path_handler(),'w',encoding='UTF-8') as fout:
                        FullDATA = previous_info + DATA
                        json.dump(FullDATA,fout,indent=4)
                    sleep(120)    
                except KeyboardInterrupt:
                    print("KeyboardInterrupt !!!")
                    with open(path_handler(),'w',encoding='UTF-8') as fout:
                        FullDATA = previous_info + DATA
                        json.dump(FullDATA,fout,indent=4)
                    return
                except Exception as err:
                    print(err)
                    with open(path_handler(),'w',encoding='UTF-8') as fout:
                        FullDATA = previous_info + DATA
                        json.dump(FullDATA,fout,indent=4)
                    sleep(120)

                    
            with open(path_handler(),'w',encoding='UTF-8') as fout:
                FullDATA = previous_info + DATA
                json.dump(FullDATA,fout,indent=4)


        except KeyboardInterrupt:
            print("KeyboardInterrupt !!!")
            with open(path_handler(),'w',encoding='UTF-8') as fout:
                FullDATA = previous_info + DATA
                json.dump(FullDATA,fout,indent=4)
            return
        



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-l', '--list', dest='list', type=str, required=True)

    args = parser.parse_args()

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )
    
    get_data_by_id(
                    api=api,
                    list_of_ids=args.list
    )
    
