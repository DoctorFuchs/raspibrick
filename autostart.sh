#! /bin/sh
# Autostart script for RaspiBrick

set -x

echo "Running autostart.sh. Sleeping a while..."
sleep 10 # Wait until system is up and running
echo "Continuing..."

# Mount file system
sudo mkdir /mnt/recovery
sudo mount /dev/mmcblk0p1 /mnt/recovery


file1="/mnt/recovery/wpa-update.requested"
if [ -f "$file1" ]
then
  # copy wlan info from FAT partition and restart wlan
  sudo cp /mnt/recovery/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
  sudo ifdown wlan0
  sudo ifup wlan0 
  sudo rm -f "$file1"
else
  # copy wlan info to FAT partition (it may have been modified by raspi GUI user)
  sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /mnt/recovery/wpa_supplicant.conf 
fi

# check if data file is present
file2="/mnt/recovery/brickgate.data"
if [ -f "$file2" ]
then
  cp /mnt/recovery/brickgate.data /home/pi/brickgate.data
fi

echo "Running ProcessMon.py"
pyrun /home/pi/raspibrick/ProcessMon.py
