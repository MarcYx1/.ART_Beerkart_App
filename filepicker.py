import customtkinter as ctk
from tkinter import messagebox
from CTkListbox import *
import os, sys, threading, subprocess
import multiprocessing
from graph import Grapher as gr  # Import graph module directly

# Helper function to get the correct resource path for PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Filepicker:
    def __init__(self, color_mode, file_action_mode, live_graph):

        self.files = {}
        self.live_graph = live_graph
        self.app = ctk.CTk()
        self.app.title("File Picker")
        self.app.geometry("400x300")
        self.app.iconbitmap(resource_path("assets/beer.ico"))
        self.app.resizable(False, False)

        ctk.set_appearance_mode(color_mode)
        ctk.set_default_color_theme(resource_path("assets/ART_theme.json"))

        self.optionlist = CTkListbox(self.app, multiple_selection=True, command=self.on_file_select)
        self.optionlist.pack(padx=10, pady=10, fill="both", expand=True)

        if file_action_mode == "open":
            self.open_button = ctk.CTkButton(self.app, text="Open Selected File(s)", command=self.open_file)
            self.open_button.pack(pady=10)
        elif file_action_mode == "delete":
            self.delete_button = ctk.CTkButton(self.app, text="Delete Selected File(s)", command=self.delete_file)
            self.delete_button.pack(pady=10)
        # print("Initializing file picker...")
        self.populate_listbox()

    def populate_listbox(self):
        # print("Populating file list...")
        if self.live_graph == "live":
            dfiles = os.listdir("./live_graphs")
        else:
            dfiles = os.listdir("./graphs")
        self.files.clear()
        # print(f'after clear {self.files}')

        for file in dfiles:
            parts = file.split('_')
            # print(f"Processing file: {file} -> parts: {parts}")
            self.files.update({file: {}})
            self.files[file]["name"] = parts[0] # name
            self.files[file]["date"] = parts[1] # date
            self.files[file]["time"] = parts[2] # time
            # print(f'after set {self.files}')
            #              name         years             month             day               hour              minute            seconds
            # print(f"Found file: {parts[0]} {parts[1][0:4]}.{parts[1][4:6]}.{parts[1][6:8]} {parts[2][0:2]}:{parts[2][2:4]}:{parts[2][4:6]}")
        
        # Sort files by date and time (newest first)
        sorted_files = sorted(self.files.keys(), 
                             key=lambda x: (self.files[x]['date'], self.files[x]['time']), 
                             reverse=True)
        
        # Insert sorted files into the listbox
        for file in sorted_files:
            self.optionlist.insert("end", f"{self.files[file]['name']}   |   {self.files[file]['date'][0:4]}.{self.files[file]['date'][4:6]}.{self.files[file]['date'][6:8]}   |   {self.files[file]['time'][0:2]}:{self.files[file]['time'][2:4]}:{self.files[file]['time'][4:6]}")  
        # print(self.files)
                

    def on_file_select(self, selection):
        self.files_list = []
        try:
            for item in selection:
                    if self.live_graph == "live":
                        self.files_list.append(f'./live_graphs/{item.replace("   |   ", "_").replace(".", "").replace(":", "")}.txt')
                    else:
                        self.files_list.append(f'./graphs/{item.replace("   |   ", "_").replace(".", "").replace(":", "")}.txt')
        except:
            pass
        # print(self.files)

    def open_file(self):
        for file in self.files_list:
            # Use multiprocessing instead of threading for matplotlib
            process = multiprocessing.Process(target=gr().plot, args=(file,))
            process.daemon = True
            process.start()
        self.app.after(10, self.app.destroy)
    
    def delete_file(self):
        bogz = messagebox.askquestion("File selection", "Are you sure you want to select the chosen file(s)?", icon='warning')
        if bogz != 'yes':
            return
        for item in self.files_list:
            try:
                os.remove(item)
            except Exception as e:
                messagebox.showerror("Hiba", f"Unable to delete file(s): {e}")
        self.app.after_idle(self.app.destroy)