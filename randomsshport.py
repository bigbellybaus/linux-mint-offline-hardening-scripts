#!/usr/bin/env python3

"""
Author: Big Belly Baus

This Python script is the magic wand for SSH port management. It does the following:

1. Generates a random port number that avoids commonly used ports (such as those lower than 1024 and others like 8080, 3306, etc.)
2. Updates the SSH configuration to set the SSH service to use this new port.
3. Restarts the SSH service to apply the change, ensuring that you're guarded by new protective spells.
4. Creates a systemd service to make these changes every time the system boots. This means your SSH port is as unpredictable as a wizard's duel!

To execute, just run the script as a superuser:

    sudo python3 this_script.py

Logs are managed by the 'logging' module and can be viewed using journalctl for the systemd service:

    journalctl -u shuffle-ssh-port.service

Remember, this script is more secretive than the Ministry of Magic, and more random than a bag of Bertie Bott's Every Flavor Beans.
"""

import random
import subprocess
import os
import logging

logging.basicConfig(level=logging.INFO)

def is_valid_port(port):
    forbidden_ports = list(range(0, 1024)) + [8080, 3306, 5432, 27017]
    return port not in forbidden_ports

def change_ssh_port(new_port):
    try:
        subprocess.run(["sed", "-i", f"s/^#?Port .*/Port {new_port}/", "/etc/ssh/sshd_config"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred: {e}")
        return False
    return True

def restart_ssh():
    try:
        subprocess.run(["systemctl", "restart", "ssh"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while restarting SSH: {e}")
        return False
    return True

def create_systemd_service(script_path):
    if os.path.exists("/etc/systemd/system/shuffle-ssh-port.service"):
        return
    
    service_content = f"""[Unit]
Description=Shuffle SSH Port on Boot
After=network.target

[Service]
ExecStart={script_path}
Type=oneshot

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/shuffle-ssh-port.service", "w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", "shuffle-ssh-port.service"], check=True)

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    new_port = random.randint(1024, 65535)
    while not is_valid_port(new_port):
        new_port = random.randint(1024, 65535)
        
    logging.info(f"Attempting to set SSH port to {new_port}")

    if change_ssh_port(new_port):
        logging.info(f"SSH port changed to {new_port}. Time to alert the Ministry of Magic!")
        
        if restart_ssh():
            logging.info("SSH service restarted. The protective spells have been recast!")
            create_systemd_service(script_path)
            logging.info("Systemd service created. Your SSH port will now shuffle on boot like a wizard in a dance-off!")
        else:
            logging.error("Couldn't restart SSH. Someone might've broken your wand!")
    else:
        logging.error("Failed to change SSH port. Maybe you're using a muggle tool?")
