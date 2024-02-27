#!python

from vmanage_api import VmanageRestApi
from env_settings import *

if __name__ == '__main__':

    vmanage = VmanageRestApi(vmanage_ip, vmanage_user, vmanage_password)
    feature_profiles = vmanage.get_request('/v1/feature-profile/sdwan')
    for num, profile in enumerate(feature_profiles):
        print(f'{(num + 1):3}: {profile["profileType"]:20}   {profile["profileName"]}')
    while True:
        try:
            choice = int(input('\nWhich profile do you want to copy: '))
            break
        except ValueError:
            continue
    payload = {
        "name": f"{feature_profiles[choice-1]['profileName']}_COPY",
        "description": f"Copy of {feature_profiles[choice-1]['profileName']}",
        "fromFeatureProfile": {
            "copy": feature_profiles[choice-1]['profileId']
        }
    }
    new_profile = vmanage.post_request(f'/v1/feature-profile/sdwan/{feature_profiles[choice-1]["profileType"]}',
                                       payload=payload)
    try:
        print(f'Success creating new profile, {new_profile["id"]}')
    except KeyError:
        print(f'Error copying profile.  If you\'ve already copied this profile, rename the copy before trying again.\n'
              f'{new_profile}')
    vmanage.logout()
