#!/bin/bash


echo '-> Setting up mock interfaces'

# Create TAP (Network TAP) Interface
sudo ip tuntap add name tap0 mode tap
sudo ip link set dev tap0 up

# Create Bridge Interface
sudo ip link add name br0 type bridge
sudo ip link set dev br0 up

# Create Bonded Interface
sudo ip link add name bond0 type bond
sudo ip link set dev bond0 up

# Create TUN (Network TUNnel) Interface
sudo ip tuntap add name tun0 mode tun
sudo ip link set dev tun0 up

# Create VETH (Virtual Ethernet) Interface
sudo ip link add name veth0 type veth peer name veth1
sudo ip link set dev veth0 up


# Log the start time
echo "-> Script started at $(date)"
python3 ipconfig.py
echo "->Script ended at $(date)"


echo '-> Removing mock interfaces'
# Remove TAP (Network TAP) Interface
sudo ip link set dev tap0 down
sudo ip link del dev tap0

# Remove Bridge Interface
sudo ip link set dev br0 down
sudo ip link del dev br0


# Remove Bonded Interface
sudo ip link set dev bond0 down
sudo ip link del dev bond0

# Remove TUN (Network TUNnel) Interface
sudo ip link set dev tun0 down
sudo ip link del dev tun0

# Remove VETH (Virtual Ethernet) Interface
sudo ip link set dev veth0 down
sudo ip link del dev veth0

echo "done"