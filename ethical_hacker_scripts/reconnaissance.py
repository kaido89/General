import subprocess
import requests


def main():
    website = input('Write website (eg. site.com): ')
    print('\n########################################################## whosis '
          '##########################################################\n')
    subprocess.run(['whois', website])
    print('\n########################################################## END '
          '##########################################################\n')
    print('\n########################################################## A Record '
          '##########################################################\n')
    a_record = subprocess.getoutput('host -t a ' + website)
    a_record_value = str(a_record).split('has address ')[1].split('\n')[0]
    print(a_record)
    print('\n########################################################## END '
          '##########################################################\n')
    print('\n########################################################## MX Record '
          '##########################################################\n')
    subprocess.run(['host', '-t', 'mx', website])
    print('\n##########################################################    END    '
          '##########################################################\n')
    print('\n########################################################## ARP Domain '
          '##########################################################\n')
    subprocess.run(['host', a_record_value])
    print('\n##########################################################    END    '
          '##########################################################\n')
    print('\n########################################################## Geo Location '
          '##########################################################\n')
    geolocation = requests.get('http://ip-api.com/json/'+a_record_value)
    print(geolocation.json())
    print('\n##########################################################    END    '
          '##########################################################\n')
    print('Please visit https://toolbar.netcraft.com/site_report?url=http://www.'+website+' or '\
          'https://toolbar.netcraft.com/site_report?url=https://www.'+website)
    print('Please visit https://www.exploit-db.com/google-hacking-database')
    print('Please search in google site:'+website)


main()
