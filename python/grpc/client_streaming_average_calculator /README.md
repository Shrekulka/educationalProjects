# This project implements a gRPC server and client for calculating the average of a stream of numbers sent by the client.
# The project uses Google Protocol Buffers (protobuf) to define the message structure and gRPC to exchange these
# messages between the client and the server.

## Main components of the project
- `client_streaming.proto`: The protocol file that defines the message structure and the gRPC service method for 
   calculating the average.
- `client_streaming_server.py`: The server script that implements the gRPC service. It receives a stream of numbers, 
   computes their average, and returns the result.
- `client_streaming_pb2.py` and `client_streaming_pb2_grpc.py`: Generated Python files needed to work with gRPC and
   protobuf. These files are created based on `client_streaming.proto`.

## Setting up the project

Before starting the server, several setup steps need to be completed:

*Install dependencies:*
To work with gRPC and protobuf, you need to install the relevant libraries. Run the following command to
install all dependencies:
```bash
pip install -r requirements.txt
```
*In this project, the necessary files have already been generated using the following commands:*
```bash
python -m grpc_tools.protoc --proto_path=. ./client_streaming.proto --python_out=. --grpc_python_out=.
```
*Explanations:*
`--proto_path=.`: Specifies the directory where the .proto file is located. 
`--python_out=.`: Specifies the directory where the generated Python files for protobuf messages will be saved. 
`--grpc_python_out=.`: Specifies the directory where the generated Python files for gRPC will be saved.

As a result of these steps, the files `client_streaming_pb2.py` and `client_streaming_pb2_grpc.py` were created based on
the definitions in `client_streaming.proto`. These files are necessary for the operation of the gRPC server and client.

## What the code does
1. The file `client_streaming.proto` defines:
   - The NumberRequest message for sending numbers in a stream.
   - The AverageResponse message, which returns the result of the average calculation.
   - The gRPC service AverageCalculator with the client-streaming method CalculateAverage.
2. The file `client_streaming_server.py` implements the server:
   - The class AverageCalculatorServicer implements the CalculateAverage method, which takes a stream of numbers and 
     computes their average.
   - The serve() method initializes the gRPC server, registers the AverageCalculatorServicer, and starts the server on 
     port 50053.

## Sequence of operations
1. The client sends a stream of NumberRequest requests to the server, containing numbers.
2. The server receives the stream of requests and passes them to the CalculateAverage method.
3. The CalculateAverage method computes the average from the received stream of numbers.
4. The server sends an AverageResponse to the client, containing the average value.

## Interaction with Postman

*Postman supports testing gRPC requests, including client-streaming requests. Here’s how you can set up and test the 
gRPC service:*
1. Start the gRPC server:
    ```bash
    python client_streaming_server.py
    ```
2. Open Postman and create a new gRPC request:
   - Click on "New" and select "gRPC Request".
   - Enter the server address: localhost:50053.
3. Choose the service and method:
   - Postman will automatically load available services and methods if reflection is enabled.
   - Select the AverageCalculator service and the CalculateAverage method.
4. Set up the request stream: Example request to send multiple numbers:
*On the right side of the selected method, click the `Invoke` button*
   - Enter and send the first message: { "number": 10 }
   - Enter and send the second message: { "number": 20 }
   - Enter and send the third message: { "number": 30 }
   - Enter and send the fourth message: { "number": 40 }
   - For the fifth time, click the button (next to `send`) `End Streaming`:
5. The response from the server with the average value will be displayed on the right side of the Postman window.

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
This project demonstrates the implementation of a client-streaming gRPC service for calculating the average from a 
stream of numbers. Client-streaming RPC allows sending a continuous stream of data from the client to the server, making
it suitable for tasks that require data aggregation on the server side before sending the final response. Using Postman
to test gRPC services simplifies the debugging and verification process of the service.

## Project Structure:

```bash
📁 client_streaming_average_calculator/ # Root directory of the project
│
├── client_streaming.proto              # Protocol Buffers file containing message and gRPC service definitions
│
├── client_streaming_pb2.py             # Generated Python file for Protocol Buffers messages
│
├── client_streaming_pb2_grpc.py        # Generated Python file for gRPC services and methods
│
├── client_streaming_server.py          # Implementation of the gRPC server with request handling logic
│
├── .gitignore                          # File to ignore files and directories in Git
│
├── README.md                           # Project description, installation, and usage instructions
│
├── requirements.txt                    # File with project dependencies for installing necessary libraries
│
├── logger_config.py                    # Logger configuration
│
└── 📁 venv/                            # Python virtual environment for isolating project dependencies
```