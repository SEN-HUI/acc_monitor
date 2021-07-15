import re
import time
import threading
from enum import Enum
import concurrent.futures as cf

class Engine:
    def __init__(self, window):
        self.window = window
        self.reader = None
        self.dispatcher = Dispatcher()
        # thread safe
        self.started = False
        self.reader_in_use = False
        # At most one task is running makes sure that it can exit normally
        # i.e. pending tasks cannot set started to True
        self.single_executor = cf.ThreadPoolExecutor(max_workers=1)

    # called only after a self.stop()
    def close_reader(self):
        if self.reader is not None: 
            # make sure that the reader is not used
            if self.reader_in_use:
                time.sleep(1)    
            self.reader.close()

    def set_reader(self, reader):
        # firstly close the old one if any
        self.close_reader()
        # then set the new one
        self.reader = reader

    def add_writer(self, writer):
        self.dispatcher.add_writer(writer)

    def task(self):
        self.started = True
        self.dispatcher.dispatch(
            "----- [start] " + self.get_current_time() + " -----\n")
        self.reader_in_use = True
        try:
            while self.started:
                data = self.reader.readline()
                # some writers will write to the screen, which send events to the main thread
                self.dispatcher.dispatch(data)
        except BaseException as e:
            print(e)
        self.reader_in_use = False
        self.dispatcher.dispatch(
            "----- [stop] " + self.get_current_time() + " -----\n")

    def start(self):
        self.single_executor.submit(self.task)

    def stop(self):
        self.started = False

    def close(self):
        # signal to stop the running task
        self.stop()
        # append a close task
        self.single_executor.submit(self.close_task)
        # shutdown the executor (non-blocking, otherwise risky deadlock)
        self.single_executor.shutdown(wait=False)
       
    def close_task(self):
        # close the reader  
        self.close_reader()
        # close the dispatcher
        self.dispatcher.close()
        # close the window
        # window destroy will destroy will sub wedgets
        # so we need to make sure displayers are not used any more before destroying the window.
        self.window.destroy()

    def get_current_time(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return current_time

class DataType(Enum):
    ACC_L = 1
    ACC_R = 2
    DBG_L = 3
    DBG_R = 4
    OTHER = 5


class Parser():
    def __init__(self, data_formats):
        self.data_formats = data_formats

    def parse(self, data):
        for k, v in self.data_formats.items():
            if re.match(k, data):
                return v[0], v[1](data)
        return DataType.OTHER, data

class Dispatcher:
    def __init__(self):
        import controller.formats as fmt
        self.parser = Parser(fmt.data_formats)
        # fromkeys: all values refer to the same [] !!! 
        self.groups = {data_type: [] for data_type in DataType}

    def add_writer(self, writer):
        data_type = writer.get_type()
        self.groups[data_type].append(writer)

    # Observer Pattern

    def dispatch(self, data):
        data_type, parsed_data = self.parser.parse(data)
        # print(parsed_data)
        group = self.groups[data_type]
        for writer in group:
            writer.write(parsed_data)

    def cleanup(self):
        for group in self.groups.values():
            for writer in group:
                writer.cleanup()

    def close(self):
        # close all writers
        for group in self.groups.values():
            for writer in group:
                writer.close()




