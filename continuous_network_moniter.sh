#!/bin/bash

INTERFACE="wlp3s0"  # Update with your active network interface
LOGFILE="continuous_network_monitor.log"

# Function to log network statistics periodically
function log_network_stats() {
    while true; do
        RX_PACKETS=$(cat /sys/class/net/$INTERFACE/statistics/rx_packets)
        TX_PACKETS=$(cat /sys/class/net/$INTERFACE/statistics/tx_packets)
        RX_BYTES=$(cat /sys/class/net/$INTERFACE/statistics/rx_bytes)
        TX_BYTES=$(cat /sys/class/net/$INTERFACE/statistics/tx_bytes)

        echo "Timestamp: $(date)" >> $LOGFILE
        echo "Received packets: $RX_PACKETS, Sent packets: $TX_PACKETS" >> $LOGFILE
        echo "Received bytes: $((RX_BYTES / 1024)) KB, Sent bytes: $((TX_BYTES / 1024)) KB" >> $LOGFILE
        echo "--------------------------" >> $LOGFILE

        sleep 0.1  # Log every second, adjust as necessary
    done
}

log_network_stats
