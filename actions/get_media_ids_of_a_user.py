from login import Login
from login import ClientError
from time import sleep
import argparse


def media_id_extractor(medias):

    """ recives a list of full media info of user and extract their ids """

    media_ids_list = []
    for media in medias:
        media_ids_list.append(str(media['caption']['media_id']))

    return media_ids_list


def Get_media_ids_of_a_user(api,id):

    try:
        result = api.user_detail_info(id)
        if result['feed']['items']:
            media_ids_list = media_id_extractor(result['feed']['items'])
            sleep(7)
            return media_ids_list
        else:
            print("Could not get user's medias")
            return []
    except ClientError as err:
        print(err)
        return []
    


if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='INSTAGRAM ROBOT')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-t', '--target_id', dest='target_id', type=str, required=True)


    args = parser.parse_args()

    api = Login(
                settings_file_path=args.settings_file_path,
                username=args.username,
                password=args.password
    )

    result = Get_media_ids_of_a_user(
                                     api=api,
                                     id=args.target_id
    )

    if result:
        print(result)