import cv2
import numpy as np
import signal
from multiprocessing import Process, Array, Lock
import ctypes
import argparse
import os

def cargar_imagen(path: str, numero_partes: int):
    """Carga una imagen desde un archivo y la divide en partes iguales."""
    imagen = cv2.imread(path)
    if imagen is None:
        raise ValueError("No se pudo cargar la imagen. Verifique la ruta.")
    altura, ancho = imagen.shape[:2]

    # Ajuste para asegurar que todas las partes tengan la misma altura
    altura_ajustada = (altura // numero_partes) * numero_partes
    imagen = imagen[:altura_ajustada, :]
    altura_partes = altura_ajustada // numero_partes

    partes_imagen = [imagen[i * altura_partes:(i + 1) * altura_partes, :] for i in range(numero_partes)]

    return partes_imagen

def filtro_blanco_y_negro(image):
    """Aplica un filtro blanco y negro a la imagen."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def filtro_sepia(image):
    """Aplica un filtro sepia a la imagen."""
    sepia_kernel = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    return cv2.transform(image, sepia_kernel)

def aplicar_filtro(image_part, filter_func):
    """Aplica una función de filtro a una parte de la imagen."""
    return filter_func(image_part)

def proceso_trabajador(image_part, filter_name, shared_array, index, lock, part_shape):
    """Proceso de trabajo que aplica un filtro a una parte de la imagen y almacena el resultado en un array compartido."""
    pid = os.getpid()
    print(f"Proceso trabajador (PID: {pid}) iniciado para filtro '{filter_name}'")

    filter_funcs = {
        'blanco_y_negro': filtro_blanco_y_negro,
        'sepia': filtro_sepia
    }
    filter_func = filter_funcs.get(filter_name)
    if not filter_func:
        raise ValueError(f"Filtro desconocido: {filter_name}")

    processed_part = filter_func(image_part)
    flat_part = processed_part.flatten()
    with lock:
        start = index * part_shape[0] * part_shape[1] * part_shape[2]
        shared_array[start:start + len(flat_part)] = flat_part

    print(f"Proceso trabajador (PID: {pid}) completado.")

def proceso_coordinador(num_parts, part_shape, shared_array, lock):
    """Combina las partes procesadas de la imagen en una sola imagen."""
    print("Proceso coordinador iniciado.")
    full_image = np.zeros((part_shape[0] * num_parts, part_shape[1], part_shape[2]), dtype=np.uint8)
    with lock:
        for i in range(num_parts):
            start = i * part_shape[0] * part_shape[1] * part_shape[2]
            end = start + (part_shape[0] * part_shape[1] * part_shape[2])
            part = np.array(shared_array[start:end]).reshape(part_shape)
            full_image[i * part_shape[0]:(i + 1) * part_shape[0], :, :] = part
    print("Proceso coordinador completado.")
    return full_image

def procesar_imagen(partes_imagenes, nombre_filtro, output_path):
    """Procesa una imagen utilizando multiprocessing y guarda el resultado en un archivo."""
    num_parts = len(partes_imagenes)
    part_shape = partes_imagenes[0].shape
    shared_array = Array(ctypes.c_uint8, num_parts * part_shape[0] * part_shape[1] * part_shape[2])
    lock = Lock()

    procesos = []
    print(f"Iniciando {num_parts} procesos de trabajo...")
    for i, part in enumerate(partes_imagenes):
        p = Process(target=proceso_trabajador, args=(part, nombre_filtro, shared_array, i, lock, part_shape))
        procesos.append(p)
        p.start()
        print(f"Proceso (PID: {p.pid}) iniciado para la parte {i + 1}.")

    for p in procesos:
        p.join()
        print(f"Proceso (PID: {p.pid}) finalizado.")

    full_image = proceso_coordinador(num_parts, part_shape, shared_array, lock)
    cv2.imwrite(output_path, full_image)
    print(f"Imagen procesada y guardada como '{output_path}'")

def manejador_senales(signal, frame):
    """Maneja la señal de interrupción para terminar procesos correctamente."""
    print("Interrupción recibida. Terminando procesos...")
    for proceso in procesos:
        proceso.terminate()
        print(f"Proceso (PID: {proceso.pid}) terminado.")
    print("Todos los procesos han sido terminados.")
    exit(0)

signal.signal(signal.SIGINT, manejador_senales)

def main():
    parser = argparse.ArgumentParser(description='Procesamiento de imágenes en paralelo.')
    parser.add_argument('path', type=str, help='Ruta a la imagen de entrada')
    parser.add_argument('output', type=str, help='Ruta para guardar la imagen de salida')
    parser.add_argument('--filtro', type=str, choices=['blanco_y_negro', 'sepia'], default='sepia',
                        help='Filtro a aplicar a la imagen')
    parser.add_argument('--procesos', type=int, default=5, help='Número de procesos paralelos')

    args = parser.parse_args()

    if not os.path.isfile(args.path):
        raise ValueError(f"La ruta especificada '{args.path}' no es válida o no es un archivo.")

    print(f"Cargando imagen desde '{args.path}' y dividiéndola en {args.procesos} partes.")
    partes_imagen = cargar_imagen(args.path, args.procesos)
    print("Imagen cargada y dividida en partes.")

    print(f"Aplicando filtro '{args.filtro}' a la imagen.")
    procesar_imagen(partes_imagen, args.filtro, args.output)
    print(f"Proceso completado. Imagen guardada como '{args.output}'.")

if __name__ == '__main__':
    main()
