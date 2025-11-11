import customtkinter as ctk
from PIL import Image
import subprocess, sys, os
    
if __name__ == "__main__":

    # CTK appearance
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # CTK itself
    app = ctk.CTk()
    app.title("Art Beerkart Manager")
    app.iconbitmap("beer.ico")
    app.geometry("750x450")
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
    left_col = ctk.CTkFrame(content_frame)
    left_col.grid(row=0, column=0, padx=(0, 6), sticky="nsew")
    right_col = ctk.CTkFrame(content_frame)
    right_col.grid(row=0, column=1, padx=(6, 0), sticky="nsew")

    # LEft coloumn content (split into two rows)

    left_col.grid_rowconfigure(0, weight=1)
    left_col.grid_rowconfigure(1, weight=1)
    left_col.grid_columnconfigure(0, weight=1)
    

    # Top row: Serial Connection widgets
    top_row = ctk.CTkFrame(left_col)
    top_row.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0,4))

    serial_label = ctk.CTkLabel(top_row, text="Serial Connection", font=ctk.CTkFont(size=16, weight="bold"))
    serial_label.pack(padx=16, pady=(8,8))
    entry = ctk.CTkEntry(top_row, placeholder_text="Enter COM port (e.g., COM3)")
    entry.pack(padx=16, pady=(0,8))
    connect_button = ctk.CTkButton(top_row, hover_color="#E9444F", fg_color="#CD1B2B", text="Connect")
    disconnect_button = ctk.CTkButton(top_row, hover_color="#E9444F", fg_color="#350A0A", text="Disconnect", state="disabled")
    connect_button.pack(side="left", padx=16)
    disconnect_button.pack(side="right", padx=16)

    # Bottom row: placeholder for additional controls
    bottom_row = ctk.CTkFrame(left_col)
    bottom_row.grid(row=1, column=0, sticky="nsew", padx=0, pady=(4,0))

    bottom_label = ctk.CTkLabel(bottom_row, text="Power limit", font=ctk.CTkFont(size=14, weight="bold"))
    bottom_label.pack(padx=16, pady=12)

    # horizontal container for entry + slider + button
    controls_frame = ctk.CTkFrame(bottom_row, fg_color="transparent")
    controls_frame.pack(fill="x", padx=16)

    power_slider = ctk.CTkSlider(controls_frame, button_color="#CD1B2B", hover="#E9444F")
    power_slider.pack(side="left", padx=(0,8), fill="x", expand=True)

    power_entry = ctk.CTkEntry(controls_frame, placeholder_text="Power", width=80, height=28)
    power_entry.pack(side="left", padx=(0,8))

    send_button = ctk.CTkButton(bottom_row, hover_color="#E9444F", fg_color="#CD1B2B", text="Send")
    send_button.pack(padx=16, pady=12)

    # Right column content
    label = ctk.CTkLabel(right_col, text="Live Data Graph", font=ctk.CTkFont(size=16, weight="bold"))
    label.pack(padx=16, pady=16)
    label = ctk.CTkLabel(right_col, text="Sampling rate", font=ctk.CTkFont(size=12))
    label.pack(padx=16, pady=8)

    controls_frame = ctk.CTkFrame(right_col, fg_color="transparent")
    controls_frame.pack(fill="x", padx=16, anchor="n")

    rate_slider = ctk.CTkSlider(controls_frame, button_color="#CD1B2B", hover="#E9444F")
    rate_slider.pack(side="left", padx=(0,8), expand=True)

    rate_entry = ctk.CTkEntry(controls_frame, placeholder_text="Rate (ms)", width=80, height=28)
    rate_entry.pack(side="left", padx=(0,8))


    # keep Popen handle so we can stop the process later
    sampler_proc = None

    # Start and Stop Sampler button functions
    def start_sampler(start_btn, stop_btn, sampler_label):

        global sampler_proc
        
        if sampler_proc is None or sampler_proc.poll() is not None:
            sampler_proc = subprocess.Popen([sys.executable, 'sampler.py'])
            start_btn.configure(state="disabled", fg_color="#350A0A", text="Sampler Running")
            stop_btn.configure(state="normal", fg_color="#CD1B2B")
            sampler_label.configure(text="Status: Running")

    def stop_sampler(stop_btn, start_btn, sampler_label):

        global sampler_proc

        if sampler_proc and sampler_proc.poll() is None:
            # ask the process to terminate, wait a bit, then kill if still alive
            sampler_proc.terminate()
            try:
                sampler_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                sampler_proc.kill()
                sampler_proc.wait()
        sampler_proc = None
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

    # Live Graph button
    button = ctk.CTkButton(right_col, hover_color="#E9444F",  fg_color="#CD1B2B", text="Live Graph(s)", command=lambda: subprocess.Popen([sys.executable, 'graph.py']))
    button.pack(padx=16, pady=16)


app.mainloop()