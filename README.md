# Fetching Running Config

A multithreaded Python Script for fetching running configurationso over SSH from multiple Cisco Devices
Configurations will be saved to file with ip and current time as file name
And optional feature for emailing confirmation to user

  # Usage
Give Network Device parameters in JSON file to add Devices


   "Device-1":{
        "device_type": "cisco_ios",
        "ip": "_device_ip_",
        "username":"_your_username",
        "password":"__password__",
        "secret" : "_enable_pass",
        "fast_cli": false
      }
      
      
  # Installation

1. Requires Python 3.6 or higher

2. Install dependencies: 
    pip install -r requirements.txt
