from melon import Melon
from genie import Genie
from time import time, sleep
import asyncio


async def get_data():
    data = {'melon': Melon().page_parse(), 'genie': Genie().page_parse()}
    return data


if __name__ == "__main__":
    t1 = time()
    print(asyncio.run(get_data()))
    t2 = time()
    print(t2 - t1)
