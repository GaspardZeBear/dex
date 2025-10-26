import asyncio
from websockets.server import serve
import logging

#---------------------------------------------------------------
class Agent() :
  #agents={}
  #---------------------------------------------------------------
  def __init__(self,ws) :
    logging.warning(f'{ws=}')
    self.websocket=ws
    #self.key=Agent.getKey(ws)
    self.msgCount=0
    self.status='INIT'
    #Agent.agents[Agent.getKey0(ws)]=self

#---------------------------------------------------------------
  def display(self) :
    return(f'{self.__dict__}')

  #---------------------------------------------------------------
  def capacities(self,capacities) :
    print(f'{capacities=}')
    self.node=capacities["node"]
    self.cpu=capacities["cpu"]
    self.mem=capacities["mem"]
    self.tags=capacities.get("tags",[])
  
  #---------------------------------------------------------------
  def getMsgCount(self) :
    return(self.msgCount)
  
  #---------------------------------------------------------------
  def addMsgCount(self,add=1) :
    self.msgCount += add

  #---------------------------------------------------------------
  def getKey(self) :
    return(Agent.getKey0(self.websocket))

  #---------------------------------------------------------------
  #def displayAgents(self) :
    #str = ''
    #for s in Agent.agents :
    #  str += f'{Agent.agents[s].display()}'
    #return(str)

  #---------------------------------------------------------------
  @staticmethod
  def getKey0(websocket) :
      return(websocket.remote_address[0]+":"+str(websocket.remote_address[1]))
      #return(str(websocket.__hash__()))
  #---------------------------------------------------------------
  #@staticmethod
  #def register(websocket) :
    #logging.warning(f'{dir(websocket)}')
    #key=Agent.getKey0(websocket)
    #if key not in Agent.agents :
    #  agent=Agent(websocket)
    #agent=Agent.agents[key]
    #return(agent)



