# -*- coding: utf-8 -*-
"""
Quad9 DNS Enthusiast Script

Are you tired of your DNS queries being intercepted by secret agents or mystical forces?
Fear not! This script transforms your Linux Mint's DNS settings into a high-speed
Quad9 DNS rocket, ready to protect your digital realm from prying eyes and supernatural beings!

Quad9, the privacy-conscious DNS provider, is your digital guardian angel. They specialize in
ensuring your online activities remain confidential, like a locked vault in cyberspace!

It's like putting a firewall around your DNS, fit for a CTO superhero!

Author: Big Belly Baus (aka the DNS Dynamo)
Disclaimer: Use with sudo-level caution! Only for DNS daredevils who know the secrets of the digital world.

Instructions:
- Run this script with sudo privileges to enable Quad9 DNS with DNS over HTTPS (DoH).
- Keep the witches and the CIA guessing as your DNS remains secure and encrypted!

What is DNS over HTTPS (DoH)?
DNS over HTTPS (DoH) is a protocol for performing DNS resolution over encrypted HTTPS connections.
It ensures that your DNS queries are private, secure, and protected from eavesdropping, making it
an excellent choice for enhancing your online privacy and security.

Remember, you're the master of your DNS domain!
"""

import os
import subprocess

def get_network_interfaces():
    """
    Retrieves a list of network interfaces available on the system.

    Returns:
        list: A list of network interface names.
    """
    try:
        result = subprocess.check_output(["ip", "link"])
        output = result.decode("utf-8")
        lines = output.split('\n')
        interfaces = [line.split(':')[1].strip() for line in lines if line.strip().startswith("2:")]
        return interfaces
    except Exception as e:
        print(f"Error retrieving network interfaces: {e}")
        return []

def enable_doh_systemd_resolved(interface):
    """
    Configures DNS settings for a network interface using Quad9 DNS.
    
    Args:
        interface (str): The name of the network interface.
    """
    config = f'''
[Resolve]
DNS=9.9.9.9 149.112.112.112 2620:fe::fe 2620:fe::9
FallbackDNS=8.8.8.8 8.8.4.4
# Quad9
DNSOverTLS=yes
DNSSEC=yes

[Network]
Name={interface}
'''
    with open(f"/etc/systemd/network/{interface}.network", "a") as f:
        f.write(config)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Hey champ, you're gonna need sudo-level clearance for this operation!")
    else:
        # Get a list of all network interfaces
        interfaces = get_network_interfaces()
        for interface in interfaces:
            enable_doh_systemd_resolved(interface)
