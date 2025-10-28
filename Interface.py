import asyncio
import threading
from websockets.server import serve
import logging
import sys
from  LoopRunner import *
from  Agent import *
import json
#loglevel=logging.WARNING
#loglevel=logging.DEBUG
#logging.basicConfig(stream=sys.stdout,format="%(asctime)s %(module)s t=%(thread)s %(name)s %(funcName)s %(lineno)s %(levelname)s %(message)s", level=loglevel)

#----------------------------------------------------------------------------
class Message() :

  #----------------------------------------------------------------------------------
  def __init__(self,message) :
    self.cmd=None
    try:
      msg=json.loads(message)
    except ValueError as e:
      print(f'{e}')
      return
    self.cmd=msg.get("cmd",None)
    self.payload=msg.get("payload",None)

  def getType(self) :
    return(self.cmd)
    
  def getPayload(self) :
    return(self.payload)
    

#----------------------------------------------------------------------------
class Interface(LoopRunner) :

  #----------------------------------------------------------------------------------
  def __init__(self,loopId,port,controller) :
    super().__init__(loopId,port)
    self.controller=controller

  #----------------------------------------------------------------------------------
  async def onMessage(self,websocket) :
    async for message in websocket:
      #self.beforeMessage()
      #print(f'LoopRunner.onMessage() {Agent.getKey0(websocket)=} {self.agents.keys()=}')
      logging.warning(f'Interface.onMessage() received  {self.msgCount=} last {message=}')
      #await websocket.send(message + agent.getKey() )
      msg=Message(message)
      if msg.cmd is not None :
        if msg.getType() == 'status' :
          agents=await self.controller.getAgents()
          await websocket.send(json.dumps({"cmd":"status","payload":f'{agents}'}))
        elif msg.getType() == 'launch' :
          launched=await self.controller.launch(msg.getPayload())
          await websocket.send(json.dumps({"cmd":"launch","payload":f'{launched}'}))
      else :
        await websocket.send(f'{message=}')
      #self.afterMessage()

        #----------------------------------------------------------------------------------
  async def XonMessage(self,websocket) :
    async for message in websocket:
      #self.beforeMessage()
      #print(f'LoopRunner.onMessage() {Agent.getKey0(websocket)=} {self.agents.keys()=}')
      logging.warning(f'Interface.onMessage() received  {self.msgCount=} last {message=}')
      #await websocket.send(message + agent.getKey() )
      parse=await self.parseMessage(message)
      if parse is not None :
        msg=json.loads(message)
        if parse == 'status' :
          agents=await self.controller.getAgents()
          await websocket.send(json.dumps({"cmd":"status","payload":f'{agents}'}))
        elif parse == 'book' :
          pass
      else :
        await websocket.send(f'{message=}')
      #self.afterMessage()



  #----------------------------------------------------------------------------------
  async def parseMessage(self,message) :
    try:
      msg=json.loads(message)
    except ValueError as e:
      return None
    if 'cmd' in msg :
      if msg['cmd'] == 'status' :
        return('status')
      else :
        return None
    else :
      return None

