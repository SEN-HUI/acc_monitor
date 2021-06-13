import io

class Writer(io.IOBase):
    def __init__(self, data_type):
        self.data_type = data_type

    def get_type(self):
        return self.data_type

    def write(self, data):
        pass

    def cleanup(self):
        pass

    def close(self):
        pass

# Decorator Pattern

class WriterWrapper(Writer):
    def __init__(self, inner_writer):
        self.inner_writer = inner_writer

    def get_type(self):
        return self.inner_writer.get_type()

    def write(self, data):
        self.inner_writer.write(data)

    def cleanup(self):
        self.inner_writer.cleanup()

    def close(self):
        self.inner_writer.close()

class BufferedWriter(WriterWrapper):
    def __init__(self, inner_writer, buf_size):
        WriterWrapper.__init__(self, inner_writer)
        self.buf_size = buf_size
        self.buf = []

    def write(self, data):
        self.buf.append(data)
        if len(self.buf) == self.buf_size:
            self.inner_writer.write(self.buf)
            self.buf = []

