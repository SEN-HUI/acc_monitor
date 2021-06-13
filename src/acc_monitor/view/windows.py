import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import view.lang.english as l_us
import view.lang.chinese as l_cn
import view.style.stylesheet as sss
import controller.event_handler as eh
import controller.engine as eg
import myio.writer
import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl

def update_lang(window, resource): 
    for group_name, sub_dir in resource.items():
        if group_name == "menu_labels":
            # update menu items
            for name, (idx, lbl) in sub_dir.items():
                exec(f"window.{name}.entryconfig({idx}, label='{lbl}')")
        elif group_name == "texts":
            # update widget texts
            for name, txt in sub_dir.items():
                exec(f"window.{name}.config(text='{txt}')")

class App(tk.Tk):
    lang = None

    def __init__(self):
        tk.Tk.__init__(self)
        
        # the window holds a reference to an engine instance
        self.engine = eg.Engine(self)
        
        self.title("Exo Skeleton")

        self.menu = tk.Menu(master=self) # menu
        self.config(menu=self.menu)

        self.menu_lang = tk.Menu(master=self.menu)
        self.menu.add_cascade(menu=self.menu_lang)
        self.menu_lang.add_command(
            label="English", command=lambda : self.switch_lang(l_us))
        self.menu_lang.add_command(
            label="中文", command=lambda : self.switch_lang(l_cn))
        '''
        self.rowconfigure([0], weight=1)
        self.columnconfigure([0], weight=1)
        
        self.canvas = MainCanvas(self)
        self.canvas.grid(row=0, column=0, cnf=sss.canvas_position_cnf)

        self.sb= tk.Scrollbar(master=self, cnf=sss.scrollbar_look_cnf, command=self.canvas.yview)
        self.sb.grid(row=0, column=1, cnf=sss.scrollbar_position_cnf)

        self.canvas["yscrollcommand"] = self.sb.set
        '''
        # grid geometry manager
        self.rowconfigure([0, 1, 2], weight=1)
        self.columnconfigure([2], weight=1)

        self.displayers = []
        # left acc text grid ([0,1],0])
        self.left_acc_text_displayer = TextDisplayer(self, eg.DataType.ACC_L)
        self.left_acc_text_displayer.grid(row=0, column=0, rowspan=2, cnf=sss.displayer_position_cnf)
        self.add_writer(self.left_acc_text_displayer)
        self.displayers.append(self.left_acc_text_displayer)
        # right acc text grid ([0,1],1)
        self.right_acc_text_displayer = TextDisplayer(self, eg.DataType.ACC_R)
        self.right_acc_text_displayer.grid(row=0, column=1, rowspan=2, cnf=sss.displayer_position_cnf)
        self.add_writer(self.right_acc_text_displayer)
        self.displayers.append(self.right_acc_text_displayer)
 
        # other grid (2,[0,1])
        self.other_text_displayer = TextDisplayer(self, eg.DataType.OTHER)
        # override default setting
        # self.other_text_displayer.text.width = 40
        self.other_text_displayer.grid(row=2, column=0, columnspan=2, cnf=sss.displayer_position_cnf)
        self.add_writer(self.other_text_displayer)
        self.displayers.append(self.other_text_displayer)
        
        # set figure buffer to speed up rendering
        self.buf_size = 5
        # left graph grid (0,2)
        self.left_acc_graph_displayer = GraphDisplayer(self, eg.DataType.ACC_L)
        self.left_acc_graph_displayer.grid(row=0, column=2, cnf=sss.displayer_position_cnf)
        self.add_writer(myio.writer.BufferedWriter(self.left_acc_graph_displayer, self.buf_size))
        self.displayers.append(self.left_acc_graph_displayer)
        # right graph grid (1,2)
        self.right_acc_graph_displayer = GraphDisplayer(self, eg.DataType.ACC_R)
        self.right_acc_graph_displayer.grid(row=1, column=2, cnf=sss.displayer_position_cnf)
        self.add_writer(myio.writer.BufferedWriter(self.right_acc_graph_displayer, self.buf_size))
        self.displayers.append(self.right_acc_graph_displayer)


        # config grid (2,0)
        self.config_form = IOConfigForm(self)
        self.config_form.grid(row=2, column=2, cnf=sss.form_position_cnf)
        # control grid (2,1)
    

        # register cleanup callback when closing window
        self.protocol("WM_DELETE_WINDOW", self.close)

        # default
        self.switch_lang(l_us)
        self.clicks = 0
        self.mainloop()
   
    def switch_lang(self, lang):
        App.lang = lang
        self.update_lang()
    
    def update_lang(self):
        update_lang(self, App.lang.app)
        for displayer in self.displayers:
            displayer.update_lang()
        self.config_form.update_lang()
    '''
    def update_lang(self):
        update_lang(self, App.lang.app)
        self.canvas.update_lang()
    '''
    def start_engine(self):
        self.engine.start()

    def stop_engine(self):
        self.engine.stop()
    
    def set_reader(self, reader):
        self.engine.set_reader(reader)

    def add_writer(self, writer):
        self.engine.add_writer(writer)

    def clean_screen(self):
        for displayer in self.displayers:
            displayer.cleanup()

    def close(self):
        self.engine.close()
