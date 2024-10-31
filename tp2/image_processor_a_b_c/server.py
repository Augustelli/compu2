import argparse
from aiohttp import web
from utils import send_to_server_b, convert_to_grayscale

async def handle_image(request):
    reader = await request.multipart()
    field = await reader.next()
    assert field.name == 'image'
    image_data = await field.read()

    # Convert image to grayscale
    grayscale_image_data = await convert_to_grayscale(image_data)

    # Send grayscale image to the second server for resizing
    resized_image_data = await send_to_server_b(grayscale_image_data)

    return web.Response(body=resized_image_data, content_type='image/png')

async def init_app():
    app = web.Application()
    app.router.add_post('/upload', handle_image)
    return app

def main():
    parser = argparse.ArgumentParser(description='Asyncio HTTP Server for Image Processing')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the server on')
    args = parser.parse_args()

    web.run_app(init_app(), host=args.host, port=args.port)

if __name__ == '__main__':
    main()