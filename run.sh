echo "Creating .."
runc create -b /h00ks/bundle c  &
sleep 1
echo "Starting .."
runc start c 
sleep 1
echo "Deleting .."
runc delete c 