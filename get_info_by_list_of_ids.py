from login import Login
from login import ClientError
from get_info_by_username import Get_info_by_username
from follow_by_id import Follow_by_id
from like_by_id import Like_by_id

from dbutils.check_for_follow_query import Check_for_follow_query
from dbutils.get_followings_query import Get_followings_query
from dbutils.follow_query import Follow_Query


from time import sleep
from datetime import datetime
import argparse
import random
import os
import sys
import json


def get_data_by_id(api,list_of_ids):

    if os.path.isfile(list_of_ids):
        path_for_list = os.path.abspath(list_of_ids)
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
        for id in ids:
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
                if counter == 1000:
                    sleep(random.randrange(300,320))
                    
            except Exception as err:
                print(err)
                with open(os.getcwd() + '/info.json','w',encoding='UTF-8') as fout:
                    json.dump(DATA,fout,indent=4)


        with open(os.getcwd() + '/info.json','w',encoding='UTF-8') as fout:
            json.dump(DATA,fout,indent=4)


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
    
