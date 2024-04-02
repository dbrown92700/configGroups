#!python

from vmanage_api import VmanageRestApi
from config_groups import ConfigGroups
import urllib.parse


def fp_copy(feature_profiles):
    # Lists current feature profiles and prompts user to copy one

    for num, profile in enumerate(feature_profiles):
        print(f'{(num + 1):3}: {profile["profileType"]:20}   {profile["profileName"]}')
    while True:
        try:
            choice = int(input('\nWhich profile do you want to copy: '))
            break
        except ValueError:
            continue
    new_name = input(f'Name for new profile [{feature_profiles[choice-1]["profileName"]}_COPY]: ') or \
               f'{feature_profiles[choice-1]["profileName"]}_COPY'
    description = input(f'Description for profile [Copy of {feature_profiles[choice-1]["profileName"]}]: ') or \
                  f"Copy of {feature_profiles[choice-1]['profileName']}"
    new_profile = config_groups.feature_profile_copy(feature_profiles[choice - 1]['profileId'], new_name, description)
    try:
        print(f'Success creating new profile, {new_profile["id"]}')
    except KeyError:
        print(f'Error copying profile.  If you\'ve already copied this profile, rename the copy before trying again.\n'
              f'{new_profile}')


def fp_delete(feature_profiles):
    # Lists all feature profiles and dependencies and provides the option to delete unused profiles

    delete_choice = input('Do you want the option to selectively delete unused profiles: yes or [no]: ')
    unused_profiles = []
    print('\nFEATURE PROFILES IN USE:')
    for profile in feature_profiles:
        groups = config_groups.feature_profile_attached(profile['profileId'])
        if not groups:
            unused_profiles.append(profile)
        else:
            print(f'\nFeature profile {profile["profileId"]}: {profile["profileType"]:20} - {profile["profileName"]}\n'
                  f'  is attached to these {len(groups)} config groups.')
            for group in groups:
                print(f'    {group["id"]}: {group["name"]}')
    for profile in unused_profiles:
        print(f'\nFeature profile {profile["profileId"]}: {profile["profileType"]:20} - {profile["profileName"]}\n'
              f'  is attached to no config groups.')
        if profile['profileType'] in ['topology']:
            print('    Cannot delete this profile type: skipped')
        else:
            if delete_choice == 'yes':
                choice = input('    Delete? yes or [no]: ').lower() or 'no'
            else:
                choice = 'no'
            if choice == 'yes':
                result = config_groups.feature_profile_delete(profile['profileId'])
                print(f'    Result: {result}')
            else:
                print('    Result: Skipped')
    print('\nEnd of list.\n\n')


def fp_sort():

    for k in config_groups.feature_profiles[0].keys():
        print(k)
    sort_key = input('What field do you want to sort with: ')

    return config_groups.feature_profiles_sort(sort_key)


def config_unlock(vmanage_conn: VmanageRestApi, uuid: str):

    url = f'/system/device/vedges?uuid={uuid}'
    dev_detail = vmanage_conn.get_request(url)
    sys_ip = dev_detail['data'][0]['configuredSystemIP']
    url = f'/system/device/{urllib.parse.quote(uuid, safe="")}/unlock'
    payload = {
        "deviceType": "vedge",
        "devices": [
            {"deviceId": uuid,
             "deviceIP": sys_ip}
                    ]
    }
    result = vmanage_conn.post_request(url, payload)

    return result

if __name__ == '__main__':

    from env_settings import *

    vmanage = VmanageRestApi(vmanage_ip, vmanage_user, vmanage_password)
    if vmanage.token:
        print('\nvManage Login Success')
    else:
        print('\nvManage Login Failure\n')
        exit()

    menu = '\n1. Copy Feature Profile\n' \
           '2. List Feature Profile dependencies with option to delete unused Feature Profiles\n' \
           '3. Sort Feature Profiles by key\n' \
           '4. Config Unlock\n' \
           '5. Exit\n\n' \
           'Which operation do you want to do: '
    config_groups = ConfigGroups(vmanage)
    while True:
        try:
            menu_choice = int(input(menu))
        except ValueError:
            menu_choice = 0
            continue
        if menu_choice == 1:
            fp_copy(config_groups.feature_profiles)
            config_groups = ConfigGroups(vmanage)
        if menu_choice == 2:
            fp_delete(config_groups.feature_profiles)
            config_groups = ConfigGroups(vmanage)
        if menu_choice == 3:
            fp_sort()
        if menu_choice == 4:
            config_unlock(vmanage, input('\nEnter device UUID: '))
        if menu_choice == 5:
            vmanage.logout()
            exit()
