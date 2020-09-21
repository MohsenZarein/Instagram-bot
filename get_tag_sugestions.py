from login import Login
from login import ClientError
import argparse

def tag_sug(api):
    
    try:
        data = api.tag_follow_suggestions()
        return data
    except ClientError as err:
        print(err)
        return None
    except Exception as err:
        print(err)
        return None



if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)

    args = parser.parse_args()

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )

    result = tag_sug(api=api)
    if result:
        print(result)