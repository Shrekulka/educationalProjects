import argparse
import logging
import signal
import socket
import sys
import traceback
from typing import Optional, Tuple

from logger_config import logger

# Constants
MAX_SIZE = 65507  # Maximum UDP datagram size
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5050
SEPARATOR = "-" * 40  # Separator for output
TIMEOUT_DEFAULT = 5.0  # Default timeout in seconds
RECV_BUFFER_SIZE = 4096  # Receive buffer size
MAX_RETRIES = 3  # Maximum number of retries for sending data


def create_socket(timeout: float) -> Optional[socket.socket]:
    """
    Creates and configures a UDP socket.

    Args:
        timeout (float): Socket timeout in seconds.

    Returns:
        Optional[socket.socket]: Created socket or None in case of error.
    """
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(timeout)
        return client
    except socket.error as e:
        logger.error(f"Failed to create socket: {e}")
        print(f"Failed to create socket: {e}")
        return None


def parse_arguments() -> argparse.Namespace:
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="UDP Client")
    parser.add_argument('--host', default=DEFAULT_HOST, help="Target host")
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help="Target port")
    parser.add_argument('--timeout', type=float, default=TIMEOUT_DEFAULT, help="Socket timeout in seconds")
    parser.add_argument('--log', help="Log file path")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
    return parser.parse_args()


def send_data(client: socket.socket, data: str, target_host: str, target_port: int) -> bool:
    """
    Sends data to the server with retry mechanism.

    Args:
        client (socket.socket): Socket object.
        data (str): Data to send.
        target_host (str): Target host to connect to.
        target_port (int): Target port to connect to.

    Returns:
        bool: True if data was sent successfully, False otherwise.
    """
    for attempt in range(MAX_RETRIES):
        try:
            client.sendto(data.encode(), (target_host, target_port))
            logger.info(f"Sent data: {data} to {target_host}:{target_port}")
            return True
        except socket.error as e:
            logger.warning(f"Failed to send data (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt == MAX_RETRIES - 1:
                logger.error("Max retries reached. Failed to send data.")
                return False
    return False


def receive_data(client: socket.socket) -> Tuple[str, bool]:
    """
    Receives data from the server.

    Args:
        client (socket.socket): Socket object.

    Returns:
        Tuple[str, bool]: Received data and a boolean indicating success.
    """
    data: bytes = b""
    try:
        while True:
            chunk, _ = client.recvfrom(RECV_BUFFER_SIZE)
            if not chunk:
                break
            data += chunk
            if len(data) > MAX_SIZE:
                logger.warning("Received data exceeds maximum UDP datagram size")
                break
        return data.decode("utf-8"), True
    except socket.timeout:
        logger.error("Connection timed out")
        return "Timeout occurred", False
    except socket.error as e:
        logger.error(f"Socket error occurred: {e}")
        return f"Socket error occurred: {e}", False


def connect_to_server(client: socket.socket, target_host: str, target_port: int, verbose: bool) -> str:
    """
    Sends data to the server via UDP and receives a response.

    Args:
        client (socket.socket): Socket object.
        target_host (str): Target host to connect to.
        target_port (int): Target port to connect to.
        verbose (bool): Flag for verbose output.

    Returns:
        str: Received data from the server or error message.
    """
    try:
        data_to_send = input("Enter data to send (or 'exit' to quit): ")

        if not data_to_send:
            logger.warning("Empty input received.")
            print("Empty input. Please enter some data.")
            return ''

        if len(data_to_send.encode()) > MAX_SIZE:
            logger.warning(f"Input data exceeds maximum UDP datagram size ({MAX_SIZE} bytes).")
            print(f"Input data exceeds maximum UDP datagram size ({MAX_SIZE} bytes). Please enter shorter data.")
            return ''

        if data_to_send.lower() == 'exit':
            return 'exit'

        if not send_data(client, data_to_send, target_host, target_port):
            return "Failed to send data"

        if verbose:
            print(f"Sent data: {data_to_send}")

        received_data, success = receive_data(client)
        if success:
            logger.info(f"Received data: {received_data}")
            if verbose:
                print(f"Received data: {received_data}")
        return received_data

    except Exception as e:
        error_message: str = traceback.format_exc()
        logger.error(f"Error in connection: {e}\n{error_message}")
        raise


def signal_handler(signum, frame):
    """
    Handles system signals for graceful shutdown.
    """
    print("\nProgram interrupted. Exiting.")
    logger.warning("Application terminated by signal")
    sys.exit(0)


def main() -> None:
    """
    Main function to run the UDP client.
    """
    args = parse_arguments()

    if args.log:
        logger.addHandler(logging.FileHandler(args.log))

    print(f"UDP Client started. Connecting to {args.host}:{args.port}")
    print("Enter 'exit' to quit the program.")

    if args.verbose:
        print(f"Verbose mode: ON")
        print(f"Timeout: {args.timeout} seconds")
        print(f"Log file: {args.log if args.log else 'Not specified'}")

    client = create_socket(args.timeout)
    if not client:
        return

    # Set up signal handling
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        while True:
            print("\n" + SEPARATOR)
            received_data = connect_to_server(client, args.host, args.port, args.verbose)
            if received_data == 'exit':
                print("Exiting program.")
                break
            if not received_data:
                print("No response from server.")
                continue
            print(f"\nReceived: {received_data}")
    finally:
        client.close()
        logger.info("Closed the client socket")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
        logger.warning("Application terminated by user")
    except Exception as error:
        detailed_error_message = traceback.format_exc()
        logger.error(f"Unexpected error in the application: {error}\n{detailed_error_message}")
    finally:
        logger.info("Application finished")
