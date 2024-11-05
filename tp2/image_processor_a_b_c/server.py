# file: image_processor_a_b_c/server.py
import asyncio
import aiohttp
from aiohttp import web
import argparse
import io
from PIL import Image
import socket
import logging
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

async def convert_to_grayscale(image_data):
    logging.info("Converting image to grayscale")
    image = Image.open(io.BytesIO(image_data)).convert('L')
    output = io.BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    logging.info("Image converted to grayscale")
    return output.read()

async def resize_image(image_data, scale_factor):
    logging.info("Connecting to image resizer server")
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    writer.write(image_data)
    await writer.drain()
    writer.write_eof()

    logging.info("Waiting for resized image")
    resized_data = await reader.read()
    writer.close()
    await writer.wait_closed()
    logging.info("Received resized image")
    return resized_data

async def handle_upload(request):
    logging.info("Handling image upload")
    reader = await request.multipart()
    field = await reader.next()
    assert field.name == 'image'
    image_data = await field.read(decode=True)

    grayscale_image = await convert_to_grayscale(image_data)
    resized_image = await resize_image(grayscale_image, 0.5)

    logging.info("Sending processed image to client")
    return web.Response(body=resized_image, content_type='image/png')

async def init_app():
    app = web.Application()
    app.router.add_post('/upload', handle_upload)
    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Image Processor Server')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the server on')
    args = parser.parse_args()

    logging.info("Starting server")
    web.run_app(init_app(), host=args.host, port=args.port)