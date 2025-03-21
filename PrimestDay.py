from collections import defaultdict
from threading import Thread
from tkinter import *
from datetime import datetime
from itertools import product
from sympy import isprime
from PrimiestConstants import *


class FilterControl(Frame):
    def __init__(self, label, root, width):
        super().__init__(root)
        self.root = root
        self.label = label
        self.control_val = BooleanVar()
        self.control = Checkbutton(self, text=label, variable=self.control_val, anchor='nw', width=width)
        self.control.pack()
        self.pack(side=TOP)


class PrimiestDayWindow(Frame):
    def __init__(self, root: Tk):
        super().__init__(root)
        self.root = root
        self.root.title("The Primiest Days")
        self.root.geometry("1800x750")

        self.apply_thread = None
        self.prime_date_times = []
        self.prime_times_per_day = {}
        self.applied_filters = {}

        self.date_filter_controls, self.time_filter_controls, self.date_time_filter_controls = self.create_filter_frame()
        self.output_list_date_time, self.output_list_times_per_date = self.create_output_frame()

        self.info_pane = self.create_info_pane()
        self.error_label, self.start_year_val, self.end_year_val, self.apply_control = self.create_control_pane()

        for i in range(3):
            self.grid_columnconfigure(i, weight=1, uniform="frame")

        self.set_defaults()
        self.pack(fill="both", expand=True)
        self.validate_years()

    def create_filter_frame(self):
        Label(self, text="Filter selection", width=75).grid(row=0, column=0, sticky="NW")
        filter_frame = Frame(self, highlightbackground="gray", highlightthickness=1)
        filter_frame.grid(row=1, column=0, columnspan=2, sticky="NW")

        date_filter_controls = {
            fc.label: fc for fc in self.get_filter_controls(filter_frame, DATE_FILTER_LABELS, 25)
        }
        time_filter_controls = {
            fc.label: fc for fc in self.get_filter_controls(filter_frame, TIME_FILTER_LABELS, 25)
        }
        date_time_filter_controls = {
            fc.label: fc for fc in self.get_filter_controls(filter_frame, DATE_TIME_FILTER_LABELS, 75)
        }
        return date_filter_controls, time_filter_controls, date_time_filter_controls

    def create_output_frame(self):
        Label(self, text="Prime Times", width=75).grid(row=0, column=2, sticky="NW")
        Label(self, text="Prime Times Per Day", width=75).grid(row=0, column=4, sticky="NW")
        output_list_frame = Frame(self)
        output_list_frame.grid(row=1, column=2, rowspan=4, columnspan=4, sticky=N+S+E+W)
        output_list_date_time = Listbox(output_list_frame, width=75)
        output_list_date_time.pack(side="left", fill="y")
        output_list_date_time.bind('<<ListboxSelect>>', self.on_select_date_time)
        output_list_date_time_scrollbar = Scrollbar(output_list_frame, orient="vertical", command=output_list_date_time.yview)
        output_list_date_time_scrollbar.pack(side="left", fill="y")
        output_list_date_time.configure(yscrollcommand=output_list_date_time_scrollbar.set)
        output_list_times_per_date = Listbox(output_list_frame, width=75, exportselection=0)
        output_list_times_per_date.pack(side="left", fill="y")
        output_list_times_per_date_scrollbar = Scrollbar(output_list_frame, orient="vertical", command=output_list_times_per_date.yview)
        output_list_times_per_date_scrollbar.pack(side="left", fill="y")
        output_list_times_per_date.configure(yscrollcommand=output_list_times_per_date_scrollbar.set)
        return output_list_date_time, output_list_times_per_date

    def create_info_pane(self):
        info_pane = Text(self, state=DISABLED)
        info_pane.grid(row=6, column=0, columnspan=6, sticky=N+S+W+E)
        info_pane.bind("<1>", lambda event: self.info_pane.focus_set())
        return info_pane

    def create_control_pane(self):
        error_label = Label(self, anchor="w", width=50)

        start_year_val = StringVar()
        start_year = Entry(self, width=25, validatecommand=self.validate_years, validate="focusout",
                                textvariable=start_year_val)

        end_year_val = StringVar()
        end_year = Entry(self, width=25, validatecommand=self.validate_years, validate="focusout",
                              textvariable=end_year_val)

        apply_control = Button(self, anchor="w", text="Apply", width=25, command=self.apply)
        default_control = Button(self, anchor="w", text="Reset Defaults", width=25, command=self.set_defaults)
        clear_control = Button(self, anchor="w", text="Clear Filters", width=25, command=self.clear_filters)

        clear_control.grid(row=2, column=0, sticky="W")
        default_control.grid(row=2, column=1, sticky="W")

        Label(self, text="Start Year").grid(row=3, column=0, sticky="W")
        Label(self, text="End Year").grid(row=3, column=1, sticky="W")
        start_year.grid(row=4, column=0, sticky="W")
        end_year.grid(row=4, column=1, sticky="W")
        apply_control.grid(row=5, column=0, sticky="W")
        error_label.grid(row=5, column=1, sticky="W")

        return error_label, start_year_val, end_year_val, apply_control

    def validate_years(self):
        return self.validate_year(self.start_year_val.get()) and self.validate_year(self.end_year_val.get())

    def validate_year(self, year):
        self.error_label.config(text="", foreground="light gray")
        self.apply_control.config(state=NORMAL)
        if self.apply_thread and self.apply_thread.is_alive():
            self.apply_control.config(state=DISABLED)
            return False
        if str.isdigit(year) and 0 < int(year) <= 9999:
            return True
        self.error_label.config(
            text="Start and End year must be integers between 1 and 9999",
            foreground="red"
        )
        self.apply_control.config(state=DISABLED)
        return False

    @staticmethod
    def get_filter_controls(filter_frame, src, width):
        filter_frame = Frame(filter_frame)
        filter_label = Label(filter_frame, text=FILTER_GROUP_DISPLAY_NAMES[id(src)], anchor="n")
        filter_label.pack(side=TOP)
        fc = [FilterControl(l, filter_frame, width) for l in src]
        filter_frame.pack(side=LEFT, anchor="n")
        return fc

    def clear_filters(self):
        for control_src in [self.date_filter_controls, self.time_filter_controls, self.date_time_filter_controls]:
            for filter_control in control_src.values():
                filter_control.control_val.set(False)

    def set_defaults(self):
        for control_src in [self.date_filter_controls, self.time_filter_controls, self.date_time_filter_controls]:
            for filter_val, filter_control in control_src.items():
                filter_control.control_val.set(filter_val in DEFAULT_FILTERS)
        self.start_year_val.set(DEFAULT_START_YEAR)
        self.end_year_val.set(DEFAULT_END_YEAR)

    def apply(self):
        if self.apply_thread and self.apply_thread.is_alive():
            self.error_label.config(
                text="Task is already running, wait for it to complete",
                foreground="red"
            )
            return
        self.apply_control.config(state=DISABLED)
        self.apply_thread = Thread(target=self.apply_async)
        self.apply_thread.start()

    def apply_async(self):
        self.applied_filters = self.get_active_filters()
        candi_dates = self.get_selected_candi_dates(self.applied_filters)
        primey_dates = self.apply_selected_date_filters(self.applied_filters, candi_dates)
        candi_times = self.get_selected_candi_times(self.applied_filters)
        primey_times = self.apply_selected_time_filters(self.applied_filters, candi_times)
        self.prime_date_times = list(self.apply_selected_date_time_filters(self.applied_filters, product(primey_dates, primey_times)))
        self.prime_times_per_day = self.times_per_day(self.prime_date_times)
        self.update_display()
        self.error_label.config(text="Complete!", foreground="green")
        self.apply_control.config(state=NORMAL)

    @staticmethod
    def format_times_per_date(prime_date_times):
        (Y, M, D), times = prime_date_times
        count = len(times)
        return f'{Y:04d}-{M:02d}-{D:02d} - {count:d} prime seconds', count

    @staticmethod
    def format_prime_date_time(prime_date_time):
        (Y, M, D), (h, m, s) = prime_date_time
        return f'{Y:04d}-{M:02d}-{D:02d} {h:02d}:{m:02d}:{s:02d}'

    def update_display(self):
        self.output_list_date_time.delete('0', 'end')
        self.output_list_times_per_date.delete('0', 'end')
        self.output_list_date_time.insert(0, *map(self.format_prime_date_time, self.prime_date_times))
        self.output_list_times_per_date.insert(0, *map(
            lambda o: o[0],
            sorted(map(self.format_times_per_date, self.prime_times_per_day.items()), key=lambda o: o[1], reverse=True)
        ))

    def on_select_date_time(self, _):
        selected_idx = self.output_list_date_time.curselection()[0]
        selected_date, selected_time = self.prime_date_times[selected_idx]
        info_text = [
            f'{label}: {fn(*selected_date, *selected_time)}'
            for (label, fn) in FUNCTION_FORMATTERS.items() if isprime(fn(*selected_date, *selected_time))
        ]
        self.info_pane.configure(state=NORMAL)
        self.info_pane.delete(1.0, 'end')
        self.info_pane.insert(1.0, ', '.join(info_text))
        self.info_pane.configure(state=DISABLED)

    def get_active_filters(self):
        active_filters = {
            fc.label: fc.control_val.get() for fc in self.date_filter_controls.values()
        }
        active_filters.update({
            fc.label: fc.control_val.get() for fc in self.time_filter_controls.values()
        })
        active_filters.update({
            fc.label: fc.control_val.get() for fc in self.date_time_filter_controls.values()
        })
        return active_filters

    @staticmethod
    def is_a_real_day(year, month, day):
        try:
            datetime.now().replace(year, month, day)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_format_fns(active_filters, format_src):
        return [FUNCTION_FORMATTERS[f] for f, v in active_filters.items() if v
                and f in FUNCTION_FORMATTERS and f in format_src]

    @staticmethod
    def apply_selected_time_filters(active_filters, candi_times):
        formatters = PrimiestDayWindow.get_format_fns(active_filters, TIME_FILTER_LABELS)
        return filter(lambda t: all([isprime(f(*FMT_FILTER_ARG_PAD, *t)) for f in formatters]), candi_times)

    @staticmethod
    def apply_selected_date_filters(active_filters, candi_dates):
        formatters = PrimiestDayWindow.get_format_fns(active_filters, DATE_FILTER_LABELS)
        return filter(lambda d: all([isprime(f(*d)) for f in formatters]) and PrimiestDayWindow.is_a_real_day(*d), candi_dates)

    @staticmethod
    def apply_selected_date_time_filters(active_filters, candi_date_times):
        formatters = PrimiestDayWindow.get_format_fns(active_filters, DATE_TIME_FILTER_LABELS)
        return filter(lambda dt: all([isprime(f(*dt[0], *dt[1])) for f in formatters]), candi_date_times)

    @staticmethod
    def times_per_day(primey_date_times):
        times_per_day = defaultdict(list)
        for date_val, time_val in primey_date_times:
            times_per_day[date_val].append(time_val)
        return times_per_day

    @staticmethod
    def get_selected_candi_times(active_filters):
        if active_filters.get(TIME_FILTER_HOUR_12) or active_filters.get(TIME_FILTER_HOUR):
            candi_hours = filter(lambda h: (not active_filters.get(TIME_FILTER_HOUR) or isprime(h))
                                           and (not active_filters.get(TIME_FILTER_HOUR_12) or isprime(h % 12)), range(1, 24, 2))
        else:
            candi_hours = range(0, 24)
        candi_minutes = filter(isprime, range(1, 61, 2)) if active_filters.get(TIME_FILTER_MINUTE) else range(1, 61)
        candi_seconds = filter(isprime, range(1, 61, 2)) if active_filters.get(TIME_FILTER_SECOND) else range(1, 61, 2)
        return product(candi_hours, candi_minutes, candi_seconds)

    def get_selected_candi_dates(self, active_filters):
        start_year = int(self.start_year_val.get())
        end_year = int(self.end_year_val.get())
        if active_filters.get(DATE_FILTER_YEAR) or active_filters.get(DATE_FILTER_YEAR_2):
            start_year = start_year + 1 if start_year % 2 == 0 else start_year
            end_year = end_year +1 if end_year % 2 != 0 else end_year
            raw_range = range(start_year, end_year, 2)
            candi_years = filter(lambda y: (not active_filters.get(DATE_FILTER_YEAR) or isprime(y)) and
                                            (not active_filters.get(DATE_FILTER_YEAR_2) or isprime(y % 100)), raw_range)
        else:
            candi_years = range(start_year, end_year+1)
        candi_months = filter(isprime, range(1, 13, 2)) if active_filters.get(DATE_FILTER_MONTH) else range(1, 13)
        candi_days = filter(isprime, range(1, 32, 2)) if active_filters.get(DATE_FILTER_DAY) else range(1, 32, 2)
        return product(candi_years, candi_months, candi_days)


def main():
    pdwin = PrimiestDayWindow(Tk())
    mainloop()


if __name__ == '__main__':
    main()
