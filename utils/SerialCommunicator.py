import serial
import serial.tools.list_ports


class SerialCommunicator:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.serial = serial.Serial(port, baudrate)

    def __del__(self):
        self.serial.close()

    def send(self, direction: str):
        self.serial.write(direction.encode('utf-8'))

    @staticmethod
    def get_all_comports():
        return [port.device for port in serial.tools.list_ports.comports()]
