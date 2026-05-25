# This project implements a bidirectional streaming gRPC service for real-time messaging. 
# The project uses Google Protocol Buffers (protobuf) to define the structure of messages and gRPC for exchanging 
# these messages between the client and the server.

## Main Components of the Project
- `bidirectional_streaming.proto:` A file that defines the protocol for the gRPC service, including chat messages and 
   the service method.
- `bidirectional_streaming_server.py:` The server script that implements the gRPC service. It handles bidirectional 
   streaming of messages between clients and the server.
- `bidirectional_streaming_pb2.py` and `bidirectional_streaming_pb2_grpc.py:` Generated Python files required 
   for working with gRPC and protobuf. These files are created based on `bidirectional_streaming.proto`.

## Project Setup
Before starting the server, several setup steps need to be performed:

*Install dependencies:*
To work with gRPC and protobuf, you need to install the necessary libraries. Run the following command to 
install all dependencies:
```bash
pip install -r requirements.txt
```
*In this project, the necessary files have already been generated using the following commands:*
```bash
python -m grpc_tools.protoc --proto_path=. ./bidirectional_streaming.proto --python_out=. --grpc_python_out=.
```
*Explanations:* 
`--proto_path=.`: Specifies the directory where the .proto file is located. 
`--python_out=.`: Specifies the directory where the generated Python files for protobuf messages will be saved. 
`--grpc_python_out=.`: Specifies the directory where the generated Python files for gRPC will be saved.

As a result of these steps, the files `bidirectional_streaming_pb2.py` and `bidirectional_streaming_pb2_grpc.py` have 
been created based on the definition in `bidirectional_streaming.proto`. These files are necessary for the gRPC server 
and client to function.

## What the Code Does
1. The file `bidirectional_streaming.proto` defines:
   - The ChatMessage message with fields for the user's name, message text, and timestamp.
   - The gRPC service ChatService with the Chat method, which implements bidirectional streaming RPC.
2. The file `bidirectional_streaming_server.py` implements the server:
   - The ChatServicer class implements the Chat method, which provides bidirectional streaming of messages.
   - The serve() method initializes the gRPC server, registers the ChatServicer, and starts the server on port 50054.
   
## Sequence of Operations
1. The client sends messages to the stream using the Chat method.
2. The server receives the messages and adds them to a shared message list.
3. The server continuously sends new messages to clients connected to the service.
4. Clients receive messages in real-time.

## Interacting with Postman

*Postman supports testing gRPC requests. Here’s how you can set up and test the gRPC service:*
1. Start the gRPC server:
    ```bash
    python bidirectional_streaming_server.py
    ```
2. Open Postman and create a new gRPC request:
   - Click on "New" and select "gRPC Request".
   - Enter the server address: localhost:50054.
3. Select the service and method:
   - Postman will automatically load available services and methods if reflection is enabled.
   - Select the ChatService and the Chat method.
4. Configure the request and response stream: Example request:
    ```bash
    {
      "user_name": "Alice",
      "message": "Hello, world!",
      "timestamp": 1692948482000
    }
    ```
5. Send the request and view the response:
   - Click "Send" to send the request to the server.
   - The server's response will be displayed on the right side of the Postman window.
   
## Differences Between RPC Types

| Characteristic           | Unary RPC                           | Server-Side Streaming RPC                                          | Client-Side Streaming RPC                               | Bidirectional Streaming RPC          |
|--------------------------|-------------------------------------|--------------------------------------------------------------------|---------------------------------------------------------|--------------------------------------|
| Data Direction           | Client → Server → Client            | Client → Server → Client (multiple times)                          | Client (multiple times) → Server → Client               | Client ↔ Server                      |
| Number of Requests       | One                                 | One                                                                | Multiple                                                | Multiple                             |
| Number of Responses      | One                                 | Multiple                                                           | One                                                     | Multiple                             |
| Example Use Case         | Simple operations (e.g., calculator)| Sending large volumes of data to the client (e.g., string analysis)| Sending a stream of data to the server (e.g., averaging)| Continuous data exchange (e.g., chat)|
| Implementation Complexity| Low                                 | Medium                                                             | Medium                                                  | High                                 |
| State Management         | Simple                              | Medium (server-side)                                               | Medium (client-side)                                    | Complex (both sides)                 |
| Latency                  | Low                                 | Medium                                                             | Medium                                                  | Can be low                           |
| Resource Usage           | Low                                 | Medium                                                             | Medium                                                  | High                                 |

## Conclusion
This project demonstrates the implementation of a bidirectional streaming gRPC service for real-time messaging. It uses
bidirectional streaming RPC, making it suitable for chat applications and other scenarios requiring continuous data 
exchange. Postman is a useful tool for testing gRPC services, thanks to its support for gRPC requests and dynamic 
service discovery.

## Project Structure:

```bash
📁 bidirectional_streaming_chat_service/ # Root directory of the project
│
├── bidirectional_streaming.proto        # Protocol Buffers file containing definitions of messages and 
│                                        # gRPC services
├── bidirectional_streaming_pb2.py       # Generated Python file for Protocol Buffers messages
│
├── bidirectional_streaming_pb2_grpc.py  # Generated Python file for gRPC services and methods
│
├── bidirectional_streaming_server.py    # Implementation of the gRPC server with request handling logic
│
├── .gitignore                           # File for ignoring files and directories in Git
│
├── README.md                            # Project description, installation, and usage instructions
│
├── requirements.txt                     # File with project dependencies for installing necessary libraries
│
├── logger_config.py                     # Logger configuration
│
└── 📁 venv/                             # Python virtual environment for isolating project dependencies
```