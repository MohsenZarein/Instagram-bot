import sys
sys.path.append('../')
from login import Login
from login import ClientError
from get_info_by_username import Get_info_by_username
from follow_by_id import Follow_by_id
from like_by_id import Like_by_id

from dbutils.check_for_follow_query import Check_for_follow_query
from dbutils.get_followings_query import Get_followings_query
from dbutils.follow_query import Follow_Query

from datetime import datetime
from time import sleep
import random
import argparse

def Follow_by_username(api , username , set_do_like):

    print("\nStart following ...")
    sleep(3)

    user = Get_info_by_username(
                                     api=api,
                                     username=username
    )

    if not user:
        print("Could not get user info!")
        return False
    
    sleep(random.randrange(50,60))

    me = Get_info_by_username(
                              api=api,
                              username=args.username
        )

    if not me:
        print('Encountered error while getting your info')
        return

    sleep(random.randrange(60,70))
        
    try:
        data = (me['id'],me['username'],user['username'],user['id'],)
        res1 = Check_for_follow_query(data)

        if res1['status'] == "ok":

            my_followings = Get_followings_query(me['id'],me['username'])

            if  my_followings['status'] == "ok":
                
                flag = True
                for following in my_followings['followings']:
                    if user['id'] == following[3] :
                        flag = False
                        break

                if flag == False:
                    print("You have already followed this user")
                    return
                else:
                    print("\n")
                    print('Following [ username: {0}  full_name: {1} ] ...'.format(user.get('username'),user.get('full_name')))
                    sleep(5)
                    
                    status = Follow_by_id(
                                            api=api,
                                            id=user.get('id')
                            )
            
                    if status == True:

                        print("Followed !")
                        sleep(5)

                        data = (me['id'],me['username'],user['username'],user['id'],str(datetime.now()))
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
                                        id=user.get('id'),
                                        amount=1,
                                        is_private=user.get('is_private')
                            )

                            sleep(random.randrange(60,70))
                            
                    else:

                        print('Could not follow [[ username: {0}  full_name: {1} ]] !'.format(user.get('username'),user.get('full_name')))
                        print("\n")
                        sleep(random.randrange(60,70))
            
            else:
                print("db error ! could not fetch your followings to check")
                return

        elif res1['status'] == "error":
            print("You have already unfollowed/followed this user once")
            return

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



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-t', '--target_username', dest='target_username', type=str, required=True)
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

    result = Follow_by_username(
                          api=api,
                          username=args.target_username,
                          set_do_like=set_do_like
    )


