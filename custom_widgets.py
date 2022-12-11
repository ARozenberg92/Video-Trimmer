class TimeSpinbox(customtkinter.CTkFrame):
    # custom spinbox for handling time inputs
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

