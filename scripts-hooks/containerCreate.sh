#!/bin/sh

# containerCreate script - test env config
# executes in the container namespace before being chrooted

SAVETO="./home/write-results/createContainer.txt";
# test network interface connectivity
ping -c 1 172.12.0.11;
# check that the next hook script is available
stat /home/tmpfssc;
# give us some info
echo "CREATE CONTAINER" > $SAVETO;
for file in /proc/self/ns/*; do
	readlink $file >> $SAVETO; 
done
echo "PID:" $$ >> $SAVETO;
for i in $(env); do 
	echo $i >> $SAVETO; 
done

