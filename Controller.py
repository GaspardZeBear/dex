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
class Controller(LoopRunner) :

  #----------------------------------------------------------------------------------
  def __init__(self,loopId,port) :
    super().__init__(loopId,port)
    self.agents={}
    self.agentsByNode={}

  #----------------------------------------------------------------------------------
  async def registerAgent(self,websocket) :
    print(f'Controller.onMessage() registering  {websocket.remote_address=} ')
    #logging.warning(f'{dir(websocket)}')
    key=Agent.getKey0(websocket)
    if key not in self.agents :
      agent=Agent(websocket)
      self.agents[key]=agent
    agent.setController(self)

  #----------------------------------------------------------------------------------
  async def onMessage(self,websocket) :
    await self.registerAgent(websocket)
    async for message in websocket:
      #self.beforeMessage()
      key=Agent.getKey0(websocket)
      agent=self.agents[key]
      agent.addMsgCount()
      #print(f'LoopRunner.onMessage() {Agent.getKey0(websocket)=} {self.agents.keys()=}')
      logging.warning(f'LoopRunner.onMessage() {self.id=} {Agent.getKey0(websocket)=} received  {self.msgCount=} {agent.getMsgCount()=} last {message=}')
      #await websocket.send(message + agent.getKey() )
      parse=await self.parseMessage(message)
      if parse is not None :
        msg=json.loads(message)
        if parse == 'capacities' :
          agent.setCapacities(msg["payload"])
          agent.setStatus('REGISTERED')
          self.agentsByNode[agent.getCapacity("node")]=agent
          print(f'Controller.onMessage() {self.id=} {Agent.getKey0(websocket)=} registered {key=}',flush=True)
          await websocket.send(json.dumps({"cmd":"registered","payload":""}))
      else :
        await websocket.send(f'{self.id}  {Agent.getKey0(websocket)=} {agent.getMsgCount()=} {agent.getKey()=} {message=}')
      #self.afterMessage()

  #----------------------------------------------------------------------------------
  async def getAgents(self) :
    str=''
    for agent in self.agents :
      str += f'{self.agents=} {agent=}'
    return(str)

  #----------------------------------------------------------------------------------
  async def launch(self,payload) :
    logging.warning(f'Controller.launch() launching {payload=} ')
    lock=asyncio.Lock()
    async with lock :
      await asyncio.sleep(5)
      logging.warning(f'Controller.launched() done ')
      return(payload)

  #----------------------------------------------------------------------------------
  async def parseMessage(self,message) :
    try:
      msg=json.loads(message)
    except ValueError as e:
      return None
    if 'cmd' in msg :
      if msg['cmd'] == 'capacities' :
        return('capacities')
      else :
        return None
    else :
      return None

