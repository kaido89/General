#!/usr/bin/env python3
import subprocess
from time import sleep


def verify_search_done(api_key, splunk_server, username, app_name, sid, flag_query_is_done, timer):
    queried_done = subprocess.check_output('curl -k -H \"Authorization: Splunk '+api_key+'\" '+splunk_server
                                           + 'servicesNS/'+username+'/'+app_name+'/search/jobs/'+sid, shell=True,
                                           universal_newlines=True)
    # wait 3 minutes to see if the query is done
    sleep_time = 180
    if queried_done.split('<s:key name="isDone">')[1].split('</s:key>')[0] == "1":
        flag_query_is_done = True
        return flag_query_is_done
    else:
        if timer == 0:
            return flag_query_is_done
        elif timer > 0:
            sleep(sleep_time)
            timer -= 1
            verify_search_done(api_key, splunk_server, username, app_name, sid, flag_query_is_done, timer)


def search_query(api_key, splunk_server, username, app_name, search_term, time_range):
    search_result = subprocess.check_output('curl -k -H \"Authorization: Splunk ' + api_key + '\" ' + splunk_server
                                            + '/servicesNS/'+username+'/'+app_name+'/search/jobs -d search=\"search '
                                            'index=' + search_term + '\" -d output_mode=csv -d \"earliest_time='
                                            + time_range + '\" -d \"latest=rt\"', shell=True, universal_newlines=True)
    return search_result


def get_api_key(splunk_server, username, password):
    result = subprocess.check_output('curl -k '+splunk_server+'/services/auth/login --data-urlencode username='
                                     + username+' --data-urlencode password='+password, shell=True,
                                     universal_newlines=True)
    api_key = str(result).split('<sessionKey>')[1].split('</sessionKey>')[0]
    return api_key


def get_input():
    splunk_server = input('Splunk server (eg. httos://splunk_server_name): ')
    username = input('Splunk username (eg. kaido89): ')
    password = input('Splunk password (eg. kaido89_pass): ')
    app_name = input('Splunk App_name (eg. example_prod): ')
    search_term = input('Splunk search term (eg. log=/user/var): ')
    return splunk_server, username, password, app_name, search_term


def main():
    splunk_server, username, password, app_name, search_term = get_input()
    api_key = get_api_key(splunk_server, username, password)
    # time range of search
    time_range = '-1d'
    search_results = search_query(api_key, splunk_server, username, app_name, search_term, time_range)
    sid = str(search_results).split('<sid>')[1].split('</sid>')[0]
    flag_query_is_done = False
    timer = 5
    search_done = verify_search_done(api_key, splunk_server, username, app_name, sid, flag_query_is_done, timer)
    if search_done:
        output_aux = subprocess.check_output('curl -k -H \"Authorization: Splunk ' + api_key + '\" '+splunk_server
                                             + '/servicesNS/'+username+'/'+ app_name+'/search/jobs/' + sid
                                             + '/results --get -d output_mode=csv -d count=0', shell=True,
                                             universal_newlines=True)
        output = output_aux.split('\n')
        print(output)
    else:
        print('Could not find a search')


main()
