import customtkinter as ctk
from PIL import Image
import subprocess, sys, os


class ArtBeerkartApp(ctk.CTk):
    if __name__ == "__main__":

        subprocess.Popen([sys.executable, 'sampler.py'])
        # CTK appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # CTK itself
        app = ctk.CTk()
        app.title("Art Beerkart Manager")
        app.iconbitmap("beer.ico")
        app.geometry("800x500")
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

        # LEft coloumn content

        # Right column content
        button = ctk.CTkButton(right_col,hover_color="#E9444F",  fg_color="#CD1B2B", text="Élő Grafikon", command=lambda: subprocess.Popen([sys.executable, 'graph.py']))


        button.pack(padx=16, pady=16, anchor="n")


    app.mainloop()