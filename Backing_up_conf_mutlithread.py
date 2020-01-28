from netmiko import Netmiko
import concurrent.futures
import datetime,time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
from os import path

#Check if 'Stored Configs Configs Configs' folder &'confirm.txt' file exists
def Check():
    
    if  path.exists('Stored Configs') is True:
        pass
    else:
        os.mkdir('Stored Configs')
    if path.exists('confirm.txt') is True:
        pass
    else:
        with open('confirm.txt','w') as f:
            f.close()
    return

Check()
print('='*50)

start_timer=time.perf_counter()


def backup_conf(dev):

    ''' 1. Passing parameters to Netmiko to fetch running configuration from Network Device
           and saving to a file with ip and current date as filename.
        2. Printing Confirmation '''

    def write_to_file(inp):
        #Appending confirmation output to file 
            with open('confirm.txt', 'a') as r:
                r.write(inp)

    try:
        my_dev=dev['ip']
        net_connect = Netmiko(**dev)
        if "secret" in dev:
            output = net_connect.send_command_timing('enable', strip_command=False, strip_prompt=False)
            if "Password:" in output:
                output += net_connect.send_command_timing(dev["secret"], strip_command=False, strip_prompt=False)
            else:
                pass
        else:
            pass
        net_connect.send_command('terminal length 0')
        run_config = net_connect.send_command_expect('show run')
        net_connect.disconnect() 


        file_n_time=datetime.datetime.now().strftime('%Y-%m-%d_%H_%M')
        with open('Stored Configs''\\'+my_dev+' '+file_n_time+'-conf.txt', 'w' , encoding='utf-8') as f:
            f.write(run_config)
            f.close()
        
        msg1 = f"Configuration for {my_dev} Saved to {my_dev +' '+file_n_time}-conf.txt ! \n "
        print(msg1)
        print('='* 50)

        write_to_file(msg1)
        return
    except:
        msg1=(f"Error While Connecting to {my_dev} !" + '\n')
        print(msg1)
        print('=' * 50)

        write_to_file(msg1)
        return

#Parsing JSON file
with open ('my_devices.json','r') as f:
    data=json.load(f)

    all_devices=[]
    for x in data:
        each_device=data[x]
        all_devices.append(each_device)

#Adding MultiThreading feature
with concurrent.futures.ThreadPoolExecutor() as executor:
    execute=executor.map(backup_conf , all_devices)


#Sending confirmation mail to user
want_mail=input('Email Confirmation file ? [Y/N]: ')
U_want_mail=want_mail.upper()

if U_want_mail == 'Y':
    print('! '*20 + '\n')
    
    email_user = 'gmail_id(from)'
    email_password = 'gmail_generated_password_for_app'
    email_send = 'email_id(to)'
    
    print('****Mailing to: ' + email_send+'****')
    
    msg = MIMEMultipart()
    
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = 'Automated Mail from Python Script'
    body = 'Confirmation Message'
    msg.attach(MIMEText(body,'plain'))
    my_file =open('confirm.txt','rb')
    part = MIMEBase('application','octet-stream')
    part.set_payload((my_file).read())
    encoders.encode_base64(part)
    
    part.add_header('Content-Disposition',"attachment; filename= "+'Confirmation.txt')
    msg.attach(part)
    text = msg.as_string()
    
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,text)
    server.quit()
else:
    pass

#Removing Contents of "confirm.txt"
empty_the_file=''
with open('confirm.txt','w') as w:
    w.write(empty_the_file)

#Printing Total execution time of Program
end_timer=time.perf_counter()
timer=f'Executed in= {round(end_timer-start_timer, 1)} second(s)'
print(timer)

exit_script=input("Press Enter To Exit")
