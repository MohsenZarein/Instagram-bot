from login import Login
from login import ClientError
from time import sleep
import argparse

def Get_followers(api,id):

    print("\nStart getting followers ...")

    try:
        followers = []
        data = api.user_followers(id,rank_token=api.generate_uuid())
        next_max_id = data.get('next_max_id')
        while next_max_id:
            #if next_max_id >= 2100:
                #break
            data = api.user_followers(id,rank_token=api.generate_uuid(),max_id=next_max_id)
            followers.extend(data.get('users',[]))
            if len(followers) >= 1500:
                break
            next_max_id = data.get('next_max_id')
            sleep(5)

        followers.extend(data.get('users', []))
        print(len(followers))
        print("Finished !")
        sleep(7)
        return followers

        """ code for saving grabed followers in file :
        with open('/home/mohsen/VSCode/instagram_private_api/avangco-followers.json','w') as fout:
            json.dump(followers,fout,default=to_json)
        """

    except Exception as err:
        print(err)
        print(len(followers))
        sleep(7)
        return followers

        """ code for saving grabed followers in file :
        with open('/home/mohsen/VSCode/instagram_private_api/avangco-followers.json','w') as fout:
            json.dump(followers,fout,default=to_json)
        """



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

    followers = Get_followers(
                              api=api,
                              id=args.target_id
    )

    print(followers)

