# frequency_updater.py

import argparse
import socket
import struct
import threading
import time

import msgpack

# Global variable to represent the buzzer frequency
# Global variables
MIN_RSSI = -105
MAX_RSSI = 0
MIN_FREQ = 1  # Minimum buzzer frequency in Hz
MAX_FREQ = 10  # Maximum buzzer frequency in Hz
GPIO_CHIP = "/dev/gpiochip1"
GPIO_OFFSET = 4
HOST = "127.0.0.1"
PORT = 8003
RETRY_INTERVAL = 1
results = []
buzzer_frequency = 1
verbose_mode = False


def calculate_buzzer_frequency(video_rx):
    global buzzer_frequency
    global verbose_mode
    # Get antenna stats
    rx_ant_stats = video_rx.get("rx_ant_stats", {})
    rssi_values = []
    num_antennas = len(rx_ant_stats)

    # Ensure there are antenna stats available
    if num_antennas > 0:
        for (
            antenna
        ) in (
            rx_ant_stats.values()
        ):  # Antenna data is stored in a dict, so use .values()
            if (
                len(antenna) >= 6
            ):  # Check if antenna data has enough values to access rssi_avg
                rssi_avg = antenna[2]  # rssi_avg is at index 2
                rssi_values.append(rssi_avg)
            else:
                if verbose_mode:
                    print(f"Warning: Antenna data is incomplete: {antenna}")
    else:
        if verbose_mode:
            print("Warning: No antenna stats available")
        return MIN_FREQ  # Exit early if no antennas

    # Sum rssi values and interpolate from 0 to MIN_RSSI. 0 means MAX_FREQ, MIN_RSSI means MIN_FREQ
    sum_rssi = sum(rssi_values)
    buzzer_frequency = MIN_FREQ + (MAX_FREQ - MIN_FREQ) * (sum_rssi - MIN_RSSI) / (
        MAX_RSSI - MIN_RSSI
    )
    return buzzer_frequency


def connect_and_receive_msgpack():
    global buzzer_frequency

    while True:
        try:
            # Create a TCP/IP socket for receiving data
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # Connect to the remote server
                if verbose_mode:
                    print(f"Connecting to {HOST}:{PORT}...")
                client_socket.connect((HOST, PORT))
                if verbose_mode:
                    print(f"Connected to {HOST}:{PORT}")

                while True:
                    # First, read 4 bytes for the length prefix
                    length_prefix = client_socket.recv(4)
                    if not length_prefix:
                        if verbose_mode:
                            print("No more data, connection closed.")
                        break

                    # Unpack the 4-byte length prefix (uint32)
                    msg_length = struct.unpack("!I", length_prefix)[0]

                    # Now read the actual MessagePack data of the given length
                    data = b""
                    while len(data) < msg_length:
                        chunk = client_socket.recv(min(4096, msg_length - len(data)))
                        if not chunk:
                            if verbose_mode:
                                print("Incomplete data, connection closed.")
                            break
                        data += chunk

                    # If we successfully received the full message, unpack it
                    if len(data) == msg_length:
                        try:
                            unpacked_data = msgpack.unpackb(
                                data, use_list=False, strict_map_key=False
                            )
                            results.append(unpacked_data)  # Append to the results array

                            # Process video_rx message
                            if (
                                unpacked_data.get("type") == "rx"
                                and unpacked_data.get("id") == "video rx"
                            ):
                                buzzer_frequency = calculate_buzzer_frequency(
                                    unpacked_data
                                )
                                if verbose_mode:
                                    print(f"Buzzer Frequency: {buzzer_frequency}")

                        except msgpack.UnpackException as e:
                            if verbose_mode:
                                print(f"Failed to unpack data: {e}")
                    else:
                        if verbose_mode:
                            print("Failed to receive full data, closing connection.")
                        break
        except Exception as e:
            if verbose_mode:
                print(
                    f"Connection failed or lost: {e}. Retrying in {RETRY_INTERVAL} seconds..."
                )
            time.sleep(RETRY_INTERVAL)  # Wait before retrying connection


def start_frequency_updater():
    # Run the updater on a separate thread
    frequency_thread = threading.Thread(target=connect_and_receive_msgpack, daemon=True)
    frequency_thread.start()


def get_current_frequency():
    global buzzer_frequency
    return buzzer_frequency

def set_verbose_mode(value):
    global verbose_mode
    verbose_mode = value