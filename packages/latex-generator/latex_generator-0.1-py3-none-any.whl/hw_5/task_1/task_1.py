import aiohttp
import asyncio
import os
from aiohttp import ClientSession


async def download_image(session: ClientSession, url: str, folder: str, filename: str) -> None:
    async with session.get(url) as response:
        content = await response.read()
        filepath = os.path.join(folder, filename)

        with open(filepath, 'wb') as f:
            f.write(content)

        print(f"Downloaded: {filename}")


async def download_images(num_images: int, folder: str) -> None:
    url = 'https://picsum.photos/200/300'

    async with aiohttp.ClientSession() as session:
        tasks = []

        for i in range(1, num_images + 1):
            filename = f'image_{i}.jpg'
            task = download_image(session, url, folder, filename)
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    num_images_to_download = int(input("Enter the number of images to download: "))
    script_directory = os.path.dirname(os.path.abspath(__file__))
    download_folder = os.path.join(script_directory, "artifacts")

    os.makedirs(download_folder, exist_ok=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_images(num_images_to_download, download_folder))
