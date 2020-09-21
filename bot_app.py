from dateutil import parser as Parser
from datetime import datetime
from time import sleep
import json
import codecs
import os.path
import logging
import argparse
import random
import os
import sys

from dbutils.check_for_follow_query import Check_for_follow_query
from dbutils.follow_query import Follow_Query
from dbutils.get_followings_query import Get_followings_query
from dbutils.unfollow_query import Unfollow_Query

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,ClientConnectionError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))



def get_followers(api,id):
    try:
        followers = []
        data = api.user_followers(id,rank_token=api.generate_uuid())
        next_max_id = data.get('next_max_id')
        while next_max_id:
            data = api.user_followers(id,rank_token=api.generate_uuid(),max_id=next_max_id)
            followers.extend(data.get('users',[]))
            next_max_id = data.get('next_max_id')

        followers.extend(data.get('users', []))
        print(len(followers))
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



def get_followings(api,id):

    try:
        followings = []
        data = api.user_following(id,rank_token=api.generate_uuid())
        next_max_id = data.get('next_max_id')
        print("next_max_id :",next_max_id)
        while next_max_id:
            if next_max_id >= 300:
                break
            data = api.user_following(id,rank_token=api.generate_uuid(),max_id=next_max_id)
            followings.extend(data.get('users',[]))
            next_max_id = data.get('next_max_id')
            print("next_max_id :",next_max_id)
            sleep(5)

        followings.extend(data.get('users', []))
        print(len(followings))
        sleep(7)
        return followings
        

    except Exception as err:
        print(err)
        print(len(followings))
        sleep(7)
        return followings




def get_info_by_username(api , username):

    data = {}
    try:
        result = api.username_info(username)
        data = {

            'id':str(result['user']['pk']),
            'username':username,
            'full_name':result['user']['full_name'],
            'is_private':result['user']['is_private'],
            'media_count':result['user']['media_count'],
            'follower_count':result['user']['follower_count'],
            'following_count':result['user']['following_count']
        }
        sleep(7)
        return data
    except ClientError as err:
        print(err)
        sleep(7)
        return data



    
"""
def get_user_info():
    data = api.user_detail_info('40885305332')
    with open('/home/mohsen/VSCode/instagram_private_api/xxxxx.json','w') as fout:
        json.dump(data,fout,indent=4,sort_keys=True)
"""   



def follow(api , id):

    result = api.friendships_create(id)

    if result['status'] == 'ok':
        return  True
    else:
        return False




def follow_tags(api,file_name):
    
    if os.path.isfile(file_name):
        path_for_tags_file = os.path.abspath(file_name)
    else:
        print("THERE IS NOT A FILE WITH '{0}' NAME IN CURRENT DIRECTORY".format(file_name))
        sys.exit()
    
    try:
        with open(path_for_tags_file , 'r') as fin:
            tags = fin.readlines()
            if not tags:
                print('TAGS FILE IS EMPTY !')
                sys.exit()
        
    except FileNotFoundError:
        print("SUCH FILE DOES NOT EXIST !")
        sys.exit()
    except IOError:
        print("COULD NOT READ THE FILE !")
        sys.exit()

    for tag in tags:
        try:
            print("\n")
            print("Following << #{0} >> ...".format(tag))
            result = api.tag_follow(tag)
            if result['status'] == 'ok':
                print("Followed !")
                print("\n")
                sleep(random.randrange(60,70))
            else:
                print("Could not follow << #{0} >>".format(tag))
                print("\n")
                sleep(random.randrange(60,70))

                
        except ClientError as err:
            if err.code == 404:
                print("Could not find this tag ! skipping ...")
                sleep(random.randrange(60,70))
            elif err.code == 400:
                print("Bad Request: You have already followed this hashtag . skipping ...")
                sleep(random.randrange(60,70))
            else:
                print(err)
        except Exception as err:
            print(err)
            sys.exit()



def tag_sug():
    data = api.tag_follow_suggestions()
    print(type(data))
    print(data)



def media_info():
    data = api.media_info(media_id='2393646214447833174')
    print(type(data))
    print(data)




