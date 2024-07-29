# Multithreaded Image Filter

`multithreaded_image_filter` es un paquete de Python que aplica filtros a imágenes en paralelo utilizando multiprocesamiento. Este paquete permite aplicar filtros de blanco y negro y sepia a imágenes, dividiéndolas en partes y procesándolas en paralelo para mejorar el rendimiento.
## Requisitos

Para ejecutar este proyecto, asegúrate de cumplir con los siguientes requisitos:

### Requisitos de Software

1. **Python 3.10 o superior**
   - Este proyecto requiere Python 3.10 o una versión superior. Puedes verificar tu versión de Python con el siguiente comando:

     ```sh
     python --version
     ```

2. **pip**
   - `pip` es el administrador de paquetes para Python. Este proyecto requiere `pip` para instalar las dependencias. Puedes verificar si `pip` está instalado con el siguiente comando:

     ```sh
     pip --version
     ```
## Instalación
Puedes instalar el paquete con 
```sh
./install.sh    
```

Asegurate de que el archivo tenga los permisos necesarios, sino ejecuta : 
```sh
chmod +x install.sh
```
En caso de no poder instalarlo de la forma anterior, puedes hacerlo desde el repositorio.
Para instalar `multithreaded_image_filter`, clona el repositorio y usa `pip` para instalar el paquete localmente:

1. **Clona el repositorio**:

   ```sh
   git clone https://github.com/Augustelli/compu2.git
    ```

2. **Navega al directorio del proyecto**
    ```sh
   cd multithreaded_image_filter
    ```

3. **Instala el paquete**
    ```sh
   pip install .
    ```

## Uso

Una vez instalado, puedes usar el comando mif desde la terminal para aplicar filtros a tus imágenes.
Sintaxis
```sh
mif --filtro <filtro_imagen> --procesos <num_procesos> <ruta_imagen_entrada> <ruta_imagen_salida>
```


- <filtro_imagen>: El filtro a aplicar a la imagen.
      - Opciones disponibles: blanco_y_negro, sepia. Por defecto, se aplica el filtro sepia.
- <num_procesos>: El número de procesos paralelos a utilizar. El valor predeterminado es 5.
- <ruta_imagen_entrada>: La ruta al archivo de imagen que deseas procesar.
- <ruta_imagen_salida>: La ruta donde se guardará la imagen procesada.


## Ejemplos

* Aplicar un filtro sepia con 4 procesos:

```sh
mif --filtro sepia --procesos 4 input.jpg output.jpg
```

* Aplicar un filtro blanco y negro con 2 procesos:

```sh
mif --filtro blanco_y_negro --procesos 2 input.jpg output.jpg
```

Descripción de los Filtros

- Blanco y Negro: Convierte la imagen a escala de grises y luego la convierte de nuevo a color.
- Sepia: Aplica un filtro sepia a la imagen, dándole un tono cálido y envejecido.

Requisitos

El paquete requiere las siguientes dependencias:

    opencv-python-headless: Para el procesamiento de imágenes.
    numpy: Para operaciones matemáticas en matrices de imágenes.