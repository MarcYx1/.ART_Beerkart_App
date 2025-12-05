import customtkinter as ctk
import random
import os

class MonitoringWindow():
    def __init__(self, color_mode):

        self.main = ctk.CTk()
        self.main.title("Monitoring Window")
        self.main.geometry(f"{600}x{400}")
        self.main.iconbitmap("assets/beer.ico")
        self.frames = []
        self.labels = []
        self.data = {}
        self.file_handles = {}
        self.main.resizable(False, False)
        ctk.set_appearance_mode(color_mode)
        ctk.set_default_color_theme("assets/ART_theme.json")

        for i in range(6):
            self.main.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.main.grid_columnconfigure(i, weight=1)
        
        asd = 0
        for row in range(6):
            for col in range(4):
                asd = asd + 1
                frame = ctk.CTkFrame(self.main)
                frame.grid(row=row, column=col, sticky="NSEW", padx=5, pady=5)
                self.frames.append(frame)

                label = ctk.CTkLabel(frame, text=f"cell#{asd}\n")
                label.pack(padx=0, pady=(12,0))
                self.labels.append(label)

        for i in range(24):
            self.data[f"cell#{i+1}"] = {"temp": None, "voltage": None}

        self.open_data_files()
        self.monitoring()
        self.main.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main.mainloop()

    def open_data_files(self):
        """Open all data files once and store file handles"""
        for i in range(24):
            for file in os.listdir("./live_graphs"):
                if file.startswith(f"cell#{i+1} voltage"):
                    self.file_handles[f"cell#{i+1}_voltage"] = open(f"./live_graphs/{file}", 'r')
                elif file.startswith(f" cell#{i+1} temp"):
                    self.file_handles[f"cell#{i+1}_temp"] = open(f"./live_graphs/{file}", 'r')

    def get_last_line(self, file_handle):
        """Get the last line from a file handle"""
        try:
            file_handle.seek(0, 2)
            file_size = file_handle.tell()
            if file_size == 0:
                return ""
            
            file_handle.seek(max(0, file_size - 1024))
            lines = file_handle.readlines()
            return lines[-1].strip() if lines else ""
        except:
            return ""

    def monitoring(self):
        for i in range(24):
            cell_key = f"cell#{i+1}"
            
            voltage_handle = self.file_handles.get(f"{cell_key}_voltage")
            if voltage_handle:
                last_line = self.get_last_line(voltage_handle)
                if last_line and ',' in last_line:
                    self.data[cell_key]["voltage"] = last_line.split(',')[1]
            
            temp_handle = self.file_handles.get(f"{cell_key}_temp")
            if temp_handle:
                last_line = self.get_last_line(temp_handle)
                if last_line and ',' in last_line:
                    self.data[cell_key]["temp"] = last_line.split(',')[1]

        for i, label in enumerate(self.labels):
            cell_name = label.cget("text").split("\n")[0]
            voltage = self.data[cell_name].get("voltage", "N/A")
            temp = self.data[cell_name].get("temp", "N/A")
            
            if voltage and temp:
                voltage_display = voltage.replace("_", " ")
                temp_display = temp.replace("_", " ")
                label.configure(text=f"{cell_name}\n{voltage_display} | {temp_display}")
            else:
                label.configure(text=f"{cell_name}\nNo data")
                
        self.main.after(50, self.monitoring)

    def on_closing(self):
        """Close all file handles before closing the window"""
        for file_handle in self.file_handles.values():
            if file_handle and not file_handle.closed:
                file_handle.close()
        self.main.destroy()

if __name__ == "__main__":
    app = MonitoringWindow(color_mode="Dark")