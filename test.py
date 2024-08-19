
import re
import serial.tools.list_ports, time

portData = serial.tools.list_ports.comports()

ser = None

# print(portData[2])

# ser = serial.Serial(portData[2].device, 9600, timeout=1)

# time.sleep(2)

# res = ser.readline()

# print(res)


# ser.write(b'5')  # Envía el número 123 al Arduino

# ser.close()

# while True:
#     if ser.in_waiting > 0:
#         ser.write(b'10')
#         # print(line)

print(portData)

for port in portData:

    print(port.description)
    
    try:

        if re.search('Arduino|CH340', port.description, re.IGNORECASE) is None:
            continue

        ser = serial.Serial(port.device, 9600, timeout=.1)
        time.sleep(2)  # Espera a que el Arduino se inicialice
        print(f'Conectado a Arduino en { port.device }')
        break
    except serial.SerialException as e:
        print(f'No se pudo abrir el puerto { port.device }: { e }')

if ser is None:
    raise serial.SerialException('No se pudo conectar a ningún puerto Arduino')

ser.write(b'5')  # Envía el número al Arduino

ser.close()
