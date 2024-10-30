from PIL import Image
import io

async def convert_to_grayscale(image_data):
    image = Image.open(io.BytesIO(image_data)).convert('L')
    output = io.BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    return output.read()