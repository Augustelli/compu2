from PIL import Image
import io
import asyncio

async def convert_to_grayscale(image_data):
    image = Image.open(io.BytesIO(image_data)).convert('L')
    output = io.BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    return output.read()

async def send_to_server_b(image_data):
    reader, writer = await asyncio.open_connection('localhost', 8888)
    writer.write(image_data)
    await writer.drain()
    
    resized_image_data = await reader.read()
    writer.close()
    await writer.wait_closed()
    
    return resized_image_data