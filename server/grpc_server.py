import sys
import os

# 서버 상위 디렉토리를 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import chat_pb2_grpc
import grpc
import asyncio

# 서버에서 gRPC 채팅을 처리하는 클래스
class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.clients = []  # 모든 클라이언트의 context를 저장

    async def Chat(self, request_iterator, context):
        """
        클라이언트로부터 메시지를 수신하고, 모든 클라이언트에게 메시지를 브로드캐스트합니다.
        """
        # 현재 클라이언트의 메시지를 수신하고 브로드캐스트
        self.clients.append(context)  # 새 클라이언트 추가
        print(f"New client connected: {context.peer()}")

        try:
            async for message in request_iterator:
                print(f"[{message.username}] {message.message}")
                # 연결된 모든 클라이언트에게 메시지 브로드캐스트
                await self.broadcast_message(message)
        except Exception as e:
            print(f"Client disconnected: {e}")
        finally:
            # 연결이 끊어진 클라이언트 제거
            self.clients.remove(context)

    async def broadcast_message(self, message):
        """
        모든 연결된 클라이언트에게 메시지를 전송합니다.
        """
        disconnected_clients = []
        for client in self.clients:
            try:
                await client.write(message)  # 메시지를 각 클라이언트에게 전송
            except Exception as e:
                print(f"Error sending to client: {e}")
                disconnected_clients.append(client)

        # 연결이 끊긴 클라이언트를 리스트에서 제거
        for client in disconnected_clients:
            self.clients.remove(client)

async def serve():
    """
    gRPC 서버 실행
    """
    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    print("Starting gRPC server on port 50051...")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
