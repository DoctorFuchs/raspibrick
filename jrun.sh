#! /bin/sh
# Launch Java JARs

if [ $# -eq 0 ]
  then
    echo "Usage: jrun <myapp>.jar, where main class is <myapp>"
    echo "   or: jrun <myapp>.jar <mainclass>"     
    exit 1
fi

if [ $# -gt 2 ]
  then
    echo "Usage: jrun -jar <myapp>.jar, where main class is <myapp>"
    echo "   or: jrun <myapp>.jar <mainclass>"     
    exit 1
fi

lib1=/home/pi/raspibrick/jars/aplu5.jar
lib2=/home/pi/raspibrick/jars/DidelJLibA.jar
lib3=/home/pi/raspibrick/jars/RaspiJLibA.jar
lib4=/home/pi/raspibrick/jars/RaspiJLibX.jar
lib5=/home/pi/raspibrick/jars/raspi-gpio.jar
lib6=/home/pi/raspibrick/jars/pi4j-core.jar

fullfile=$1
fname=$(basename $fullfile)
fbname=${fname%.*}
#echo $fbname

if [ $# -eq 1 ]
  then
#    set -x  # echo on console
    sudo java -cp .:$lib1:$lib2:$lib3:$lib4:$lib5:$lib6:$fullfile $fbname
fi

if [ $# -eq 2 ]
  then
#    set -x  # echo on console
    sudo java -cp .:$lib1:$lib2:$lib3:$lib4:$lib5:$lib6:$fullfile $2
fi
