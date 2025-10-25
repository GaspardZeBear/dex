import asyncio
import threading
from websockets.server import serve
import logging
import sys
from  Agent import *
#loglevel=logging.WARNING
#loglevel=logging.DEBUG
#logging.basicConfig(stream=sys.stdout,format="%(asctime)s %(module)s t=%(thread)s %(name)s %(funcName)s %(lineno)s %(levelname)s %(message)s", level=loglevel)


#----------------------------------------------------------------------------
class LoopRunner() :
  def __init__(self,loopId,port) :
    self.id=loopId
    self.port=port
    pass

  async def init(self) :
    async with serve(self.onMessage, "", self.port):
      await asyncio.Future()  # run forever

  async def onMessage(self,websocket) :
    print(f'LoopRunner.onMessage() registering  {websocket.remote_address=} ')
    agent=Agent.register(websocket)
    async for message in websocket:
      print(f'LoopRunner.onMessage() {self.id=} received  {message=}')
      #await websocket.send(message + agent.getKey() )
      await websocket.send(f'{self.id} {message} + {agent.getKey()}')



