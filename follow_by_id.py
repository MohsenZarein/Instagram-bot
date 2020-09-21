from login import Login
from login import ClientError
from time import sleep
import argparse

def Follow_by_id(api , id):

    result = api.friendships_create(id)

    if result['status'] == 'ok':
        return  True
    else:
        return False


if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-t', '--target_id', dest='target_id', type=str, required=True)

    args = parser.parse_args()

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )

    result = Follow_by_id(
                          api=api,
                          id=args.target_id
    )

    if result == True:
        print("followed!")
    else:
        print("Could not follow!")

