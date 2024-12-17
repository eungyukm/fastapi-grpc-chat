import grpc
from concurrent import futures
import time

import chat_pb2
import chat_pb2_grpc

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.subscribers = []

    def SendMessage(self, request, context):
        print(f"[gRPC] {request.username}: {request.message}")
        for subscriber in self.subscribers:
            subscriber.write(request)
        return chat_pb2.Empty()

    def StreamMessages(self, request, context):
        print("[gRPC] New subscriber connected.")
        self.subscribers.append(context)
        try:
            while True:
                time.sleep(1)
        except:
            self.subscribers.remove(context)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Server running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()