import controller.engine as eg

def parse_acc(data):
    return list(map(int, data[7:].split(" ")))

data_formats = {
    "^\[ACC_L\]-?[0-9]+ -?[0-9]+ -?[0-9]+\n$": [eg.DataType.ACC_L, parse_acc],
    "^\[ACC_R\]-?[0-9]+ -?[0-9]+ -?[0-9]+\n$": [eg.DataType.ACC_R, parse_acc],
    "^\[DEBUG\].*": [eg.DataType.DEBUG, lambda data: data],
}


