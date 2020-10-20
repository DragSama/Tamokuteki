from TamokutekiBot import Tamokuteki
import asyncio

async def close_session():
    print("Closing aiohttp session")
    await Tamokuteki.aio_session.close()
    print("Closed")

if __name__ == "__main__":
    try:
        Tamokuteki.start()
        Tamokuteki.run_until_disconnected()
    except KeyboardInterrupt:
        pass
    finally:
        asyncio.get_event_loop().run_until_complete(close_session())
