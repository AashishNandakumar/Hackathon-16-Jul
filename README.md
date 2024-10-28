# Zypher Chronicles

A secure, end-to-end encrypted chat application built with Python, featuring RSA encryption and a Tkinter-based GUI interface.

## Features

- 🔒 End-to-end encryption using RSA-2048
- 💬 Real-time messaging capabilities
- 👥 Multiple client support
- 🖥️ GUI interface for both server and client
- 🔑 Automatic key exchange and management
- 🌐 Network-based communication using sockets

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.6+
- pycryptodome library for encryption
- tkinter (usually comes with Python)

```bash
pip install pycryptodome
```

## Project Structure
```
└── ./
    ├── src
    │   ├── client.py    # Client-side implementation with GUI and encryption
    │   └── server.py    # Server implementation handling multiple clients
    └── README.md        # Project documentation
```

### Client.py
The client component provides:
- GUI interface for sending/receiving messages
- RSA key pair generation (2048-bit)
- Message encryption/decryption
- Real-time message handling
- Automatic server connection management

### Server.py
The server component handles:
- Multiple client connections using threading
- Public key distribution and management
- Message broadcasting
- Connection status monitoring
- GUI interface for server logs

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd zypher-chronicles
```

2. Install the required dependencies:
```bash
pip install pycryptodome
```

## Usage

### Starting the Server

1. Navigate to the src directory:
```bash
cd src
```

2. Run the server script:
```bash
python server.py
```

The server GUI will launch and display:
- Connection logs
- Message activity
- Client status updates

### Connecting Clients

1. Open a new terminal and navigate to the src directory:
```bash
cd src
```

2. Run the client script:
```bash
python client.py
```

3. Use the client GUI to:
- Send encrypted messages
- View received messages
- Monitor connection status

> **Note**: The default connection settings use `192.168.0.131:5000`. Modify these values in both `server.py` and `client.py` if needed for your network configuration.

## Security Features

### Encryption
- RSA-2048 encryption for all messages
- PKCS1_OAEP padding scheme
- Unique key pair generation per session
- Secure key exchange protocol

### Privacy
- No message persistence
- In-memory key storage only
- No logging of message content
- No user data storage

## Technical Details

### Communication Flow
1. Server starts and listens for connections
2. Client connects and initiates key exchange
3. Public keys are exchanged between client and server
4. Messages are encrypted with recipient's public key
5. Server broadcasts encrypted messages to appropriate clients
6. Clients decrypt messages using their private keys

### Threading Model
- Server uses multiple threads to handle:
  - Client connections
  - Message broadcasting
  - GUI updates
- Client uses separate threads for:
  - Message receiving
  - GUI updates
  - Connection management

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security Considerations

- RSA encryption implementation is suitable for educational purposes
- Additional security measures recommended for production use:
  - Perfect forward secrecy
  - Message authentication codes
  - Secure key storage
  - User authentication

## Future Improvements

- [ ] Implement perfect forward secrecy
- [ ] Add user authentication system
- [ ] Support file transfers
- [ ] Add group chat functionality
- [ ] Implement message persistence (optional)
- [ ] Add typing indicators
- [ ] Implement read receipts
- [ ] Add emoji support
- [ ] Implement user profiles
- [ ] Add voice/video call support

## License

This project is licensed under the MIT License - see the LICENSE file for details.