def like_by_id(api,id,amount,is_private=False):

    print("Start liking ...")
    sleep(3)

    
    if is_private == False:

        print("Gettings all posts ...")
        posts = get_media_ids_of_a_user(api,id)
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
                    print(err+"Exiting ...")
                    sys.exit()
        else:
            print("User {0} has no posts ...".format(id))
    
    else:
        print("Account {0} is Privte".format(id))
        sleep(3)



def like_by_username(apiii,username,amount):

    print("Start liking ...")
    sleep(3)

    user_info = get_info_by_username(api,username).get('id')
    if not user_info:
        print('Encountered error while getting user info')
        return

    sleep(random.randrange(50,60))

    user_id = user_info.get('id')

    

    if user_info.get('is_private') == False:

        print("Gettings all posts ...")
        posts = get_media_ids_of_a_user(api,id)
        sleep(random.randrange(50,60))
        print("Finished getting posts .")

        if posts :
            for post in posts[:amount]:
                try:
                    print("Liking one of {0} posts ...".format(user_id))
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
                    print(err+"Exiting ...")
                    sys.exit()

        else:
            print("This user has not any posts")

    else:
        print("Account {0} is Privte".format(username))
        sleep(5)



def get_likers(api,media_id):

    result = api.media_likers(media_id=str(media_id))

    if result['status'] == 'ok':
        users = []
        for user in result['users']:
            data = {}
            data = {

                'id':str(user['pk']),
                'username':user['username'],
                'full_name':user['full_name'],
                'is_private':user['is_private']
            }
            users.append(data)
        
        sleep(7)
        return users
    
    else:
        print('Could not get likers from media with id {0}'.format(media_id))
        sleep(7)
        return None




def get_media_ids_of_a_user(api,id):

    result = api.user_detail_info(id)
    media_ids_list = media_id_extractor(result['feed']['items'])
    sleep(7)
    return media_ids_list
    

def media_id_extractor(medias):

    """ recives a list of full media info of user and extract their ids """

    media_ids_list = []
    for media in medias:
        media_ids_list.append(str(media['caption']['media_id']))

    return media_ids_list



def follow_likers(api,username,num_of_posts,num_of_likers_each_post,set_do_like):

    print("Start following likers ...")

    try:
        target_user_id = get_info_by_username(api,username).get('id')
        if not target_user_id:
            print('Encountered error while getting user info')
            return
        sleep(random.randrange(60,70))
        print("Gettings all posts ...")
        posts =  get_media_ids_of_a_user(api,target_user_id)[:num_of_posts]
        sleep(random.randrange(50,60))
        print("Finished getting posts .")
    except ClientError as err:
        print(err)
        sys.exit()

    
    if posts:
        
        me = get_info_by_username(api , args.username)
        if not me:
            print('Encountered error while getting user info')
            return

        for post in posts:
            try:
                users = get_likers(api,post)
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
                                    status = follow(api,user.get('id'))
                            
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

                                            like_by_id(api , user.get('id'),1,user.get('is_private'))
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




def unfollow(api,amount):

    print("Start unfollowing ...")
    sleep(3)

    me = get_info_by_username(api , args.username)
    if not me:
        print('Encountered error while getting user info')
        return
    
    sleep(random.randrange(60,70))
    
    me_id = me['id']
    my_followings = Get_followings_query(me['id'],me['username'])

    if my_followings['status'] == "ok":

        for user in my_followings['followings'][:amount]:

            try:
                print("Unfollowing << {0} >> ...".format(user[2]))

                date_of_follow = Parser.parse(user[4])
                now = datetime.now()
                delta = now - date_of_follow
                print(delta)

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





def follow_user_followers(api,username,amount,set_do_like):

    print("Start following user's followers ...")
    sleep(3)

    user_info = get_info_by_username(api,username)
    if not user_info:
        print('Encountered error while getting user info')
        return

    sleep(random.randrange(60,70))

    me = get_info_by_username(api , args.username)
    if not me:
        print('Encountered error while getting your info')
        return
    
    sleep(random.randrange(60,70))

    print("Getting users's followers ...")
    followers = get_followers(api,user_info['id'])
    print("Finished getting followers ...\n")

    counter = 0
    if followers:
        for user in followers:
            if counter >= amount :
                print("\nFinished following users's followers ...\n")
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
                            status = follow(api,user.get('pk'))
                    
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

                                    like_by_id(api , user.get('pk'),1,user.get('is_private'))
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






