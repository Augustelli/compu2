import asyncio
import socket
import io
import argparse
import logging
from PIL import Image, UnidentifiedImageError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageProcessorServer:
    def __init__(self, host, port, scale_host, scale_port):
        self.host = host
        self.port = port
        self.scale_host = scale_host
        self.scale_port = scale_port

    async def handle_client(self, reader, writer):
        data = await reader.read()
        if not data:
            logging.error("No se recibió ningún dato del cliente")
            return
        logging.info("Imagen recibida del cliente")

        try:
            # Convertir a escala de grises
            image = Image.open(io.BytesIO(data))
            grayscale_image = image.convert("L")
        except UnidentifiedImageError:
            logging.error("No se pudo identificar el archivo de imagen")
            return

        # Enviar la imagen escalada al segundo servidor
        scaled_image = await self.send_to_scaling_server(grayscale_image)

        # Enviar la imagen final al cliente
        writer.write(scaled_image)
        await writer.drain()
        writer.close()
        logging.info("Imagen procesada enviada al cliente")

    async def send_to_scaling_server(self, grayscale_image):
        # Convertir la imagen a bytes
        with io.BytesIO() as output:
            grayscale_image.save(output, format='PNG')
            image_data = output.getvalue()

        # Conectar con el segundo servidor para escalado
        reader, writer = await asyncio.open_connection(self.scale_host, self.scale_port)
        writer.write(image_data)
        await writer.drain()
        logging.info("Imagen enviada al servidor de escalado")

        # Leer la imagen escalada del segundo servidor
        data = await reader.read()
        writer.close()
        await writer.wait_closed()
        logging.info("Imagen escalada recibida del servidor de escalado")
        return data

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        logging.info(f"Servidor de procesamiento de imágenes iniciado en {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

def main():
    parser = argparse.ArgumentParser(description="Servidor HTTP de procesamiento de imágenes")
    parser.add_argument('-i', '--ip', required=False, help="Dirección de escucha", default='0.0.0.0')
    parser.add_argument('-p', '--port', required=False, type=int, help="Puerto de escucha", default=8080)
    parser.add_argument('--scale-ip', required=False, help="IP del servidor de escalado", default='127.0.0.1')
    parser.add_argument('--scale-port', required=False, type=int, help="Puerto del servidor de escalado", default=8081)
    args = parser.parse_args()

    image_server = ImageProcessorServer(args.ip, args.port, args.scale_ip, args.scale_port)
    asyncio.run(image_server.start_server())

if __name__ == "__main__":
    main()