# This project implements a simple gRPC server for performing basic arithmetic operations, such as addition,
# subtraction, multiplication, and division. The project uses Google Protocol Buffers (protobuf) to define the structure 
# of messages and gRPC to exchange these messages between the client and server.

## Key Components of the Project
- `unary.proto:` A file defining the protocol for the gRPC service, including request and response messages, as well as 
   service methods.
- `unary_server.py:` The server script that implements the gRPC service. It receives requests to perform arithmetic 
   operations and sends back the results.
- `unary_pb2.py` and `unary_pb2_grpc.py:` Generated Python files necessary for working with gRPC and protobuf. These 
   files are created based on `unary.proto`.

## Project Setup
Before starting the server, you need to perform a few setup steps:

*Install Dependencies:*
To work with gRPC and protobuf, you need to install the necessary libraries. Run the following command to install all 
dependencies:
```bash
pip install -r requirements.txt
```
*In this project, the necessary files have already been generated using the following commands:*
```bash
python -m grpc_tools.protoc --proto_path=. ./unary.proto --python_out=. --grpc_python_out=.
```
*Explanation:*
`--proto_path=.`: Specifies the directory where the .proto file is located. 
`--python_out=.`: Specifies the directory where the generated Python files for protobuf messages will be saved. 
`--grpc_python_out=.`: Specifies the directory where the generated Python files for gRPC will be saved.

As a result of these steps, `unary_pb2.py` and `unary_pb2_grpc.py` files were created based on the definition in 
`unary.proto`. These files are necessary for the gRPC server and client to function.

## What the Code Does

1. `unary.proto` defines:
   - The Operation enumeration with operation types: ADD, SUBTRACT, MULTIPLY, DIVIDE.
   - The CalculationRequest and CalculationResponse messages that describe the format of requests and responses.
   - The Calculator gRPC service with a unary method Calculate.
2. `unary_server.py` implements the server:
   - The CalculatorServicer class implements the Calculate method, which performs the arithmetic operation specified in 
     the request.
   - The serve() method initializes the gRPC server, registers the CalculatorServicer, and starts the server on port 50051.
   
## Sequence of Operations
1. The client sends a CalculationRequest to the server with two numbers and the type of operation.
2. The server receives the request and passes it to the Calculate method.
3. The Calculate method performs the operation (addition, subtraction, multiplication, or division) and forms a CalculationResponse.
4. The server sends the response back to the client.

## Interacting with Postman
*Postman supports testing gRPC requests. Here's how you can set up and test the gRPC service:*

1. Start the gRPC server:
    ```bash
    python unary_server.py
    ```
2. Open Postman and create a new gRPC request:
   - Click on "New" and select "gRPC Request".
   - Enter the server address: localhost:50051.
3. Select the service and method:
   - Postman will automatically load available services and methods if reflection is enabled.
   - Choose the Calculator service and the Calculate method.
4. Configure the request body: 
   *Example request for an addition operation:*
    ```bash
    {
      "num1": 10,
      "num2": 5,
      "operation": "ADD"
    }
    ```
5. Send the request and view the response:
   - Click "Send" to send the request to the server.
   - The response from the server will be displayed on the right side of the Postman window.
   
## Differences Between RPC Types

| Characteristic         | Unary RPC                 | Server Streaming RPC             | Client Streaming RPC               | Bidirectional Streaming RPC             |
|------------------------|---------------------------|----------------------------------|------------------------------------|-----------------------------------------|
| **Definition in proto**| One request, one response | One request, stream of responses | Stream of requests, one response   | Stream of requests, stream of responses |
| **`stream` keyword**   | Not used                  | Used for response                | Used for request                   | Used for request and response           |
| **Server Method**      | Regular function          | Uses `yield`                     | Accepts iterator                   | Accepts and returns iterator            |
| **Data Handling**      | One-time                  | Sequential sending               | Aggregation of incoming data       | Interactive exchange                    |
| **Use Case**           | Simple requests           | Sending large volumes of data    | Sending a stream of data to server | Chat, real-time interaction             |

## Conclusion
This project demonstrates the implementation of a basic gRPC service for performing arithmetic operations. It uses a 
unary RPC type, which makes it suitable for simple requests and responses. Postman is a convenient tool for testing gRPC
services due to its support for gRPC requests and dynamic service discovery.

## Project Structure:

```bash
📁 unary_grpc_calculator/              # Root directory of the project
│
├── unary.proto                        # Protocol Buffers file containing gRPC messages and service definitions
│
├── unary_pb2.py                       # Generated Python file for Protocol Buffers messages
│
├── unary_pb2_grpc.py                  # Generated Python file for gRPC services and methods
│
├── unary_server.py                    # Implementation of the gRPC server with request handling logic
│
├── .gitignore                         # File to ignore files and directories in Git
│
├── README.md                          # Project description, installation, and usage instructions
│
├── requirements.txt                   # Dependency file for installing necessary libraries
│
├── logger_config.py                   # Logger configuration
│
└── 📁 venv/                           # Python virtual environment for isolating project dependencies
```
