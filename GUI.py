import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import customtkinter
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from typing import Union
import re
import os

ctk = customtkinter
tk = tkinter

# class for custom time spinbox


class TimeSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 145,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="▼", width=height - 6, height=height / 3,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(
            row=0, column=2, padx=(0, 3), pady=(height / 1.5, 0))

        self.entry = customtkinter.CTkEntry(
            self, width=width - (2 * height), height=height - 6, border_width=0, validate='focusout', validatecommand=self.validate_timestamp)
        self.entry.bind('<Return>', self.remove_focus)
        self.entry.grid(row=0, column=1, columnspan=1,
                        padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="▲", width=height - 6, height=height / 4,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3),
                             pady=(0, height / 1.5))

        # default value
        self.entry.insert(0, "00:00:00.00")

    def remove_focus(self, key):
        self.add_button.focus_set()

    def validate_timestamp(self):
        time_input = [m.start() for m in re.finditer(':', self.entry.get())]
        string_check = self.entry.get()
        timestamp = self.entry.get()
        string_check = string_check.replace('.', '')
        string_check = string_check.replace(':', '')
        if string_check.isnumeric():
            total_seconds = self.time_to_seconds(timestamp)
            timestamp = self.convert_to_timestamp(total_seconds)
        else:
            timestamp = 'Input Error'
        self.entry.delete(0, "end")
        self.entry.insert(0, timestamp)
        return True

    def convert_to_timestamp(self, value: float):
        hours = int(value // 3600)
        minutes = int((value - hours * 3600) // 60)
        seconds = value - (hours * 3600 + minutes * 60)
        timestamp = str(hours).zfill(2) + ':' + \
            str(minutes).zfill(2) + ':' + \
            str(format(seconds, '.2f')).zfill(5)
        return(timestamp)

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = self.time_to_seconds(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, self.convert_to_timestamp(value))
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = self.time_to_seconds(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, self.convert_to_timestamp(value))
        except ValueError:
            return

    def get(self):
        try:
            return self.entry.get()
        except ValueError:
            return None

    def set(self, value: str):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)

    def time_to_seconds(self, timestamp: str):
        time_input = [m.start() for m in re.finditer(':', timestamp)]
        if len(time_input) == 0:
            return float(timestamp)
        elif len(time_input) == 1:
            minutes = float(timestamp[:time_input[0]])
            seconds = float(timestamp[time_input[0] + 1:])
            return minutes * 60 + seconds
        elif len(time_input) == 2:
            hours = float(timestamp[:time_input[0]])
            minutes = float(timestamp[time_input[0] + 1:time_input[1]])
            seconds = float(timestamp[time_input[1] + 1:])
            return hours * 3600 + minutes * 60 + seconds
        else:
            return 0


# functions
def select_file():
    filetypes = (
        ('MP4 files', '*.mp4'),
        ('MKV files', '*.mkv'),
        ('MOV files', '*.mov'),
        ('WMV files', '*.wmv'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file', initialdir='/', filetypes=filetypes)
    if not filename:
        return
    else:
        clip = VideoFileClip(filename)
        clip_time = clip.duration
        clip.close()
        video_path.set(filename)
        video_path_entry.xview("end")
        if check_out_folder.get() == 1:
            set_output_folder()
        start_time.set('00:00:00.00')
        end_time.set(sec_to_timestamp(clip_time))


def select_folder():
    selected_folder = fd.askdirectory()
    output_folder.set(selected_folder)


def time_to_sec(timestamp):
    [j, i] = [m.start() for m in re.finditer(':', timestamp)]
    hour = float(timestamp[:j])
    minute = float(timestamp[j + 1:i])
    second = float(timestamp[i + 1:])
    return((hour * 3600 + minute * 60 + second))


def sec_to_timestamp(total_seconds):
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds - hours * 3600) // 60)
    seconds = round(total_seconds - (hours * 3600) - (minutes * 60), 2)
    return(str(hours).zfill(2) + ':' + str(minutes).zfill(2) + ':'
           + str(seconds).zfill(4))


def set_output_folder():
    # print(check_out_folder.get())
    if(check_out_folder.get() == 1):
        output_folder.set(get_source(video_path.get()))
        output_entry.xview("end")
        output_entry.configure(text_color='light grey',
                               fg_color='grey', state='disabled')
    else:
        output_entry.configure(
            text_color="#DCE4EE", fg_color="#343638", state='normal')


def get_source(filepath):
    if not filepath:
        return ""
    else:
        return(filepath[:filepath.rfind('/')])


def trim_video():
    file_extension = video_path.get()[video_path.get().rfind('.'):]
    if not filename.get():
        index = video_path.get().rfind('/') + 1
        out_filename = video_path.get(
        )[index:-4] + '_trimmed' + video_path.get()[-4:]
    elif filename.get()[-4:] != file_extension:
        out_filename = filename.get() + file_extension
    else:
        out_filename = filename.get()

    if not output_folder.get():
        out_folder = get_source(video_path.get())
    else:
        out_folder = output_folder.get()

    output_file = out_folder + '/' + out_filename
    # print(output_file)

    clip_start = time_to_sec(start_time.get())
    clip_end = time_to_sec(end_time.get())

    if delete_file.get():
        old_name = video_path.get()
        new_name = get_source(old_name) + 'temp.mp4'
        os.rename(old_name, new_name)
        ffmpeg_extract_subclip(new_name, clip_start,
                               clip_end, targetname=output_file)
        os.remove(new_name)
    else:
        ffmpeg_extract_subclip(video_path.get(), clip_start,
                               clip_end, targetname=output_file)
    mb.showinfo("", 'Video trimming completed.', icon="question")


# GUI code
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

gui = customtkinter.CTk()
gui.minsize(601, 132)
gui.title("MP4 Video Trimmer")
# scrollbar_x = ctk.Scrollbar(orient="horizontal")

mainframe = ctk.CTkFrame(master=gui,
                         width=601,
                         height=132)
mainframe.grid(column=0, row=0, sticky=('N, W, E, S'))
gui.columnconfigure((0, 1), weight=1)
gui.columnconfigure((2, 3, 4), weight=0)
gui.rowconfigure((0, 1, 2, 3, 4), weight=1)

# display video path
video_path = tk.StringVar()
# video_path.set('C:/Users/adamm/Downloads/sample-mp4-file.mp4')  # debug only
video_path_entry = ctk.CTkEntry(
    mainframe, width=500, textvariable=video_path)
video_path_entry.grid(column=2, row=1, sticky='we',
                      columnspan=2, pady=(4, 4))


# button to open file dialog to select file
file_select = ctk.CTkButton(mainframe, text='Choose file', command=select_file)
file_select.grid(column=4, row=1, padx=4, pady=(4, 4))

# output folder path
output_folder = tk.StringVar()
output_entry = ctk.CTkEntry(mainframe, width=100, textvariable=output_folder)
output_entry.grid(column=2, row=2, sticky='we', columnspan=2, pady=(0, 4))


# button to open file dialog to select output location
output_select = ctk.CTkButton(
    mainframe, text='Choose folder', command=select_folder)
output_select.grid(column=4, row=2, pady=(0, 4))

# start time
start_time = TimeSpinbox(mainframe)
start_time.grid(column=2, row=3, sticky='w', pady=(0, 4))

# end time
end_time = TimeSpinbox(mainframe)
end_time.grid(column=2, row=4, sticky='w', pady=(0, 4))

# check box for placing video in original folder
check_out_folder = tk.IntVar()
check_folder = ctk.CTkCheckBox(mainframe, variable=check_out_folder,
                               command=set_output_folder,
                               text='Output file to input folder')
check_folder.grid(column=2, row=3, sticky='w',
                  columnspan=2, padx=(120, 0), pady=(0, 4))

# check box for deleting original file after trim
delete_file = tk.BooleanVar()
check_delete = ctk.CTkCheckBox(mainframe, variable=delete_file,
                               offvalue=False, onvalue=True,
                               text='Delete original file after trimming')
check_delete.grid(column=2, row=4, sticky='w',
                  columnspan=2, padx=(120, 0), pady=(0, 4))

# Entry for new filename
filename = tk.StringVar()
new_filename = ctk.CTkEntry(mainframe, width=100, textvariable=filename)
new_filename.grid(column=2, row=5, sticky='we', pady=(0, 2))

# trim video button
trim_button = ctk.CTkButton(mainframe, text='Trim video', command=trim_video)
trim_button.grid(column=4, row=4, rowspan=2, sticky='ns', pady=(0, 2))


# labels
ctk.CTkLabel(mainframe, text="Video File:").grid(
    column=1, row=1, sticky='W', padx=(5, 0), pady=(4, 4))
ctk.CTkLabel(mainframe, text="Output Folder:").grid(
    column=1, row=2, sticky='W', padx=(5, 0), pady=(0, 4))
ctk.CTkLabel(mainframe, text="Start Time:").grid(
    column=1, row=3, sticky='W', padx=(5, 0), pady=(0, 4))
ctk.CTkLabel(mainframe, text="End Time:").grid(
    column=1, row=4, sticky='W', padx=(5, 0), pady=(0, 4))
ctk.CTkLabel(mainframe, text="New Filename:").grid(
    column=1, row=5, sticky='W', padx=(5, 2), pady=(0, 4))


gui.mainloop()
