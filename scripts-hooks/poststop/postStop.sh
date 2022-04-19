#!/bin/sh

# postStop script - brings everything back to normal
# executes in the runtime namespace without chroot
SAVETO="results-scripts/postStop.txt";

echo "$0"

# delete namespaces -> delete both interfaces
ip netns delete contNetNs;
# kill http server
kill -s 9 $(pgrep -f "httph.py");
# delete the runc container object
runc delete c;

# some info
# program name
echo "$0" > $CDIR/$SAVETO;
for file in /proc/self/ns/*; do
	readlink $file >> $CDIR/$SAVETO; 
done
# pid info
echo "PID:" $$ >> $CDIR/$SAVETO;
# environment info
for i in $(env); do 
	echo $i >> $CDIR/$SAVETO; 
done
