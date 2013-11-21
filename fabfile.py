from fabric.api import run, cd, env

env.hosts = ["nickhs.com"]
env.use_ssh_config = True
env.reject_unknown_hosts = False


def deploy():
    with cd("/srv/vowel_private"):
        run("git pull")

    with cd("/srv/vowel"):
        run("git pull")

def full_deploy():
    deploy()

    with cd("/srv/vowel"):
        run("pip install -r requirements.txt")
        run("supervisorctl restart vowel")
