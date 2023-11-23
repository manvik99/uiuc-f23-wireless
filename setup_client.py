import subprocess
import os
dir = '/home/raspberrypi/mesh_networking/'
​
def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    if result.returncode == 0:
        print(f"Command executed successfully: {command}")
    else:
        print(f"Command failed: {command}")
        print(f"Error message: {result.stderr}")
​
def install_batctl():
    run_command('sudo apt-get install -y batctl')
​
def create_start_batman_adv_script():
    script_content = '''#!/bin/sh
# batman-adv interface to use
sudo ifconfig bat0 down 
sudo batctl if add wlan0
sudo ifconfig bat0 mtu 1468
​
# Tell batman-adv this is a gateway client
sudo batctl gw_mode client
​
# Activates batman-adv interfaces
sudo ifconfig wlan0 up
sudo ifconfig bat0 up
​
#assign a static IP
sudo ifconfig bat0 192.168.199.11 netmask 255.255.255.0
sudo route add default gw 192.168.199.1
sudo iwconfig wlan0 channel 6 essid mesh-network mode ad-hoc
'''
    with open(os.path.expanduser(dir + 'start-batman-adv.sh'), 'w') as f:
        f.write(script_content)
    run_command('chmod +x ' + dir + 'start-batman-adv.sh')
​
def configure_batman_adv_module():
    run_command('echo "batman-adv" | sudo tee --append /etc/modules')
​
def configure_dhcpcd():
    run_command('echo "denyinterfaces wlan0" | sudo tee --append /etc/dhcpcd.conf')
​
def setup_nameserver():
    run_command('echo "nameserver 192.168.199.1" | sudo tee --append /etc/resolv.conf')
def configure_rc_local():
    rc_local_content = 'sudo rfkill unblock all\n' + 'sudo sh ' + dir + 'start-batman-adv.sh &\n'
    with open('/etc/rc.local', 'r') as f:
        lines = f.readlines()
    lines.insert(-1, rc_local_content)
​
    with open('/etc/rc.local', 'w') as f:
        f.writelines(lines)
​
if __name__ == "__main__":
    install_batctl()
    create_start_batman_adv_script()
    configure_batman_adv_module()
    configure_dhcpcd()
    setup_nameserver()
    configure_rc_local()
​
    print("All configurations done. You can now reboot the Pi.")
