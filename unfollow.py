from login import Login
from login import ClientError
from get_info_by_username import Get_info_by_username

from dbutils.get_followings_query import Get_followings_query
from dbutils.unfollow_query import Unfollow_Query

from dateutil import parser as Parser
from datetime import datetime
from time import sleep
import argparse
import random


def Unfollow(api,amount):

    print("\nStart unfollowing ...\n")
    sleep(3)

    me = Get_info_by_username(
                             api=api,
                             username=args.username
        )
    if not me:
        print('Encountered error while getting user info')
        return
    
    sleep(random.randrange(60,70))
    
    me_id = me['id']
    my_followings = Get_followings_query(me['id'],me['username'])
    my_followings['followings'] = my_followings['followings'][::-1]

    if my_followings['status'] == "ok":

        for user in my_followings['followings'][:amount]:

            try:
                print("Unfollowing [ {0} ] ...".format(user[2]))

                date_of_follow = Parser.parse(user[4])
                now = datetime.now()
                delta = now - date_of_follow

                if delta.seconds > 900:
                    
                    try:
                        result = api.friendships_destroy(user[3])
                        if result['status'] == 'ok':

                            print("Unfollowed !")

                            data = (me['id'],me['username'],user[2],user[3],str(datetime.now()))
                            res = Unfollow_Query(data)

                            if res['status'] == "ok":
                                print('Saved into database !')
                            else:
                                print('Could not save into database !')
                                
                            print("\n")
                            sleep(random.randrange(70,80))
                        else:
                            print("Couldn't Unfollow !")
                            sleep(random.randrange(70,80))
                            
                    except ClientError as err:
                        print(err)

                else:
                    print("This user hasn't reached to specified time for unfollow . skipping ...")
                    sleep(5)

            except ClientError as err:
                if err.code == 404:
                    print("Couldn't find {0} in your followings . skipping ...".format(user['username']))
                    print("\n")
                    sleep(7)
                elif err.code == 400:
                    print(err)
                    print("\n")
                    sleep(7)
                else:
                    print(err)
                    sleep(7)
            except Exception as err:
                print(err)
                sys.exit()

    else:
        print('Database error ! Could not fetch your followings .')



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-a', '--amount', dest='amount', type=int, required=True)

    args = parser.parse_args()

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )
    
    Unfollow(
            api=api,
            amount=args.amount
    )

    

