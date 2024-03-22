import os
import sys
import time
import requests
import threading
import multiprocessing
import aiohttp
import asyncio


async def download_image_async(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            filename = url.split('/')[-1]
            with open(filename, 'wb') as f:
                f.write(await response.read())
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {url}")


async def download_images_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(session, url) for url in urls]
        await asyncio.gather(*tasks)


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {url}")


def download_images_threaded(urls):
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_image, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def download_images_multiprocess(urls):
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=download_image, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    urls = sys.argv[1:]

    start_time = time.time()
    download_images_threaded(urls)
    end_time = time.time()
    print(f"Threaded execution time: {end_time - start_time} seconds")

    start_time = time.time()
    download_images_multiprocess(urls)
    end_time = time.time()
    print(f"Multiprocess execution time: {end_time - start_time} seconds")

    start_time = time.time()
    asyncio.run(download_images_async(urls))
    end_time = time.time()
    print(f"Asynchronous execution time: {end_time - start_time} seconds")
