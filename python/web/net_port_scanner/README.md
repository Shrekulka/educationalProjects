# Project Overview
The project is an asynchronous port scanner designed to check the availability of network ports on target hosts. It utilizes the asyncio library for performing port scanning asynchronously, which allows for efficient handling of a large number of ports and hosts. The scanner supports scanning both a single target host and all network interfaces of the current host. Scanning results are saved to a CSV file and can also be output to a log.

## Project Tasks
1. Asynchronous Port Scanning: Perform port status checks on the target host asynchronously to improve performance and scalability.
2. Support for Scanning All Network Interfaces: If no target host is specified, scan ports on all network interfaces of the current host.
3. Results Recording: Save the scanning results to a CSV file for subsequent analysis.
4. Logging: Display scanning results and errors for ease of debugging and monitoring.
5. Configuration: Allow configuration of scanning parameters through configuration files and command-line arguments.

## How the Project Works
1. `Initialization:` When running the main.py script, settings are loaded, and necessary modules are initialized.
2. `Command-Line Argument Processing:` The user specifies the target host, port range for scanning, and a file for saving results.
3. `Port Scanning:` Depending on the provided arguments, ports are scanned on the specified host or on all network interfaces of the current host.
4. `Recording and Logging Results:` Scanning results are saved to a CSV file and logged.

## Features
1. `Asynchronous Execution:` Uses asynchronous programming to increase performance when scanning a large number of ports.
2. `Network Interface Support:` The network_utils.py module allows scanning all network interfaces of the current host.
3. `Service Caching:` Utilizes caching for storing service names by port numbers to avoid repeated lookups.
4. `Progress Bar:` tqdm displays scanning progress, allowing the user to monitor execution.

## Project Settings
- `MAX_CONCURRENT_TASKS:` Maximum number of concurrent asynchronous tasks.
- `CONNECT_TIMEOUT:` Timeout for connecting to a port.
- `DEFAULT_START_PORT:` Starting port for scanning.
- `DEFAULT_END_PORT:` Ending port for scanning.
- `DEFAULT_OUTPUT_FILE:` File for saving results in CSV format.
- `THREAD_POOL_MAX_WORKERS:` Maximum number of threads for performing blocking operations.
- `MAX_RETRIES:` Maximum number of attempts to retrieve a service name by port.
- `RETRY_DELAY:` Delay between attempts to retrieve a service name.

## Execution Flow
1. `Running the Script:` The user runs the script, specifying necessary arguments.
2. `Argument Initialization:` Command-line arguments are processed to determine the target host, port range, and result file.
3. `Getting Network Interfaces:` If no target host is specified, IP addresses of all network interfaces are retrieved.
4. `Port Scanning:` Asynchronous scanning of specified ports is performed.
5. `Recording and Logging:` Scanning results are written to a CSV file and logged.

## Command Line Examples

*Scanning a single host with a specified port range:*
```bash
python main.py example.com -s 1 -e 1000 -o results.csv
```

*Scanning all network interfaces of the current host:*
```bash
python main.py
```

*Scanning a specific IP address with a specified port range and output file:*
```bash
python main.py 192.168.1.1 -s 80 -e 443 -o scan_results.csv
```

*Getting help on available command-line arguments:*
```bash
python main.py -h
```

## Project Structure:

```bash
📁 net_port_scanner/                  # Root directory of the project
│
├── 📁 data/                          # Directory for storing data
│   │
│   └── port_scan_results.csv         # File with port scanning results
│ 
├── .gitignore                        # File to specify files and folders ignored by Git
│ 
├── config.py                         # Project configuration file
│ 
├── logger_config.py                  # Logging configuration
│ 
├── main.py                           # Main entry point of the application
│ 
├── network_utils.py                  # Utilities for working with the network
│ 
├── README.md                         # Project description and usage instructions
│ 
├── scanner.py                        # Module for performing asynchronous port scanning
│ 
├── requirements.txt                  # List of project dependencies
│ 
└── 📁 venv/                          # Python virtual environment directory
```