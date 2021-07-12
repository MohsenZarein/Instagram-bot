from login import Login
from login import ClientError
from time import sleep
import argparse

def Get_likers(api,media_id):

    print("Getting likers ...")

    result = api.media_likers(media_id=str(media_id))

    if result['status'] == 'ok':
        users = []
        for user in result['users']:
            data = {}
            data = {

                'id':str(user['pk']),
                'username':user['username'],
                'full_name':user['full_name'],
                'is_private':user['is_private']
            }
            users.append(data)
        
        sleep(7)
        print("Finished !")
        return users
    
    else:
        print('Could not get likers from media with id {0}'.format(media_id))
        sleep(7)
        return None



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-media_id', '--media_id', dest='media_id', type=str, required=True)


    args = parser.parse_args()

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )

    result = Get_likers(
                        api=api,
                        media_id=args.media_id
    )

    if result:
        print(result)

