import socketserver
from PIL import Image
import io
import argparse
import socket
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

class ImageResizerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Handling image resize request")
        data = b''
        while True:
            packet = self.request.recv(1024*1024)
            if not packet:
                break
            data += packet

        try:
            logging.info("Resizing image")
            image = Image.open(io.BytesIO(data))
            scale_factor = 0.5
            new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
            resized_image = image.resize(new_size)

            output = io.BytesIO()
            resized_image.save(output, format='PNG')
            self.request.sendall(output.getvalue())
            logging.info("Image resized and sent back to client")
        except Exception as e:
            logging.error(f"Error processing image: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Image Resizer Server')
    parser.add_argument('--host', type=str, default='::', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8888, help='Port to run the server on')
    args = parser.parse_args()

    logging.info("Starting image resizer server")
    with socketserver.TCPServer((args.host, args.port), ImageResizerHandler, bind_and_activate=False) as server:
        server.address_family = socket.AF_INET6 if socket.has_ipv6 else socket.AF_INET

        server.server_bind()
        server.server_activate()
        server.serve_forever()