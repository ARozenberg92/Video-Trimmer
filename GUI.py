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
from custom_widgets import TimeSpinbox
from functions import *

ctk = customtkinter
tk = tkinter

# GUI code


class GUI:
    def __init__(self, root=None):
        # scrollbar_x = ctk.Scrollbar(orient="horizontal")

        self.mainframe = ctk.CTkFrame(master=root,
                                      width=601,
                                      height=132)
        self.mainframe.grid(column=0, row=0, sticky=('N, W, E, S'))
        # self.columnconfigure((0, 1), weight=1)
        # self.columnconfigure((2, 3, 4), weight=0)
        # self.rowconfigure((0, 1, 2, 3, 4), weight=1)
        # display video path
        self.video_path = tk.StringVar()
        # video_path.set('C:/Users/adamm/Downloads/sample-mp4-file.mp4')  # debug only
        self.video_path_entry = ctk.CTkEntry(
            self.mainframe, width=500, textvariable=self.video_path)
        self.video_path_entry.grid(column=2, row=1, sticky='we',
                                   columnspan=2, pady=(4, 4))

        # button to open file dialog to select file
        self.file_select = ctk.CTkButton(
            self.mainframe, text='Choose file', command=lambda: select_file(self))
        self.file_select.grid(column=4, row=1, padx=4, pady=(4, 4))

        # output folder path
        self.output_folder = tk.StringVar()
        self.output_entry = ctk.CTkEntry(
            self.mainframe, width=100, textvariable=self.output_folder)
        self.output_entry.grid(column=2, row=2, sticky='we',
                               columnspan=2, pady=(0, 4))

        # button to open file dialog to select output location
        self.output_select = ctk.CTkButton(
            self.mainframe, text='Choose folder', command=lambda: select_folder(self))
        self.output_select.grid(column=4, row=2, pady=(0, 4))

        # start time
        self.start_time = TimeSpinbox(self.mainframe)
        self.start_time.grid(column=2, row=3, sticky='w', pady=(0, 4))

        # end time
        self.end_time = TimeSpinbox(self.mainframe)
        self.end_time.grid(column=2, row=4, sticky='w', pady=(0, 4))

        # check box for placing video in original folder
        self.check_out_folder = tk.BooleanVar()
        self.check_folder = ctk.CTkCheckBox(self.mainframe, variable=self.check_out_folder,
                                            offvalue=False, onvalue=True,
                                            command=lambda: set_output_folder(
                                                gui),
                                            text='Output file to input folder')
        self.check_folder.grid(column=2, row=3, sticky='w',
                               columnspan=2, padx=(120, 0), pady=(0, 4))

        # check box for deleting original file after trim
        self.delete_file = tk.BooleanVar()
        self.check_delete = ctk.CTkCheckBox(self.mainframe, variable=self.delete_file,
                                            offvalue=False, onvalue=True,
                                            text='Delete original file after trimming')
        self.check_delete.grid(column=2, row=4, sticky='w',
                               columnspan=2, padx=(120, 0), pady=(0, 4))

        # Entry for new filename
        self.filename = tk.StringVar()
        self.new_filename = ctk.CTkEntry(
            self.mainframe, width=100, textvariable=self.filename)
        self.new_filename.grid(column=2, row=5, sticky='we', pady=(0, 2))

        # trim video button
        self.trim_button = ctk.CTkButton(
            self.mainframe, text='Trim video', command=lambda: trim_video(self))
        self.trim_button.grid(column=4, row=4, rowspan=2,
                              sticky='ns', pady=(0, 2))

        # labels
        ctk.CTkLabel(self.mainframe, text="Video File:").grid(
            column=1, row=1, sticky='W', padx=(5, 0), pady=(4, 4))
        ctk.CTkLabel(self.mainframe, text="Output Folder:").grid(
            column=1, row=2, sticky='W', padx=(5, 0), pady=(0, 4))
        ctk.CTkLabel(self.mainframe, text="Start Time:").grid(
            column=1, row=3, sticky='W', padx=(5, 0), pady=(0, 4))
        ctk.CTkLabel(self.mainframe, text="End Time:").grid(
            column=1, row=4, sticky='W', padx=(5, 0), pady=(0, 4))
        ctk.CTkLabel(self.mainframe, text="New Filename:").grid(
            column=1, row=5, sticky='W', padx=(5, 2), pady=(0, 4))


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.minsize(601, 132)
root.title("MP4 Video Trimmer")
GUI(root)

startup_sequence()
root.mainloop()
end_sequence()
