import aiohttp
import asyncio
from random import randint

TIME_DRONE_SLEEP = 5

async def sleep_async_rand():
    await asyncio.sleep(randint(4,8))


async def sleep_async(seconds):
    await asyncio.sleep(seconds)


def create_dict(id, type, seq=0, lat=5.02, log=-9.02, high=10.3, data="0"):
    return {"id": id, "type": type, "seq": seq, "lat": lat, "log": log, "high": high, "DATA": data}


async def handle_disconnection_exception():
  for task in tasks:
    task.cancel()


async def send_drone1_json(session):
  seq = 0
  location_index = 0
  locations=[
    [-22.954132, -43.164714],
    [-22.953855, -43.163813],
    [-22.953657, -43.162997],
    [-22.953460, -43.162053],
    [-22.952709, -43.161023],
    [-22.953144, -43.160165],
    [-22.953183, -43.158963],
    [-22.953065, -43.157547],
    [-22.953183, -43.158963],
    [-22.953144, -43.160165],
    [-22.952709, -43.161023],
    [-22.953460, -43.162053],
    [-22.953657, -43.162997],
    [-22.953855, -43.163813] 
  ]
  await sleep_async(1)
  while True:
    lat = locations[location_index][0]
    log = locations[location_index][1]
    data_dict = create_dict(7, 102, seq=seq, lat=lat, log=log)
    async with session.post(url, data=data_dict) as resp:
      response = await resp.json() 
      print(response)

    seq += 1
    location_index+=1
    if seq >= 255:
      seq = 0
    if location_index >= len(locations):
      location_index = 0
    await sleep_async(TIME_DRONE_SLEEP)


async def send_drone2_json(session):
  seq = 0
  location_index = 0
  locations=[
    [-22.955110, -43.166151],
    [-22.954754, -43.167439],
    [-22.954517, -43.168641],
    [-22.955317, -43.168447],
    [-22.955989, -43.168834],
    [-22.957056, -43.169220],
    [-22.957491, -43.167975],
    [-22.957332, -43.166559],
    [-22.956582, -43.165229],
    [-22.955396, -43.165400],
  ]
  while True:
    lat = locations[location_index][0]
    log = locations[location_index][1]
    data_dict = create_dict(8, 102, seq=seq, lat=lat, log=log)
    async with session.post(url, data=data_dict) as resp:
      response = await resp.json() 
      print(response)

    seq += 1
    location_index+=1
    if seq >= 255:
      seq = 0
    if location_index >= len(locations):
      location_index = 0
    await sleep_async(TIME_DRONE_SLEEP)


async def main():
  async with aiohttp.ClientSession() as session:
    writer_drone1 = asyncio.create_task(send_drone1_json(session))
    writer_drone2 = asyncio.create_task(send_drone2_json(session))

    tasks.extend([writer_drone1, writer_drone2])
    await asyncio.gather(*tasks)

    await handle_disconnection_exception()


url = 'http://localhost:8000/update-drone/'
tasks = []
asyncio.run(main())