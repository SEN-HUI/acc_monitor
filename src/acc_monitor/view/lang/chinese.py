import controller.engine as eg

app = {     
    "menu_labels": {
        "menu": (1, "语言"),
        },
    }

text_displayer = {
    eg.DataType.ACC_L: {
        "texts": {
            "lbl_title": "加速度数据(L)",
            },
        },
    eg.DataType.ACC_R: {
        "texts": {
            "lbl_title": "加速度数据(R)",
            },
        },

    eg.DataType.OTHER: {
        "texts": {
            "lbl_title": "其他信息",
            },
        },
    }

io_config_form = {
    "texts": {
        "lbl_input": "信号源:",
        "btn_start": "开始",
        "btn_stop": "停止",
        "btn_clean": "清除窗口",
        },
    }

com_config_dialog = {
    "texts": {
        "lbl_port_head": "端口号:",
        "lbl_baudrate": "波特率:",
        "lbl_bytesize":  "字节大小:",
        "lbl_timeout": "超时(秒):",
        "lbl_stopbits": "停止位:",
        "btn_ok": "OK",
        },
    }
graph_displayer ={}
