# dex
Distributed EXecutor

## Why :

Try asyncio and websockets

LoopRunner : creates an event loop an a server on a given port
Controller :  extends LoopRunner to create controller controller-agent architecture
  Controller manages agents, booking etc 
Agent : a remote agent with capacities (cpu, mem, node, tags). One per node.
Interface : will receive commands from user to get rigs etc ..  and ask to controller

Server : python3 WServer.py
Simulateur agents : python3 WAgent.py
Client interface : Client.html
