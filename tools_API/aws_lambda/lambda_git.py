import os
import subprocess
import boto3


def execute_git_push(repo_dir, new_file_name, git_commit_message, git_user, git_email):
    git_conf_username = 'config --local user.name '+git_user
    git_conf_email = 'config --local user.email '+git_email
    git_conf_add = 'add '+str(repo_dir)+str(new_file_name)
    git_conf_status = 'status'
    git_conf_commit = 'commit -m "'+git_commit_message+'"'
    git_conf_push = 'push --set-upstream origin master'
    try:
        execute_git_command(repo_dir, git_conf_username)
        execute_git_command(repo_dir, git_conf_email)
        execute_git_command(repo_dir, git_conf_add)
        execute_git_command(repo_dir, git_conf_status)
        execute_git_command(repo_dir, git_conf_commit)
        execute_git_command(repo_dir, git_conf_push)
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)


def execute_git_command(repo_dir, command):
    print(subprocess.check_output('cd '+repo_dir+' && /tmp/git/usr/bin/git '+command,
                                  stderr=subprocess.STDOUT, shell=True, encoding=None))


def create_new_file(git_dir, repo_name, new_file_name, new_file_content):
    repo_dir = os.path.expanduser(git_dir + '/' + repo_name + '/')
    new_file = open(repo_dir + new_file_name, 'w')
    new_file.write(new_file_content)
    new_file.close()
    return repo_dir


def setup_git(tmp_dir):
    aws_region = os.environ['AWS_REGION']
    rpm_package = 'git-2.14.5-1.60.amzn1.x86_64.rpm'
    git_url = 'http://packages.' + aws_region + '.amazonaws.com/2018.03/updates/e0c0ed50838c/x86_64/' + 'Packages/' \
              + rpm_package

    # # Setup Git environment
    subprocess.check_output('rm -rf ' + tmp_dir + ' && mkdir ' + tmp_dir + ' && cd ' + tmp_dir + ' && curl -s -O '
                            + git_url + ' && rpm2cpio ' + rpm_package + ' | cpio -id && rm ' + rpm_package,
                            stderr=subprocess.STDOUT, shell=True)


def get_user_pass():
    # The Git repository to clone
    ssm = boto3.client("ssm")
    password = ssm.get_parameter(Name='git_password', WithDecryption=True)['Parameter']['Value']
    username = ssm.get_parameter(Name='git_user', WithDecryption=True)['Parameter']['Value']
    return username, password


def lambda_handler(event, context):
    username, password = get_user_pass()
    git_dir = '/tmp/git'
    setup_git(git_dir)
    # CHANGE ALL THIS VALUES                            |
    repo_name = 'CHANGE_REPO_NAME'
    repo_path = '/CHANGE_TO_ORGANISATION/'
    new_file_name = 'CHANGE_NEW_FILE_NAME'
    new_file_content = 'CHANGE_NEW_FILE_NAME_CONTENT'
    git_commit_message = 'CHANGE_NEW_COMMIT_MESSAGE'
    git_user = 'CHANGE_GIT_USER'
    git_email = 'CHANGE_GIT_EMAIL'
    # CHANGE ALL THIS VALUES                            |
    remote_repository = 'https://'+username+':'+password+'@github.com'+repo_path+repo_name+'.git'
    git_clone = 'clone '+remote_repository
    os.environ['HOME'] = '/var/task GIT_TEMPLATE_DIR=' + git_dir + '/usr/share/git-core/templates'
    os.environ['GIT_EXEC_PATH'] = '/tmp/git/usr/libexec/git-core'
    execute_git_command(git_dir, git_clone)
    repo_dir = create_new_file(git_dir, repo_name, new_file_name, new_file_content)
    execute_git_push(repo_dir, new_file_name, git_commit_message, git_user, git_email)
    print(os.listdir(git_dir+'/'+repo_name))
