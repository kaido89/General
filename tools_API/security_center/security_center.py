#!/usr/bin/env python3
import requests
import os
import csv
import zipfile
import xml.etree.ElementTree as Element_Tree
import json
from datetime import datetime
today = str(datetime.now().date())


# This method will parse the data from /output/*.nessus and create EC2 Report
def parse_vulnerability_report_data(data_path, output_path):
    # create the file vulnerability report
    report = open(output_path+'sc_vulnerability_report_'+today+'.csv', 'w')
    # transform to csv file
    report_csv_writer = csv.writer(report)
    # write the header of csv
    report_csv_writer.writerow(['Report Name', 'Host Scan End', 'Credentialed Scan', 'Host Name', 'Port',\
                                'SVC Name', 'Plugin ID', 'Plugin Name', 'Plugin Family', 'Description',\
                                'Plugin Type', 'Risk Factor', 'Solution', 'Synopsis', 'Fname'])
    print('Parsing data to Vulnerability Report ...', end='')
    # find files in output/scans/
    files_name = os.listdir(data_path)
    # iterate the list of files in output/scans/
    for nessus_file in files_name:
        # if it is .nessus file it continues
        if ".nessus" in nessus_file:
            # start reading the file
            file = open(data_path + nessus_file, 'r')
            # create a xml parsing module xml.etree.ElementTree
            tree = Element_Tree.parse(file)
            # enter the root directory of xml
            root = tree.getroot()
            # enter subtree Report
            for child in root.iter('Report'):
                report_name = child.attrib['name']
            # enter subtree ReportHost
            for child in root.iter('ReportHost'):
                host_name = child.attrib['name']
                for child2 in child.findall('HostProperties/tag'):
                    if child2.attrib['name'] == "HOST_END":
                        host_scan_end = str(child2.text)
                    if child2.attrib['name'] == "Credentialed_Scan":
                        credentialed_scan = str(child2.text)
                for child2 in child.findall('ReportItem'):
                    description = plugin_type = risk_factor = solution = synopsis = "None"
                    port = '"' + child2.attrib['port'] + '"'
                    svc_name = '"' + child2.attrib['svc_name'] + '"'
                    plugin_id = child2.attrib['pluginID']
                    plugin_name = '"' + child2.attrib['pluginName'] + '"'
                    plugin_family = '"' + child2.attrib['pluginFamily'] + '"'
                    for child3 in child2.iter('description'):
                        description = '"' + child3.text.replace("\n", "|") + '"'
                    for child3 in child2.iter('plugin_type'):
                        plugin_type = '"' + child3.text + '"'
                    for child3 in child2.iter('risk_factor'):
                        risk_factor = '"' + child3.text + '"'
                    for child3 in child2.iter('solution'):
                        solution = '"' + child3.text.replace("\n", "|") + '"'
                    for child3 in child2.iter('synopsis'):
                        synopsis = '"' + child3.text + '"'
                    for child3 in child2.iter('fname'):
                        fname = '"' + child3.text + '"'
                    # write the data to csv file
                    report_csv_writer.writerow([report_name, host_scan_end, credentialed_scan, host_name, port,
                                                svc_name, plugin_id, plugin_name, plugin_family, description,
                                                plugin_type, risk_factor, solution, synopsis, fname])
    report.close()
    print('Finished')
    return


