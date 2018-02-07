from tkinter import *
import ctypes
import time

import baidu_search
from baidu_search.spiders.baidu_spider import BaiduSpider
from baidu_search.spiders.ip_agent import IPAgentHelper
from scrapy.cmdline import execute
import logging
import datetime
import baidu_search.settings

logging.basicConfig(filename='..\crawler_%s.log' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S'),
                    level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %p')
logging.debug('Test....')

class Application(Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.center_window(self.master, 250, 150)
        self.pack()
        self.input_text = '天涯'
        self.create_widgets()

    def create_widgets(self):
        label = Label(self, text='Input the key words what you think')
        label.pack(padx=5, pady=10)
        self.nameInput = Entry(self, width=40)
        self.nameInput.pack(padx=5, pady=5)
        closeButton = Button(self, text='confirm', command=self.closeFrame)
        closeButton.pack(padx=5, pady=20)

    def closeFrame(self):
        text = self.nameInput.get()
        if text:
            self.input_text = text
        self.quit()

    def center_window(self, root, width, height):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2 - 100)
        root.maxsize(width, height)
        root.minsize(width, height)
        root.iconbitmap('6464.ico')
        # root.wm_iconbitmap(r'6464.ico')
        root.geometry(size)

app = Application()
app.master.title('Input')
app.mainloop()
print(app.input_text)
logging.info('<BDS> keyword: %s' % app.input_text)
BaiduSpider.key_word = app.input_text
execute(['scrapy', 'crawl', 'baidu_search'])
