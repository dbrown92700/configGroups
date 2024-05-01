#!python

from vmanage_api import VmanageRestApi
from vmanage_ux2 import ConfigGroups, FeatureProfiles, TopologyGroup, PolicyGroup
import urllib.parse


def fp_copy():
    # Lists current feature profiles and prompts user to copy one

    fp = FeatureProfiles(vmanage)
    profiles = [x for x in fp.profiles if x['profileType'] in fp.cg_profile_types]
    profiles = sorted(profiles, key=lambda x: x['profileType'])
    for num, profile in enumerate(profiles):
        print(f'{(num + 1):3}: {profile["profileType"]:20}   {profile["profileName"]}')
    while True:
        try:
            choice = int(input('\nWhich profile do you want to copy: '))
            break
        except ValueError:
            continue
    new_name = input(f'Name for new profile [{profiles[choice-1]["profileName"]}_COPY]: ') or \
               f'{profiles[choice-1]["profileName"]}_COPY'
    description = input(f'Description for profile [Copy of {profiles[choice-1]["profileName"]}]: ') or \
                  f"Copy of {profiles[choice-1]['profileName']}"
    new_profile = fp.duplicate(profiles[choice - 1]['profileId'], new_name, description)
    try:
        print(f'Success creating new profile, {new_profile["id"]}')
    except KeyError:
        print(f'Error copying profile.  If you\'ve already copied this profile, rename the copy before trying again.\n'
              f'{new_profile}')


def fp_delete():
    # Lists all feature profiles and dependencies and provides the option to delete unused profiles

    fp = FeatureProfiles(vmanage)
    delete_choice = input('Do you want the option to selectively delete unused profiles: yes or [no]: ')
    choice = 'no'
    while True:
        try:
            key_choice = int(input('Sort by:\n 1) Name\n 2) Type\n? '))
            if key_choice in [1, 2]:
                break
        except ValueError:
            print('Choose 1 or 2.')
    fp.sort({1: 'profileName', 2: 'profileType'}[key_choice])
    unused_profiles = []
    print('\n\nFEATURE PROFILES IN USE:\n')
    for profile in fp.profiles:
        groups = fp.is_part_of(profile['profileId'])
        if not groups:
            unused_profiles.append(profile)
        else:
            print(f'\nFeature profile {profile["profileId"]}: {profile["profileType"]:20} - {profile["profileName"]}\n'
                  f'  is attached to these {len(groups)} objects.')
            for group in groups:
                print(f'    {group["id"]}: {group["name"]}')
    print('\n\nFEATURE PROFILES NOT USED:\n')
    for profile in unused_profiles:
        print(f'\nFeature profile {profile["profileId"]}: {profile["profileType"]:20} - {profile["profileName"]}')
        if delete_choice == 'yes':
            choice = input('    Delete unused profile? yes or [no]: ').lower() or 'no'
        if choice == 'yes':
            result = fp.delete(profile['profileId'])
            print(f'    Result: {result}')
    print('\nEnd of list.\n\n')


def config_unlock(uuid: str):

    url = f'/system/device/vedges?uuid={uuid}'
    dev_detail = vmanage.get_request(url)
    sys_ip = dev_detail['data'][0]['configuredSystemIP']
    url = f'/system/device/{urllib.parse.quote(uuid, safe="")}/unlock'
    payload = {
        "deviceType": "vedge",
        "devices": [
            {"deviceId": uuid,
             "deviceIP": sys_ip}
                    ]
    }
    result = vmanage.post_request(url, payload)

    return result


def topo_copy():

    groups = TopologyGroup(vmanage)
    for num, topology in enumerate(groups.topologies):
        print(f'{num+1}: {topology["name"]}')
    choice = input('Which topology group do you want to duplicate: ')
    top_id = groups.topologies[int(choice)-1]['id']
    result = groups.duplicate(top_id)
    print(result)


def topo_delete():

    groups = TopologyGroup(vmanage)
    for num, topology in enumerate(groups.topologies):
        print(f'{num+1}: {topology["name"]}')
    choice = input('Which topology group do you want to delete: ')
    top_id = groups.topologies[int(choice)-1]['id']
    result = groups.delete(top_id)
    print(result)


def policy_dup(policy_type: str):

    profiles = []
    fp = FeatureProfiles(vmanage)
    for profile in fp.profiles:
        if profile['profileType'] == policy_type:
            profiles.append(profile)
    for num, profile in enumerate(profiles):
        print(f'{num+1}: {profile["profileName"]}')
    choice = input(f'Which {policy_type} feature profile do you want to duplicate: ')
    profile_id = profiles[int(choice)-1]['profileId']
    result = fp.duplicate(profile_id)
    print(result)


def clear_task():

    url = '/device/action/status/tasks'
    tasks = vmanage.get_request(url)
    for num, task in tasks['runningTasks']:
        print(f'{num+1}: {task["processId"]}')
    task_choice = input('Which task do you want to terminate: ')
    process_id = tasks['runningTasks'][int(task_choice-1)]['processId']
    url = f'/device/action/status/tasks/clean?processId={process_id}'
    response = vmanage.get_request(url)
    print(response)


if __name__ == '__main__':

    from env_settings import *

    vmanage = VmanageRestApi(vmanage_ip, vmanage_user, vmanage_password)
    if vmanage.token:
        print('\nvManage Login Success')
    else:
        print('\nvManage Login Failure\n')
        exit()

    menu = '\n' \
           '1. Feature Profile: Duplicate\n' \
           '2. Feature Profile: List dependencies with option to delete unused\n' \
           '3. Topology Group: Duplicate\n' \
           '4. Topology Group: Delete\n' \
           '5. Policy Group: Duplicate a policy element (Application Priority & SLA Policy,\n' \
           '                 Embedded Security, SIG/SASE, or DNS Security)\n' \
           '6. Config Unlock\n' \
           '7. Clear a stuck Task\n' \
           '8. Exit\n\n' \
           'Which operation do you want to do: '
    config_groups = ConfigGroups(vmanage)
    while True:
        try:
            menu_choice = int(input(menu))
        except ValueError:
            menu_choice = 0
            continue
        if menu_choice == 1:
            fp_copy()
        if menu_choice == 2:
            fp_delete()
        if menu_choice == 3:
            topo_copy()
        if menu_choice == 4:
            topo_delete()
        if menu_choice == 5:
            policy_choice = input('1. App Priority & SLA\n'
                                  '2. Embedded Security\n'
                                  '3. SIG / SASE\n'
                                  '4. DNS Security\n'
                                  'Which policy element do you want to duplicate? ')
            pol_type = ['application-priority', 'embedded-security', 'sig-security',
                        'dns-security'][int(policy_choice)-1]
            policy_dup(pol_type)
        if menu_choice == 6:
            config_unlock(input('\nEnter device UUID: '))
        if menu_choice == 7:
            clear_task()
        if menu_choice == 8:
            vmanage.logout()
            exit()
