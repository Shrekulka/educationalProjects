# This project is a steganography tool that allows for hiding and encrypting messages in images, as well as extracting 
# and decrypting them.

*Steganography* is a method of hiding information within other data, such as images, so that the information is not 
visible during normal viewing. In this project, messages are not only hidden in images but also encrypted using a 
cryptographic algorithm to ensure their security and protection against unauthorized access.

## Main Components
1. *config.py:*
   - Contains application configuration parameters such as image paths, encryption keys, default actions, and console 
     color styles.
   - Uses the pydantic library for managing configuration and environment variables.

2. *steganography.py:*
   - Defines the `Steganographer` class, which performs steganography: hiding messages in images and extracting them.
   - Uses Fernet encryption from the cryptography library to protect messages and stegano for embedding and extracting 
     messages in/from images.

3. *cli.py:*
   - Handles command-line arguments using the argparse library.
   - Defines functions to parse arguments and perform actions based on the provided arguments (hiding or extracting 
     messages).

4. *main.py:*
   - The main script that starts the application.
   - Processes command-line arguments or performs default actions using configuration from `config.py` and functionality
     from `steganography.py`.

## Code Execution Flow
1. Initialization:
   - Configuration is loaded from `config.py` when creating a `Settings` instance.
   - When the `main.py` script is executed, an instance of `Steganographer` is created using the secret from the 
     configuration.

2. Command-Line Processing:
   - `cli.py` is responsible for parsing command-line arguments.
   - Arguments specify what to do (hide or extract a message) and which files to use.

3. Action Execution:
   - Based on command-line arguments, the `hide_payload` or `extract_payload` methods of the `Steganographer` class are
     called:
     - `hide_payload` hides an encrypted message in an image.
     - `extract_payload` extracts and decrypts a message from an image.

4. Default Handling:
   - If no command-line arguments are provided, `main.py` performs a default action, either hiding or extracting a
     message from files specified in the configuration.

## *Command-Line Usage*

*The application can be used via the command line to perform the following actions:*

1. Hide a message:
    ```bash
    ./dist/main hide <path_to_image> --message '<message>'
    ```
    - `hide`: Indicates the need to hide a message.
    - `<path_to_image>`: Path to the image where the message will be hidden.
    - `--message "<message>"`: The message to be hidden. If not specified, the default value is used.
    *Example:*
   ```bash
   ./dist/main hide ./input_image/1.jpg --message 'Run, they are after you, buy Coca-Cola on the way!'
   ```
2. Extract a message:
    ```bash
    ./dist/main extract <path_to_image>
    ```
    - extract: Indicates the need to extract a message.
    - <path_to_image>: Path to the image from which the message will be extracted.
    Example:
    ```bash
    ./dist/main extract ./output_image/stego_20240726_087fdbad23f8b566.jpg  
    ```

## *Usage via IDE*

*In an IDE, you can perform the same actions as from the command line, but using the IDE's built-in capabilities for*
*running code:*
1. Hide a message:
- Run main.py with arguments passed in the IDE's run configuration.

2. Extract a message:
- Run main.py with arguments for extracting a message.

## Features
1. Configuration:
- Configuration parameters can be modified in config.py or in a .env file used for loading environment variables.

2. Encryption and Decryption:
- Fernet encryption is used to protect hidden messages.

3. Format Support:
- Supports images with .jpg, .jpeg, and .png extensions.

4. Logging:
- Error and message logging is handled using settings in logger_config.py.

5. Error Handling:
- In case of errors, the program logs them and provides the user with information about encountered issues.

This project is a useful tool for hiding and extracting data in images and can be adapted for various tasks related to 
information protection and concealment.

## Project Structure:

```bash
📁 messages_to_images_and_back/  # Root directory of the project, containing all files and folders.
│
├── 📁 build/                    # Directory where files created by the builder (e.g., PyInstaller) are placed during 
│                                # the build.
├── 📁 dist                      # Directory containing compiled executable files (e.g., created by PyInstaller).
│
├── 📁 input_image               # Directory for storing input images to be processed.
│
├── 📁 output_image              # Directory for storing output images where hidden messages are saved.
│
├── 📁 venv                      # Directory for Python virtual environment, containing installed packages and 
│                                # dependencies.
├── .gitignore                   # File for ignoring specific files and directories when working with Git.
│
├── cli.py                       # Script for command-line interface, argument parsing, and executing actions 
│                                # (hiding/extracting messages).
├── config.py                    # Configuration file containing application settings (file paths, keys, and other 
│                                # parameters).
├── logger_config.py             # Logger configuration file defining log format and level.
│
├── main.py                      # Main script of the application, containing the entry point and managing execution logic.
│
├── main.spec                    # Spec file for the builder (e.g., PyInstaller) describing how to build the application.
│
├── profiling_results.prof       # Profiling results file used for performance analysis.
│
├── requirements.txt             # File listing Python package dependencies required for the project.
│
├── README.md                    # File with project description, installation, and usage instructions.
│
└── steganography.py             # Module for performing steganographic operations (hiding and extracting messages).
```