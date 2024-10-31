import socketserver
from PIL import Image
import io

class ImageResizerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = b''
        while True:
            packet = self.request.recv(1024*1024)
            if not packet:
                break
            data += packet

        try:
            image = Image.open(io.BytesIO(data))
            scale_factor = 0.5
            new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
            resized_image = image.resize(new_size)

            output = io.BytesIO()
            resized_image.save(output, format='PNG')
            self.request.sendall(output.getvalue())
        except Exception as e:
            print(f"Error processing image: {e}")

if __name__ == "__main__":
    import argparse
    import multiprocessing

    parser = argparse.ArgumentParser(description='Image Resizer Server')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8888, help='Port to run the server on')
    args = parser.parse_args()

    with socketserver.TCPServer((args.host, args.port), ImageResizerHandler) as server:
        server.serve_forever()