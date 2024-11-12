
# Servidor de Procesamiento de Imágenes - Mancuso Augusto Tomás

## Descripción
Este proyecto es un servidor de procesamiento de imágenes que convierte imágenes a escala de grises y las redimensiona. Utiliza `aiohttp` para manejar solicitudes HTTP y `Pillow` para el procesamiento de imágenes.

## Requisitos
- Python 3.7+
- `pip` (instalador de paquetes de Python)

## Configuración

1. **Clonar el repositorio:**
    ```sh
    git clone <url-del-repositorio>
    cd <directorio-del-repositorio>
    ```

2. **Crear un entorno virtual:**
    ```sh
    python -m venv venv
    ```

3. **Activar el entorno virtual:**
    - En Linux/Mac:
        ```sh
        source venv/bin/activate
        ```
    - En Windows:
        ```sh
        venv\Scripts\activate
        ```

4. **Instalar las dependencias:**
    ```sh
    pip install -r requirements.txt
    ```

## Ejecutar el Proyecto

1. **Ejecutar el servidor:**
    ```sh
    ./run_project.sh
    ```

## Uso

- El servidor comenzará y escuchará en la IP predeterminada `::` (IPv6) y el puerto `8080`.
- Puedes subir una imagen al servidor usando una herramienta como `curl`:
    ```sh
    curl -X POST -F "image=@ruta/a/tu/imagen.png" http://[::1]:8080/upload
    ```

Reemplaza `ruta/a/tu/imagen.png` con la ruta real de la imagen que deseas subir.

## Notas

- Asegúrate de que el script `run_project.sh` tenga permisos de ejecución:
    ```sh
    chmod +x run_project.sh
    ```

- El servidor también se conecta a un servidor de redimensionamiento de imágenes que se ejecuta en la IP `::1` y el puerto `8888`. Asegúrate de que este servidor esté en funcionamiento y sea accesible.
