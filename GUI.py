import customtkinter as ctk
import tkinter as tk
from Youtube import ytb
from yt_dlp.utils import DownloadError
from concurrent.futures import ThreadPoolExecutor
import os
import webbrowser
from PIL import Image

#https://www.youtube.com/watch?v=0CYfRc0wjiE&list=RD8nfhHBJQXOY&index=10
executor = ThreadPoolExecutor()
class gui:
    def __init__(self,root):
        self.root = root
        self.root.geometry("700x350")
        self.root.title("Yt_To_Mp3")
        self.root.minsize(700, 350)
        self.counter = 1
        ctk.set_appearance_mode("dark")
        ctk.set_widget_scaling(1.5)  # Scale widgets by 1.5x
        ctk.set_window_scaling(1.5)  # Scale the window by 1.5x

        self.main_app()
        self.context_menu()
    
    def main_app(self):
        # Option Mode
        self.option_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.option_frame.pack(side="top", anchor="n")

        # Input Frame
        self.input_frame = ctk.CTkFrame(self.root, fg_color = "transparent")
        self.input_frame.pack()

        self.load_download_frame = ctk.CTkFrame(self.root, fg_color = "transparent")
        self.load_download_frame.pack()

        self.respond_frame = ctk.CTkFrame(self.root, width=200, height=40, border_width=1, border_color="darkred")
        self.respond_frame.pack(pady=5)

        self.result_label = ctk.CTkLabel(self.respond_frame, text="")
        self.result_label.pack(padx=20,pady=10)

        self.label = ctk.CTkLabel(self.input_frame, text="URL:", font=("Arial", 14, "bold"))
        self.label.pack(pady=10)

        # Entry widget for user input
        self.entry = ctk.CTkEntry(self.input_frame, width=300, border_width=1, border_color="darkred", placeholder_text="URL..")
        self.entry.pack()

        # Image widget for thumbnail
        self.image = ctk.CTkLabel(self.root, text="")
        self.image.place_forget()
        # Git redirection button
        self.git_button = ctk.CTkButton(self.root, text="GitHub", width = 28, image=self.get_icon("git.png"), hover_color= "#2d3436", fg_color = "transparent", cursor="hand2", command = lambda: webbrowser.open_new_tab("https://github.com/KwnPal"))
        self.git_button.pack(padx=10, pady=10, side = "right", anchor = "se")
        # Load Button
        self.load_button = ctk.CTkButton(self.load_download_frame, border_width=2, border_color="#0047A0", text="Load Video", fg_color="transparent", font=("Arial", 12, "bold"), cursor="hand2", command = lambda: executor.submit(self.load_video))
        self.load_button.pack(side="left", pady=10)

        self.entry.bind("<Return>", lambda e: self.load_button.invoke())
        # Bind right-click to show the context menu
        self.entry.bind("<Button-3>", self.right_click)
        
        # Download Button
        self.download_button = ctk.CTkButton(self.load_download_frame, text="Download", font=("Arial", 12, "bold"), border_width=2, border_color="#0047A0", cursor="hand2", fg_color="transparent", height=30, width=90, command =lambda: executor.submit(self.download))
        self.download_button.pack_forget()
        # Video Mode
        self.video_button = ctk.CTkButton(self.option_frame, border_width=2, border_color="#0047A0", fg_color="transparent", text="Video",font=("Arial", 12, "bold"), height=30, width=70, cursor="hand2", command = self.video_option)
        self.video_button.pack(side="left", padx=10, pady=10)
        # Audio Mode
        self.audio_button = ctk.CTkButton(self.option_frame,border_width=2, border_color="#0047A0", fg_color="darkred", text="Audio", font=("Arial", 12, "bold"), state="disabled", height=30, width=70, cursor="hand2", command= self.audio_option)
        self.audio_button.pack(side="left", padx=10, pady=10)

    def context_menu(self):
    # Create a context menu
        self.menu = tk.Menu(self.root, tearoff=0, bg="#212121",fg="white", font=("Arial", 12, "bold"))
        self.menu.add_command(label="Paste", command= self.paste_text)

    def right_click(self,event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def paste_text(self):
        # Get clipboard content
        clipboard = self.root.clipboard_get()
        # Insert clipboard content at the current cursor position
        self.entry.insert(0, clipboard)

    def load_video(self):
        self.load_button.configure(state="disabled", text = "Loading...")
        url = self.entry.get()
        if url:
            self.video = ytb.extract_audio(url)
            if isinstance(self.video, ytb):
                self.on_button_press()
                self.result_label.configure(text = f"{self.video.type}: {self.video.title}",font=(("Arial", 15 ,"bold")))
            else:
                self.result_label.configure(text = self.video,font = ("Arial", 12 ,"bold"))
                self.load_button.configure(state="normal",text = "Load Video")
                self.entry.delete(0,"end")
        else:
            self.result_label.configure(text = "WHERE IS THE URL", font = ("Arial", 12 ,"bold"))
            self.load_button.configure(state="normal",text = "Load Video")
    
    def progress_hook_video(self, prog):
        message = f"Downloading: {prog['_percent_str']}"
        self.result_label.configure(text = message, font = ("Arial", 12 ,"bold"))
        if prog["status"] == "finished" and ytb.option["name"] == "Songs":
           self.result_label.configure(text = "Converting to mp3...", font = ("Arial", 15 ,"bold"))

    def progress_hook_playlist(self, prog):
        video_counter = f"{self.counter} of {self.video.num_songs}: "
        message = video_counter+f"Downloading: {prog['_percent_str']}"
        self.result_label.configure(text = message, font = ("Arial", 12 ,"bold"))
        if prog["status"] == "finished" and ytb.option["name"] == "Songs":
            self.result_label.configure(text = video_counter+f"Converting to mp3...", font = ("Arial", 12 ,"bold"))
            self.counter += 1


    def download(self):
        self.load_button.configure(state = "disabled")
        self.download_button.configure(state = "disabled", text = "Downloading")
        if self.video.type == "Video":
            self.video.option["progress_hooks"] = [self.progress_hook_video]
        else:
            self.video.option["progress_hooks"] = [self.progress_hook_playlist]
        self.counter=1
        self.video.download()
        self.on_button_complete(f"Successfully downloaded:\n[{self.video.title}]")

    def on_button_press(self):
        self.load_image()
        self.load_button.configure(state="normal", text = "Skip", command = lambda: self.on_button_complete(""), height=30, width=90)
        self.download_button.configure(state = "normal", text = "Download")
        self.download_button.pack(side="left", pady=10, padx=10)
        
    def on_button_complete(self,message):
        self.image.place_forget()
        self.input_frame.pack()
        self.download_button.pack_forget()
        self.entry.delete(0,"end")
        self.load_button.configure(text = "Load Video", state = "normal", command = lambda: executor.submit(self.load_video))
        self.result_label.configure(text = message, font = ("Arial", 15 ,"bold"))

    def audio_option(self):
        ytb.change_option(0)
        self.video_button.configure(state = "enabled", fg_color="transparent", cursor="hand2")
        self.audio_button.configure(state = "disabled", fg_color="darkred", cursor="hand2")

    def video_option(self):
        ytb.change_option(1)
        self.video_button.configure(state = "disabled", fg_color="darkred", cursor="hand2")
        self.audio_button.configure(state = "enabled", fg_color="transparent", cursor="hand2")

    def load_image(self):
        thumbnail = self.video.get_thumbnail()
        if thumbnail:
            thumbnail = ctk.CTkImage(light_image = thumbnail, size=(200, 100))
            self.image.configure(image = thumbnail)
            self.image.place(relx=0.5, y=290, anchor="center") 

    def get_icon(self,name):
        main_path=os.path.realpath(os.path.dirname(__file__))
        icon_path = os.path.join(main_path, "icon", name)
        image = Image.open(icon_path)
        image = ctk.CTkImage(light_image = image, size=(28, 28))
        return image


if __name__ == "__main__":
    root = ctk.CTk()
    gui(root)
    root.mainloop()

     
