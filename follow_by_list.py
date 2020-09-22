from login import Login
from login import ClientError
from get_info_by_username import Get_info_by_username
from follow_by_id import Follow_by_id
from like_by_id import Like_by_id

from dbutils.check_for_follow_query import Check_for_follow_query
from dbutils.get_followings_query import Get_followings_query
from dbutils.follow_query import Follow_Query


from time import sleep
from datetime import datetime
import argparse
import random
import os
import sys



def Follow_by_list(api,list_of_users,amount,set_do_like):

    if os.path.isfile(list_of_users):
        path_for_list = os.path.abspath(list_of_users)
    else:
        print("THERE IS NOT A FILE WITH '{0}' NAME IN CURRENT DIRECTORY".format(list_of_users))
        sys.exit()
    
    try:
        with open(path_for_list , 'r') as fin:
            content = fin.readlines()
            if content:
                users = []
                for i in content:
                    users.append(i.replace('\n',''))
            else:
                print('USERS FILE IS EMPTY !')
                sys.exit()
        
    except FileNotFoundError:
        print("SUCH FILE DOES NOT EXIST !")
        sys.exit()
    except IOError:
        print("COULD NOT READ THE FILE !")
        sys.exit()


    print("\nStart following by list ...")

    me = Get_info_by_username(
                              api=api,
                              username=args.username
        )

    if not me:
        print('Encountered error while getting your info')
        return

    sleep(random.randrange(60,70))

    counter = 0
    if users:

        my_followings = Get_followings_query(me['id'],me['username'])

        for username in users:
            
            if counter >= amount :
                print("\nFinished following users in a list ...\n")
                sleep(5)
                break
            
            user = Get_info_by_username(
                                        api=api,
                                        username=username
                    )

            if not user:
                print('Encountered error while getting user info')
                sleep(random.randrange(30,40))
                continue

            sleep(random.randrange(60,70))

            try:
                data = (me['id'],me['username'],user['username'],user['id'],)
                res1 = Check_for_follow_query(data)

                if res1['status'] == "ok":

                    if  my_followings['status'] == "ok":
                        
                        flag = True
                        for following in my_followings['followings']:
                            if user['id'] == following[3] :
                                flag = False
                                break

                        if flag == False:
                            #You have already followed this user
                            continue
                        else:
                            print("\n")
                            print('Following [ username: {0}  full_name: {1} ] ...'.format(user.get('username'),user.get('full_name')))
                            sleep(5)

                            status = Follow_by_id(
                                                  api=api,
                                                  id=user.get('id')
                                    )
                    
                            if status == True:

                                counter = counter + 1
                                print("Followed !")

                                if counter % 5 == 0:
                                    sleep(random.randrange(60,70))
                                else:
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

                                print('Could not follow [ username: {0}  full_name: {1} ] !'.format(user.get('username'),user.get('full_name')))
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
                    sleep(random.randrange(60,70))
                elif err.code == 404:
                    print("Could not find this user . skipping ...")
                    sleep(random.randrange(60,70))
                else:
                    print(err)
                    
            except Exception as err:
                print(err)

        print("\nFinished following users in a list ...\n")
    
    else:
        print("Could not get any user . list is empty ...")



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-l', '--list', dest='list', type=str, required=True)
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

    Follow_by_list(
                   api=api,
                   list_of_users=args.list,
                   amount=args.amount,
                   set_do_like=set_do_like
    )