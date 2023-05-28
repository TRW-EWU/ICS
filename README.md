# ICS
## Requirements
### You will need to install pymodbus to use this code
sudo pip install pymodbus

##
Also need to run the following command:
sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s <src_ip> -j DROP

## Execution
python3 tip.py --help

## Fro a Modbus Server
python3 tip.py -s modbus

