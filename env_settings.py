# ######## User Parameters - Set the following variables for your environment #########
import dotenv
from cryptography.fernet import Fernet
import os
from getpass import getpass
from pathlib import Path
import argparse

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

help = f'Collection of SDWAN tools.\n' \
       f'You can use the following options or the script will prompt you for settings and store those\n' \
       f'to environment variables.'

cli_parser = argparse.ArgumentParser(description=help)
cli_parser.add_argument('-a', '--address', metavar='<vmanage-ip>', required=False,
                        help='vManage IP address, can also be defined via VMANAGE_IP environment variable. '
                             'If neither is provided user is prompted for the address.')
cli_parser.add_argument('-u', '--user', metavar='<user>', required=False,
                        help='username, can also be defined via VMANAGE_USER environment variable. '
                             'If neither is provided user is prompted for username.')
cli_parser.add_argument('-p', '--password', metavar='<password>', required=False,
                        help='password, can also be defined via VMANAGE_PASSWORD environment variable. '
                             ' If neither is provided user is prompted for password.')
cli_parser.add_argument('--port', metavar='<port>', default='443',
                        help='vManage port number, can also be defined via VMANAGE_PORT environment variable '
                             '(default: %(default)s)')

cli_args = cli_parser.parse_args()

print("Argument settings:\n", cli_args)

address = None
if cli_args.address:
    address = f'{cli_args.address}:{cli_args.port}'

vmanage_ip = address or get_setting('VMANAGE_IP1', 'Input address of SDWAN Manager: ', False)
vmanage_user = cli_args.user or get_setting('VMANAGE_USER', 'Input admin username: ', False)
vmanage_password = cli_args.password or get_setting('VMANAGE_PASSWORD', 'Input admin password: ', True)

if input('Type "reset" to clear the env settings, or anything else to proceed: ') == 'reset':
    os.remove(configdir / '.env')
    print('Settings cleared.  Restart script to proceed.')
    exit()
