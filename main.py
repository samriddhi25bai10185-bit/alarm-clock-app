import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
import threading
import time
import pygame
import os

pygame.mixer.init()

root = tk.Tk()
root.title("Smart Alarm Clock")
root.geometry("650x550")
root.resizable(False, False)

alarm_time = ""
alarm_active = False
alarm_tone = ""

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
    text="Hour",
    font=("Segoe UI", 10)
).grid(row=0, column=0, padx=10)

tk.Label(
    time_frame,
    text="Minute",
    font=("Segoe UI", 10)
).grid(row=0, column=1, padx=10)

tk.Label(
    time_frame,
    text="Second",
    font=("Segoe UI", 10)
).grid(row=0, column=2, padx=10)

hour_menu = ttk.Combobox(
    time_frame,
    textvariable=hour_var,
    values=hours,
    width=5,
    state="readonly"
)
hour_menu.grid(row=1, column=0, padx=10, pady=5)

minute_menu = ttk.Combobox(
    time_frame,
    textvariable=minute_var,
    values=minutes,
    width=5,
    state="readonly"
)
minute_menu.grid(row=1, column=1, padx=10, pady=5)

second_menu = ttk.Combobox(
    time_frame,
    textvariable=second_var,
    values=seconds,
    width=5,
    state="readonly"
)
second_menu.grid(row=1, column=2, padx=10, pady=5)

def select_tone():
    global alarm_tone

    file_path = filedialog.askopenfilename(
        title="Select Alarm Tone",
        filetypes=[
            ("Audio Files", "*.mp3 *.wav"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        alarm_tone = file_path

        tone_label.config(
            text=f"Selected: {os.path.basename(file_path)}"
        )

def check_alarm():
    global alarm_active

    while alarm_active:

        current_time = datetime.now().strftime("%H:%M:%S")

        if current_time == alarm_time:

            status_label.config(
                text="🔔 ALARM RINGING!"
            )

            if alarm_tone:
                pygame.mixer.music.load(alarm_tone)
                pygame.mixer.music.play(-1)

            alarm_active = False
            break

        time.sleep(1)

def set_alarm():
    global alarm_time
    global alarm_active

    if not alarm_tone:
        messagebox.showerror(
            "Error",
            "Please select an alarm tone."
        )
        return

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

def stop_alarm():
    global alarm_active

    pygame.mixer.music.stop()
    alarm_active = False

    status_label.config(
        text="Alarm Stopped"
    )

def snooze_alarm():
    global alarm_time
    global alarm_active

    pygame.mixer.music.stop()

    new_time = datetime.now() + timedelta(minutes=5)

    alarm_time = new_time.strftime("%H:%M:%S")

    alarm_active = True

    status_label.config(
        text=f"Snoozed Until: {alarm_time}"
    )

    threading.Thread(
        target=check_alarm,
        daemon=True
    ).start()

tone_button = tk.Button(
    root,
    text="Select Alarm Tone",
    font=("Segoe UI", 11),
    command=select_tone
)
tone_button.pack(pady=10)

tone_label = tk.Label(
    root,
    text="No Tone Selected",
    font=("Segoe UI", 10)
)
tone_label.pack()

set_button = tk.Button(
    root,
    text="Set Alarm",
    font=("Segoe UI", 12, "bold"),
    command=set_alarm
)
set_button.pack(pady=10)

snooze_button = tk.Button(
    root,
    text="Snooze 5 Min",
    font=("Segoe UI", 12),
    command=snooze_alarm
)
snooze_button.pack(pady=5)

stop_button = tk.Button(
    root,
    text="Stop Alarm",
    font=("Segoe UI", 12),
    command=stop_alarm
)
stop_button.pack(pady=5)

status_label = tk.Label(
    root,
    text="No Alarm Set",
    font=("Segoe UI", 12, "bold"),
    fg="green"
)
status_label.pack(pady=15)

def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")

    clock_label.config(text=current_time)

    root.after(1000, update_clock)

update_clock()

root.mainloop()