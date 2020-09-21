from login import Login
from login import ClientError
from get_media_ids_of_a_user import Get_media_ids_of_a_user
from time import sleep
import random
import argparse

def Like_by_id(api,id,amount,is_private=False):

    print("Start liking ...")
    sleep(3)
 
    if is_private == False:

        print("Gettings all posts ...")

        posts = Get_media_ids_of_a_user(
                                        api=api,
                                        id=id
                )

        sleep(random.randrange(50,60))
        print("Finished getting posts .")
    
        if posts:
            for post in posts[:amount]:
                try:
                    print("Liking one of {0} posts ...".format(id))
                    sleep(5)
                    result = api.post_like(media_id=post)
                    if result['status'] == 'ok':
                        print("Liked Image !")
                        print("\n")
                        sleep(random.randrange(60,70))
                    else:
                        print("Couldn't like the image !")
                        print("\n")
                        sleep(random.randrange(60,70))
                except ClientError as err:
                    if err.code == 404:
                        print(err)
                    if err.code == 400:
                        print(err)
                except Exception as err:
                    print(err+" Exiting ...")
                    sys.exit()
        else:
            print("User {0} has no posts ...".format(id))
    
    else:
        print("Account {0} is Privte".format(id))
        sleep(3)




if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-t', '--target_id', dest='target_id', type=str, required=True)
    parser.add_argument('-a', '--amount', dest='amount', type=int, required=True)

    args = parser.parse_args()

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )

    Like_by_id(
               api=api,
               id=args.target_id,
               amount=args.amount
    )