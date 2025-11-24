import customtkinter as ctk
from CTkListbox import *
import os, sys

class Main:
    def __init__(self, color_mode):

        self.files = {}
        self.app = ctk.CTk()
        self.app.title("File Picker")
        self.app.geometry("400x300")
        self.app.iconbitmap("./assets/beer.ico")
        self.app.resizable(False, False)

        ctk.set_appearance_mode(color_mode)
        ctk.set_default_color_theme("./assets/ART_theme.json")


        self.label = ctk.CTkLabel(self.app, text="Select a file from the list:")
        self.label.pack(pady=10)

        self.optionlist = CTkListbox(self.app, multiple_selection=True, command=self.on_file_select)
        self.optionlist.pack(pady=10, fill="both", expand=True)

        self.open_button = ctk.CTkButton(self.app, text="Open Selected File", command=self.open_file)
        self.open_button.pack(pady=10)
        print("Initializing file picker...")
        self.populate_listbox()

    def populate_listbox(self):
        print("Populating file list...")
        files = os.listdir("./graphs")

        for index, file in enumerate(files):
            parts = file.split('_')
            print(f"Processing file: {file} -> parts: {parts}")
            self.files.update({file: {}})
            self.files[file]["name"] = parts[0] # name
            self.files[file]["date"] = parts[1] # date
            self.files[file]["time"] = parts[2] # time
            #              name         years             month             day               hour              minute            seconds
            print(f"Found file: {parts[0]} {parts[1][0:4]}.{parts[1][4:6]}.{parts[1][6:8]} {parts[2][0:2]}:{parts[2][2:4]}:{parts[2][4:6]}")
        
        # Sort files by date and time (newest first)
        sorted_files = sorted(self.files.keys(), 
                             key=lambda x: (self.files[x]['date'], self.files[x]['time']), 
                             reverse=True)
        
        # Insert sorted files into the listbox
        for file in sorted_files:
            self.optionlist.insert("end", f"{self.files[file]['name']}   |   {self.files[file]['date'][0:4]}.{self.files[file]['date'][4:6]}.{self.files[file]['date'][6:8]}   |   {self.files[file]['time'][0:2]}:{self.files[file]['time'][2:4]}:{self.files[file]['time'][4:6]}")
        
        print(self.files)
                

    def on_file_select(self, selection):
        print("Selected file:", selection)
        self.selected_file = selection

    def open_file(self):
        print(f"Opening file: {self.selected_file}")


if __name__ == "__main__":
    Main(color_mode=sys.argv[1]).app.mainloop()