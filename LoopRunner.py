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
    self.msgCount=0
    pass

  async def init(self) :
    async with serve(self.onMessage, "", self.port):
      await asyncio.Future()  # run forever

  def beforeMessage(self) :
    self.msgCount += 1

  def afterMessage(self) :
    pass

  async def onMessage(self,websocket) :
    print(f'LoopRunner.onMessage() default should be overrided ')
    async for message in websocket:
      print(f'LoopRunner.onMessage() {self.id=} received  {message=}')
      await websocket.send(f'{self.id} echo {message}')

  async def _onMessage(self,websocket) :
    logging.debug(f'LoopRunner._onMessage() contacted by {websocket.remote_address=} ')
    self.beforeMessage()
    #async for message in websocket:
    #  print(f'LoopRunner.onMessage() {self.id=} received  {message=}')
    #  await websocket.send(f'{self.id} {message}')
    await self.onMessage(websocket)
    self.after()

#----------------------------------------------------------------------------
##class Controller(LoopRunner) :
##
##  def __init__(self,loopId,port) :
##    super().__init__(loopId,port) 
##    self.agents={}
##
##  async def onMessage(self,websocket) :
##    print(f'Controller.onMessage() registering  {websocket.remote_address=} ')
##        #logging.warning(f'{dir(websocket)}')
##    key=Agent.getKey0(websocket)
##    if key not in self.agents :
##      agent=Agent(websocket)
##      self.agents[key]=agent
##    agent=self.agents[key]
##
##    async for message in websocket:
##      self.beforeMessage()
##      agent=self.agents[key]
##      agent.addMsgCount()
##      #print(f'LoopRunner.onMessage() {Agent.getKey0(websocket)=} {self.agents.keys()=}')
##      print(f'LoopRunner.onMessage() {self.id=} {Agent.getKey0(websocket)=} received  {self.msgCount=} {agent.getMsgCount()=} last {message=}',flush=True)
##      #await websocket.send(message + agent.getKey() )
##      await websocket.send(f'{self.id}  {Agent.getKey0(websocket)=} {agent.getMsgCount()=} {agent.getKey()=} {message=}')
##      self.afterMessage()
##
