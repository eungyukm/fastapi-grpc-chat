import asyncio
import websockets

async def chat(username: str):
    uri = f"ws://localhost:8000/ws/{username}"
    async with websockets.connect(uri) as websocket:
        print("Connected to the chat server.")
        while True:
            message = input("You: ")
            await websocket.send(message)
            print("Message sent.")

if __name__ == "__main__":
    username = input("Enter your username: ")
    asyncio.run(chat(username))