'''
class MainCanvas(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, master=parent)
        
        #self.rowconfigure([0], weight=1)
        #self.columnconfigure([0], weight=1)
        
        self.main_frame = MainFrame(self)
        # self.main_frame.grid(row=0, column=0, cnf=sss.main_frame_position_cnf)
        self.main_frame_iid = self.create_window(0, 0, window=self.main_frame, anchor="nw")
        self.main_frame.bind("<Configure>", self.canvas_configure)
     
    def canvas_configure(self, event):
        self.itemconfigure(self.main_frame_iid, width=self.winfo_width())
        self.configure(scrollregion=self.bbox("all"))

    def start_engine(self):
        self.master.start_engine()

    def stop_engine(self):
        self.master.stop_engine()
    
    def set_reader(self, reader):
        self.master.set_reader(reader)

    def add_writer(self, writer):
        self.master.add_writer(writer)

    def update_lang(self):
        self.main_frame.update_lang()

class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, master=parent)
        
        # grid geometry manager
        self.rowconfigure([0], weight=1)
        self.columnconfigure([2], weight=1)

        # data grid (0,0)
        self.acc_text_displayer = TextDisplayer(self, eg.DataType.ACC)
        self.acc_text_displayer.grid(row=0, column=0, cnf=sss.displayer_position_cnf)
        self.add_writer(self.acc_text_displayer)
        
        # other grid (0,1)
        self.other_text_displayer = TextDisplayer(self, eg.DataType.OTHER)
        self.other_text_displayer.grid(row=0, column=1, cnf=sss.displayer_position_cnf)
        self.add_writer(self.other_text_displayer)
        
        # graph grid (0,2)
        self.acc_graph_displayer = GraphDisplayer(self)
        self.acc_graph_displayer.grid(row=0, column=2, cnf=sss.displayer_position_cnf)
        self.add_writer(self.acc_graph_displayer)
        

        # config grid (1,0)
        self.config_form = IOConfigForm(self)
        self.config_form.grid(row=1, column=0, columnspan=3, cnf=sss.form_position_cnf)
        # control grid (2,1)
    
    def start_engine(self):
        self.master.start_engine()

    def stop_engine(self):
        self.master.stop_engine()
    
    def set_reader(self, reader):
        self.master.set_reader(reader)

    def add_writer(self, writer):
        self.master.add_writer(writer)

    def update_lang(self):
        update_lang(self, App.lang.main_frame)
        self.acc_text_displayer.update_lang()
        self.other_text_displayer.update_lang()
        self.acc_graph_displayer.update_lang()
        self.config_form.update_lang()
    
'''
class TextDisplayer(tk.Frame, myio.writer.Writer):
    def __init__(self, parent, data_type):
        tk.Frame.__init__(self, master=parent, cnf=sss.monitor_look_cnf)
        myio.writer.Writer.__init__(self, data_type)

        self.rowconfigure([1], weight=1)
        # self.columnconfigure([0], weight=1)

        self.lbl_title = tk.Label(master=self) # lbl_title
        self.lbl_title.grid(row=0, column=0, columnspan=2)
        
        self.text = tk.Text(master=self, cnf=sss.text_look_cnf)
        self.text.grid(row=1, column=0, cnf=sss.text_position_cnf)

        self.sb = tk.Scrollbar(master=self, cnf=sss.scrollbar_look_cnf, command=self.text.yview)
        self.sb.grid(row=1, column=1, cnf=sss.scrollbar_position_cnf)

        self.text["yscrollcommand"] = self.sb.set

    def write(self, data):
        if isinstance(data, str):
            line = data
        else:
            line = str(data) + "\n"
        self.text.insert(tk.END, line) 
        self.text.see(tk.END)

    def cleanup(self):
        self.text.delete("1.0", tk.END)
    
    def update_lang(self):
        update_lang(self, App.lang.text_displayer[self.data_type])

