# The provided code includes two Python scripts that establish a TCP connection with a server, send data to the server,
# receive a response, and then print the received data.

Here is a step-by-step description of how both scripts work:

## Script `simple_tcp_client.py`:

1. **Import necessary modules**: The modules `socket`, `traceback`, and `logger` from `logger_config` are imported.

2. **Main function `main`**:
   - The target host and port are set: `target_host = "localhost"` and `target_port = 5050`.
   - A socket object `client` is created using IPv4 and TCP.
   - The client socket connects to the specified host and port using `client.connect((target_host, target_port))`.
   - A "Hello, world!" message is sent to the server using `client.send(b"Hello, world!")`.
   - A response is received from the server using `client.recv(4096)`.
   - The response is decoded from bytes to a string and printed to the screen.
   - The socket is closed.

3. **Running the script**:
   - If the script is run directly, the `main` function is called.
   - Exceptions `KeyboardInterrupt` and any other exceptions are handled, errors and warnings are logged.
   - The application shutdown is logged.

## Script `advanced_tcp_client.py`:

1. **Import necessary modules**: The modules `socket`, `traceback`, and `logger` from `logger_config` are imported.

2. **Function `connect_to_server`**:
   - Accepts input parameters `target_host` and `target_port`.
   - A socket object `client` is created using IPv4 and TCP.
   - An attempt to connect to the server is logged and the client connects to the server.
   - User input is requested for data to send to the server.
   - The input data is encoded into bytes and sent to the server using `client.send()`.
   - An empty byte object `data` is created to store the received data.
   - Data is received from the server in chunks up to 4096 bytes using `client.recv(4096)`.
   - The received data is added to the `data` object.
   - The receiving loop continues until no more data is received.
   - The received data is decoded from bytes to a string and returned.
   - In case of an exception, the error is logged and an exception is raised.
   - The client socket is closed and this action is logged.

3. **Main function `main`**:
   - The target host and port are set: `target_host = "localhost"` and `target_port = 5050`.
   - The `connect_to_server` function is called with the specified host and port as arguments.
   - The received data is stored in the `received_data` variable and printed to the screen.

4. **Running the script**:
   - If the script is run directly, the `main` function is called.
   - Exceptions `KeyboardInterrupt` and any other exceptions are handled, errors and warnings are logged.
   - The application shutdown is logged.

## Usage:

1. **Set the target host and port**: The variables `target_host` and `target_port` are defined in the code. Replace the 
   values of these variables with the appropriate host and port you want to connect to.
2. **Run the script**: Save the file and run it using the Python interpreter. The script will establish a connection 
   with the specified host and port, send data to the server, receive a response, and print it to the screen.
3. **Enter data to send**: In the case of `advanced_tcp_client.py`, after running the script, you will be prompted to 
   enter the data to be sent to the server. Enter the necessary data and press Enter.
4. **Wait for a response**: The script will wait for a response from the server. When the response is received, it will 
   be printed to the screen.

*Important:*
Ensure that the target server is available and running on the specified host and port. Otherwise, the script may fail to
establish a connection or encounter an error when sending data.

This is the basic process for using these scripts. You can customize the code and make changes to meet your needs and 
requirements for interacting with the server.
