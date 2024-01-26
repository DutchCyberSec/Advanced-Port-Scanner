# Advanced Port Scanner

## Overview

The Advanced Port Scanner is a Python script that allows users to perform various network scanning tasks. It includes features such as TCP, UDP, and ICMP port scanning, as well as scanning for common admin pages on websites.

## Features

- **TCP Scan:** Scan for open TCP ports on a target.
- **UDP Scan:** Scan for open UDP ports on a target.
- **ICMP Scan:** Perform ICMP ping to check if a target is reachable.
- **Admin Page Scan:** Scan a target website for common admin pages.

## Usage

1. Enter the target in the provided GUI.
2. Choose the scan type from the menu (TCP, UDP, ICMP, or Admin Page).
3. Click the appropriate scan button to initiate the scan.
4. View the results in the text area provided.

## Disclaimer

This tool is created for educational purposes only. Users are advised to use it responsibly and with proper authorization. The creator is not responsible for any misuse or damage caused by this script.

## Creator

Dutch Cyber Sec

## Dependencies

The script uses the `requests` library. Install dependencies using:

```bash
pip install -r requirements.txt



How to Run

    Clone the repository. git clone https://github.com/DutchCyberSec/Advanced-Port-Scanner.git
    Install dependencies (pip install -r requirements.txt).
    Run the script: sudo python3 ./Advanced_Port_Scanner.py
