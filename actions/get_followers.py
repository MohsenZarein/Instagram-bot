from login import Login
from login import ClientError
from login import to_json
from get_info_by_username import Get_info_by_username

from pathlib import Path
from time import sleep
import argparse
import json
import os

def Get_followers(api,username,target_username,target_id):

    print("\nStart getting followers ...")

    try:
        followers = []
        
        if target_id:
            id = target_id
            data = api.user_followers(id,rank_token=api.generate_uuid())
            next_max_id = data.get('next_max_id')
        else:
            user_info = Get_info_by_username(
                                             api=api,
                                             username=target_username
            )
            id = user_info['id']
            data = api.user_followers(id,rank_token=api.generate_uuid())
            next_max_id = data.get('next_max_id')

        while next_max_id:
            
            data = api.user_followers(id,rank_token=api.generate_uuid(),max_id=next_max_id)
            followers.extend(data.get('users',[]))
            if len(followers) >= 1900:
                break
            next_max_id = data.get('next_max_id')
            sleep(5)

        followers.extend(data.get('users', []))
        print(len(followers))
        print("Finished !")
        sleep(7)

        cwd = os.getcwd()
        try:
            Path(cwd + '/LOGS/{0}'.format(username)).mkdir(parents=True, exist_ok=False)
            dest_file_path = cwd + '/LOGS/{0}/{1}-followers.json'.format(username,target_username)
        except FileExistsError:
            dest_file_path = cwd + '/LOGS/{0}/{1}-followers.json'.format(username,target_username)
            
        with open(dest_file_path,'w') as fout:
            json.dump(followers,fout,default=to_json)
        
        return followers
        

    except Exception as err:
        print(err)
        print(len(followers))
        sleep(7)
        
        cwd = os.getcwd()
        try:
            Path(cwd + '/LOGS/{0}'.format(username)).mkdir(parents=True, exist_ok=False)
            dest_file_path = cwd + '/LOGS/{0}/{1}-followers.json'.format(username,target_username)
        except FileExistsError:
            dest_file_path = cwd + '/LOGS/{0}/{1}-followers.json'.format(username,target_username)
            
        with open(dest_file_path,'w') as fout:
            json.dump(followers,fout,default=to_json)
        
        return followers



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

    followers = Get_followers(
                              api=api,
                              username=args.username,
                              target_username=args.target_username,
                              target_id=target_id
    )

    print(followers)

