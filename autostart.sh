#! /bin/sh
# Autostart script for RaspiBrick
# Version Aug. 27, 2015

set -x

echo Running autostart.sh
sleep 5 # Wait until system is up and running

# Select audio output (not HDMI)
amixer cset numid=3 1

# Mount file system
sudo mkdir /mnt/recovery
sudo mount /dev/mmcblk0p1 /mnt/recovery

file1="/mnt/recovery/wpa-update.requested"
if [ -f "$file1" ]
then
  # copy wlan info from FAT partition and reboot
  sudo cp /mnt/recovery/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
  sudo rm -f "$file1"
  pyrun /home/pi/raspibrick/UpdateSSID.py
  sudo shutdown -r now
  exit
else
  # copy wlan info to FAT partition (it may have been modified by raspi GUI user)
  sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /mnt/recovery/wpa_supplicant.conf 
fi

file11="/mnt/recovery/raspibrick-rename.requested"
if [ -f "$file11" ]
then
  pyrun /home/pi/raspibrick/RenameHost.py
fi


# make Bluetooth discoverable
sudo hciconfig hci0 piscan
# start Bluetooth RFComm server
/home/pi/bluetooth-server/start-server &

# check if data file is present
file2="/mnt/recovery/brickgate.data"
if [ -f "$file2" ]
then
  cp /mnt/recovery/brickgate.data /home/pi/brickgate.data
fi

sleep 5 # Wait until system is up and running

# check if autostart script is present
file2="/home/pi/scripts/autostart.py"
if [ -f "$file2" ]
then
  echo "Running autostart.py"
  pyrun /home/pi/scripts/autostart.py
else
  echo "Running ProcessMon.py"
  pyrun /home/pi/raspibrick/ProcessMon.py
fi



