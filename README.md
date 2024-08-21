
# opencv2-python

## Pasos recomendados
Se usó la version de python 3.12.4.
- Link de instalador de python para windows: [Python 3.12.4](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe)
- Para otras plataformas: [Python 3.12.4
](python.org/downloads/release/python-3124/)
- Actualizar pip
```bash
# pip install --upgrade pip
python.exe -m pip install --upgrade pip
```
- Instalar las librerias necesarias
```bash
pip install -r requirements.txt
```
- Ejecutar el archivo main.py
```bash
python main.py 
```

## Consideraciones
- Al momento de ejecutar el archivo main.py, se inicilizará la conexión con arduino, por lo que es necesario tenerlo conectado.
- Se debe tener en cuenta que usualmente la primera vez no se conecta correctamente, por lo que se recomienda desconectar el arduino y volver a conectarlo, y guardar en cualquier archivo para que se actualice la conexión o ingrese a la ruta /admin en el navegador y presione el botón de 'Inicializar Arduino', se debe asegurar que el puerto COM sea el correcto.
- Se debe tener en cuenta que el arduino debe tener el código de arduino cargado, el cual se encuentra en la carpeta arduino-codes.
- Para poder usarla solo se debe acceder a la dirección que se muestra en la consola, la ruta / muestra las opciones disponibles.
- En dado caso no se enciendan las leds de la cámara y esté conectado el arduino, considere guardar en cualquier archivo para que se actualice la conexión.
