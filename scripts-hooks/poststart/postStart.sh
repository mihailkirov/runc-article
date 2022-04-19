#!/bin/sh

# postStart script - to indicate if the env config and test phase went okey
# and trigger post-setup actions on the host
# executed in the runtime namespace without chroot

SAVETO="results-scripts/postStart.txt";
# starts a small python3 server

python3 $CDIR/scripts-hooks/httph.py; # goes in the background

# give us some info
echo "$0" > $CDIR/$SAVETO;
for file in /proc/self/ns/*; do
	readlink $file >> $CDIR/$SAVETO; 
done
echo "PID: " $$ >> $CDIR/$SAVETO;
for i in $(env); do 
	echo $i >> $CDIR/$SAVETO; 
done
