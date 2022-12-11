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
import configparser

ctk = customtkinter
tk = tkinter


# class for custom time spinbox


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
check_out_folder = tk.BooleanVar()
check_folder = ctk.CTkCheckBox(mainframe, variable=check_out_folder,
                               offvalue=False, onvalue=True,
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

startup_sequence()
gui.mainloop()
end_sequence()
