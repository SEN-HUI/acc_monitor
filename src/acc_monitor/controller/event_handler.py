import io
import serial 
import serial.tools.list_ports as l_p;
import view.windows as ws
import myio.reader

class EventHandler:
    pass

class InputSelector(EventHandler):
    def __init__(self):
        self.options = []

    def scan(self):
        self.options = []
        # scan serial ports
        self.options += [ComConfig(port_info) for port_info in l_p.comports()]
        # scan wifis

        # read from a file
        self.options += [FileConfig()]

    def get_descriptions(self):
        return [option.get_description() for option in self.options]

    def config_input(self, idx, parent_window):
        self.options[idx].popup_config(parent_window)


class ReaderConfig:
    def get_description(self):
        pass
    def popup_config(self, parent):
        pass
    def create_reader(self, **kargs):
        pass

class ComConfig(ReaderConfig):
    parameters = {
        "baudrate": [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 256000, 460800, 500000],
        "bytesize": [
            serial.FIVEBITS,
            serial.SIXBITS,
            serial.SEVENBITS,
            serial.EIGHTBITS,
            ],
        "timeout": [0, 0.01, 0.1, 1, 2, 5, 10, None],
        "stopbits": [
            serial.STOPBITS_ONE,
            serial.STOPBITS_ONE_POINT_FIVE,
            serial.STOPBITS_TWO,
            ],
    }
    def __init__(self, port_info):
        self.port_info = port_info

    def get_description(self):
        return self.port_info.description

    def popup_config(self, parent):
        ws.ComConfigDialog(parent, self)
    
    def create_reader(self, **kargs):
        raw_com = serial.Serial(port=self.port_info.name, **kargs)
        self.reader_des = "   [port]  " + raw_com.name
        for param in ComConfig.parameters:
            exec(f"self.reader_des += '  [{param}]  ' + str(raw_com.{param})")
        return myio.reader.Reader(raw_io=raw_com), self.reader_des

class WifiConfig(ReaderConfig):
    pass

class FileConfig(ReaderConfig):
    def get_description(self):
        return "Choosing from a file..."

    def popup_config(self, parent):
        ws.FileConfigDialog(parent, self)

    def create_reader(self, **kargs):
        raw_file = io.FileIO(**kargs)
        return myio.reader.Reader(raw_io=raw_file), "[filename]  " + raw_file.name


