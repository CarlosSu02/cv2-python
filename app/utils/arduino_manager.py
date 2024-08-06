import time
import serial
import serial.tools.list_ports

class ArduinoManager:

    def __init__(self):
        self.arduino = None
        self.portData = serial.tools.list_ports.comports()
        self.initialize_arduino()

    def initialize_arduino(self):

        for port in self.portData:
            # print(port)
            try:
                self.arduino = serial.Serial(port.device, 9600, timeout=.1)
                time.sleep(2)  # Espera a que el Arduino se inicialice
                
                print(f'Conectado a Arduino en { port.device }')
                break

            except serial.SerialException as e:
                print(f'No se pudo abrir el puerto { port.device }: { e }')

        if self.arduino is None:
            raise serial.SerialException('No se pudo conectar a ningún puerto Arduino')

    def ser(self):
        return self.arduino
    
    def write(self, data):
        if self.arduino:
            self.arduino.write(data.encode())
        else:
            print('Arduino no está conectado')

    # def send_command(self, command):
    #     if self.arduino:
    #         self.arduino.write(command.encode())
    #     else:
    #         print('Arduino no está conectado')

    # def read_response(self):
    #     if self.arduino:
    #         return self.arduino.readline().decode()
    #     else:
    #         return 'Arduino no está conectado'

    def close(self):
        if self.arduino:
            self.arduino.close()
            print('Conexión con Arduino cerrada')
