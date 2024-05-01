from vmanage_api import VmanageRestApi
import random


class ConfigGroups:

    def __init__(self, vmanage: VmanageRestApi):
        self.vmanage = vmanage
        self.config_groups = vmanage.get_request('/v1/config-group')


class FeatureProfiles:

    def __init__(self, vmanage: VmanageRestApi):
        self.vmanage = vmanage
        self.profiles = vmanage.get_request('/v1/feature-profile/sdwan/')
        self.cg_profile_types = ['service', 'transport', 'system', 'cli', 'other']

    def get_detail(self, profile_id: str) -> dict:
        # Returns the full detail of a feature profile

        for profile in self.profiles:
            if profile['profileId'] == profile_id:
                break
        detail = self.vmanage.get_request(f'/v1/feature-profile/sdwan/{profile["profileType"]}/{profile_id}')

        return detail

    def duplicate(self, profile_id: str, new_name='', description='') -> dict:
        # Copies a feature profile

        detail = self.get_detail(profile_id)
        payload = {
            "name": new_name or f'{detail["profileName"]}_COPY{"".join(random.choices("1234567890", k=5))}',
            "description": description or f'COPY OF {detail["description"]}',
            "fromFeatureProfile": {
                "copy": profile_id
            }
        }
        new_profile = self.vmanage.post_request(f'/v1/feature-profile/sdwan/{detail["profileType"]}',
                                                payload=payload)

        return new_profile

    def is_part_of(self, profile_id: str) -> list:
        # Returns a list of groups (config, policy, topology) that feature profile is used in

        config_groups = ConfigGroups(self.vmanage).config_groups
        topos = TopologyGroup(self.vmanage).topologies
        policy_groups = PolicyGroup(self.vmanage).policy_groups
        all_groups = config_groups + topos + policy_groups
        groups = []
        for group in all_groups:
            for profile in group['profiles']:
                if profile['id'] == profile_id:
                    groups.append({'id': group['id'], 'name': group['name']})

        return groups

    def delete(self, profile_id):
        # Delete a feature profile

        detail = self.get_detail(profile_id)
        result = self.vmanage.delete_request(f'/v1/feature-profile/sdwan/{detail["profileType"]}/{profile_id}')

        return result

    def sort(self, sort_key):

        self.profiles = sorted(self.profiles, key=lambda x: x[sort_key])


class PolicyGroup:
    # Have not found a need for this class so far
    def __init__(self, vmanage: VmanageRestApi):
        self.vmanage = vmanage
        self.policy_groups = self.vmanage.get_request('/v1/policy-group')

    def duplicate(self, topo_id: str, new_name='', new_description='') -> str:

        ## THIS FUNCTION IS NOT PARTICULARLY USEFUL...THE GUI WORKS FINE

        profiles = FeatureProfiles(self.vmanage)
        for policy in self.policy_groups:
            if policy['id'] == topo_id:
                break
        new_policy_group = {
            "name": new_name or f'{policy["name"]}_COPY{"".join(random.choices("1234567890", k=5))}',
            "description": new_description or f'COPY OF {policy["description"]}',
            "solution": "sdwan",
            "profiles": [
            ]
        }
        for fp in policy['profiles']:
            if fp['type'] == 'policy-object':
                new_policy_group['profiles'].append({'id': fp['id']})
            else:
                new_id = profiles.duplicate(fp['id'])['id']
                new_policy_group['profiles'].append({'id': new_id})
        url = '/v1/topology-group'
        new_pol_id = self.vmanage.post_request(url, new_policy_group)
        self.policy_groups = self.vmanage.get_request('/v1/policy-group')

        return new_pol_id


class TopologyGroup:

    def __init__(self, vmanage: VmanageRestApi):
        self.vmanage = vmanage
        self.topologies = self.vmanage.get_request('/v1/topology-group')

    def get_details(self, topo_fp_id: str) -> dict:

        url = f'/v1/feature-profile/sdwan/topology/{topo_fp_id}?details=true'
        topo_detail = self.vmanage.get_request(url)

        return topo_detail

    def duplicate(self, topo_id: str, new_name='', new_description='') -> str:
        # Creates a deep copy of the original topology

        profiles = FeatureProfiles(self.vmanage)
        for this_topo in self.topologies:
            if this_topo['id'] == topo_id:
                break
        new_topo = {
            "name": new_name or f'{this_topo["name"]}_COPY{"".join(random.choices("1234567890", k=5))}',
            "description": new_description or f'COPY OF {this_topo["description"]}',
            "solution": "sdwan",
            "profiles": [
            ]
        }
        for fp in this_topo['profiles']:
            if fp['type'] == 'policy-object':
                new_topo['profiles'].append({'id': fp['id']})
            else:
                new_id = profiles.duplicate(fp['id'])
                new_topo['profiles'].append(new_id)
        url = '/v1/topology-group'
        new_topo_id = self.vmanage.post_request(url, new_topo)
        self.topologies = self.vmanage.get_request('/v1/topology-group')

        return new_topo_id

    def delete(self, topo_id: str):

        profiles = FeatureProfiles(self.vmanage)
        for this_topo in self.topologies:
            if this_topo['id'] == topo_id:
                break
        url = f'/v1/topology-group/{topo_id}'
        result = self.vmanage.delete_request(url)
        for fp in this_topo['profiles']:
            if fp['type'] != 'policy-object':
                profiles.delete(fp['id'])
        self.topologies = self.vmanage.get_request('/v1/topology-group')

        return result
