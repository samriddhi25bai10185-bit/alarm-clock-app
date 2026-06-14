import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import time

root = tk.Tk()
root.title("Smart Alarm Clock")
root.geometry("600x500")

alarm_time = ""
alarm_active = False

title = tk.Label(
    root,
    text="Smart Alarm Clock",
    font=("Segoe UI", 24, "bold")
)
title.pack(pady=20)

clock_label = tk.Label(
    root,
    text="00:00:00",
    font=("Consolas", 32, "bold")
)
clock_label.pack(pady=20)

hour_var = tk.StringVar(value="00")
minute_var = tk.StringVar(value="00")
second_var = tk.StringVar(value="00")

hours = [f"{i:02}" for i in range(24)]
minutes = [f"{i:02}" for i in range(60)]
seconds = [f"{i:02}" for i in range(60)]

time_frame = tk.Frame(root)
time_frame.pack(pady=20)

tk.Label(
    time_frame,
    text="Hour"
).grid(row=0, column=0, padx=10)

tk.Label(
    time_frame,
    text="Minute"
).grid(row=0, column=1, padx=10)

tk.Label(
    time_frame,
    text="Second"
).grid(row=0, column=2, padx=10)

hour_menu = ttk.Combobox(
    time_frame,
    textvariable=hour_var,
    values=hours,
    width=5,
    state="readonly"
)
hour_menu.grid(row=1, column=0, padx=10)

minute_menu = ttk.Combobox(
    time_frame,
    textvariable=minute_var,
    values=minutes,
    width=5,
    state="readonly"
)
minute_menu.grid(row=1, column=1, padx=10)

second_menu = ttk.Combobox(
    time_frame,
    textvariable=second_var,
    values=seconds,
    width=5,
    state="readonly"
)
second_menu.grid(row=1, column=2, padx=10)

def check_alarm():
    global alarm_active

    while alarm_active:

        current_time = datetime.now().strftime("%H:%M:%S")

        if current_time == alarm_time:

            status_label.config(
                text="🔔 ALARM RINGING!"
            )

            alarm_active = False
            break

        time.sleep(1)

def set_alarm():
    global alarm_time
    global alarm_active

    alarm_time = (
        f"{hour_var.get()}:"
        f"{minute_var.get()}:"
        f"{second_var.get()}"
    )

    alarm_active = True

    status_label.config(
        text=f"Alarm Set For: {alarm_time}"
    )

    threading.Thread(
        target=check_alarm,
        daemon=True
    ).start()

set_button = tk.Button(
    root,
    text="Set Alarm",
    font=("Segoe UI", 12, "bold"),
    command=set_alarm
)
set_button.pack(pady=15)

status_label = tk.Label(
    root,
    text="No Alarm Set",
    font=("Segoe UI", 12),
    fg="green"
)
status_label.pack()

def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")

    clock_label.config(text=current_time)

    root.after(1000, update_clock)

update_clock()

root.mainloop()