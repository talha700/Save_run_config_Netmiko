# Fetching Running Config

A multithreaded Python Script based on Netmiko for fetching running configurations over SSH from multiple Cisco Devices
Configurations will be saved to file with ip and current time as file name
and optional feature for emailing confirmation to user.

  ## Usage
Give Network Device parameters in JSON file to add Devices.
- SSH credentials
- ip
- enable pass('secret') for users less Priviledge than 15, 
remove 'secret' row for user with Priviledge level 15

   "Device-1":{
        "device_type": "cisco_ios",
        "ip": "_device_ip_",
        "username":"_your_username",
        "password":"__password__",
        "secret" : "_enable_pass",
        "fast_cli": false
      }
      
   
Give email Credentials in script


     email_user = 'gmail_id(from)'
     email_password = 'gmail_generated_password_for_app'
     email_send = 'email_id(to)'

  ## Installation

1. Requires Python 3.6 or higher

2. Install dependencies: 
    pip install -r requirements.txt
