from login import Login
from login import ClientError
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


def Follow_user_followings(api,username,amount,set_do_like):

    print("\nStart following user's followings ...")
    sleep(3)

    user_info = Get_info_by_username(
                                     api=api,
                                     username=username
                )

    if not user_info:
        print('Encountered error while getting user info')
        return
    """
    if user_info['is_private'] == True:
        print("You can't get this users's followings , cause the account is private")
        return
    """

    sleep(random.randrange(60,70))

    me = Get_info_by_username(
                              api=api,
                              username=args.username
        )

    if not me:
        print('Encountered error while getting your info')
        return

    sleep(random.randrange(60,70))

    
    followings = Get_followings(
                                api=api,
                                id=user_info['id']
                )

    counter = 0
    if followings:
        for user in followings:
            if counter >= amount :
                print("\nFinished following user's followings ...\n")
                break

            print("\n")
            print('Following [ username:{0}  full_name:{1} ] ...'.format(user.get('username'),user.get('full_name')))
            sleep(5)

            try:
                data = (me['id'],me['username'],user['username'],user['pk'],)
                res1 = Check_for_follow_query(data)

                if res1['status'] == "ok":

                    my_followings = Get_followings_query(me['id'],me['username'])

                    if  my_followings['status'] == "ok":
                        
                        flag = True
                        for following in my_followings['followings']:
                            if str(user['pk']) == following[3] :
                                flag = False
                                break

                        if flag == False:
                            print("You have already followed this user . skipping ...")
                            sleep(5)
                        else:
                            status = Follow_by_id(
                                                 api=api,
                                                 id=user.get('pk')
                                    )
                    
                            if status == True:

                                counter = counter + 1
                                print("Followed !")
                                sleep(5)

                                data = (me['id'],me['username'],user['username'],user['pk'],str(datetime.now()))
                                res2 = Follow_Query(data)

                                if res2["status"] == "ok":
                                    print("saved to database !")
                                    sleep(5)
                                else:
                                    print("could not save to database !")
                                    sleep(5)

                                print("\n")
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

                    print("You have already unfollowed this user once . skipping ...")
                    print("\n")
                    sleep(5)

                else:
                    
                    print("db error . could not check for follow ")
                    print("\n")
                    sleep(5)

            except ClientError as err:
                if err.code == 400:
                    print("Bad Request: You have already followed this user . skipping ...")
                    sleep(7)
                elif err.code == 404:
                    print("Could not find this user . skipping ...")
                    sleep(7)
                else:
                    print(err)
                    
            except Exception as err:
                print(err)
    
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