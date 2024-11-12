import socketserver
from PIL import Image
import io
import argparse
import logging
import socket
from concurrent.futures import ProcessPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scale_image(data):
    logging.info("Resizing image in process")
    image = Image.open(io.BytesIO(data))
    scale_factor = 0.5
    new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
    scaled_image = image.resize(new_size)

    output = io.BytesIO()
    scaled_image.save(output, format='PNG')
    return output.getvalue()

class ImageScalerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Handling image resize request")
        data = b''
        while True:
            packet = self.request.recv(1024*1024)
            if not packet:
                break
            data += packet

        try:
            with ProcessPoolExecutor() as executor:
                future = executor.submit(scale_image, data)
                scaled_image = future.result()
                self.request.sendall(scaled_image)
                logging.info("Image resized and sent back to client")
        except Exception as e:
            logging.error(f"Error processing image: {e}")

class IPTCPServer(socketserver.TCPServer):
    address_family = socket.AF_INET

def run_scaling_server(host, port):
    with IPTCPServer((host, port), ImageScalerHandler) as server:
        logging.info(f"Scaling server started on {host}:{port}")
        server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Scaling Server")
    parser.add_argument('-i', '--ip', required=False, default='127.0.0.1')
    parser.add_argument('-p', '--port', required=False, type=int, help="Listening port", default=8081)
    args = parser.parse_args()

    run_scaling_server(args.ip, args.port)