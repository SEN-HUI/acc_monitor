import io
import serial
class Reader(io.IOBase):
    def __init__(self, raw_io, encoding='utf-8'):
        self.encoding = encoding
        self.raw_io = raw_io 

    def readline(self):
        return self.raw_io.readline().decode(self.encoding)

    def close(self):
        self.raw_io.close()
