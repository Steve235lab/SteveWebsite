import asyncio
import websockets
import time


async def echo(websocket, path):
    async for message in websocket:
        message = "I got your message: {}".format(message)
        await websocket.send(message)

        while True:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if str(t).endswith("0"):
                await websocket.send(t)
                break


asyncio.get_event_loop().run_until_complete(websockets.serve(echo, '42.192.44.52', 8000))
asyncio.get_event_loop().run_forever()
