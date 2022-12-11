import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import customtkinter
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from typing import Union
import re
import os
import configparser


def select_file(root):
    global input_file_dir
    filetypes = (
        ('MP4 files', '*.mp4'),
        ('MKV files', '*.mkv'),
        ('MOV files', '*.mov'),
        ('WMV files', '*.wmv'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file', initialdir=input_file_dir, filetypes=filetypes)
    if not filename:
        return
    else:
        clip = VideoFileClip(filename)
        clip_time = clip.duration
        clip.close()
        root.video_path.set(filename)
        root.video_path_entry.xview("end")
        if root.check_out_folder.get() == 1:
            set_output_folder()
        root.start_time.set('00:00:00.00')
        root.end_time.set(sec_to_timestamp(clip_time))
        input_file_dir = get_source(filename)


def select_folder(root):
    global output_file_dir
    selected_folder = fd.askdirectory(
        title='Select a Folder', initialdir=output_file_dir)
    root.output_folder.set(selected_folder)
    output_file_dir = selected_folder


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
           + str(seconds).zfill(5))


def set_output_folder(root):
    global output_file_dir
    if root.check_out_folder.get():
        out_dir = get_source(root.video_path.get())
        root.output_folder.set(out_dir)
        root.output_entry.xview("end")
        root.output_entry.configure(text_color='light grey',
                                    fg_color='grey', state='disabled')
        output_file_dir = out_dir
    else:
        root.output_entry.configure(
            text_color="#DCE4EE", fg_color="#343638", state='normal')


def get_source(filepath):
    if not filepath:
        return ""
    else:
        return(filepath[:filepath.rfind('/')])


def trim_video(root):
    file_extension = root.video_path.get()[root.video_path.get().rfind('.'):]
    if not root.filename.get():
        index = root.video_path.get().rfind('/') + 1
        out_filename = root.video_path.get(
        )[index:-4] + '_trimmed' + root.video_path.get()[-4:]
    elif root.filename.get()[-4:] != file_extension:
        out_filename = root.filename.get() + file_extension
    else:
        out_filename = root.filename.get()

    if not root.output_folder.get():
        out_folder = get_source(root.video_path.get())
    else:
        out_folder = root.output_folder.get()

    output_file = out_folder + '/' + out_filename
    # print(output_file)

    clip_start = time_to_sec(root.start_time.get())
    clip_end = time_to_sec(root.end_time.get())

    if root.delete_file.get():
        old_name = root.video_path.get()
        new_name = get_source(old_name) + 'temp.mp4'
        os.rename(old_name, new_name)
        ffmpeg_extract_subclip(new_name, clip_start,
                               clip_end, targetname=output_file)
        os.remove(new_name)
    else:
        ffmpeg_extract_subclip(root.video_path.get(), clip_start,
                               clip_end, targetname=output_file)
    mb.showinfo("", 'Video trimming completed.', icon="question")


def startup_sequence():
    global input_file_dir
    global output_file_dir
    cfg = configparser.ConfigParser()
    path = 'settings/default.ini'

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'settings')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    if not os.path.isfile(path):
        cfg['inout_settings'] = {'input_file_dir': current_directory,
                                 'output_file_dir': current_directory}
        with open(path, 'w') as configfile:
            cfg.write(configfile)

    cfg.read(path)
    inout_settings = cfg['inout_settings']
    input_file_dir = inout_settings['input_file_dir']
    output_file_dir = inout_settings['output_file_dir']


def end_sequence():
    global input_file_dir
    global output_file_dir
    cfg = configparser.ConfigParser()
    path = 'settings/default.ini'

    cfg['inout_settings'] = {'input_file_dir': input_file_dir,
                             'output_file_dir': output_file_dir}
    with open(path, 'w') as configfile:
        cfg.write(configfile)
