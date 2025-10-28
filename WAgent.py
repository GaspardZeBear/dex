import asyncio
import websockets
import random
import time
import json



#--------------------------------------------------------------------------
async def main():
  while True :
    tasks = []
    for i in range(0,2) :
      tasks.append(asyncio.create_task(cnx(i)))
    await asyncio.wait(tasks)
    print("main() over, retry")
    await asyncio.sleep(10)

#--------------------------------------------------------------------------
# Function to handle the client
async def cnx(num):
  async with websockets.connect(f'ws://localhost:{random.choice([8080,8080,8080])}') as websocket:
      message={
        "cmd" : "capacities",
        "payload" : {
          "node" : "node",
          "cpu" : 2,
          "mem" : 512
       }
      }
      await websocket.send(json.dumps(message))
      response = await websocket.recv()
      print(f"Received: {response}")
      response = await websocket.recv()
      while True:
        await asyncio.sleep(random.randrange(5,10))
        # Send the message to the server
        #message=time.ctime()
        message={ "cmd" : "ping", "payload" : f'{time.ctime()}'}
        await websocket.send(json.dumps(message))
        # Receive a message from the server
        response = await websocket.recv()
        print(f"Received: {response}")

# Run the client
if __name__ == "__main__":
  asyncio.run(main())

