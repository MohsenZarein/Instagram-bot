import sys
sys.path.append('../')
from login import Login
from login import to_json
from login import ClientError
from get_info_by_username import Get_info_by_username

from pathlib import Path
from time import sleep
import argparse
import json
import os

def Get_followings(api,username,target_username,target_id):

    print("\nStart getting followings ...")

    try:
        followings = []

        if target_id:
            id = target_id
            data = api.user_following(id,rank_token=api.generate_uuid())
            next_max_id = data.get('next_max_id')
        else:
            user_info = Get_info_by_username(
                                             api=api,
                                             username=target_username
            )
            id = user_info['id']
            data = api.user_following(id,rank_token=api.generate_uuid())
            next_max_id = data.get('next_max_id')

        while next_max_id:
            if next_max_id >= 1900:
                break
            data = api.user_following(id,rank_token=api.generate_uuid(),max_id=next_max_id)
            followings.extend(data.get('users',[]))
            next_max_id = data.get('next_max_id')
            sleep(5)

        followings.extend(data.get('users', []))
        print(len(followings))
        print("Finished !")
        sleep(7)

        cwd = os.getcwd()
        try:
            Path(cwd + '/LOGS/{0}'.format(username)).mkdir(parents=True, exist_ok=False)
            dest_file_path = cwd + '/LOGS/{0}/{1}-followings.json'.format(username,target_username)
        except FileExistsError:
            dest_file_path = cwd + '/LOGS/{0}/{1}-followings.json'.format(username,target_username)

        with open(dest_file_path,'w') as fout:
            json.dump(followings,fout,default=to_json)

        return followings
        

    except Exception as err:
        print(err)
        print(len(followings))
        sleep(7)

        cwd = os.getcwd()
        try:
            Path(cwd + '/LOGS/{0}'.format(username)).mkdir(parents=True, exist_ok=False)
            dest_file_path = cwd + '/LOGS/{0}/{1}-followings.json'.format(username,target_username)
        except FileExistsError:
            dest_file_path = cwd + '/LOGS/{0}/{1}-followings.json'.format(username,target_username)

        with open(dest_file_path,'w') as fout:
            json.dump(followings,fout,default=to_json)

        return followings



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-tu', '--target_username', dest='target_username', type=str, required=True)
    parser.add_argument('-ti', '--target_id', dest='target_id', type=str, required=False)

    args = parser.parse_args()

    if args.target_id:
        target_id = args.target_id
    else:
        target_id = None

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )

    followings = Get_followings(
                              api=api,
                              username=args.username,
                              target_username=args.target_username,
                              target_id=target_id
    )

    print(followings)