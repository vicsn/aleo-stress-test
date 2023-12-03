echo "Starting network"
echo | ./03_start.sh
echo "Sleep 60 seconds"
sleep 60
echo "Initiating transfers"
echo | ./05_transfers.sh
echo "Starting other nodes"
echo | ./06_start_other_nodes.sh
echo "Sleep 60 seconds"
sleep 60
echo "Bonding and unbonding other nodes"
echo | ./08_bond_and_unbond_other_nodes.sh