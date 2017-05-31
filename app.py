#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as Tk
import ttk

class App(object):
    def __init__(self, master, datasource, exporter):
        self.datasource = datasource
        self.exporter = exporter
        master.geometry('{}x{}'.format(250, 200))
        self.layout = Tk.Frame(master)
        self.layout.pack(padx=15, pady=10, fill=Tk.X)
        self.__create_widgets()

    def __create_widgets(self):
        database_label = Tk.Label(self.layout, text='Select a database:', justify=Tk.RIGHT)
        database_label.pack(anchor='w', pady=(0, 5))

        self.database_combobox = ttk.Combobox(self.layout, values=self.datasource.get_database_names(), state="readonly")
        self.database_combobox.current(0)
        self.database_combobox.pack(anchor='w', fill=Tk.X, pady=(0, 15))
        self.database_combobox.bind('<<ComboboxSelected>>', self.__populate_collections)

        collection_label = Tk.Label(self.layout, text='Select a collection:', justify=Tk.RIGHT)
        collection_label.pack(anchor='w', pady=(0, 5))

        self.collection_combobox = ttk.Combobox(self.layout, state="readonly")
        self.collection_combobox.pack(anchor='w', fill=Tk.X, pady=(0, 10))

        self.button = Tk.Button(self.layout, state=Tk.DISABLED, text='Export', justify=Tk.RIGHT, command=lambda: self.__export_collection())
        self.button.pack(anchor='w', pady=(0, 10))

        self.info_label = Tk.Label(self.layout, text='', justify=Tk.RIGHT)
        self.info_label.pack(anchor='w', pady=(0, 5))

    def __export_collection(self):
        self.info_label['text'] = 'Generating file..'
        database = self.database_combobox.get()
        collection = self.collection_combobox.get()
        filename = self.exporter.export({'db': database, 'collection': collection, 'data': self.datasource.get_data_from_collection(database, collection)})
        self.info_label['text'] = filename

    def __populate_collections(self, event):
        database_name = event.widget.get()
        self.collection_combobox['values'] = self.datasource.get_collections(database_name)
        self.collection_combobox.current(0)
        self.button['state'] = Tk.NORMAL
