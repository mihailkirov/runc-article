

# postStop script - brings everything back to normal
# executes in the runtime namespace without chroot
SAVETO="results-scripts/postStop.txt";

# delete namespaces -> delete both interfaces
ip netns delete contNetNs;
# kill http server
kill -s 9 $(pgrep -f "httph.py");
# delete the runc container object
runc delete c;

# give us some info
echo "POSTSTOP" > $CDIR/$SAVETO;
for file in /proc/self/ns/*; do
	readlink $file >> $CDIR/$SAVETO; 
done
echo "PID:" $$ >> $CDIR/$SAVETO;
for i in $(env); do 
	echo $i >> $CDIR/$SAVETO; 
done
