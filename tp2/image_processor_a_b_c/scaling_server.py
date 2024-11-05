import socketserver
from PIL import Image
import io
import argparse
import logging
import socket

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageScalerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Recibir la imagen enviada por el servidor principal
        data = self.request.recv(1024 * 1024)  # Ajusta el tamaño si necesitas recibir imágenes más grandes
        logging.info("Imagen recibida para escalado")

        try:
            # Convertir a imagen, escalar y preparar para enviar de vuelta
            image = Image.open(io.BytesIO(data))
            scale_factor = 0.5  # Factor de escala
            new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
            scaled_image = image.resize(new_size)

            # Convertir imagen escalada a bytes y enviarla de vuelta
            output = io.BytesIO()
            scaled_image.save(output, format='PNG')
            self.request.sendall(output.getvalue())
            logging.info("Imagen escalada enviada de vuelta al servidor principal")
        except Exception as e:
            logging.error(f"Error al procesar la imagen: {e}")

class IPv6TCPServer(socketserver.TCPServer):
    address_family = socket.AF_INET6  # Especifica el uso de IPv6

def run_scaling_server(host, port):
    with IPv6TCPServer((host, port), ImageScalerHandler) as server:
        logging.info(f"Servidor de escalado iniciado en {host}:{port}")
        server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor de escalado de imágenes")
    parser.add_argument('-i', '--ip', required=True, help="Dirección de escucha en IPv6 (por ejemplo, :: o ::1)")
    parser.add_argument('-p', '--port', required=True, type=int, help="Puerto de escucha")
    args = parser.parse_args()

    run_scaling_server(args.ip, args.port)
