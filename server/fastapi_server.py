import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import grpc
import chat_pb2
import chat_pb2_grpc
import asyncio

app = FastAPI()

# gRPC 채널 및 클라이언트 설정
grpc_channel = grpc.insecure_channel("localhost:50051")
grpc_client = chat_pb2_grpc.ChatServiceStub(grpc_channel)

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    print(f"WebSocket connected: {username}")
    try:
        while True:
            data = await websocket.receive_text()
            # gRPC를 통해 메시지를 전송
            message = chat_pb2.ChatMessage(username=username, message=data)
            grpc_client.SendMessage(message)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected: {username}")