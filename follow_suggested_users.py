from login import Login
from login import ClientError
from follow_by_id import Follow_by_id
from like_by_id import Like_by_id
from get_info_by_username import Get_info_by_username

from dbutils.check_for_follow_query import Check_for_follow_query
from dbutils.get_followings_query import Get_followings_query
from dbutils.follow_query import Follow_Query

from datetime import datetime
from time import sleep
import random
import argparse


def Follow_suggested_users(api,amount,set_do_like):
    
    print("\nStart following suggested users ...")
    sleep(3)

    try:
        data = api.friendships_pending()
        if data:
            suggested_users = data['suggested_users']['suggestions']
        else:
            print("Could not get suggested users !")
            return
    except ClientError as err:
        print(err)
        return
    except Exception as err:
        print(err)
        return

    sleep(random.randrange(60,70))

    me = Get_info_by_username(
                              api=api,
                              username=args.username
        )

    counter = 0
    if suggested_users:

        my_followings = Get_followings_query(me['id'],me['username'])

        for user in suggested_users:
    
            if counter >= amount :
                print("\nFinished following suggested users ...\n")
                break

            try:
                data = (me['id'],me['username'],user['user']['username'],user['user']['pk'],)
                res1 = Check_for_follow_query(data)

                if res1['status'] == "ok":


                    if  my_followings['status'] == "ok":
                        
                        flag = True
                        for following in my_followings['followings']:
                            if str(user['user']['pk']) == following[3] :
                                flag = False
                                break

                        if flag == False:
                            #You have already followed this user
                            continue
                        else:
                            print("\n")
                            print('Following   [[ username:{0}  full_name:{1} ]] ...'.format(user['user']['username'],user['user']['full_name']))
                            sleep(5)

                            status = Follow_by_id(
                                                 api=api,
                                                 id=user['user']['pk']
                                    )
                    
                            if status == True:

                                counter = counter + 1
                                print("Followed !")

                                data = (me['id'],me['username'],user['user']['username'],user['user']['pk'],str(datetime.now()))
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
                                                id=user['user']['pk'],
                                                amount=1,
                                                is_private=user['user']['is_private']
                                    )

                                    sleep(random.randrange(60,70))
                                    
                            else:

                                print('Could not follow [ username:{0}  full_name:{1} ] !'.format(user['user']['username'],user['user']['full_name']))
                                print("\n")
                                sleep(random.randrange(60,70))
                    
                    else:
                        print("db error ! could not fetch your followings to check")
                        return

                elif res1['status'] == "error":
                    #You have already unfollowed this user once 
                    continue

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
        print("You dont have any suggestions right now")


if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
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

    Follow_suggested_users(
                           api=api,
                           amount=args.amount,
                           set_do_like=set_do_like
    )