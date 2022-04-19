#!/bin/sh

# startContainer script - alerts for the incoming container launch
# executes in the container namespace after chroot

# relative to the container rootfs path
SAVETO="/home/write-results/startContainer.txt"
# give us some info
echo "$0" > $SAVETO;
for file in /proc/self/ns/*; do
	readlink $file >> $SAVETO; 
done
echo "PID:" $$ >> $SAVETO;
for i in $(env); do 
	echo $i >> $SAVETO; 
done

