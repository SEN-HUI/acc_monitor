import controller.engine as eg

def parse_acc(data):
    return list(map(int, data[7:].split(" ")))

def parse_dbg(data):
    return data[:7]

data_formats = {
    "^\[ACC_L\]-?[0-9]+ -?[0-9]+ -?[0-9]+\n$": [eg.DataType.ACC_L, parse_acc],
    "^\[ACC_R\]-?[0-9]+ -?[0-9]+ -?[0-9]+\n$": [eg.DataType.ACC_R, parse_acc],
    "^\[DBG_L\].*": [eg.DataType.DBG_L, parse_dbg],
    "^\[DBG_R\].*": [eg.DataType.DBG_R, parse_dbg],
}


