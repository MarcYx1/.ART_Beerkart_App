import customtkinter as ctk
import tkinter as tk
from PIL import Image
import subprocess, sys, os, threading, darkdetect
from sampler import Sampler as slr
    
# Declare globals at module level
sampler_thread = None
data_indicator_job = None  # Add this for the flashing animation

color_mode = "Dark"

if __name__ == "__main__":

    color_mode = "Dark" if darkdetect.isDark() else "Light"

    # CTK appearance
    ctk.set_appearance_mode(color_mode)
    ctk.set_default_color_theme("./assets/ART_theme.json")

    # Logic for changing the theme with the color_button button
    def color_mode_change(theme):
        global color_mode
        if theme == "Dark":
            color_mode = "Dark"
            ctk.set_appearance_mode("Dark")
            right_col_top.configure(fg_color="#2B2B2B")
            right_col_bottom.configure(fg_color="#2B2B2B")
            top_row.configure(fg_color="#2B2B2B")
            bottom_row.configure(fg_color="#2B2B2B")
            power_entry.configure(border_color="#565B5E")
            rate_entry.configure(border_color="#565B5E")
            serial_button.configure(fg_color="#CD1B2B")
            serial_button.configure(unselected_color="#565B5E")
            color_button.configure(
                image = ctk.CTkImage(Image.open("./assets/light_mode.png"), size=(24, 24)),
                hover_color="#969696",
                command=lambda: color_mode_change("Light")
            )
        elif theme == "Light":
            color_mode = "Light"
            ctk.set_appearance_mode("Light")
            right_col_top.configure(fg_color="#E4E4E4")
            right_col_bottom.configure(fg_color="#E4E4E4")
            top_row.configure(fg_color="#E4E4E4")
            bottom_row.configure(fg_color="#E4E4E4")
            power_entry.configure(border_color="#CD1B2B")
            rate_entry.configure(border_color="#CD1B2B")
            serial_button.configure(fg_color="#565B5E")
            serial_button.configure(unselected_color="#CD1B2B")
            color_button.configure(
                image = ctk.CTkImage(Image.open("./assets/dark_mode.png"), size=(24, 24)),
                hover_color="#5F5F5F",
                command=lambda: color_mode_change("Dark")
            )

    # CTK itself
    app = ctk.CTk()
    app.title("Art Beerkart Manager")
    app.iconbitmap("./assets/beer.ico")
    app.geometry("770x565")
    app.resizable(False, False)

    # The top frame with the title and logo
    top_frame = ctk.CTkFrame(app, height=64, fg_color="#CD1B2B")
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
    pil_img = Image.open("./assets/Art_logo.png")
    logo_image = ctk.CTkImage(pil_img, size=(93, 48))
    img_label = ctk.CTkLabel(top_frame, image=logo_image, text="")
    img_label.image = logo_image  # keep reference
    img_label.grid(row=0, column=1, padx=12, pady=8, sticky="e")

    # Title placement
    title_label.grid(row=0, column=0, padx=12, pady=8, sticky="w")

    # Columns (2)
    content_frame = ctk.CTkFrame(app, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=(12,0), pady=12)
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    # Left column and Right column
    left_col = ctk.CTkFrame(content_frame, fg_color="transparent")
    left_col.grid(row=0, column=0, padx=(0, 6), sticky="nsew")
    right_col = ctk.CTkFrame(content_frame, fg_color="transparent")
    right_col.grid(row=0, column=1, padx=(6, 0), sticky="nsew")

    right_col_top = ctk.CTkFrame(right_col)
    right_col_top.grid(row=0, column=0, sticky="ew", padx=0, pady=(0,4))

    right_col_bottom = ctk.CTkFrame(right_col)
    right_col_bottom.grid(row=1, column=0, sticky="nsew", padx=0, pady=(4,0))

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
    top_row = ctk.CTkFrame(left_col)
    top_row.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0,4), ipady=9)

    # COM / serial ports
    serial_label = ctk.CTkLabel(top_row, text="Serial Connection", font=ctk.CTkFont(size=16, weight="bold"))
    serial_label.pack(padx=16, pady=(8,8))

    refresh_button = ctk.CTkButton(top_row, text="Refresh Ports", command=refresh_ports)
    refresh_button.pack(padx=16, pady=(0,8))

     # Segmented button for available serial ports
    serial_button = ctk.CTkSegmentedButton(top_row, values=slr().list_available_ports(), selected_color="#350A0A")
    serial_button.pack(padx=16, pady=(0,8))

    # Name implies, connects to the selected serial port
    def connect_serial():
        port = serial_button.get()
        try:
            slr().connect(port)
        except Exception as e:
            tk.messagebox.showerror("Connection Error", f"Could not connect to {port}:\n{str(e)}")
            return

        status_label.configure(text="Status: Connected")
        connect_button.configure(state="disabled", fg_color="#350A0A")
        disconnect_button.configure(state="normal", fg_color="#CD1B2B")
        serial_button.configure(state="disabled")
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
        serial_button.configure(state="normal")

     # Status label + Connect / Disconnect buttons
    status_label = ctk.CTkLabel(top_row, text="Status: Disconnected", font=ctk.CTkFont(size=12))
    status_label.pack(padx=16, pady=(0,8))

    connect_button = ctk.CTkButton(top_row, text="Connect", command=connect_serial)
    disconnect_button = ctk.CTkButton(top_row, fg_color="#350A0A", text="Disconnect", state="disabled", command=disconnect_serial)
    
    connect_button.pack(side="left", padx=16, pady=(0,16))
    disconnect_button.pack(side="right", padx=16, pady=(0,16))

    # Bottom row: placeholder for additional controls
    bottom_row = ctk.CTkFrame(left_col)
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
                tk.messagebox.showerror("Input Error", "Please enter a valid power percentage (0-100).")
        except Exception as e:
            tk.messagebox.showerror("Send Error", f"Could not send power data:\n{str(e)}")
    
    # Slider for the power amount
    power_slider = ctk.CTkSlider(controls_frame, from_=0, to=100, command=power_slider_event)
    power_slider.pack(side="left", padx=(0,8), fill="x", expand=True)

    # First layer of checking the entry if it contains a valid value, if a character is present delete the whole entry
    def power_entry_event(self):
        val = power_entry.get()
        if val.isdigit() and 0 <= int(val) <= 100:
            power_slider.set(int(val))
        else:  # Remove last char if invalid
            power_entry.delete(0, ctk.END)

    # Entry next to slider, shows value of slider, allows manual editing of value
    power_entry = ctk.CTkEntry(controls_frame, placeholder_text="Power (%)", width=80, height=28)
    power_entry.bind("<KeyRelease>", power_entry_event)
    power_entry.pack(side="left", padx=(0,8))

    send_button = ctk.CTkButton(bottom_row, text="Send", command=power_data_send)
    send_button.pack(padx=16, pady=12)

    # Button to change theme of window
    color_mode_frame = ctk.CTkFrame(bottom_row, fg_color="transparent")
    color_mode_frame.pack(anchor="sw", pady=(60,0))
    color_button = ctk.CTkButton(color_mode_frame, 
                                 text ="",
                                 width=40,
                                 height=40,
                                 fg_color="transparent", 
                                 hover_color="#969696", 
                                 image = ctk.CTkImage(Image.open("./assets/light_mode.png"), size=(24, 24)),
                                 command=lambda: color_mode_change("Light"))
    color_button.pack(padx=8)
    version_label = ctk.CTkLabel(color_mode_frame, text="v0.8", font=ctk.CTkFont(size=10))
    version_label.pack(padx=8, pady=(0,8))

    # Right column content
    label = ctk.CTkLabel(right_col_top, text="Live Data Graph", font=ctk.CTkFont(size=16, weight="bold"))
    label.pack(padx=16, pady=16)
    label = ctk.CTkLabel(right_col_top, text="Sampling rate", font=ctk.CTkFont(size=12))
    label.pack(padx=16, pady=8)

    controls_frame = ctk.CTkFrame(right_col_top, fg_color="transparent")
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
                tk.messagebox.showerror("Input Error", "Please enter a valid rate percentage (1-1000).")
        except Exception as e:
            tk.messagebox.showerror("Send Error", f"Could not send rate data:\n{str(e)}")
    
    # Slider for the rate amount
    global rate_slider
    rate_slider = ctk.CTkSlider(controls_frame, from_=1, to=1000, command=rate_slider_event)
    rate_slider.pack(side="left", padx=(0,8), fill="x", expand=True)

    # First layer of checking the entry if it contains a valid value, if a character is present delete the whole entry
    def rate_entry_event(self):
        val = rate_entry.get()
        if val.isdigit() and 0 <= int(val) <= 1000:
            rate_slider.set(int(val))
        else:  # Remove last char if invalid
            rate_entry.delete(0, ctk.END)

    # Entry next to slider, shows value of slider, allows manual editing of value
    global rate_entry
    rate_entry = ctk.CTkEntry(controls_frame, placeholder_text="Rate (ms)", width=80, height=28)
    rate_entry.bind("<KeyRelease>", rate_entry_event)
    rate_entry.pack(side="left", padx=(0,16))

    send_button = ctk.CTkButton(right_col_top, text="Send", command=rate_data_send)
    send_button.pack(pady=16, padx=(0,16))


    # Global sampler instance and thread
    sampler_instance = slr()

    # Starts sampler duh
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
                        tk.messagebox.showerror("Sampler Error", f"Error: {str(e)}")

                # Start the sampler thread
                sampler_thread = threading.Thread(target=run_sampler, daemon=True)
                sampler_thread.start()
                
                start_btn.configure(state="disabled",  text="Sampler Running", fg_color="#350A0A")
                stop_btn.configure(state="normal", fg_color="#CD1B2B")
                sampler_label.configure(text="Status: Running")
            except Exception as e:
                tk.messagebox.showerror("Sampler Error", f"Could not start sampler on {port}:\n{str(e)}")

    # stops sampler duh
    def stop_sampler(stop_btn, start_btn, sampler_label):
        global sampler_thread
        sampler_instance.disconnect()

        files = os.listdir("./live_graphs")
        for file in files:
            src_path = os.path.join("./live_graphs", file)
            dest_path = os.path.join("./graphs", file)
            os.rename(src_path, dest_path)
        
        start_btn.configure(state="normal", text="Start Sampler", fg_color="#CD1B2B")
        stop_btn.configure(state="disabled", fg_color="#350A0A")
        sampler_label.configure(text="Status: Stopped")

    # place Start + Stop buttons side-by-side
    buttons_frame = ctk.CTkFrame(right_col_top, fg_color="transparent")
    buttons_frame.pack(padx=16, pady=16)

    start_button = ctk.CTkButton(
        buttons_frame,
        fg_color="#CD1B2B",
        text="Start Sampler",
    )
    stop_button = ctk.CTkButton(
        buttons_frame,
        text="Stop Sampler",
        state="disabled",
        fg_color="#350A0A"
    )
    
    # sampler status label
    sampler_label = ctk.CTkLabel(buttons_frame, text="Status: Stopped", font=ctk.CTkFont(size=12))

    # start stop button
    start_button.configure(command=lambda sl=sampler_label, sb=start_button, pb=stop_button: start_sampler(sb, pb, sl))
    stop_button.configure(command=lambda pb=stop_button, sb=start_button, sl=sampler_label: stop_sampler(pb, sb, sl))

    sampler_label.pack(side="top", pady=16)
    start_button.pack(side="left", padx=16)
    stop_button.pack(side="left", padx=16)

    # open live graphs
    def live_graphs():
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "filepicker.py"), color_mode, "open", "live"]) # <- since the filepicker handles both deletion and opening files, i need to specify which action to tike in sys.argv

    # open saved graphs, launches filepicker.py                                                     || this is so the filepicker.py follows theme
    def open_graphs(): #                                                                            V 
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "filepicker.py"), color_mode, "open", ""]) # <- since the filepicker handles both deletion and opening files, i need to specify which action to tike in sys.argv
        print(color_mode)

    def delete_graphs():
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "filepicker.py"), color_mode, "delete", ""]) # <- since the filepicker handles both deletion and opening files, i need to specify which action to tike in sys.argv
    
    garph_label = ctk.CTkLabel(right_col_bottom, text="Graphs", font=ctk.CTkFont(size=16, weight="bold"))
    garph_label.pack(pady=(16,0))

    buttons_frame_graph = ctk.CTkFrame(right_col_bottom, fg_color="transparent")
    buttons_frame_graph.pack(padx=16, pady=4)

    # Live Graph button
    graph_button = ctk.CTkButton(buttons_frame_graph, text="Live Graph(s)", command=live_graphs)
    graph_button.pack(side="left", padx=16, pady=4)
    live_button = ctk.CTkButton(buttons_frame_graph, text="Saved Graph(s)", command=open_graphs)
    live_button.pack(side="left", padx=16, pady=4)
    delete_button = ctk.CTkButton(right_col_bottom, text="Delete Graph Files", command=delete_graphs)
    delete_button.pack(side="top", padx=16, pady=(4,16))

# CTk mainloop
color_mode_change(color_mode)
app.mainloop()