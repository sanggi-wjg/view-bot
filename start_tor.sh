#!/bin/bash
# Start Tor with dynamic number of SOCKS ports

# Default values
NUM_PORTS=${1:-5}
START_PORT=${2:-9050}

# Build the tor command with multiple SocksPort arguments
TOR_CMD="tor"
for ((i=0; i<NUM_PORTS; i++)); do
    PORT=$((START_PORT + i))
    TOR_CMD="$TOR_CMD --SocksPort $PORT"
done

echo "Starting Tor with $NUM_PORTS ports (${START_PORT}-$((START_PORT + NUM_PORTS - 1)))"
echo "Command: $TOR_CMD"
echo ""
echo "To stop Tor, press Ctrl+C or run: ./stop_tor.sh"
echo ""

# Execute the tor command
exec $TOR_CMD
