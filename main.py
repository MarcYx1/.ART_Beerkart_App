import customtkinter as ctk
from PIL import Image
import subprocess, sys, os
import threading
from tkinter import messagebox
from sampler import Sampler as slr
    
# Declare globals at module level
sampler_thread = None
data_indicator_job = None  # Add this for the flashing animation

if __name__ == "__main__":

    # CTK appearance
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # CTK itself
    app = ctk.CTk()
    app.title("Art Beerkart Manager")
    app.iconbitmap("beer.ico")
    app.geometry("770x520")
    app.resizable(False, False)

    # The top frame with the title and logo
    top_frame = ctk.CTkFrame(app, fg_color="#CD1B2B", height=64)
    top_frame.pack(fill="x", side="top", padx=10, pady=10)
    top_frame.grid_columnconfigure(0, weight=1)
    top_frame.grid_columnconfigure(1, weight=0)
    
    # Title
    title_label = ctk.CTkLabel(top_frame,
                    text="Art Beerkart Manager",
                    text_color="white",
                    fg_color="transparent",
                    font=ctk.CTkFont(size=20, weight="bold"))
    
    # Logo
    pil_img = Image.open("Art_logo.png")
    logo_image = ctk.CTkImage(pil_img, size=(93, 48))
    img_label = ctk.CTkLabel(top_frame, image=logo_image, text="")
    img_label.image = logo_image  # keep reference
    img_label.grid(row=0, column=1, padx=12, pady=8, sticky="e")

    # Title placement
    title_label.grid(row=0, column=0, padx=12, pady=8, sticky="w")

    # Columns (2)
    content_frame = ctk.CTkFrame(app, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=12, pady=12)
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    # Left column and Right column
    left_col = ctk.CTkFrame(content_frame, fg_color="transparent")
    left_col.grid(row=0, column=0, padx=(0, 6), sticky="nsew")
    right_col = ctk.CTkFrame(content_frame, fg_color="#2B2B2B")
    right_col.grid(row=0, column=1, padx=(6, 0), sticky="nsew")

    # LEft coloumn content (split into two rows)

    left_col.grid_rowconfigure(0, weight=1)
    left_col.grid_rowconfigure(1, weight=1)
    left_col.grid_columnconfigure(0, weight=1)
    
    # Name implies, refreshes the COM ports list in the segmented button
    def refresh_ports():
        ports = slr().list_available_ports()
        serial_button.configure(values=ports)
        if ports:
            serial_button.set(ports[0])
        else:
            serial_button.set("No Ports")

    # Top row: Serial Connection widgets
    top_row = ctk.CTkFrame(left_col, fg_color="#2B2B2B")
    top_row.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0,4))

    # COM / serial ports
    serial_label = ctk.CTkLabel(top_row, text="Serial Connection", font=ctk.CTkFont(size=16, weight="bold"))
    serial_label.pack(padx=16, pady=(8,8))

    refresh_button = ctk.CTkButton(top_row, hover_color="#E9444F", fg_color="#CD1B2B", text="Refresh Ports", command=refresh_ports)
    refresh_button.pack(padx=16, pady=(0,8))

     # Segmented button for available serial ports
    serial_button = ctk.CTkSegmentedButton(top_row, values=slr().list_available_ports(), fg_color="#CD1B2B", selected_color="#350A0A")
    serial_button.pack(padx=16, pady=(0,8))

    # Name implies, connects to the selected serial port
    def connect_serial():
        port = serial_button.get()
        try:
            slr().connect(port)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to {port}:\n{str(e)}")
            return

        status_label.configure(text="Status: Connected")
        connect_button.configure(state="disabled", fg_color="#350A0A")
        disconnect_button.configure(state="normal", fg_color="#CD1B2B")
        # Start checking for data

    # Name implies, disconnects from the serial port
    def disconnect_serial():

        global data_indicator_job

        stop_sampler(stop_button, start_button, sampler_label)

        sampler_instance.disconnect()
        status_label.configure(text="Status: Disconnected")
        connect_button.configure(state="normal", fg_color="#CD1B2B")
        disconnect_button.configure(state="disabled", fg_color="#350A0A")
        # Cancel any pending flash animation
        if data_indicator_job:
            app.after_cancel(data_indicator_job)
        # Reset button color
        serial_button.configure(selected_color="#350A0A")

     # Status label + Connect / Disconnect buttons
    status_label = ctk.CTkLabel(top_row, text="Status: Disconnected", font=ctk.CTkFont(size=12))
    status_label.pack(padx=16, pady=(0,8))

    connect_button = ctk.CTkButton(top_row, hover_color="#E9444F", fg_color="#CD1B2B", text="Connect", command=connect_serial)
    disconnect_button = ctk.CTkButton(top_row, hover_color="#E9444F", fg_color="#350A0A", text="Disconnect", state="disabled", command=disconnect_serial)
    
    connect_button.pack(side="left", padx=16)
    disconnect_button.pack(side="right", padx=16)

    # Bottom row: placeholder for additional controls
    bottom_row = ctk.CTkFrame(left_col, fg_color="#2B2B2B")
    bottom_row.grid(row=1, column=0, sticky="nsew", padx=0, pady=(4,0))

    bottom_label = ctk.CTkLabel(bottom_row, text="Power limit", font=ctk.CTkFont(size=14, weight="bold"))
    bottom_label.pack(padx=16, pady=12)

    # horizontal container for entry + slider + button
    controls_frame = ctk.CTkFrame(bottom_row, fg_color="transparent")
    controls_frame.pack(fill="x", padx=16)

    # When slider changes, update entry
    def power_slider_event(value):
        power_entry.delete(0, ctk.END)
        power_entry.insert(0, str(int(value)))

    # Send power data
    def power_data_send():
        try:
            # I already have a layer that prevents sending non numbers or negative numbers but just in case this checks if the entry is a number and higher than 0
            # checks if it's a valid percentage (0-100)
            if power_entry.get().isdigit() and 0 <= int(power_entry.get()) <= 100:
                sampler_instance.send_data("power", power_entry.get())
            else:
                messagebox.showerror("Input Error", "Please enter a valid power percentage (0-100).")
        except Exception as e:
            messagebox.showerror("Send Error", f"Could not send power data:\n{str(e)}")
    
    power_slider = ctk.CTkSlider(controls_frame, from_=0, to=100, button_color="#CD1B2B", hover="#E9444F", command=power_slider_event)
    power_slider.pack(side="left", padx=(0,8), fill="x", expand=True)

    # First layer of checking the entry if it contains a valid value, if a character is present delete the whole entry
    def power_entry_event(self):
        val = power_entry.get()
        if val.isdigit() and 0 <= int(val) <= 100:
            power_slider.set(int(val))
        else:  # Remove last char if invalid
            power_entry.delete(0, ctk.END)

    power_entry = ctk.CTkEntry(controls_frame, placeholder_text="Power (%)", width=80, height=28)
    power_entry.bind("<KeyRelease>", power_entry_event)
    power_entry.pack(side="left", padx=(0,8))

    send_button = ctk.CTkButton(bottom_row, hover_color="#E9444F", fg_color="#CD1B2B", text="Send", command=power_data_send)
    send_button.pack(padx=16, pady=12)

    # Right column content
    label = ctk.CTkLabel(right_col, text="Live Data Graph", font=ctk.CTkFont(size=16, weight="bold"))
    label.pack(padx=16, pady=16)
    label = ctk.CTkLabel(right_col, text="Sampling rate", font=ctk.CTkFont(size=12))
    label.pack(padx=16, pady=8)

    controls_frame = ctk.CTkFrame(right_col, fg_color="transparent")
    controls_frame.pack(fill="x", padx=16, anchor="n")

    # When slider changes, update entry
    def rate_slider_event(value):
        rate_entry.delete(0, ctk.END)
        rate_entry.insert(0, str(int(value)))

    # Send rate data
    def rate_data_send():
        val = rate_entry.get()
        try:
            if val.isdigit() and int(val) <= 1000 and int(val) >= 1:
                sampler_instance.send_data("rate", rate_entry.get())
            else:
                messagebox.showerror("Input Error", "Please enter a valid rate percentage (1-1000).")
        except Exception as e:
            messagebox.showerror("Send Error", f"Could not send rate data:\n{str(e)}")
    
    global rate_slider
    rate_slider = ctk.CTkSlider(controls_frame, from_=0, to=1000, button_color="#CD1B2B", hover="#E9444F", command=rate_slider_event)
    rate_slider.pack(side="left", padx=(0,8), fill="x", expand=True)

    # First layer of checking the entry if it contains a valid value, if a character is present delete the whole entry
    def rate_entry_event(self):
        val = rate_entry.get()
        if val.isdigit() and 0 <= int(val) <= 1000:
            rate_slider.set(int(val))
        else:  # Remove last char if invalid
            rate_entry.delete(0, ctk.END)

    global rate_entry
    rate_entry = ctk.CTkEntry(controls_frame, placeholder_text="Rate (ms)", width=80, height=28)
    rate_entry.bind("<KeyRelease>", rate_entry_event)
    rate_entry.pack(side="left", padx=(0,8))

    send_button = ctk.CTkButton(right_col, hover_color="#E9444F", fg_color="#CD1B2B", text="Send", command=rate_data_send)
    send_button.pack(pady=16, padx=(0,8))


    # Global sampler instance and thread
    sampler_instance = slr()

    # Start and Stop Sampler button functions
    def start_sampler(start_btn, stop_btn, sampler_label):
        global sampler_thread
        port = serial_button.get()
        if port and port != "No Ports":
            try:
                if not sampler_instance.is_connected():
                    sampler_instance.connect(port)
                
                def run_sampler():
                    try:
                        sampler_instance.write_file()
                    except Exception as e:
                        messagebox.showerror("Sampler Error", f"Error: {str(e)}")

                # Start the sampler thread
                sampler_thread = threading.Thread(target=run_sampler, daemon=True)
                sampler_thread.start()
                
                start_btn.configure(state="disabled", fg_color="#350A0A", text="Sampler Running")
                stop_btn.configure(state="normal", fg_color="#CD1B2B")
                sampler_label.configure(text="Status: Running")
            except Exception as e:
                messagebox.showerror("Sampler Error", f"Could not start sampler on {port}:\n{str(e)}")

    def stop_sampler(stop_btn, start_btn, sampler_label):
        global sampler_thread
        if sampler_thread and sampler_thread.is_alive():
            sampler_thread.join(timeout=1)
        start_btn.configure(state="normal", fg_color="#CD1B2B", text="Start Sampler")
        stop_btn.configure(state="disabled", fg_color="#350A0A")
        sampler_label.configure(text="Status: Stopped")

    # place Start + Stop buttons side-by-side
    buttons_frame = ctk.CTkFrame(right_col, fg_color="transparent")
    buttons_frame.pack(padx=16, pady=16)

    start_button = ctk.CTkButton(
        buttons_frame,
        hover_color="#E9444F",
        fg_color="#CD1B2B",
        text="Start Sampler",
    )
    stop_button = ctk.CTkButton(
        buttons_frame,
        hover_color="#E9444F",
        fg_color="#350A0A",
        text="Stop Sampler",
        state="disabled"
    )
        
    sampler_label = ctk.CTkLabel(buttons_frame, text="Status: Stopped", font=ctk.CTkFont(size=12))

    start_button.configure(command=lambda sl=sampler_label, sb=start_button, pb=stop_button: start_sampler(sb, pb, sl))
    stop_button.configure(command=lambda pb=stop_button, sb=start_button, sl=sampler_label: stop_sampler(pb, sb, sl))

    sampler_label.pack(side="top", pady=16)
    start_button.pack(side="left", padx=16)
    stop_button.pack(side="left")

    def open_graphs():
        for file in os.listdir("."):
            if os.path.isfile(os.path.join(".", file)) and file.endswith(".txt"):
                subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "graph.py"), file])

    def delete_graphs():
        bogz = messagebox.askquestion("Graph deletion", "This action will delete all graph files and cannot be undone. Are you sure you want to proceed?", icon='warning')
        if bogz == 'yes':
            for file in os.listdir("."):
                if os.path.isfile(os.path.join(".", file)) and file.endswith(".txt"):
                    os.remove(os.path.join(".", file))
    
    # Live Graph button
    button = ctk.CTkButton(right_col, hover_color="#E9444F",  fg_color="#CD1B2B", text="Live Graph(s)", command=open_graphs)
    button.pack(padx=16, pady=16)
    button = ctk.CTkButton(right_col, hover_color="#E9444F",  fg_color="#CD1B2B", text="Delete Graph Files", command=delete_graphs)
    button.pack(padx=16, pady=0)


app.mainloop()