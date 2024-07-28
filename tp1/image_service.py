import cv2
import numpy as np
import signal
from multiprocessing import Process, Array, Lock
import ctypes


def cargar_imagen(path: str, numero_partes: int = 5):
    """Carga una imagen desde un archivo"""
    imagen = cv2.imread(path)
    print("Cargando imagen - path: ", path)
    if imagen is None:
        raise ValueError("No se pudo cargar la imagen.")
    altura, ancho = imagen.shape[:2]
    altura_ajustada = (altura // numero_partes) * numero_partes
    imagen = imagen[:altura_ajustada, :]
    altura_partes = altura_ajustada // numero_partes

    partes_imagen = []
    for i in range(numero_partes):
        start_y = i * altura_partes
        end_y = start_y + altura_partes
        part = imagen[start_y:end_y, :]
        partes_imagen.append(part)

    print(f"Imagen cargada con éxito. Dimensiones ajustadas: {ancho}x{altura_ajustada}. En {numero_partes} partes.")
    return partes_imagen


def filtro_blanco_y_negro(image):
    return cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

def filtro_sepia(image):
    sepia_kernel = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    return cv2.transform(image, sepia_kernel)


def aplicar_filtro(image_part, filter_func):
    return filter_func(image_part)


def proceso_trabajador(image_part, filter_name, shared_array, index, lock, part_shape):
    print(f"Proceso trabajador iniciado para filtro {filter_name}")
    filter_funcs = {
        'blanco_y_negro': filtro_blanco_y_negro,
        'sepia': filtro_sepia
    }

    filter_func = filter_funcs.get(filter_name)
    if not filter_func:
        print(f"Filtro desconocido: {filter_name}")
        return

    try:
        processed_part = filter_func(image_part)
        #if processed_part.shape != part_shape:
        #    raise ValueError(f"Dimensiones incorrectas del procesamiento: {processed_part.shape}, esperadas: {part_shape}")
        with lock:
            start = index * part_shape[0] * part_shape[1] * part_shape[2]
            end = (index + 1) * part_shape[0] * part_shape[1] * part_shape[2]
            shared_array[start:end] = processed_part.flatten()
        print(f"Proceso trabajador completado para filtro {filter_name}")
    except Exception as e:
        print(f"Error en el proceso trabajador: {str(e)}")

def proceso_coordinador(num_parts, part_shape, shared_array, lock):
    print("Proceso coordinador iniciado")
    full_image = np.zeros((part_shape[0] * num_parts, part_shape[1], part_shape[2]), dtype=np.uint8)
    with lock:
        for i in range(num_parts):
            start = i * part_shape[0] * part_shape[1] * part_shape[2]
            end = (i + 1) * part_shape[0] * part_shape[1] * part_shape[2]
            part = np.array(shared_array[start:end]).reshape(part_shape)
            full_image[i * part_shape[0]:(i + 1) * part_shape[0], :, :] = part
    print("Proceso coordinador completado")
    return full_image

def procesar_imagen(partes_imagenes, nombre_filtro):
    global procesos
    num_parts = len(partes_imagenes)
    part_shape = partes_imagenes[0].shape
    shared_array = Array(ctypes.c_uint8, num_parts * part_shape[0] * part_shape[1] * part_shape[2])
    lock = Lock()

    procesos = []

    for i, part in enumerate(partes_imagenes):
        p = Process(target=proceso_trabajador, args=(part, nombre_filtro, shared_array, i, lock, part_shape))
        procesos.append(p)
        p.start()

    # Esperar a que todos los procesos trabajadores terminen
    for p in procesos:
        p.join()

    # Proceso coordinador para combinar los resultados
    full_image = proceso_coordinador(num_parts, part_shape, shared_array, lock)

    # Guardar la imagen resultante
    cv2.imwrite('imagen_procesada.jpg', full_image)
    print("Imagen procesada y guardada como 'imagen_procesada.jpg'")
    print("Todos los procesos han terminado")

# Manejo de señales
def manejador_senales(signal, frame):
    print("Interrupción recibida. Terminando procesos...")
    for proceso in procesos:
        proceso.terminate()
    print("Procesos terminados.")
    exit(0)
signal.signal(signal.SIGINT, manejador_senales)