
import sys
import os
import getpass
from netmiko import ConnectHandler

'''

Cisco IOS batch configuration pusher

requires getpass and netmiko modules to be installed;

python3 -m pip install getpass
python3 -m pip install netmiko


requires two text files - 

    a hosts file with hosts you want to modify one IP per line
    a config file with the snipper you want to push out


'''

def configure_device(ip, username, password, config_file):

    # connect timeout delay
    DELAY = 3
    CONNECTED = False

    # connect
    if not CONNECTED:
        try:
            print('\t[-] Connecting to SSH')
            session = ConnectHandler(device_type = 'cisco_ios', ip = ip, username = username, password = password, global_delay_factor = DELAY)
            CONNECTED = True

        except:
            CONNECTED = False
            print('\t[*] SSH Connection error, attempting Telnet')

    
    if not CONNECTED:
        try:
            print('\t[-] Connecting to Telnet')
            session = ConnectHandler(device_type = 'cisco_ios_telnet', ip = ip, username = username, password = password, global_delay_factor = DELAY)
            CONNECTED = True

        except:
            print('\t Unable to connect, skipping host')
            return False

    # configure
    try:
        print('\t[-] Enable')
        enable = session.enable()

        print('\t[-] Configure')
        cmd = session.send_config_from_file(config_file)

        session.dc = session.disconnect()

    except:
        print('\t[*] error configuring host')
        return False

    # if we didnt error out, return complete
    return True    

print('\n\nCisco batch configurator\n')

def main():

    
    # credentials
    username = input('enter username : ')
    password = getpass.getpass('enter password : ')

    # configuration file
    config_check = False
    while not config_check:
        config_file = input('configuration filename : ')
    
        if os.path.isfile(config_file):
            try:
                resp = input('show config (y/n) : ')
                if resp.lower() == 'y':

                    cf = open(config_file, 'r')
                    config = cf.readlines()
                    cf.close()

                    print('-------------------------------------------')
                    for line in config:
                        print(line)
                    print('-------------------------------------------')
                    
                else:
                    config_check = True
                    
                if not config_check:
                    resp = input('is the config correct (y/n) : ')
                    if resp.lower() == 'y':
                        config_check = True

            except:
                print('File IO error with \'%s\'\nquitting.' % config_file)
                sys.exit()


    # hosts list
    host_file = input('enter host ip list filename : ')
    if os.path.isfile(host_file):
        try:
            hf = open(host_file, 'r')
            hosts = hf.readlines()

        except:
            print('File IO error with \'%s\'\nquitting.' % host_file)
            sys.exit()

    # display info
    print('\n\n')
    print('-------------------------------------------')
    print('applying batch change as user : %s' % username)
    print('configuration file            : %s' % config_file)
    print('hosts file                    : %s' % host_file)
    print('no. hosts                     : %i' % len(hosts))
    print('-------------------------------------------')
    print('\n')

    # continue ?
    resp = input('continue with configuration? (y/n) : ')
    if resp.lower() != 'y':
        print('quitting.')
        sys.exit()

    # run
    for host in hosts:
        ip = host.strip('\n')
        if ip:
            print('[+] host %s' % ip)
            if configure_device(ip, username, password, config_file):
                print('\t[-] OK')
                
            else:
                print('\t[*] Failed')
                
        else:
            pass

    # done!
    sys.exit()

if __name__ == '__main__':
    main()
