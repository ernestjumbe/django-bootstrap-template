import os
import logging
#logging.basicConfig(level=logging.DEBUG)
#from fabric.api import env
from cuisine import *
from fabric.context_managers import cd, prefix
from fabric.api import env, run, sudo, put, local


env.use_ssh_config = True
#env.ssh_config_path = '~/.ssh/config'
env.hosts = ['']
env.disable_known_hosts = True

ROOT_PATH = os.path.dirname(__file__)

REMOTE_PROJECT_PATH = '/opt/' + {{project_name}} +'env'

tmp_dir = REMOTE_PROJECT_PATH + "/tmp"

PROJECT_NAME = {{project_name}}


venv = 'source ' + REMOTE_PROJECT_PATH +'/bin/activate'

def _install_deps():
	with cd(REMOTE_PROJECT_PATH + {{project_name}}), prefix(venv):
		sudo("pip install -r requirements.txt")

def restart():
	with cd(REMOTE_PROJECT_PATH + '/' + PROJECT_NAME), prefix(venv):
		sudo("supervisorctl restart gunicorn")
		sudo("service nginx restart")

def _djangoManage(command):
	with cd(REMOTE_PROJECT_PATH +'/' + PROJECT_NAME), prefix(venv):
		sudo("./manage.py %s --settings=" + PROJECT_NAME + ".settings.prod" % command)

def _get_code():
	local("git pull")

def _migrate():
	_djangoManage("makemigrations")
	_djangoManage("migrate")

def backup():
	local('pip freeze > requirements.txt')
	local('git pull')
	local('git add -A')
	print("Enter your commit message:")
	comment = raw_input()
	local('git commit -m "%s"' % comment)

	local('git push')

def csu():
	_djangoManage("createsuperuser")

def testgunicorn():
	with cd(REMOTE_PROJECT_PATH +'/' + PROJECT_NAME):
		sudo(REMOTE_PROJECT_PATH +'/bin/gunicorn -c '+ REMOTE_PROJECT_PATH +'/gunicorn_config.py '+ PROJECT_NAME +'.wsgi:application')

def _pack():
	with cd(ROOT_PATH):
		if not file_exists('latest.zip'):
			local('rm latest.zip')

	local('git archive --format zip -o latest.zip HEAD')

def _install_gunicorn():
	with cd(REMOTE_PROJECT_PATH + '/' + PROJECT_NAME), prefix(venv):
		sudo("pip install gunicorn")

def _collectstatic():
	_djangoManage("collectstatic --noinput")


def _gunicorn():
	put('setup/dev_gunicorn_config.py', REMOTE_PROJECT_PATH + '/tmp')
	with cd(REMOTE_PROJECT_PATH):
		sudo('cp tmp/dev_gunicorn_config.py gunicorn_config.py')

def _supa_gunicorn():
	put('setup/dev_gunicorn.conf', REMOTE_PROJECT_PATH + '/tmp')
	with cd(REMOTE_PROJECT_PATH):
		sudo('cp tmp/dev_gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf')
		sudo('supervisorctl reread')
		sudo('supervisorctl update')

def _rmTemp():
	with cd(REMOTE_PROJECT_PATH):
		sudo('rm -rf tmp/')


def deploy():
	#backup()
	_pack()

	if not dir_exists(REMOTE_PROJECT_PATH):
		sudo('virtualenv --no-site-packages /opt/drbenv')

	with cd('/opt/drbenv'):
		run('mkdir -Rf ' + PROJECT_NAME)
		run('mkdir -Rf tmp')
	
	put('latest.zip', REMOTE_PROJECT_PATH + '/' + PROJECT_NAME)

	with cd(REMOTE_PROJECT_PATH + '/' +PROJECT_NAME):
		sudo('unzip latest.zip')
		sudo('rm latest.zip')

	sudo('mkdir -Rf /var/www/'+ PROJECT_NAME +'/static')
	sudo('mkdir -Rf /var/www/'+ PROJECT_NAME +'/media')

	_install_deps()
	_migrate()
	_install_gunicorn()
	_gunicorn()
	_supa_gunicorn()
	_rmTemp()
	_collectstatic()
	restart()

def pdeploy():
	#backup()
	_pack()
	sudo('rm -rf ' + REMOTE_PROJECT_PATH + '/' +PROJECT_NAME + '/*')
	put('latest.zip', REMOTE_PROJECT_PATH + '/' +PROJECT_NAME)

	with cd(REMOTE_PROJECT_PATH + '/' +PROJECT_NAME):
		sudo('unzip latest.zip')
		sudo('rm -Rf latest.zip')

	_install_deps()
	_migrate()
	_collectstatic()
	restart()

def cleanup():
	sudo('rm -rf ' + REMOTE_PROJECT_PATH)
	sudo('rm -rf /etc/supervisor/conf.d/gunicorn.conf')
	sudo('rm -rf '+ REMOTE_PROJECT_PATH +'/gunicorn_config.py')
	#_rmTemp()

def remote_uname():
	sudo('uname -a')

def tpath():
	print ROOT_PATH