# parse the data from data center
def parse_ec2_report_data(data_path, output_path):
    print('Parsing data to EC2 Report ... ', end='')
    # create ec2 report csv
    ec2_report = open(output_path+'sc_ec2_report_'+today+'.csv', 'w')
    # transform the file in csv format
    host_csv_writer = csv.writer(ec2_report)
    # write the header in csv file
    host_csv_writer.writerow(['Report Name', 'VPC ID', 'EC2 Instance ID', 'Host IP', 'AWS Instance AMI ID', 'Hostname',
                              'AWS Instance Hostname', 'Host FQDN', 'MAC Address', 'SSH Auth Method', 'Host Start',
                              'Host End', 'Policy Used', 'Operating System', 'CPE', 'CPE 0', 'CPE 1', 'CPE 2', 'CPE 3',
                              'CPE 4', 'System Type', 'Last Authenticated Results', 'Last Unauthenticated Results',
                              'SSH Login Used', 'Credentialed Scan', 'SSH Fingerprint'])
    # find files in output/scans/
    files_name = os.listdir(data_path)
    # iterate the list of files in output/scans/
    for file_in_name in files_name:
        # if it is .nessus file it continues
        if ".nessus" in file_in_name:
            # start reading the file
            file = open(data_path + file_in_name, 'r')
            # create a xml parsing module xml.etree.ElementTree
            tree = Element_Tree.parse(file)
            # enter the root directory of xml
            root = tree.getroot()
            # enter subtree Report
            for child in root.iter('Report'):
                report_name = child.attrib['name']
            # enter subtree Host Properties
            for host_properties in root.iter('HostProperties'):
                host_ip = aws_instance_ami_id = hostname = aws_instance_hostname = host_fqdn = mac_address = \
                    ssh_auth_method = host_start = host_end = policy_used = cpe = cpe_0 = cpe_1 = cpe_2 = cpe_3 = \
                    cpe_4 = osx = system_type = last_auth_results = last_unauth_results = ssh_login_used = \
                    credentialed_scan = ssh_fingerprint = aws_instance_id = aws_vpc_id = ""
                for child in host_properties:
                    name = child.attrib['name']
                    value = child.text
                    if name == 'host-ip':
                        host_ip = str(value)
                    if name == 'aws-instance-ami-id':
                        aws_instance_ami_id = str(value)
                    if name == 'aws-instance-instance-id':
                        aws_instance_id = str(value)
                    if name == 'aws-instance-vpc-id':
                        aws_vpc_id = str(value)
                    if name == 'hostname':
                        hostname = str(value)
                    if name == 'aws-instance-hostname':
                        aws_instance_hostname = str(value)
                    if name == 'host-fqdn':
                        host_fqdn = str(value)
                    if name == 'mac-address':
                        mac_address = str(value).replace('\n', ' + ')
                    if name == 'ssh-auth-meth':
                        ssh_auth_method = str(value)
                    if name == 'HOST_START':
                        host_start = str(value)
                    if name == 'HOST_END':
                        host_end = str(value)
                    if name == 'policy-used':
                        policy_used = str(value)
                    if name == 'os':
                        osx = str(value)
                    if name == 'cpe':
                        cpe = str(value)
                    if name == 'cpe-0':
                        cpe_0 = str(value)
                    if name == 'cpe-1':
                        cpe_1 = str(value)
                    if name == 'cpe-2':
                        cpe_2 = str(value)
                    if name == 'cpe-3':
                        cpe_3 = str(value)
                    if name == 'cpe-4':
                        cpe_4 = str(value)
                    if name == 'system-type':
                        system_type = str(value)
                    if name == 'LastAuthenticatedResults':
                        last_auth_results = str(value)
                    if name == 'LastUnauthenticatedResults':
                        last_unauth_results = str(value)
                    if name == 'ssh-login-used':
                        ssh_login_used = str(value)
                    if name == 'Credentialed_Scan':
                        credentialed_scan = str(value)
                    if name == 'ssh-fingerprint':
                        ssh_fingerprint = str(value)
                host_csv_writer.writerow([report_name, aws_vpc_id, aws_instance_id, host_ip,  aws_instance_ami_id,
                                          hostname, aws_instance_hostname, host_fqdn, mac_address, ssh_auth_method,
                                          host_start, host_end, policy_used, osx, cpe, cpe_0, cpe_1, cpe_2, cpe_3,
                                          cpe_4, system_type, last_auth_results, last_unauth_results, ssh_login_used,
                                          credentialed_scan, ssh_fingerprint])
    ec2_report.close()
    print('Finished')
    return


# extract scan list results
def extract_scan_list(path):
    for file in os.listdir(path):
        if ".zip" in file:
            print('Extracting '+file+" ...")
            try:
                zip_file = zipfile.ZipFile(path+file, 'r')
                zip_file.extractall(path)
                zip_file.close()
                os.remove(path + file)
            except Exception as ex:
                print(ex)
                continue
    return


# transfer scan list results
def get_scan_list(header, company_url, session, fetch_list, data_path):
    # run all the ids that contains "Term" and download the data
    for index in fetch_list:
        value = session.post(company_url + "/rest/scanResult/" + index + "/download", headers=header,
                             allow_redirects=True)
        print("Downloading: "+index+".zip ....")
        open(data_path + index + '.zip', 'wb').write(value.content)
    return


# search the query with title Term
def set_csv_and_fetch_file(json_data, nessus_vulnerability_name):
    print("Creating fetch.csv and sc_data.csv ... ")
    fetch_list = []
    # create scan folder in case it is not present
    if not os.path.exists(os.path.expanduser('~/output/')):
        os.makedirs(os.path.expanduser('~/output/'))
    if not os.path.exists(os.path.expanduser('~/output/security_center')):
        os.makedirs(os.path.expanduser('~/output/security_center'))
    if not os.path.exists(os.path.expanduser('~/output/security_center/scans/')):
        os.makedirs(os.path.expanduser('~/output/security_center/scans/'))
        # define the parameter you want to receive
    for response in json_data.json()['response']['usable']:
        if nessus_vulnerability_name in response['name'].upper():
            fetch_list.append(response['id'])
    return fetch_list


# make login api call return token and post data
def get_api_token(session, company_url, username, password):
    payload = {"username": username, "password": password}
    post_data = session.post(company_url + "/rest/token", data=json.dumps(payload))
    try:
        token = post_data.json()['response']['token']
    except Exception as ex:
        print(ex)
    return str(token)


def main():
    # read the conf file and return company_url, username, password
    company_url = input('company security center url (eg. example.com): ')
    username = input('Nessus username (eg. kaido89): ')
    password = input('Nessus password (eg. kaido89_pass): ')
    nessus_vulnerability_name = input('Nessus vulnerability name (eg. PROD): ')
    # create a session for sc api
    session = requests.Session()
    # call a method to get token
    token = get_api_token(session, company_url, username, password)
    header = {'X-SecurityCenter': token, 'Content-Type': 'application/json'}
    fields = "name,ownerGroup,repository,details,startTime,finishTime"
    json_data = session.get(company_url+"/rest/scanResult?fields="+fields, headers=header)
    # build csv file and fetch_file
    fetch_list = set_csv_and_fetch_file(json_data, nessus_vulnerability_name)
    download_path = os.path.expanduser('~/output/security_center/scans/')
    output_path = os.path.expanduser('~/output/security_center/')
    get_scan_list(header, company_url, session, fetch_list, download_path)
    # extract scan list
    extract_scan_list(download_path)
    # parse data from scan list to get ec2 host data
    parse_ec2_report_data(download_path, output_path)
    # parse data from scan list to get vulnerability data
    parse_vulnerability_report_data(download_path, output_path)


main()
