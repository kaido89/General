from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES
import os
import csv
import datetime


def main():
    ldap_server = input('LDAP SERVER url (eg. example.com): ')
    # it should be the ldap_server
    server = Server(ldap_server, get_info=ALL)
    # it should have the login user
    ldap_user = input('LDAP USER (eg. KAIDO89): ')
    # it should have the user password
    ldap_pass = input('LDAP PASSWORD (eg. KAIDO89_PASSWORD): ')
    # it should have the company forest
    forest = input('LDAP FOREST (eg. COMPANY_NAME): ')
    conn = Connection(server, user=forest+"\\"+ldap_user, password=ldap_pass, auto_bind=True)
    search_user = input('SEARCH USER in LDAP (eg. KAIDO89_FRIEND): ')
    search_user_result = conn.search('dc='+str(forest).lower()+',dc=com',
                                     '(&(objectclass=person)(mailNickname=' + search_user + '))',
                                     attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
    # confirmed search run correctly
    if search_user_result:
        print(conn.entries)
    # if did not found anything
    else:
        print('Did not found this user')
    conn.unbind()


main()
