from vmanage_api import VmanageRestApi


class ConfigGroups:

    def __init__(self, vmanage: VmanageRestApi):
        self.vmanage = vmanage
        self.config_groups = vmanage.get_request('/v1/config-group')
        self.feature_profiles = vmanage.get_request('/v1/feature-profile/sdwan/')

    def feature_profile_detail(self, profile_id: str) -> dict:
        # Returns the full detail of a feature profile

        for profile in self.feature_profiles:
            if profile['profileId'] == profile_id:
                break
        detail = self.vmanage.get_request(f'/v1/feature-profile/sdwan/{profile["profileType"]}/{profile_id}')

        return detail

    def feature_profile_copy(self, profile_id: str, new_name: str, description: str) -> dict:
        # Copies a feature profile

        detail = self.feature_profile_detail(profile_id)
        payload = {
            "name": f"{new_name}",
            "description": f"{description}",
            "fromFeatureProfile": {
                "copy": profile_id
            }
        }

        new_profile = self.vmanage.post_request(f'/v1/feature-profile/sdwan/{detail["profileType"]}',
                                                payload=payload)

        return new_profile

    def feature_profile_attached(self, profile_id: str) -> list:
        # Returns a list of config groups that feature profile is attached to

        groups = []
        for config_group in self.config_groups:
            for profile in config_group['profiles']:
                if profile['id'] == profile_id:
                    groups.append({'id': config_group['id'], 'name': config_group['name']})
                    continue

        return groups

    def feature_profile_delete(self, profile_id):
        # Delete a feature profile

        detail = self.feature_profile_detail(profile_id)
        result = self.vmanage.delete_request(f'/v1/feature-profile/sdwan/{detail["profileType"]}/{profile_id}')

        return result

    def feature_profiles_sort(self, sort_key):

        fp_sorted = sorted(self.feature_profiles, key=lambda x: x[sort_key])
        self.feature_profiles = fp_sorted

        return fp_sorted
    