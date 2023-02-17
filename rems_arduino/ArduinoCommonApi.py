import time
import serial
from dataclasses import dataclass


@dataclass(frozen=True)
class PIN_MODE:
    INPUT: str = 'INPUT'
    INPUT_PULLUP: str = 'INPUT_PULLUP'
    OUTPUT: str = 'OUTPUT'

    HIGH: str = 'HIGH'
    LOW: str = 'LOW'


@dataclass(frozen=True)
class COMMAND:
    write: str = 'w'
    read: str = 'w'
    pin_mode:str ='p'

    separator:str = '.'
    end: str = ''

    @classmethod
    def create(obj, com, target=None, val=None):
        if target is None and val is None:
            return com
        if target is None:
            return com + obj.separator + val

        if val is None:
            return com + obj.separator + target

        return com + obj.separator + target + obj.separator + val




@dataclass(frozen=True)
class DEFAULT:
    BAUDRATE: int = 9600
    CONNECTION_TIMEOUT = 1


class ArduinoCommonApi:
    def __init__(self):
        self.device = None

    def connect(self, port, baudrate=DEFAULT.BAUDRATE, timeout=DEFAULT.CONNECTION_TIMEOUT):
        if self.device is None:
            self.device = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            time.sleep(2)
        return self.get_device_info()

    def check_connection(self):
        if self.device is None:
            raise(ConnectionError('No Device connected'))
        return bool(self.device is not None)

    def get_device_info(self):
        return None

    def close(self):
        if self.device is not None:
            self.device.close()

    def write(self, pin, value):
        self.device.write(self.to_byte_com(COMMAND.write + str(pin) + str(value)))
        time.sleep(0.001)

    def read(self, pin):
        self.device.write(self.to_byte_com(COMMAND.create(COMMAND.read, str(pin))))
        return self.decode_command(self.device.readline())

    def set_pin_mode(self, pin, mode):
        self.check_connection()
        if PIN_MODE.INPUT == mode or PIN_MODE.INPUT_PULLUP == mode:
            self.device.write(self.to_byte_com(COMMAND.pin_mode + str(pin) + 'i'))

        elif PIN_MODE.OUTPUT == mode:
            self.device.write(self.to_byte_com(COMMAND.pin_mode + str(pin) + 'o'))

    def to_byte_com(self, string):
        return str.encode(string + "\n", 'utf_8')

    def decode_command(self, command):
        if isinstance(command, bytes):
            command = self.decode(command)

        com_iter = iter(command.split(COMMAND.separator))
        com = None
        pin = None
        value = None
        try:
            com = next(com_iter)
            pin = next(com_iter)
            value = next(com_iter)
        except StopIteration:
            pass
        return com, pin, value


    def decode(self, byte_daata):
        return str(byte_daata, 'ascii').strip('\r\n')



    def __del__(self):
        self.close()
        # pyserial also has __del__ which try to close the port

