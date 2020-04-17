#!/bin/sh

# bool function to test if the user is root or not (POSIX only)
is_user_root() { [ "$(id -u)" -eq 0 ]; }

if is_user_root; then
    wireshark -i any -Y "tcp.port == 8080" -k &
else
    echo 'Please run this script as root (sudo)' >&2
    exit 1
fi