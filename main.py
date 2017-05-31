#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as Tk
from app import App
from datasource import MongoDataSource
from exporter import ExcelExporter

if __name__ == "__main__":
    window = Tk.Tk()
    App(window, MongoDataSource(), ExcelExporter())
    window.mainloop()
