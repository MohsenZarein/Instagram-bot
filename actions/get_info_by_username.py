from login import Login
from login import ClientError
from time import sleep
import argparse


def Get_info_by_username(api , username):

    data = {}
    try:
        result = api.username_info(username)
        data = {

            'id':str(result['user']['pk']),
            'username':username,
            'full_name':result['user']['full_name'],
            'is_private':result['user']['is_private'],
            'media_count':result['user']['media_count'],
            'follower_count':result['user']['follower_count'],
            'following_count':result['user']['following_count']
        }
        sleep(7)
        return data
    except ClientError as err:
        print(err)
        sleep(7)
        return data



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-t', '--target_username', dest='target_username', type=str, required=True)

    args = parser.parse_args()

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )

    user_info = Get_info_by_username(
                                     api=api,
                                     username=args.target_username
    )

    print(user_info)