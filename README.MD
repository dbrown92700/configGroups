# Overview
Set of tools for manipulating Cisco Catalyst SDWAN Manager UX2.0 Elements

Current capabilities:


1. Feature Profile: Duplicate
2. Feature Profile: List dependencies with option to delete unused
3. Topology Group: Duplicate
4. Topology Group: Delete
5. Policy Group: Duplicate a policy element (Application Priority & SLA Policy,
                 Embedded Security, SIG/SASE, or DNS Security)
6. Config Unlock
7. Clear a stuck Task

# Use

Running main.py prompts for SDWAN Manager address and credentials followed by a user menu. \
SDWAN Manager information is saved to environmental variables and password is encrypted. \
Manager, user ID, and password can also be passed as arguments.

# Install
Requires python 3.9 or later

Clone repository:
> git clone https://github.com/dbrown92700/configGroups

Recommend creating a virtual environment:
> python -m venv venv \
> source venv/bin/activate

Install python dependencies
> pip install -r requirements.txt

# Execute
> ./main.py

or

> python3 main.py

Optionally, specify credentials at runtime as follows

~~~
./main.py -h
usage: main.py [-h] [-a <vmanage-ip>] [-u <user>] [-p <password>] [--port <port>]

Collection of SDWAN tools. You can use the following options or the script will prompt you for settings and store those to environment variables.

options:
  -h, --help            show this help message and exit
  -a <vmanage-ip>, --address <vmanage-ip>
                        vManage IP address, can also be defined via VMANAGE_IP environment variable. If neither is provided user is prompted for the address.
  -u <user>, --user <user>
                        username, can also be defined via VMANAGE_USER environment variable. If neither is provided user is prompted for username.
  -p <password>, --password <password>
                        password, can also be defined via VMANAGE_PASSWORD environment variable. If neither is provided user is prompted for password.
  --port <port>         vManage port number, can also be defined via VMANAGE_PORT environment variable (default: 443)
~~~


# Author
Dave Brown, Cisco SDWAN TSA, davibrow@cisco.com

