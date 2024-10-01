#!/bin/bash

INTERFACE="wlp3s0"  # Updated to your Wi-Fi interface
LOGFILE="network_monitor.log"
PIPE="./Pipe_net_log"

# Create a named pipe (FIFO) for communication
if [[ ! -p $PIPE ]]; then
    mkfifo $PIPE
fi

# Function to log network statistics
function log_network_stats() {
    local segment=$1

    # Capture stats before transmission
    RX_PACKETS_BEFORE=$(cat /sys/class/net/$INTERFACE/statistics/rx_packets)
    TX_PACKETS_BEFORE=$(cat /sys/class/net/$INTERFACE/statistics/tx_packets)
    RX_BYTES_BEFORE=$(cat /sys/class/net/$INTERFACE/statistics/rx_bytes)
    TX_BYTES_BEFORE=$(cat /sys/class/net/$INTERFACE/statistics/tx_bytes)

    # Simulate segment transmission delay
    sleep 2  # Adjust based on segment size if necessary

    # Capture stats after transmission
    RX_PACKETS_AFTER=$(cat /sys/class/net/$INTERFACE/statistics/rx_packets)
    TX_PACKETS_AFTER=$(cat /sys/class/net/$INTERFACE/statistics/tx_packets)
    RX_BYTES_AFTER=$(cat /sys/class/net/$INTERFACE/statistics/rx_bytes)
    TX_BYTES_AFTER=$(cat /sys/class/net/$INTERFACE/statistics/tx_bytes)

    RX_PACKETS=$((RX_PACKETS_AFTER - RX_PACKETS_BEFORE))
    TX_PACKETS=$((TX_PACKETS_AFTER - TX_PACKETS_BEFORE))
    RX_BYTES=$((RX_BYTES_AFTER - RX_BYTES_BEFORE))
    TX_BYTES=$((TX_BYTES_AFTER - TX_BYTES_BEFORE))

    # Log the network activity
    echo "Segment $segment - Received: $RX_PACKETS packets, Sent: $TX_PACKETS packets" >> $LOGFILE
    echo "Segment $segment - Received: $((RX_BYTES / 1024)) KB, Sent: $((TX_BYTES / 1024)) KB" >> $LOGFILE
}

# Continuously listen for requests to log network statistics
while true; do
    if read segment < $PIPE; then
        log_network_stats $segment
    fi
done