def follow_user_followings(api,username,amount,set_do_like):

    print("Start following user's followings")
    sleep(3)

    user_info = get_info_by_username(api,username)
    if not user_info:
        print('Encountered error while getting user info')
        return

    sleep(random.randrange(60,70))

    me = get_info_by_username(api , args.username)
    if not me:
        print('Encountered error while getting your info')
        return

    sleep(random.randrange(60,70))

    print("Getting users's followings ...")
    followings = get_followings(api,user_info['id'])
    print("Finished getting followings ...\n")

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
                            status = follow(api,user.get('pk'))
                    
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

                                    like_by_id(api , user.get('pk'),1,user.get('is_private'))
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
            



def follow_by_list(api,list_of_users,amount,set_do_like):

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


    print("Start following by list ...")

    me = get_info_by_username(api , args.username)
    if not me:
        print('Encountered error while getting your info')
        return


    counter = 0
    if users:
        for username in users:
            if counter >= amount :
                print("\nFinished following users in a list ...\n")
                sleep(5)
                break
            
            user = get_info_by_username(api,username)
            if not user:
                print('Encountered error while getting user info')
                sleep(30)
                continue


            print("\n")
            print('Following [ username: {0}  full_name: {1} ] ...'.format(user.get('username'),user.get('full_name')))
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
                            status = follow(api,user.get('id'))
                    
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

                                    like_by_id(api , user.get('id'),1,user.get('is_private'))
                                    sleep(random.randrange(60,70))
                                    
                            else:

                                print('Could not follow [ username: {0}  full_name: {1} ] !'.format(user.get('username'),user.get('full_name')))
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




if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api')
    logger.setLevel(logging.WARNING)

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-debug', '--debug', action='store_true')

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    print('Client version: {0!s}'.format(client_version))

    device_id = None
    try:

        settings_file = args.settings_file_path
        if not os.path.isfile(settings_file):
            # settings file does not exist
            print('Unable to find file: {0!s}'.format(settings_file))

            # login new
            api = Client(
                args.username, args.password,
                on_login=lambda x: onlogin_callback(x, args.settings_file_path))
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            print('Reusing settings: {0!s}'.format(settings_file))

            device_id = cached_settings.get('device_id')
            # reuse auth settings
            api = Client(
                args.username, args.password,
                settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(
            args.username, args.password,
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, args.settings_file_path))

    except ClientLoginError as e:
        print('ClientLoginError {0!s}'.format(e))
        exit(9)
    except ClientError as e:
        print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print('Unexpected Exception: {0!s}'.format(e))
        exit(99)

    # Show when login expires
    cookie_expiry = api.cookie_jar.auth_expires
    print('Cookie Expiry: {0!s}'.format(datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))

    # Call the api
    #results = api.user_feed('2958144170')
    #assert len(results.get('items', [])) > 0

    print('All ok')

    """
    follow_likers(
                  api=api,
                  username='net.seo',
                  num_of_posts=1,
                  num_of_likers_each_post=10,
                  set_do_like=True
    )

    """

    #follow_tags(api,'tags.txt')


     
    try:
        follow_likers(
                  api=api,
                  username='net.seo',
                  num_of_posts=3,
                  num_of_likers_each_post=3,
                  set_do_like=True
        )
        sleep(700)
        follow_user_followers(
                            api=api,
                            username='net.seo',
                            amount=5,
                            set_do_like=True
        )
        sleep(700)
        unfollow(
                api=api,
                amount=5
        )
    except ClientConnectionError as err:
        print(err)
        print("Run the scrip in a few minutes ...")
        sys.exit()
    except Exception as err:
        print("[!] ",err)
        sys.exit()
    
