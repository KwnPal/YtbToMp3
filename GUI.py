import customtkinter as ctk
from Youtube import ytb
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
        ctk.set_appearance_mode("dark")
        self.main_app()
    
    def main_app(self):
        # Option Mode
        self.option_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.option_frame.pack(side="top", anchor="n")

        # Git redirection button
        

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
        
        self.git_button = ctk.CTkButton(self.root, text="GitHub", width = 28, image=self.get_icon("git.png"), hover_color= "#2d3436", fg_color = "transparent", command = lambda: webbrowser.open_new_tab("https://github.com/KwnPal"))
        self.git_button.pack(side = "right", anchor="se")

        # Image widget for thumbnail
        self.image = ctk.CTkLabel(self.root, text="")
        self.image.pack_forget()

        # Entry widget for user input
        self.entry = ctk.CTkEntry(self.input_frame, width=300, border_width=1, border_color="darkred")
        self.entry.pack()

        # Load Button
        self.load_button = ctk.CTkButton(self.load_download_frame, border_width=2, border_color="#0047A0", text="Load Video", fg_color="transparent", font=("Arial", 12, "bold"), command = lambda: executor.submit(self.load_video))
        self.load_button.pack(side="left", pady=10)
        # Download Button
        self.download_button = ctk.CTkButton(self.load_download_frame, text="Download", font=("Arial", 12, "bold"), border_width=2, border_color="#0047A0", fg_color="transparent", height=30, width=90, command = lambda: executor.submit(self.download))
        self.download_button.pack_forget()
        # Video Mode
        self.video_button = ctk.CTkButton(self.option_frame, border_width=2, border_color="#0047A0", fg_color="transparent", text="Video",font=("Arial", 12, "bold"), height=30, width=70, command = self.video_option)
        self.video_button.pack(side="left", padx=10, pady=10)
        # Audio Mode
        self.audio_button = ctk.CTkButton(self.option_frame,border_width=2, border_color="#0047A0", fg_color="darkred", text="Audio", font=("Arial", 12, "bold"), state="disabled", height=30, width=70, command= self.audio_option)
        self.audio_button.pack(side="left", padx=10, pady=10)

    def load_video(self):
        self.load_button.configure(state="disabled", text = "Loading...")
        url = self.entry.get()
        if url:
            self.video = ytb.extract_audio(url)
            if isinstance(self.video, ytb):
                self.result_label.configure(text = f"{self.video.type}: {self.video.title}",font=(("Arial", 15 ,"bold")))
                self.on_button_press()
            else:
                self.result_label.configure(text = self.video,font = ("Arial", 12 ,"bold"))
                self.load_button.configure(state="normal",text = "Load Video")
                self.entry.delete(0,"end")
        else:
            self.result_label.configure(text = "WHERE IS THE URL", font = ("Arial", 12 ,"bold"))
            self.load_button.configure(state="normal",text = "Load Video")
    
    def download(self):
        self.load_button.configure(state = "disabled")
        self.download_button.configure(state = "disabled", text = "Downloading")
        self.video.download()
        self.on_button_complete("Download Complete")
            
    def on_button_press(self):
        self.load_button.configure(state="normal", text = "Skip", command = lambda: self.on_button_complete(""), height=30, width=90)
        self.download_button.configure(state = "normal", text = "Download")
        self.download_button.pack(side="left", pady=10, padx=10)
        self.load_image()

    def on_button_complete(self,message):
        self.image.pack_forget()
        self.input_frame.pack()
        self.download_button.pack_forget()
        self.entry.delete(0,"end")
        self.load_button.configure(text = "Load Video", state = "normal", command = lambda: executor.submit(self.load_video))
        self.result_label.configure(text = message, font = ("Arial", 12 ,"bold"))

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
        thumbnail = ctk.CTkImage(light_image = thumbnail, size=(200, 100))
        if thumbnail:
            self.image.configure(image = thumbnail)
            self.image.pack()

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

     
