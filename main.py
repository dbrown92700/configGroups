#!python

from vmanage_api import VmanageRestApi
from config_groups import ConfigGroups
from env_settings import *


def fp_copy(feature_profiles):
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
    for profile in feature_profiles:
        groups = config_groups.feature_profile_attached(profile['profileId'])
        if not groups:
            print(f'Feature profile {profile["profileId"]}: {profile["profileType"]:20} - {profile["profileName"]} '
                  f'is attached to no config groups.')
            if profile['profileType'] in ['topology']:
                print('    Cannot delete this profile type: skipped')
            else:
                choice = input('    Delete? yes or [no]: ').lower() or 'no'
                if choice == 'yes':
                    result = config_groups.feature_profile_delete(profile['profileId'])
                    print(f'    Result: {result}')
                else:
                    print('    Result: Skipped')
        else:
            print(f'Feature profile {profile["profileId"]}: {profile["profileType"]:20} - {profile["profileName"]} '
                  f'is attached to these {len(groups)} config groups.')
            for group in groups:
                print(f'    {group["id"]}: {group["name"]}')
    print('End of list.\n\n')

if __name__ == '__main__':

    vmanage = VmanageRestApi(vmanage_ip, vmanage_user, vmanage_password)
    menu = '1. Copy Feature Profile\n' \
           '2. Delete Unused Feature Profiles\n' \
           '3. Exit\n\n' \
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
            vmanage.logout()
            exit()