class GraphDisplayer(tk.Frame, myio.writer.Writer):
    def __init__(self, parent, data_type):
        tk.Frame.__init__(self, master=parent, cnf=sss.monitor_look_cnf)
        myio.writer.Writer.__init__(self, data_type)
        
        self.rowconfigure([0], weight=1)
        self.columnconfigure([0], weight=1)

        self.fig, self.ax = plt.subplots()
       
        self.len = 500
        self.X = np.arange(self.len)
        self.acc = np.zeros((2, self.len))
        self.lines = self.ax.plot(self.X, self.acc.T)
        self.lbls = ["x", "y"]
        for line, lbl in zip(self.lines, self.lbls):
            line.set_label(lbl)
        self.ax.set_xlabel("time")
        self.ax.set_ylabel("acc(g)")
        self.ax.set_ylim(-2000, 2000)
        self.ax.legend()

        mpl.rcParams["path.simplify"] = True
        mpl.rcParams["path.simplify_threshold"] = 1
        mpl.rcParams['agg.path.chunksize'] = self.len / 10

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.bm = BlitManager(self.canvas, self.lines)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, cnf=sss.canvas_position_cnf)
       

    def update_acc(self, accs):
        n = len(accs)
        ACC = np.array(accs).T[:2]
        self.acc = np.append(self.acc[:, n:], ACC, axis=1)
        [line.set_ydata(acc) for line, acc in zip(self.lines, self.acc)]

    def write(self, accs):
        self.update_acc(accs)
        self.bm.update()

    def cleanup(self):
        self.write(np.zeros((self.len, 3)))

    def update_lang(self):
        update_lang(self, App.lang.graph_displayer)

class BlitManager:
    def __init__(self, canvas, animated_artists):
        self.canvas = canvas
        self.bg = None
        self.artists = []

        for a in animated_artists:
            self.add_artist(a)
        
        canvas.mpl_connect("draw_event", self.on_draw)

    def on_draw(self, event):
        cv = self.canvas
        self.bg = cv.copy_from_bbox(cv.figure.bbox)
        self.draw_animated()

    def add_artist(self, art):
        art.set_animated(True)
        self.artists.append(art)

    def draw_animated(self):
        fig = self.canvas.figure
        for a in self.artists:
            fig.draw_artist(a)

    def update(self):
        
        cv = self.canvas
        fig = cv.figure
        if self.bg is None:
            self.on_draw(None)
        else:
            cv.restore_region(self.bg)
            self.draw_animated()
            cv.blit(fig.bbox)
            cv.flush_events()
            

class IOConfigForm(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, master=parent)
        # self.frm_config.grid(row=2, column=0, cnf=sss.form_position_cnf)
        self.columnconfigure([1], weight=1, minsize=100)

        self.lbl_input = tk.Label(master=self, cnf=sss.form_lbl_look_cnf) # lbl_input
        self.lbl_input.grid(row=0, column=0, cnf=sss.form_lbl_position_cnf)

        # the configure Frame holds a reference to a input selector instance
        self.input_selector = eh.InputSelector()

        self.cbx_input = ttk.Combobox(master=self, state="readonly", 
                postcommand=self.update_inputs)
        self.cbx_input.grid(row=0, column=1, cnf=sss.form_input_position_cnf)
        self.cbx_input.bind("<<ComboboxSelected>>", self.config_input)
        ''' 
        self.reader_details_table = Table(self, {})
        self.reader_details_table.grid(row=1, column=1, cnf=sss.table_position_cnf)
        '''
        self.lbl_reader_description = tk.Label(master=self)
        self.lbl_reader_description.grid(row=1, column=1)

        self.frm_btns = tk.Frame(master=self)
        self.frm_btns.grid(row=2, column=0, columnspan=2, cnf=sss.form_btns_position_cnf)

        self.btn_stop = tk.Button(master=self.frm_btns, command=self.stop_engine) # btn_stop
        self.btn_stop.pack(cnf=sss.btn_position_cnf)
        self.btn_stop["state"] = tk.DISABLED 

        self.btn_start = tk.Button(master=self.frm_btns, command=self.start_engine) # btn_start
        self.btn_start.pack(cnf=sss.btn_position_cnf)
        self.btn_start["state"] = tk.DISABLED 
        
        self.btn_clean = tk.Button(master=self.frm_btns, command=self.clean_screen) # btn_clean
        self.btn_clean.pack(cnf=sss.btn_position_cnf, before=self.btn_stop)
       
    def clean_screen(self):
        self.master.clean_screen()

    def start_engine(self):
        self.btn_start["state"] = tk.DISABLED 
        self.cbx_input["state"] = "disabled"
        self.master.start_engine()
        self.btn_stop["state"] = tk.NORMAL

    def stop_engine(self):
        self.btn_stop["state"] = tk.DISABLED
        self.master.stop_engine()
        self.btn_start["state"] = tk.NORMAL
        self.cbx_input["state"] = "readonly"

    def update_inputs(self):
        self.input_selector.scan()    
        self.cbx_input["values"] = self.input_selector.get_descriptions()
    
    def config_input(self, event):
        self.input_selector.config_input(event.widget.current(), self)
    
    def set_reader(self, reader, description):
        '''
        details = reader.get_details()
        self.reader_details_table.destroy()
        self.reader_details_table = Table(self, details)
        self.reader_details_table.grid(row=1, column=1, cnf=sss.table_position_cnf)
        '''
        self.btn_start["state"] = tk.NORMAL
        self.lbl_reader_description["text"] = description 
        self.master.set_reader(reader)
    
    def update_lang(self):
        update_lang(self, App.lang.io_config_form)
