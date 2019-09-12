import paramiko
import os
import subprocess

def lambda_handler(event, context):
    private_key = 'GET_PRIVATE_RSA'
    csv_path = os.path.expanduser('/tmp/')
    private_key = open(csv_path + 'new_private_key', 'w')
    private_key.write(value_string)
    private_key.close()
    paramiko_key = paramiko.RSAKey.from_private_key_file('/tmp/new_private_key')
    paramiko_client = paramiko.SSHClient()
    paramiko_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko_client.connect(hostname='GET_HOST', username='GET_USER', pkey=paramiko_key)
    # Execute command
    paramiko_client.exec_command(“ls”)
    # Transfer file
    paramiko_client.open_sftp()
    ftp_client.get('PATH_TO_REMOTE_FILE','PATH_TO_LOCAL_FILE')
    paramiko_client.close()
    subprocess.check_output('rm -rf /tmp/new_private_key', stderr=subprocess.STDOUT, shell=True)
