import sys
sys.path.append('../')
from login import Login
from login import from_json
from login import to_json
from instagram_private_api import (ClientChallengeRequiredError,
                                   ClientCheckpointRequiredError,
                                   ClientSentryBlockError,
                                   ClientThrottledError,
                                   ClientError
)
from get_info_by_username import Get_info_by_username
from get_media_ids_of_a_user import Get_media_ids_of_a_user
from get_likers import Get_likers
from follow_by_id import Follow_by_id
from like_by_id import Like_by_id

from dbutils.check_for_follow_query import Check_for_follow_query
from dbutils.get_followings_query import Get_followings_query
from dbutils.follow_query import Follow_Query

from datetime import datetime
from time import sleep
from pathlib import Path
import random
import argparse
import json
import os


def Follow_likers(api,username,num_of_posts,num_of_likers_each_post,set_do_like):

    print("\nStart following likers ...\n")

    try:
        target_user = Get_info_by_username(
                                            api=api,
                                            username=username
                        )

        target_user_id = target_user.get('id')
        
        if not target_user_id:
            print('Encountered error while getting user info')
            return

        sleep(random.randrange(60,70))

        print("Gettings all posts ...")
        posts = Get_media_ids_of_a_user(
                                        api=api,
                                        id=target_user_id
                )[:num_of_posts]

    except ClientError as err:
        print(err)
        return

    
    if posts:

        sleep(random.randrange(50,60))
        print("Finished getting posts .")
        
        me = Get_info_by_username(
                                  api=api,
                                  username=args.username
            )

        if not me:
            print('Encountered error while getting user info')
            return
        
        sleep(random.randrange(50,60))

        ClientErrorCounter = 0
        for post in posts:

            cwd = os.getcwd()
            try:
                Path(cwd + '/LOGS/{0}'.format(args.username)).mkdir(parents=True, exist_ok=False)
                path_for_likers_file = cwd + '/LOGS/{0}/{1}-likers-{2}.json'.format(args.username,target_user['username'],post)
            except FileExistsError:
                path_for_likers_file = cwd + '/LOGS/{0}/{1}-likers-{2}.json'.format(args.username,target_user['username'],post)

            if os.path.isfile(path_for_likers_file):
                with open(path_for_likers_file,'r') as fin:
                    try:
                        users = json.load(fin,object_hook=from_json)
                    except Exception:
                        try:
                            users = Get_likers(
                                                api=api,
                                                media_id=post
                                    )
                            with open(path_for_likers_file,'w') as fout:
                                json.dump(users,fout,default=to_json)

                            sleep(random.randrange(50,60))
                        except ClientError as err:
                            print(err)
                            sys.exit()

            else:
                try:
                    users = Get_likers(
                                        api=api,
                                        media_id=post
                            )
                    with open(path_for_likers_file,'w') as fout:
                        json.dump(users,fout,default=to_json)

                    sleep(random.randrange(50,60))
                except ClientError as err:
                    print(err)
                    sys.exit()
            

            counter = 0
            if users:

                my_followings = Get_followings_query(me['id'],me['username'])

                for user in users:
                
                    if counter >= num_of_likers_each_post :
                        print("\n")
                        print("Finished following users of this post , going for next post ....")
                        print("\n")
                        sleep(random.randrange(100,120))
                        break

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
                                    print('Following [ username:{0}  full_name:{1} ] ...'.format(user.get('username'),user.get('full_name')))
                                    sleep(5)

                                    status = Follow_by_id(
                                                          api=api,
                                                          id=user.get('id') 
                                            )
                            
                                    if status == True:

                                        counter = counter + 1
                                        print("Followed !")

                                        data = (me['id'],me['username'],user['username'],user['id'],str(datetime.now()))
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
                                                        id=user.get('id'),
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
                                return

                        elif res1['status'] == "error":
                            #You have already unfollowed this user once 
                            continue

                        else:
                            print("db error . could not check for follow ")
                            print("\n")
                            sleep(5)

                    except ClientChallengeRequiredError as err:
                        print("ClientChallengeRequiredError : ",err)
                        return
                    except ClientCheckpointRequiredError as err:
                        print("ClientCheckpointRequiredError : ",err)
                        return
                    except ClientSentryBlockError as err:
                        print("ClientSentryBlockError : ",err)
                        return
                    except ClientThrottledError as err:
                        print("ClientThrottledError : ",err)
                        return
                    except ClientError as err:
                        if ClientErrorCounter == 6:
                            print("Reached maximum ClientError . Return")
                            return
                        if err.code == 400:
                            ClientErrorCounter = ClientErrorCounter + 1
                            print("Bad Request: ",err)
                            sleep(random.randrange(60,70))
                        elif err.code == 404:
                            print("User not found !")
                            sleep(random.randrange(60,70))
                        else:
                            ClientErrorCounter = ClientErrorCounter + 1
                            print(err)
                            sleep(random.randrange(60,70))
                            
                    except Exception as err:
                        print("None client error: ",err)
                        
            
            else:
                print("This post has not any likers OR Couln't fetch them . skipping this post ...")

    else:
        print("\n")
        print("This user has not any post ...")
        print("\n")



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-t', '--target_username', dest='target_username', type=str, required=True)
    parser.add_argument('-n', '--number_of_posts', dest='number_of_posts', type=int, required=True)
    parser.add_argument('-f', '--number_of_likers_each_post', dest='number_of_likers_each_post', type=int, required=True)
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

    Follow_likers(
                  api=api,
                  username=args.target_username,
                  num_of_posts=args.number_of_posts,
                  num_of_likers_each_post=args.number_of_likers_each_post,
                  set_do_like=set_do_like
    )

