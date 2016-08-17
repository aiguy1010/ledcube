import time
import serial
import serial.tools.list_ports

class Cube():
    def __init__(self, verbose=False):
        self.state = [False]*64
        for device in [port.device for port in serial.tools.list_ports.comports()]:
            if verbose:
                print(device)
            self.ser = serial.Serial(device, 115200, timeout=1)
            time.sleep(4)
            self.ser.write([2])
            response = self.ser.read(17).decode('ascii')
            if verbose:
                print(response)
            if response:
                if verbose:
                    print('Found a cube device!')
                break
            else:
                if verbose:
                    print('No response')
                self.ser.close()

    def __del__(self):
        self.ser.close()

    def get(self, i, j, k):
        if not Cube.__checkIndex__(i, j, k):
            raise(IndexError('Only values from 0 to 3 inclusive are valid for cube indices.'))
        return self.state[(3-j)+4*(3-i)+16*k]

    def set(self, i, j, k, value=True, immediate=True):
        if not Cube.__checkIndex__(i, j, k):
            raise(IndexError('Only values from 0 to 3 inclusive are valid for cube indices.'))
        if type(value) != bool:
            raise(TypeError('Cube elements can only accept boolian values.'))
        self.state[(3-j)+4*(3-i)+16*k] = value
        if immediate:
            self.update()

    def clear(self, immediate=True):
        self.state = [False]*64

    def update(self):
        byteList = []
        for i in range(8):
            byteList.append( Cube.__toByte__(self.state[8*i:8*i+8]) )
        self.ser.write([42]+byteList)
        

    @staticmethod
    def __checkIndex__(i, j, k):
        if i < 0 or j < 0 or k < 0 or i > 3 or j > 3 or k > 3:
            return False
        else:
            return True

    @staticmethod
    def __toByte__(bools):
        total = 0
        for n in range(8):
            total += bools[n]*2**n
        return total

if __name__ == '__main__':
    print('Initializing global Cube object as "cube" for testing.')
    global cube
    cube = Cube(True)
