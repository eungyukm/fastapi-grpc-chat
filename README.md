# FastAPI gRPC Chat

A real-time chat application built using **FastAPI** for WebSocket communication and **gRPC** for server-to-server communication.

---

## 📜 **Overview**

This project demonstrates how to combine **FastAPI** (WebSocket) and **gRPC** to build a scalable real-time chat system.  
- FastAPI handles WebSocket communication between clients.  
- gRPC handles communication between multiple servers to broadcast messages efficiently.

---

## 🚀 **Features**

- **Real-Time Chat**: WebSocket enables instant messaging between users.
- **Server-to-Server Communication**: gRPC broadcasts messages across servers.
- **Scalable Architecture**: Easily extendable to support multiple servers.
- **Protocol Buffers**: Efficient serialization for gRPC communication.

---

## 🛠️ **Technologies Used**

| **Technology**    | **Purpose**                             |
|-------------------|-----------------------------------------|
| **gRPC**          | Server-to-server communication          |
| **Protocol Buffers** | gRPC message serialization            |
| **Python 3.8+**   | Programming language                    |

---

## 📂 **Project Structure**

```plaintext
chat_project/
│-- proto/                     # gRPC .proto files
│   └── chat.proto
│-- server/
│   ├── grpc_server.py         # gRPC server implementation
│   └── fastapi_server.py      # FastAPI server with WebSocket support
│-- client/
│   └── chat_client.py         # WebSocket chat client
│-- requirements.txt           # Python dependencies
