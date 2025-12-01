#!/bin/bash
# Stop Tor processes

echo "Stopping Tor processes..."

# Find and kill tor processes
TOR_PIDS=$(pgrep -f "^tor --SocksPort")

if [ -z "$TOR_PIDS" ]; then
    echo "No Tor processes found"
    exit 0
fi

echo "Found Tor process(es): $TOR_PIDS"
kill $TOR_PIDS

# Wait a bit and check if processes are still running
sleep 1
REMAINING=$(pgrep -f "^tor --SocksPort")

if [ -n "$REMAINING" ]; then
    echo "Force killing remaining processes: $REMAINING"
    kill -9 $REMAINING
fi

echo "Tor stopped successfully"
