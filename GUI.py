from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import re
import os

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
        output_entry.config(state='disabled')
    else:
        output_entry.config(state='enabled')


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
    mb.showinfo("", 'Video trimming completed.')


# GUI code
gui = Tk()
gui.minsize(601, 132)
gui.title("MP4 Video Trimmer")
# scrollbar_x = ttk.Scrollbar(orient="horizontal")

mainframe = ttk.Frame(gui, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
gui.columnconfigure(0, weight=1)
gui.rowconfigure(0, weight=1)

# display video path
video_path = StringVar()
video_path_entry = ttk.Entry(
    mainframe, width=50, textvariable=video_path)
video_path_entry.grid(column=2, row=1, sticky=(W, E), columnspan=2)


# button to open file dialog to select file
file_select = ttk.Button(mainframe, text='Choose file', command=select_file)
file_select.grid(column=4, row=1, sticky='we')

# output folder path
output_folder = StringVar()
output_entry = ttk.Entry(mainframe, width=50, textvariable=output_folder)
output_entry.grid(column=2, row=2, sticky='we', columnspan=2)


# button to open file dialog to select output location
output_select = ttk.Button(
    mainframe, text='Choose folder', command=select_folder)
output_select.grid(column=4, row=2, sticky='we')

# start time
start_time = StringVar()
start_entry = ttk.Entry(mainframe, width=10, textvariable=start_time)
start_entry.grid(column=2, row=3, sticky='w')
# start_time = StringVar()
# start_entry2 = ttk.Spinbox(
#     mainframe, from_=0, to=100, width=10, textvariable=start_time, increment=1,
#     format='%2.2f')
# start_entry.grid(column=2, row=3, sticky='w')

# end time
end_time = StringVar()
end_entry = ttk.Entry(mainframe, width=10, textvariable=end_time)
end_entry.grid(column=2, row=4, sticky='w')

# check box for placing video in original folder
check_out_folder = IntVar()
check_folder = ttk.Checkbutton(mainframe, variable=check_out_folder,
                               command=set_output_folder,
                               text='Output file to input folder')
check_folder.grid(column=3, row=3, sticky='w', columnspan=2)

# check box for deleting original file after trim
delete_file = BooleanVar()
check_delete = ttk.Checkbutton(mainframe, variable=delete_file,
                               offvalue=False, onvalue=True,
                               text='Delete original file after trimming')
check_delete.grid(column=3, row=4, sticky='w', columnspan=2)

# Entry for new filename
filename = StringVar()
new_filename = ttk.Entry(mainframe, width=50, textvariable=filename)
new_filename.grid(column=2, row=5)

# trim video button
trim_button = ttk.Button(mainframe, text='Trim video', command=trim_video)
trim_button.grid(column=4, row=5, sticky='we')


# labels
ttk.Label(mainframe, text="Video File:").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Output Folder:").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Start Time:").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="End Time:").grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, text="New Filename:").grid(column=1, row=5, sticky=W)


gui.mainloop()
