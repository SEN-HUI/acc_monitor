import controller.engine as eg

app = {     
    "menu_labels": {
        "menu": (1, "Language"),
        },
    }

text_displayer = {
    eg.DataType.ACC_L: {
        "texts": {
            "lbl_title": "Raw Acc (L)",
            },
        },
    eg.DataType.ACC_R: {
        "texts": {
            "lbl_title": "Raw Acc (R)",
            },
        },
    eg.DataType.DBG_L: {
        "texts": {
            "lbl_title": "Walk (L)"
            },
        },
    eg.DataType.DBG_R: {
        "texts": {
            "lbl_title": "Walk (R)"
            },
        },
    eg.DataType.OTHER: {
        "texts": {
            "lbl_title": "Other Infors",
            },
        },
    }

io_config_form = {
    "texts": {
        "lbl_input": "Source:",
        "btn_start": "Start",
        "btn_stop": "Stop",
        "btn_clean": "Clean",
        },
    }

com_config_dialog = {
    "texts": {
        "lbl_port_head": "Port:",
        "lbl_baudrate": "Baud rate:",
        "lbl_bytesize":  "Byte Size:",
        "lbl_timeout": "Timeout (seconds)",
        "lbl_stopbits": "Stop Bits:",
        "btn_ok": "OK",
        },
    }
graph_displayer = {}
