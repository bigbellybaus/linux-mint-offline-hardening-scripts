#!/usr/bin/env python3

"""
Author: Big Belly Baus

Purpose: This Python script is designed to be the Gandalf of your Linux Mint system, shouting "You shall not pass!" to all incoming network traffic. It uses GUFW (Graphical Uncomplicated Firewall) to enforce this policy.

Usage:
    Run this script as a superuser:
    sudo python3 this_script.py

May your system be as impenetrable as Hogwarts during a Dumbledore speech.
"""

import subprocess

def enable_gufw():
    try:
        subprocess.run(["ufw", "enable"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to enable UFW: {e}")

def deny_incoming_traffic():
    try:
        subprocess.run(["ufw", "default", "deny", "incoming"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to deny incoming traffic: {e}")

if __name__ == "__main__":
    # Attempt to enable GUFW and deny incoming traffic
    enable_gufw()
    deny_incoming_traffic()
