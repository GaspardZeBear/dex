import asyncio
import websockets
import random
import time



async def main():
    tasks = []
    for i in range(0,10) :
      tasks.append(asyncio.create_task(cnx(i)))
    await asyncio.wait(tasks)


# Function to handle the client
async def cnx(num):
    async with websockets.connect(f'ws://localhost:{random.choice([8080,8081,8082])}') as websocket:
        while True:
            # Prompt the user for a message
            await asyncio.sleep(random.randrange(0,10))
            # Send the message to the server
            message=time.ctime()
            await websocket.send(message)
            # Receive a message from the server
            response = await websocket.recv()
            print(f"Received: {response}")

# Run the client
if __name__ == "__main__":
    asyncio.run(main())
