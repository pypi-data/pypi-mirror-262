
import asyncio
import json
import logging
from topicsync.server.update_buffer import UpdateBuffer

from topicsync.state_machine.state_machine import ALREADY_LOGGED_ERROR_NOTE, StateMachine
from topicsync.utils import SimpleAction
logger = logging.getLogger(__name__)
import traceback
from typing import Awaitable, Callable, Dict, List, Tuple, AsyncIterator, Protocol
from itertools import count
from collections import defaultdict

from topicsync.change import Change, SetChange

def make_message(message_type,**kwargs)->str:
    return json.dumps({"type":message_type,"args":kwargs})

def parse_message(message_json)->Tuple[str,dict]:
    message = json.loads(message_json)
    return message["type"],message["args"]

class ClientCommProtocol(Protocol):
    def messages(self) -> AsyncIterator[str]:
        pass

    async def send(self, message):
        pass

class ConnectionClosedException(Exception):
    def __init__(self, concrete_exception: Exception):
        self._inner_exception = concrete_exception

    def __repr__(self):
        return repr(self._inner_exception)

class Client:
    def __init__(self, id, comm: ClientCommProtocol, sending_queue:asyncio.Queue[Tuple['Client',Tuple,Dict]]):
        self.id = id
        self._comm = comm
        self._sending_queue = sending_queue

    async def _send_raw(self,message):
        await self._comm.send(message)
        logger.debug(f"<{self.id} {message[:100]}")

    async def send_async(self,*args,**kwargs):
        await self._send_raw(make_message(*args,**kwargs))

    def send(self,*args,**kwargs):
        self._sending_queue.put_nowait((self,args,kwargs))

    @property
    def messages(self) -> AsyncIterator[str]:
        return self._comm.messages()

ClientCommFactory = Callable[[], ClientCommProtocol]
class ClientManager:
    def __init__(self,state_machine:StateMachine) -> None:
        self._state_machine = state_machine
        self._clients:Dict[int,Client] = {}
        self._client_id_count = count(1)
        self._message_handlers:Dict[str,Callable[...,None|Awaitable[None]]] = {'subscribe':self._handle_subscribe,
                                                                               'unsubscribe':self._handle_unsubscribe,}
        self._subscriptions:defaultdict[str,set] =defaultdict(set)
        self._sending_queue:asyncio.Queue[Tuple[Client,Tuple,Dict]] = asyncio.Queue()

        self._update_buffer = UpdateBuffer(self._state_machine,self.send_update)
        self.on_client_connect = SimpleAction()
        self.on_client_disconnect = SimpleAction()

    async def run(self):
        asyncio.get_event_loop().create_task(self._update_buffer.run())
        while True:
            client,args,kwargs = await self._sending_queue.get()
            try:
                await client.send_async(*args,**kwargs)
            except ConnectionClosedException:
                self._cleanup_client(client)

    def send(self,client:Client,*args,**kwargs):
        self._sending_queue.put_nowait((client,args,kwargs))


    async def handle_client(self, client_comm_factory: ClientCommFactory):
        '''
        Handle a client connection. 
        '''

        client_id = next(self._client_id_count)
        client = self._clients[client_id] = Client(client_id, client_comm_factory(), self._sending_queue)

        try:
            logger.info(f"Client {client_id} connected")
            await client.send_async("hello",id=client_id)
            self.on_client_connect.invoke(client_id)

            async for message in client.messages:
                logger.debug(f"> {message[:100]}")

                message_type, args = parse_message(message)
                if message_type not in self._message_handlers:
                    logger.error(f"Unknown message type: {message_type}")
                    continue

                try:
                    return_value = self._message_handlers[message_type](sender = client,**args)
                    if isinstance(return_value,Awaitable):
                        await return_value
                except Exception as e:
                    if not hasattr(e,"__notes__") or ALREADY_LOGGED_ERROR_NOTE not in e.__notes__:
                        logger.warn(f"Error handling message {message_type}:\n{traceback.format_exc()}")
                    continue

        except ConnectionClosedException as e:
            logger.info(f"Client {client_id} disconnected: {repr(e)}")
            self._cleanup_client(client)
        except Exception as e:
            logger.error(f"Error handling client {client_id}:\n{traceback.format_exc()}")
            self._cleanup_client(client)

    def send_update_or_buffer(self,changes:List[Change],action_id:str):
        self._update_buffer.add_changes(changes,action_id)

    def send_update(self,changes:List[Change],action_id:str):
        '''
        Broadcast a list of changes to all clients subscribed to the topics in the changes.
        '''
        messages_for_client = defaultdict(list)
        for change in changes:
            for client_id in self._subscriptions[change.topic_name]:
                messages_for_client[client_id].append(change.serialize())

        for client_id in messages_for_client:
            client = self._clients[client_id]
            self.send(client,"update",changes=messages_for_client[client_id],action_id=action_id)
    
    def register_message_handler(self,message_type:str,handler:Callable[...,None|Awaitable[None]]):
        self._message_handlers[message_type] = handler

    def _cleanup_client(self,client:Client):
        for topic in self._subscriptions:
            self._subscriptions[topic].discard(client.id)
        self.on_client_disconnect.invoke(client.id)

    def _handle_subscribe(self,sender:Client,topic_name:str):
        if not self._state_machine.has_topic(topic_name):
            # This happens when a removal message of the topic is not yet arrived at the client
            #? Should we send a message to the client?
            #logger.warning(f"Client {sender.id} tried to subscribe to non-existing topic {topic_name}")
            return
        
        self._update_buffer.flush() # clear the buffer before sending `init` so the client starts at a correct state

        self._subscriptions[topic_name].add(sender.id)
        logger.debug(f"Client {sender.id} subscribed to {topic_name}")
        msg = self._state_machine.get_topic(topic_name).get_init_message()
        self.send(sender,"init",**msg)

    def _handle_unsubscribe(self,sender:Client,topic_name:str):
        self._subscriptions[topic_name].discard(sender.id)
    
    def set_client_id_count(self,id_count):
        self._client_id_count = count(id_count)

    def get_client_id_count(self):
        return next(self._client_id_count)