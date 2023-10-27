"""
Welcome to the "Disable Wake-on-LAN and Confuse the CIA and Witches" script!

If you're a noob (or even a seasoned warlock), here's a quick rundown:

1. Wake-on-LAN (WoL) is like a magic spell that can wake up your computer from afar.
   Imagine you're a witch; it's like someone using a remote control to start your broomstick.
   
2. The CIA, witches, or your annoying younger sibling might misuse this magic to wake up
   your computer when you're not looking. We don't want that!
   
3. This script performs the equivalent of hiding your magic wand AND your broomstick,
   so no one can start them without your say-so. It disables WoL on your computer.

4. To make sure even a reboot won't give the CIA or witches their powers back, this script
   also casts a permanent "protection spell" using something called "systemd," which is a
   guardian spirit that helps manage tasks on your computer.

So grab your potion and magic hat, and let's disable some WoL!
"""
import os
import subprocess

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")

if __name__ == "__main__":
    # Ensure we're running as root
    if os.getuid() != 0:
        print("This script must be run as root. Just like how you need to be a grand wizard to banish witches.")
        exit(1)

    print("Disabling Wake-on-LAN... CIA's magical powers are weakening!")

    # Fetch all network interfaces
    get_interfaces_command = "ls /sys/class/net"
    interfaces = subprocess.getoutput(get_interfaces_command).split("\n")

    for interface in interfaces:
        if interface != 'lo':  # Ignore the loopback interface
            ethtool_command = f"ethtool -s {interface} wol d"
            
            print(f"Turning off the WoL charm for {interface}... it's like hiding your magic wand from the witches.")
            run_command(ethtool_command)

    # Create a systemd service file to exorcise WoL demons
    service_file_path = "/etc/systemd/system/disable-wol@.service"
    service_content = """[Unit]
Description=Wake-on-LAN (%i)
Requires=network.target
After=network.target

[Service]
ExecStart=/usr/sbin/ethtool -s %i wol d
Type=oneshot

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/disable-wol@.service", "w") as f:
        f.write(service_content)

    print("Writing the spell into the Book of Shadows...or, uh, systemd.")

    # Set secure permissions on the systemd service file
    os.chmod(service_file_path, 0o644)  # Set permissions to rw-r--r--

    # Reload systemd to make sure it gets the memo that we're not welcoming the CIA or witches
    run_command("systemctl daemon-reload")

    # Enable the systemd service for each interface
    for interface in interfaces:
        if interface != 'lo':
            print(f"Casting protective spells on {interface}...")
            run_command(f"systemctl enable disable-wol@{interface}")

    print("WoL is now as disabled as a CIA agent trying to outwit a witch. Mission accomplished.")
