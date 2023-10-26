"""
Ahoy, Big Belly Baus! Below be me evaluation of yer code to keelhaul those pesky Bluetooth connections on yer Linux ship:

    blacklist_bluetooth_modules:
        This here function be scribblin' entries into /etc/modprobe.d/blacklist.conf like a good pirate scribe. It be addin' two lines, one for btusb and t'other for bluetooth, effectively cuttin' 'em off from yer system.

    systemd_disable_bluetooth:
        This function be summonin' the subprocess sea monster to run a command that says, "No more Bluetooth service for ye!" It be like tossin' that Bluetooth parrot overboard to Davy Jones' locker.

    grub_disable_bluetooth:
        This function be messin' with the ship's GRUB configuration at /etc/default/grub. When it spies the GRUB_CMDLINE_LINUX_DEFAULT line, it sneaks in rfkill block bluetooth like a secret weapon. Then, it rings the ship's bell with sudo update-grub to announce the changes to the crew.

In the __main__ block:

    The script be checkin' if it's wearin' the captain's hat (root privileges), and if not, it be tellin' ye, "Even witches need permissions!" Arrr!
    It summons the three functions mentioned above to work their magic in disabling Bluetooth.
    At the end, it be advisin' ye to reboot the ship to make sure the spell sticks and Bluetooth be sent to the shadow realm for good!

Remember, matey, tinkerin' with system settings can have consequences, so tread carefully on the high seas of system administration!
"""
import os
import subprocess

def blacklist_bluetooth_modules():
    with open('/etc/modprobe.d/blacklist.conf', 'a') as f:
        f.write('\n# Disable Bluetooth\n')
        f.write('blacklist btusb\n')
        f.write('blacklist bluetooth\n')
    print("Bluetooth modules blacklisted.")

def systemd_disable_bluetooth():
    subprocess.run(['sudo', 'systemctl', 'disable', 'bluetooth'])
    print("Bluetooth service disabled.")

def grub_disable_bluetooth():
    grub_file_path = '/etc/default/grub'
    with open(grub_file_path, 'r') as f:
        lines = f.readlines()

    with open(grub_file_path, 'w') as f:
        for line in lines:
            if line.startswith('GRUB_CMDLINE_LINUX_DEFAULT'):
                if 'rfkill block bluetooth' not in line:
                    line = line.strip('\n') + ' rfkill block bluetooth"\n'
            f.write(line)

    subprocess.run(['sudo', 'update-grub'])
    print("Bluetooth disabled from GRUB.")

if __name__ == '__main__':
    print("Disabling Bluetooth... Hold onto your broomsticks!")
    
    if os.geteuid() != 0:
        print("You need to run this script as root. Even witches need permissions!")
        exit(1)

    blacklist_bluetooth_modules()
    systemd_disable_bluetooth()
    grub_disable_bluetooth()

    print("Bluetooth has been sent to the shadow realm. A reboot is needed to complete the spell.")
