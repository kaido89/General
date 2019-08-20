
import requests

def main():
    file = input('Write filename to be read (eg. filename): ')
    print('\n########################################################## Copying website '
          '##########################################################\n')
    subprocess.run(['exiftool', file])
    print('\n########################################################## END '
          '##########################################################\n')


main()
