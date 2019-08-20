import requests

def main():
    website = input('Write website to be copied (eg. https://www.site.com): ')
    print('\n########################################################## Copying website '
          '##########################################################\n')
    subprocess.run(['httrack', website])
    print('\n########################################################## END '
          '##########################################################\n')


main()
