# ######## User Parameters - Set the following variables for your environment #########
import dotenv
from cryptography.fernet import Fernet
import os
from getpass import getpass
from pathlib import Path

setting_key = b'dUxSOp1SDOKvfUt7oGNpQcMFgehFFJoVXWTHngyq1f8='
basedir = Path(os.path.abspath(__file__)).parent
configdir = basedir


def get_setting(variable, prompt, secret):
    # Get environment variable or prompt user
    dotenv.load_dotenv(configdir / '.env')
    try:
        response = os.environ[variable]
        if secret:
            print(f'{variable} = *******')
            response = Fernet(setting_key).decrypt((response.encode('ascii'))).decode('ascii')
        else:
            print(f'{variable} = {response}')
    except KeyError:
        if secret:
            response = getpass(prompt)
            dotenv.set_key(configdir / '.env', variable,
                           Fernet(setting_key).encrypt(bytes(response, 'ascii')).decode('ascii'))
        else:
            response = input(prompt)
            dotenv.set_key(configdir / '.env', variable, response)
    return response


vmanage_ip = get_setting('VMANAGE_IP1', 'Input address of SDWAN Manager: ', False)
vmanage_user = get_setting('VMANAGE_USER', 'Input admin username: ', False)
vmanage_password = get_setting('VMANAGE_PASSWORD', 'Input admin password: ', True)

if input('Type "reset" to clear the settings, or anything else to proceed: ') == 'reset':
    os.remove(configdir / '.env')
    print('Settings cleared.  Restart script to proceed.')
    exit()
