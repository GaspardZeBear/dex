#!/usr/bin/env python
# python3 -m pip install websockets

import asyncio
import threading
from websockets.server import serve
import logging
import sys
from  Agent import *
from  LoopRunner import *
loglevel=logging.WARNING
#loglevel=logging.DEBUG
logging.basicConfig(stream=sys.stdout,format="%(asctime)s %(module)s t=%(thread)s %(name)s %(funcName)s %(lineno)s %(levelname)s %(message)s", level=loglevel)

#----------------------------------------------------------------------------
threads = list()
port=8080
ctrl=LoopRunner(f'controller',port)
interface=LoopRunner(f'interface',port+1)
dummy=LoopRunner(f'dummy',port+2)
threads.append(threading.Thread(target=asyncio.run, args=(ctrl.init(),)))
threads.append(threading.Thread(target=asyncio.run, args=(interface.init(),)))
threads.append(threading.Thread(target=asyncio.run, args=(dummy.init(),)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
