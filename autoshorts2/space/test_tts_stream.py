import asyncio
import edge_tts

async def test():
    comm = edge_tts.Communicate("Hello world, this is a test of edge tts.", "en-US-ChristopherNeural")
    async for chunk in comm.stream():
        t = chunk.get("type")
        if t != "audio":
            print("Chunk type:", t, chunk)

asyncio.run(test())
