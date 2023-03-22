import os
from tkinter import messagebox, ttk
import re
import paramiko
from tkinter import *
import time
def add_raspberry():
    
    # Get the token
    token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhWDdPVTJxODRNRU5MNm9uQkYzIiwiYXVkIjoiY3JlYXRlLXNlcnZlciIsImlzcyI6InBsYXRmb3JtLWVudGVycHJpc2UtcG9ydGFsOk5DRFVBaWVEOEhKM0xMdVE2M0IiLCJpZCI6InJlQ2ZDUEg3NGpvWWlkeHo4blRVIiwiaWF0IjoxNjU1NDYyNDM0fQ.EJRHdKwnMfGBYMxB8TW6XA-2esFuxO6H_AR-UkEOEBk"
    
    # Get the hostname and name of the Raspberry Pi from the user
    hostname = hostname_entry.get()
    raspberry_name = name_entry.get()
    print(raspberry_name)

    if not hostname:
        messagebox.showerror("Error", "Hostname field is empty")
        return
    if not raspberry_name:
        messagebox.showerror("Error", "Name field is empty")
        return    
    if not re.match("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$", hostname):
        messagebox.showerror("Error", "Invalid hostname or IP address")
        return
    try:
        # Create an SSH client
        client = paramiko.SSHClient()

        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the Raspberry Pi
        client.connect(hostname=hostname, username='pi', password='COSMOPHYSIO123')
        stdin, stdout, stderr = client.exec_command(f'sudo hostnamectl set-hostname {raspberry_name}')
        if stderr.channel.recv_exit_status() == 0:
            print("Command executed successfully")
        else:
            print(stderr.read().decode())
        stdin, stdout, stderr = client.exec_command(f'sudo reboot')
        if stderr.channel.recv_exit_status() == 0:
            print("Command executed successfully")
        else:
            print(stderr.read().decode())
        progress_bar.pack()
         # Wait for the Raspberry Pi to reboot
        update_progress(16)
        time.sleep(10) # waiting for 10 seconds after reboot
        update_progress(16)
        time.sleep(10) # waiting for 10 seconds after reboot
        update_progress(32)
        time.sleep(10) # waiting for 10 seconds after reboot
        update_progress(48)
        time.sleep(10) # waiting for 10 seconds after reboot
        update_progress(64)
        time.sleep(10) # waiting for 10 seconds after reboot
        update_progress(80)
        time.sleep(10) # waiting for 10 seconds after reboot
        update_progress(96)
        update_progress(100)
        client.connect(hostname=hostname, username='pi', password='COSMOPHYSIO123')
        # Install and configure VNC server on the Raspberry Pi
        # stdin, stdout, stderr = client.exec_command('sudo apt-get install tightvncserver')
        # stdin, stdout, stderr = client.exec_command('tightvncserver :1')
        # Add the Raspberry Pi to the VNC cloud
        stdin, stdout, stderr = client.exec_command(f'sudo vncserver-x11 -service -joinCloud {token}')
        if stderr.channel.recv_exit_status() == 0:
            print("Command executed successfully")
        else:
            print(stderr.read().decode())
        time.sleep(30) # waiting for 10 seconds after reboot
        stdin, stdout, stderr = client.exec_command(f'sudo printf "exec openbox-session &\n#vncserver & while true; do\n sudo python COSMOSOFT/Ui_Test.py\ndone">.xsession')
        stdin, stdout, stderr = client.exec_command(f'sudo reboot')
        messagebox.showinfo("Info","Raspberry added succesfully")
    except paramiko.ssh_exception.NoValidConnectionsError:
        messagebox.showerror("Error", "Could not connect to the Raspberry Pi, Please check the hostname and IP")
    except paramiko.ssh_exception.AuthenticationException:
        messagebox.showerror("Error", "Authentication failed, Please check the username and password")
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occured: " + str(e))
    # Close the SSH connection
    client.close()
def update_progress(value):
    progress_bar["value"] = value
    root.update()
root = Tk()
root.title("Add Raspberry Pi to VNC Cloud")

hostname_label = Label(root, text="Enter the hostname or IP address of the Raspberry Pi: ")
hostname_label.pack()

hostname_entry = Entry(root)
hostname_entry.pack()

name_label = Label(root, text="Enter S/N for the Raspberry Pi: ")
name_label.pack()

name_entry = Entry(root)
name_entry.pack()

add_button = Button(root, text="Add", command=add_raspberry)
add_button.pack()
# Create a progressbar widget
progress_bar = ttk.Progressbar(root, orient="horizontal",
                              mode="determinate", maximum=100, value=0)
root.mainloop()