'''
class Table(tk.Frame):
    def __init__(self, parent, data):
        tk.Frame.__init__(self, master=parent)
        
        self.len = len(data)
        for (k, v), idx in zip(data.items(), range(self.len)):
            th = tk.Label(master=self, text=k, cnf=sss.form_lbl_look_cnf)
            th.grid(row=idx, column=0, cnf=sss.form_lbl_position_cnf)
            td = tk.Label(master=self, text=v)
            td.grid(row=idx, column=1)
'''          
class ReaderConfigDialog():
    """Reader config Dialog Base Class"""
    def __init__(self, parent, reader_config):
        self.parent = parent
        self.reader_config = reader_config

    def submit(self):
        pass

class FileConfigDialog(ReaderConfigDialog):
    def __init__(self, parent, file_config):
        ReaderConfigDialog.__init__(self, parent, file_config)
        self.filename = fd.askopenfilename()
        if self.filename != "":
            self.submit()

    def submit(self):
        self.parent.set_reader(*self.reader_config.create_reader(file=self.filename))

class ComConfigDialog(tk.Toplevel, ReaderConfigDialog):
    def __init__(self, parent, com_config):
        tk.Toplevel.__init__(self, master=parent)
        ReaderConfigDialog.__init__(self, parent, com_config)
        
        # form
        self.columnconfigure(1, weight=1, minsize=150)   
        
        self.lbl_port_head = tk.Label(master=self, cnf=sss.form_lbl_look_cnf)
        self.lbl_port_head.grid(row=0, column=0, cnf=sss.form_lbl_position_cnf)
        self.lbl_port_value = tk.Label(master=self, text=self.reader_config.get_description())
        self.lbl_port_value.grid(row=0, column=1)

        # GUI should not be coupled to controller attributes
        self.params = self.reader_config.parameters
        for (param, param_options), idx in zip(self.params.items(), range(1, len(self.params) + 1)):
            exec(f"self.lbl_{param} = tk.Label(master=self, cnf=sss.form_lbl_look_cnf)")
            exec(f"self.lbl_{param}.grid(row={idx}, column=0, cnf=sss.form_lbl_position_cnf)")

            exec(f"self.cb_{param} = ttk.Combobox(master=self, values=param_options)")
            exec(f"self.cb_{param}.grid(row={idx}, column=1, cnf=sss.form_input_position_cnf)")
           
        
        # buttons
        self.btn_ok = tk.Button(master=self, command=self.submit) # btn_ok
        self.btn_ok.grid(row=len(self.params)+1, column=1)

        self.update_lang()
    
    def submit(self):
        args = {}
        for param in self.params:
            exec(f"args[param] = self.params[param][self.cb_{param}.current()]")
        self.parent.set_reader(*self.reader_config.create_reader(**args))
        self.destroy()
        
    def update_lang(self):
        update_lang(self, App.lang.com_config_dialog)

