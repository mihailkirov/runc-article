#!/bin/bash
# createRuntime script - init env
# executes in the runtime namespace without chroot

# the script will conf the network namespace of the process 
runcInitPid=$(pgrep -f "runc init");
SAVETO="results-scripts/runtimeScript.txt";

# create the pair of network interfaces
ip link add veth0 type veth peer name ceth0; 
# attach+config one interface to the container net namespace 
ip netns attach contNetNs $runcInitPid;
ip link set ceth0 netns contNetNs;
ip netns exec contNetNs ip addr add  172.12.0.12/24  dev ceth0 ;
ip netns exec contNetNs ip link set dev ceth0 up ;
# configure net ns in runtime namespace
ip addr add 172.12.0.11/24 dev veth0;
ip link set veth0 up;

# give us some info
echo "$0" > $CDIR/$SAVETO;
for file in /proc/self/ns/*; do
	readlink $file >> $CDIR/$SAVETO; 
done
echo "PID:" $$ >> $CDIR/$SAVETO;
for i in $(env); do 
	echo $i >> $CDIR/$SAVETO; 
done


