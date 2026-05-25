# This project implements a gRPC server and client for streaming string analysis. The server accepts a string for analysis
# and returns the analysis results using gRPC streams. The project uses Google Protocol Buffers (protobuf) to define
# the structure of messages and gRPC to exchange these messages between the client and server.

## Main Components of the Project
- `streaming.proto`: A file that defines the protocol for the gRPC service, including request and response messages, as
   well as service methods.
- `streaming_server.py`: The server script that implements the gRPC service. It accepts strings for analysis and sends
   back the results as data streams.
- `streaming_pb2.py` and `streaming_pb2_grpc.py`: Generated Python files needed to work with gRPC and protobuf.
   These files are created based on `streaming.proto`.

## Project Setup

Before running the server, you need to perform a few setup steps:

*Install dependencies:*
To work with gRPC and protobuf, you need to install the necessary libraries. Run the following command to install all 
dependencies:
```bash
pip install -r requirements.txt
```
*In this project, the required files have already been generated using the following commands:*
```bash
python -m grpc_tools.protoc --proto_path=. ./streaming.proto --python_out=. --grpc_python_out=.
```
*Explanations:*
`--proto_path=.`: Specifies the directory where the .proto file is located. 
`--python_out=.`: Specifies the directory where the generated Python files for protobuf messages will be saved. 
`--grpc_python_out=.`: Specifies the directory where the generated Python files for gRPC will be saved.

As a result of these steps, the `streaming_pb2.py` and `streaming_pb2_grpc.py` files will be created based on the 
definitions in `streaming.proto`. These files are necessary for the gRPC server and client to function.

## What the Code Does
1. The `streaming.proto` file defines:
   - The StreamDataRequest and StreamDataResponse messages, which describe the format of requests and responses.
   - The StreamingService gRPC service with methods for streaming string analysis.
2. The `streaming_server.py` file implements the server:
   - The StringAnalyzerStreamingServicer class implements the StreamData method, which analyzes a string and sends a 
     stream of results.
   - The serve() method initializes the gRPC server, registers the StringAnalyzerStreamingServicer, and starts the 
     server on port 50052.
   
## Operation Sequence
1. The client sends a StreamDataRequest to the server with the input string for analysis.
2. The server receives the request and passes it to the StreamData method.
3. The StreamData method performs string analysis (checking for palindromes, counting words, letters, spaces, special 
   characters, uppercase, and lowercase letters) and returns a stream of StreamDataResponse.
4. The server sends the analysis results back to the client through the stream.

## Interaction with Postman

*Postman supports testing gRPC requests. Here’s how you can set up and test the gRPC service:*
1. Start the gRPC server:
    ```bash
    python streaming_server.py
    ```
2. Open Postman and create a new gRPC request:
   - Click on "New" and select "gRPC Request".
   - Enter the server address: localhost:50052.
3. Select the service and method:
   - Postman will automatically load available services and methods if reflection is enabled.
   - Choose the StreamingService service and the StreamData method.
4. Configure the request body: 
   *Example request for string analysis:*
    ```bash
    {
      "input_text": "Hello World"
    }
    ```
5. Send the request and view the stream of responses:
   - Click "Send" to send the request to the server.
   - The right side of the Postman window will display the stream of server responses.
   
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
This project demonstrates the implementation of a gRPC service for streaming string analysis. The use of streaming RPC 
makes it suitable for tasks that require sequential processing and transmission of results. Postman is a convenient tool
for testing gRPC services, thanks to its support for gRPC requests and dynamic service discovery.

## Project Structure:

```bash
📁 streaming_grpc_string_analyzer/     # Root directory of the project
│
├── streaming.proto                    # Protocol Buffers file containing gRPC service and message definitions
│
├── streaming_pb2.py                   # Generated Python file for Protocol Buffers messages
│
├── streaming_pb2_grpc.py              # Generated Python file for gRPC services and methods
│
├── streaming_server.py                # Implementation of the gRPC server with request handling logic
│
├── .gitignore                         # File to ignore certain files and directories in Git
│
├── README.md                          # Project description, installation, and usage instructions
│
├── requirements.txt                   # Project dependencies for installing necessary libraries
│
├── logger_config.py                   # Logger configuration
│
└── 📁 venv/                           # Python virtual environment for isolating project dependencies
```
