from login import Login
from login import ClientError
from time import sleep
import os
import sys
import random
import argparse

def Follow_tags(api,file_name):
    
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



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-l', '--list', dest='list', type=str, required=True)

    args = parser.parse_args()

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )

    Follow_tags(
                api=api,
                file_name=args.list
    )