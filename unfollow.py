from login import Login
from login import ClientError
from instagram_private_api import (ClientChallengeRequiredError,
                                   ClientCheckpointRequiredError,
                                   ClientSentryBlockError,
                                   ClientThrottledError
)
from get_info_by_username import Get_info_by_username

from dbutils.get_followings_query import Get_followings_query
from dbutils.unfollow_query import Unfollow_Query
from dbutils.delete_from_followings import Delete_from_followings

from dateutil import parser as Parser
from datetime import datetime
from time import sleep
import argparse
import random


def Unfollow(api,amount):

    print("\nStart unfollowing ...\n")
    sleep(3)

    try:

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
        #my_followings['followings'] = my_followings['followings'][::-1]

        if my_followings['status'] == "ok":
            
            counter = 0
            ClientErrorCounter = 0
            for user in my_followings['followings']:

                print("Unfollowing [ {0} ] ...".format(user[2]))

                date_of_follow = Parser.parse(user[4])
                now = datetime.now()
                delta = now - date_of_follow

                if delta.days > 4:
                    
                    try:
                        result = api.friendships_destroy(user[3])
                        if result['status'] == 'ok':

                            print("Unfollowed !")
                            sleep(3)
                            counter = counter + 1

                            data = (me['id'],me['username'],user[2],user[3],str(datetime.now()))
                            res = Unfollow_Query(data)

                            if res['status'] == "ok":
                                print('Saved into database !')
                            else:
                                print('Could not save into database !')
                                
                            
                            if counter >= amount:
                                print("Unfollowed {0} users !".format(amount))
                                break
                            
                            if counter % 5 == 0:
                                sleep(random.randrange(600,620))
                            else:
                                sleep(random.randrange(70,80))

                        else:
                            print("Couldn't Unfollow !")
                            sleep(random.randrange(70,80))


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
                        if err.code == 404:
                            print("User {0} not found !".format(user[2]))
                            data = (me['id'],me['username'],user[2],user[3])
                            res = Delete_from_followings(data)
                            if res['status'] == "ok":
                                pass
                            else:
                                print("Could not delete from followings")
                            sleep(random.randrange(70,80))
                        elif err.code == 400:
                            ClientErrorCounter = ClientErrorCounter + 1
                            print("Bad Request : ",err)
                            sleep(random.randrange(70,80))
                        else:
                            ClientErrorCounter = ClientErrorCounter + 1
                            print(err)
                            sleep(random.randrange(70,80))
                    except Exception as err:
                        print(err)

                else:
                    print("This user hasn't reached to specified time for unfollow . skipping ...")
                    sleep(5)
                    print("There is not any other users in your followings who has been reached to the sepecific time to unfollow !")
                    break


            print("Finished unfollowing !")

        else:
            print('Database error ! Could not fetch your followings .')


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
    except Exception as err:
        print(err)
        return

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

    

