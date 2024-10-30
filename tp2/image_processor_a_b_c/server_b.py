import socketserver
from multiprocessing import Process
from PIL import Image
import io

class ImageResizeHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024*1024)
        image = Image.open(io.BytesIO(data))
        
        # Resize image
        scale_factor = 0.5  # Example scale factor
        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        resized_image = image.resize(new_size)
        
        output = io.BytesIO()
        resized_image.save(output, format='PNG')
        self.request.sendall(output.getvalue())

def start_server():
    server = socketserver.TCPServer(('localhost', 8888), ImageResizeHandler)
    server.serve_forever()

if __name__ == '__main__':
    process = Process(target=start_server)
    process.start()
    process.join()