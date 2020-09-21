from login import Login
from login import ClientError
from get_info_by_username import Get_info_by_username
import argparse

def Follow_by_username(api , username):

    user_info = Get_info_by_username(
                                     api=api,
                                     username=username
    )

    if user_info:

        result = api.friendships_create(user_info['id'])

        if result['status'] == 'ok':
            return  True
        else:
            return False

    else:
        print("Could not get user info!")
        return False


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

    result = Follow_by_username(
                          api=api,
                          username=args.target_username
    )

    if result == True:
        print("followed!")
    else:
        print("Could not follow!")

