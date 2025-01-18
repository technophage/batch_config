Cisco IOS batch configuration pusher

requires getpass and netmiko modules to be installed;

python3 -m pip install getpass
python3 -m pip install netmiko


requires two text files - 

    a hosts file with hosts you want to modify one IP per line
    a config file with the snipper you want to push out



-- example run --

<pre>
./batch_change.py

Cisco batch configurator

enter username : admin
enter password : 
configuration filename : config.txt
show config (y/n) : y
-------------------------------------------
show run

wr

-------------------------------------------
is the config correct (y/n) : y
enter host ip list filename : hosts.txt



-------------------------------------------
applying batch change as user : admin
configuration file            : config.txt
hosts file                    : hosts.txt
no. hosts                     : 3
-------------------------------------------


continue with configuration? (y/n) : y
[+] host 10.1.1.2
        [-] Connecting to SSH
        [-] Enable
        [-] Configure
        [-] OK
[+] host 10.1.1.3
        [-] Connecting to SSH
        [-] Enable
        [-] Configure
        [-] OK
[+] host 10.1.1.4
        [-] Connecting to SSH
        [*] SSH Connection error, attempting Telnet
        [-] Connecting to Telnet
        [-] Enable
        [-] Configure
        [-] OK
</pre>
        
--
