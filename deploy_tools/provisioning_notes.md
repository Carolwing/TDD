Provisioning a new site
=======================

## Required packages:

* nginx
* python 3.6
* Virtualenv + pip
* Git


eg, on Ubuntu:

	sudo add-apt-repository ppa:fkrull/deadsnakes
	sudo apt-get install nginx git python3.6 python3.6-venv


## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.my-domain.com

## Folder structure:
Assume wo have a user account at /home/username

/home/username
|____ sites
	|____ SITENAME
		|____ database
		|____ source
		|____ static
		|____ virtualenv