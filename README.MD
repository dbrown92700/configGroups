# Overview
Set of tools for manipulating feature profiles and config groups.

Current capabilities:
1. Copy a feature profile
2. Display and prompt to delete feature profiles that aren't being used
3. Sort feature profiles
4. Config unlock a device from a Config Group (if this doesn't work in vManage properly)

# Use

Running main.py prompts for SDWAN Manager address and credentials followed by a user menu.
SDWAN Manager information is saved to environmental variables and password is encrypted.

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

> main.py

# Author
Dave Brown, Cisco SDWAN TSA, davibrow@cisco.com

