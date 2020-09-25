from login import Login
from login import ClientError
from login import from_json
from get_info_by_username import Get_info_by_username
from get_followings import Get_followings
from follow_by_id import Follow_by_id
from like_by_id import Like_by_id

from dbutils.check_for_follow_query import Check_for_follow_query
from dbutils.get_followings_query import Get_followings_query
from dbutils.follow_query import Follow_Query

from datetime import datetime
from time import sleep
import argparse
import random
import json
import os

def Follow_user_followings(api,username,amount,set_do_like):

    user_info = Get_info_by_username(
                                     api=api,
                                     username=username
                )

    if not user_info:
        print('Encountered error while getting user info')
        return

    """
    if user_info['is_private'] == True:
        print("You can't get {0} followings , cause the account is private".format(user_info['username']))
        return
    """

    print("\nStart following {0} followers ...".format(user_info['username']))
    sleep(3)
    
    sleep(random.randrange(60,70))

    me = Get_info_by_username(
                              api=api,
                              username=args.username
        )

    if not me:
        print('Encountered error while getting your info')
        return

    sleep(random.randrange(60,70))

    followers_file_path = os.getcwd() + '/LOGS/{0}/{1}-followings.json'.format(args.username,user_info['username'])

    if os.path.isfile(followers_file_path):

        with open(followers_file_path,'r') as fin:
            try:
                followings = json.load(fin,object_hook=from_json)
            except Exception:
                followings = Get_followings(
                                            api=api,
                                            username=args.username,
                                            target_username=user_info['username'],
                                            target_id=user_info['id']
                    )

    
    else:
        followings = Get_followings(
                                    api=api,
                                    username=args.username,
                                    target_username=user_info['username'],
                                    target_id=user_info['id']
                    )
 
    sleep(random.randrange(60,70))

    counter = 0
    if followings:

        my_followings = Get_followings_query(me['id'],me['username'])

        for user in followings:
            if counter >= amount :
                print("\nFinished following user's followings ...\n")
                break

            try:
                data = (me['id'],me['username'],user['username'],user['pk'],)
                res1 = Check_for_follow_query(data)

                if res1['status'] == "ok":

                    if  my_followings['status'] == "ok":
                        
                        flag = True
                        for following in my_followings['followings']:
                            if str(user['pk']) == following[3] :
                                flag = False
                                break

                        if flag == False:
                            #You have already unfollowed this user once 
                            continue
                        else:
                            print("\n")
                            print('Following [ username:{0}  full_name:{1} ] ...'.format(user.get('username'),user.get('full_name')))
                            sleep(5)

                            status = Follow_by_id(
                                                 api=api,
                                                 id=user.get('pk')
                                    )
                    
                            if status == True:

                                counter = counter + 1
                                print("Followed !")

                                data = (me['id'],me['username'],user['username'],user['pk'],str(datetime.now()))
                                res2 = Follow_Query(data)

                                if res2["status"] == "ok":
                                    print("saved to database !")
                                    sleep(5)
                                else:
                                    print("could not save to database !")
                                    sleep(5)

                                if counter % 5 == 0:
                                    sleep(random.randrange(600,620))
                                else:
                                    sleep(random.randrange(60,70))

                                if set_do_like == True:

                                    Like_by_id(
                                                api=api,
                                                id=user.get('pk'),
                                                amount=1,
                                                is_private=user.get('is_private')
                                    )

                                    sleep(random.randrange(60,70))
                                    
                            else:

                                print('Could not follow [ username:{0}  full_name:{1} ] !'.format(user.get('username'),user.get('full_name')))
                                print("\n")
                                sleep(random.randrange(60,70))
                    
                    else:
                        print("db error ! could not fetch your followings to check")
                        sleep(5)

                elif res1['status'] == "error":
                    #You have already unfollowed this user once 
                    continue

                else:
                    
                    print("db error . could not check for follow ")
                    print("\n")
                    sleep(5)

            except ClientError as err:
                if err.code == 400:
                    print("Bad Request: ",err)
                    sleep(random.randrange(60,70))
                elif err.code == 404:
                    print(err)
                    sleep(random.randrange(60,70))
                else:
                    print(err)
                    sleep(random.randrange(60,70))
                    
            except Exception as err:
                print("None client error: ",err)
                sleep(random.randrange(30,40))
    
    else:
        print("Could not get any user . list is empty ...")




if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-t', '--target_username', dest='target_username', type=str, required=True)
    parser.add_argument('-a', '--amount', dest='amount', type=int, required=True)
    parser.add_argument('-set_do_like', '--set_do_like', action='store_true')

    args = parser.parse_args()

    if args.set_do_like:
        set_do_like = True
    else:
        set_do_like = False

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )

    Follow_user_followings(
                          api=api,
                          username=args.target_username,
                          amount=args.amount,
                          set_do_like=set_do_like
    )