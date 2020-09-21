from login import Login
from login import ClientError
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
import random
import argparse


def Follow_likers(api,username,num_of_posts,num_of_likers_each_post,set_do_like):

    print("\nStart following likers ...\n")

    try:
        target_user_id = Get_info_by_username(
                                            api=api,
                                            username=username
                        ).get('id')

        if not target_user_id:
            print('Encountered error while getting user info')
            return
        sleep(random.randrange(60,70))
        print("Gettings all posts ...")
        posts = Get_media_ids_of_a_user(
                                        api=api,
                                        id=target_user_id
                )[:num_of_posts]

        sleep(random.randrange(50,60))
        print("Finished getting posts .")
    except ClientError as err:
        print(err)
        sys.exit()

    
    if posts:
        
        me = Get_info_by_username(
                                  api=api,
                                  username=args.username
            )

        if not me:
            print('Encountered error while getting user info')
            return

        for post in posts:
            try:
                users = Get_likers(
                                    api=api,
                                    media_id=post
                        )
            except ClientError as err:
                print(err)
                sys.exit()

            counter = 0
            if users:
                for user in users:
                    if counter >= num_of_likers_each_post :
                        print("\n")
                        print("Finished following users of this post , going for next post ....")
                        print("\n")
                        break

                    print("\n")
                    print('Following [ username:{0}  full_name:{1} ] ...'.format(user.get('username'),user.get('full_name')))
                    sleep(5)

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
                                    print("You have already followed this user . skipping ...")
                                    sleep(5)
                                else:
                                    status = Follow_by_id(
                                                          api=api,
                                                          id=user.get('id') 
                                            )
                            
                                    if status == True:

                                        counter = counter + 1
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

