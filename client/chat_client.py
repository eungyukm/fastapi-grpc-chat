import sys
import os

# 서버 상위 디렉토리를 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import grpc
import chat_pb2
import chat_pb2_grpc
import asyncio

def clean_input(prompt: str) -> str:
    """
    입력된 문자열에서 비정상적인 유니코드 문자를 제거합니다.
    """
    try:
        user_input = input(prompt)
        # 비정상적인 문자(서로게이트)를 제거
        return user_input.encode("utf-8", "ignore").decode("utf-8")
    except Exception as e:
        print(f"Input error: {e}")
        return ""

async def chat(username: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # 메시지 전송을 위한 async generator
        async def send_messages():
            try:
                while True:
                    message = await asyncio.to_thread(clean_input, "You: ")
                    if message:  # 빈 메시지는 보내지 않음
                        yield chat_pb2.ChatMessage(username=username, message=message)
            except Exception as e:
                print(f"Send task error: {e}")

        # 서버로부터 메시지를 수신하는 함수
        async def receive_messages(response_iterator):
            try:
                async for response in response_iterator:
                    print(f"\n[{response.username}] {response.message}\nYou: ", end="")
            except Exception as e:
                print(f"Receive task error: {e}")

        try:
            # 양방향 스트리밍 시작
            response_iterator = stub.Chat(send_messages())

            # 서버 메시지 수신
            await receive_messages(response_iterator)

        except Exception as e:
            print(f"Disconnected: {e}")

if __name__ == "__main__":
    username = input("Enter your username: ")
    asyncio.run(chat(username))
