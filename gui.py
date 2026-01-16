import customtkinter as ctk
import cv2
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self, video_source=0):
        super().__init__()

        self.title("AI Gesture Control")
        self.geometry("1000x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Video Frame
        self.video_frame = ctk.CTkFrame(self.main_frame)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.video_label = ctk.CTkLabel(self.video_frame, text="")
        self.video_label.pack(fill="both", expand=True)

        # Control Panel
        self.control_panel = ctk.CTkFrame(self.main_frame)
        self.control_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.label_title = ctk.CTkLabel(self.control_panel, text="Controls", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=20)

        self.status_label = ctk.CTkLabel(self.control_panel, text="Status: Active", text_color="green")
        self.status_label.pack(pady=10)

        self.vol_label = ctk.CTkLabel(self.control_panel, text="Volume: 0%")
        self.vol_label.pack(pady=5)
        self.vol_bar = ctk.CTkProgressBar(self.control_panel)
        self.vol_bar.pack(pady=5)
        self.vol_bar.set(0)

        self.bright_label = ctk.CTkLabel(self.control_panel, text="Brightness: 0%")
        self.bright_label.pack(pady=5)
        self.bright_bar = ctk.CTkProgressBar(self.control_panel)
        self.bright_bar.pack(pady=5)
        self.bright_bar.set(0)
        
        self.quit_button = ctk.CTkButton(self.control_panel, text="Quit", command=self.on_closing)
        self.quit_button.pack(pady=20, side="bottom")

    def update_video(self, frame):
        # Convert image for Tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ctk.CTkImage(light_image=img, dark_image=img, size=(640, 480))
        self.video_label.configure(image=imgtk)
        self.video_label.image = imgtk # Keep reference

    def update_status(self, vol, bright):
        self.vol_label.configure(text=f"Volume: {int(vol)}%")
        self.vol_bar.set(vol / 100)
        self.bright_label.configure(text=f"Brightness: {int(bright)}%")
        self.bright_bar.set(bright / 100)

    def on_closing(self):
        self.destroy()
